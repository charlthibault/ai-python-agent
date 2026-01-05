import time

import pexpect
from google.genai import types

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
    def __init__(self):
        self.child = None
        # Support multiple common terminal prompts
        self.prompt_pattern = r"❯|➜|\$|\#|>>>|> "

    def open(self, working_directory="/tmp"):
        """Open a bash shell with pexpect control"""
        # Spawn bash with pexpect
        self.child = pexpect.spawn("/bin/bash", encoding="utf-8", echo=False)

        # Set a simple, recognizable prompt
        self.child.sendline('export PS1="PEXPECT$ "')
        time.sleep(0.2)
        self._wait_for_prompt()

        # Change to working directory
        self.child.sendline(f"cd {working_directory}")
        self._wait_for_prompt()

    def _wait_for_prompt(self, timeout=10):
        """Wait for the shell prompt"""
        try:
            self.child.expect(self.prompt_pattern, timeout=timeout)
        except pexpect.TIMEOUT:
            time.sleep(0.5)

    def run_command(self, command, timeout=30):
        """
        Send command and capture output.

        Args:
            command: The command to run
            timeout: Timeout in seconds

        Returns:
            Dictionary with stdout, stderr, and exit_code
        """
        # Run command and capture exit code
        self.child.sendline(command)

        # Wait for command to complete
        try:
            self._wait_for_prompt(timeout=timeout)
            output = self.child.before

            # Get the exit code of the last command
            self.child.sendline("echo $?")
            self._wait_for_prompt()
            exit_code_output = self.child.before.strip()

            # Extract exit code (first line after the command)
            exit_code = 0
            try:
                exit_code = int(exit_code_output.split("\n")[0].strip())
            except (ValueError, IndexError, AttributeError):
                exit_code = 0

            return {"stdout": output.strip(), "exit_code": exit_code, "success": exit_code == 0}
        except pexpect.TIMEOUT:
            return {"stdout": "", "exit_code": -1, "success": False, "error": "Command timed out"}

    def expect(self, pattern, timeout=30):
        """Wait for a specific pattern in output"""
        return self.child.expect(pattern, timeout=timeout)

    def is_alive(self):
        """Check if the terminal session is still active"""
        return self.child and self.child.isalive()

    def close(self):
        """Close the terminal session"""
        if self.child and self.child.isalive():
            self.child.sendline("exit")
            time.sleep(0.2)
            self.child.close()


# Global terminal instance
terminal = PexpectTerminal()


def run_command_in_terminal(working_directory: str, command_line_args: list[str]):
    try:
        # Ensure terminal is open
        if not terminal.is_alive():
            terminal.open(working_directory)

        # Run the command
        command = " ".join(command_line_args)
        result = terminal.run_command(command)

        if result["success"]:
            return f"COMMAND EXECUTED SUCCESSFULLY\n\nOutput:\n{result['stdout']}"
        else:
            return f"COMMAND FAILED (exit code: {result['exit_code']})\n\nOutput:\n{result['stdout']}"

    except Exception as error:
        return f"Error: {error}"
