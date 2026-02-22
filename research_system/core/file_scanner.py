import os
from typing import List
from config import SUPPORTED_EXTENSIONS,MAX_FILE_SIZE_KB,MAX_TOKENS,EXCLUDED_DIRS
from core.state import Fileinfo

def scan_directory(target_directory:str) -> tuple[List[Fileinfo], List[str]]:
    files = List[Fileinfo] = []
    errors = List[str] = [] 
       

    if not os.path.isdir(target_directory):
        raise ValueError(f"Provided path '{target_directory}' is not a valid directory.")   
    
    for root,dirs, filenames in os.walk(target_directory):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in filenames:
            extension = os.path.splitext(filename)[1].lower()
            if extension not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, target_directory)
            size_kb = os.path.getsize(full_path) / 1024

            if size_kb > MAX_FILE_SIZE_KB:
                errors.append(f"Skipped (too large {size_kb:.1f}KB): {relative_path}")
                continue

            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()

                files.append(Fileinfo(
                    path=relative_path,
                    content=content,
                    extension=extension,
                    size_kb=round(size_kb, 2)
                ))
            except Exception as e:
                errors.append(f"Failed to read {relative_path}: {str(e)}")

    return files, errors    