import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def create_dirs(file_path):
    os.makedirs(file_path, exist_ok=True)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        create_dirs(file_path)

        with open(target_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
