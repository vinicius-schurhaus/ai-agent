import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        valid_file_path = (
            os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        )

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        with open(file_path_abs, "w", encoding="utf-8") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Create or overwrite a file with the specified content. Use this "
            "function when the user asks to write, create, save, or put text/content "
            "into a file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to create or overwrite, "
                        "relative to the working directory."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": "The exact content that should be written to the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
