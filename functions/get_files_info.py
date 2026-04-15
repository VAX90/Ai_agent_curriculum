import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    try:    
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        contents = os.listdir(target_dir)
        files_info = []
        for content in contents:
            content_path = os.path.join(target_dir, content)
            is_dir = os.path.isdir(content_path)
            size = os.path.getsize(content_path)
            files_info.append(f"- {content}: file_size={size} bytes, is_dir={is_dir}")
        
            
            
            
    except Exception as e:
        return f'Error: {str(e)}'
    return "\n".join(files_info)



