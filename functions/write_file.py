import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file content to a file path relative to the working directory, returning the number of character written",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file_path",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str):
    try:
        abs_working_directory = os.path.abspath(working_directory)

        abs_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

        if os.path.commonpath([abs_working_directory, abs_file_path]) != abs_working_directory:
            raise ValueError(f'Cannot write "{file_path}" as it is outside the permitted working directory')

        abs_parent_file_path = os.path.split(abs_file_path)[0]
        if os.path.exists(abs_parent_file_path) and os.path.isdir(abs_file_path):
            raise ValueError(f'Cannot write to "{file_path}" as it is a directory')

        os.makedirs(abs_parent_file_path, exist_ok=True)

        with open(abs_file_path, "w") as fd:
            fd.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as error:
        return f"Error: {error}"
