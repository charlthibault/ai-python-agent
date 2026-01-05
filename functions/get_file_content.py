import os

from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Get file content from a file path relative to the working directory, returning content of file potentially truncated if more than {MAX_CHARS} character to read",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory",
            ),
        },
    ),
)


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))
        abs_file_path = os.path.normpath(abs_file_path)

        if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
            raise ValueError(f'Cannot read "{file_path}" as it is outside the permitted working directory')

        if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
            raise ValueError(f'File not found or is not a regular file: "{file_path}"')

        with open(abs_file_path) as fd:
            content = fd.read(MAX_CHARS)

            if fd.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as error:
        return f"Error: {error}"
