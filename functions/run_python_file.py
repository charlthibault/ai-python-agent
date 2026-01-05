import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run (execute) the given python script path relative to the working directory, returning execution info like stderr/stdout and execution code if any error happens",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python script path to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The argument to pass to the python script",
            ),
        },
    ),
)


def run_python_file(working_directory: str, file_path: str, args: None | list[str] = None) -> str:
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
        abs_file_path = os.path.normpath(abs_file_path)

        if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
            raise ValueError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
            raise ValueError(f'"{file_path}" does not exist or is not a regular file')

        _, filename = os.path.split(abs_file_path)
        if not filename.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        result: subprocess.CompletedProcess = subprocess.run(
            args=["python", abs_file_path] + (args or []),
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        execution_output = []
        if result.returncode != 0:
            execution_output.append(f"Process exited with code {result.returncode}")
        else:
            if result.stdout:
                execution_output.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                execution_output.append(f"STDERR: {result.stderr}")
            if not result.stderr and not result.stdout:
                execution_output.append("No output produced")

        return "\n".join(execution_output)
    except Exception as error:
        return f"Error: {error}"
