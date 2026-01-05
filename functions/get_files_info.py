import logging
import os

from google.genai import types

logger = logging.getLogger(__name__)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        if not os.path.commonpath([abs_working_dir, abs_target_dir]) == abs_working_dir:
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.exists(abs_target_dir):
            raise ValueError(f'"{directory}" is not a directory')

        files_info = []
        for item in os.listdir(abs_target_dir):
            item_path = os.path.join(abs_target_dir, item)
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else None
            is_dir = os.path.isdir(item_path)
            info = {"name": item, "is_directory": is_dir, "size": size}
            files_info.append(info)

        return "\n".join(
            [f"- {info['name']}, size={info['size']} bytes, is_dir={info['is_directory']}" for info in files_info]
        )
    except Exception as error:
        return f"Error: {error}"
