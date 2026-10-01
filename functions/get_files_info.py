import os


def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(working_dir_abs, directory))

        if not os.path.isdir(target_dir):
            return f"Error: {directory} is not a directory."

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if valid_target_dir:
            dir_content = os.listdir(target_dir)
            content_str = []

            for item in dir_content:
                item_path = os.path.join(target_dir, item)

                content_str.append(
                    f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
                )

            return "\n".join(content_str)
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"
