import os
import re
import sys
import time

import pexpect
from google.genai import types

from .terminal_ui import (
    print_command_error,
    print_command_output,
    print_command_start,
    print_command_success,
    print_command_timeout,
)

schema_run_command_in_terminal = types.FunctionDeclaration(
    name="run_command_in_terminal",
    description="Run (execute) the given command line in working directory, returning execution info like stderr/stdout and execution code if any error happens",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "command_line_args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The command line to launch in the terminal",
            ),
        },
    ),
)


class PexpectTerminal:
    """
    A persistent terminal session using pexpect for command execution.

    Supports real-time output streaming with rich terminal UI formatting.
    """

    # Custom prompt that's easy to detect. Use a unique, exact string so
    # we can rely on `expect_exact` instead of a regex which can match
    # normal command output inadvertently.
    PROMPT = "PEXPECT_PROMPT_END__> "

    def __init__(self):
        self.child = None

    def open(self, working_directory: str = "/tmp") -> None:
        self.child = pexpect.spawn(
            "/bin/bash",
            args=["--norc", "--noprofile"],
            encoding="utf-8",
            echo=False,
        )

        if os.getenv("PEXPECT_DEBUG"):
            self.child.logfile_read = sys.stdout

        self.child.sendline(f"export PS1='{self.PROMPT}'")
        time.sleep(0.3)
        self._consume_until_prompt(timeout=5)

        self.child.sendline(f"cd {working_directory}")
        self._consume_until_prompt(timeout=5)

    def _consume_until_prompt(self, timeout: float = 10) -> str:
        buffer = ""
        try:
            self.child.expect_exact([self.PROMPT, pexpect.EOF], timeout=timeout)
            output = self.child.before or ""
            if output.endswith(self.PROMPT):
                output = output[: -len(self.PROMPT)]
            return output
        except pexpect.TIMEOUT:
            try:
                out = self.child.read_nonblocking(size=4096, timeout=0)
                if out:
                    buffer += out
            except (pexpect.exceptions.TIMEOUT, EOFError, OSError):
                pass
            return buffer
        except pexpect.EOF:
            try:
                out = self.child.read_nonblocking(size=4096, timeout=0)
                if out:
                    buffer += out
            except Exception:
                pass
            return buffer

    def run_command(self, command: str, timeout: float = 30) -> dict:
        start_time = time.time()

        print_command_start(command)

        self.child.sendline(command)

        buffer = ""
        prompt_detected = False

        patterns = [self.PROMPT, pexpect.EOF]

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.child.expect_exact(patterns, timeout=0.5)
                out = self.child.before or ""
                if out:
                    buffer += out
                    print_command_output(out)

                prompt_detected = True
                break

            except pexpect.TIMEOUT:
                try:
                    out = self.child.read_nonblocking(size=4096, timeout=0)
                    if out:
                        buffer += out
                        print_command_output(out)
                except (pexpect.exceptions.TIMEOUT, EOFError, OSError):
                    pass
            except pexpect.EOF:
                try:
                    out = self.child.read_nonblocking(size=4096, timeout=0)
                    if out:
                        buffer += out
                        print_command_output(out)
                except Exception:
                    pass
                break

        execution_time = time.time() - start_time

        if not prompt_detected:
            print_command_timeout()
            return {
                "stdout": buffer.strip(),
                "exit_code": -1,
                "success": False,
                "error": f"Command timed out after {timeout} seconds",
            }

        self.child.sendline("echo code:$?")
        exit_code_output = self._consume_until_prompt(timeout=5)
        exit_code = 0

        try:
            exit_code_match = re.search(r"code:(\d+)", exit_code_output, re.MULTILINE)
            if exit_code_match:
                exit_code = int(exit_code_match.group(1))
        except (ValueError, AttributeError):
            exit_code = 0

        # Clean up the output
        output = self._clean_output(buffer, command)

        # Display completion status
        if exit_code == 0:
            print_command_success(exit_code, execution_time)
        else:
            print_command_error(exit_code)

        return {
            "stdout": output,
            "exit_code": exit_code,
            "success": exit_code == 0,
        }

    def _clean_output(self, output: str, command: str) -> str:
        lines = output.split("\n")

        # Remove the first line if it's the echoed command
        if lines and command in lines[0]:
            lines = lines[1:]

        # Remove empty lines at start and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        return "\n".join(lines)

    def is_alive(self) -> bool:
        """Check if the terminal session is still active."""
        return self.child is not None and self.child.isalive()

    def close(self) -> None:
        """Close the terminal session gracefully."""
        if self.child and self.child.isalive():
            self.child.sendline("exit")
            time.sleep(0.2)
            self.child.close()


# Global terminal instance for persistent sessions
terminal = PexpectTerminal()


def run_command_in_terminal(working_directory: str, command_line_args: list[str]) -> str:
    try:
        # Ensure terminal is open
        if not terminal.is_alive():
            terminal.open(working_directory)

        # Join args into command string
        command = " ".join(command_line_args)
        result = terminal.run_command(command)

        if result["success"]:
            return f"COMMAND EXECUTED SUCCESSFULLY\n\nOutput:\n{result['stdout']}"
        else:
            error_msg = result.get("error", "")
            if error_msg:
                raise RuntimeError(
                    f"Command failed with exit code {result['exit_code']}: {error_msg}\n\nOutput:\n{result['stdout']}"
                )
            raise RuntimeError(f"Command failed with exit code {result['exit_code']}\n\nOutput:\n{result['stdout']}")
    except Exception as error:
        return f"Error: {error}"
