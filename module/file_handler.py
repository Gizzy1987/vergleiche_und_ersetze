import os
import shutil
from tqdm import tqdm

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def list_asm_files(directory, ignore_dirs, ignore_files):
    asm_files = []
    for root, dirs, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)
        if any(relative_root.startswith(ignore_dir) for ignore_dir in ignore_dirs):
            continue
        for file in files:
            if file.endswith('.asm') and os.path.relpath(os.path.join(root, file), directory) not in ignore_files:
                asm_files.append(os.path.relpath(os.path.join(root, file), directory))
    return asm_files

def read_ignore_list(ignore_file_path):
    ignore_dirs = []
    ignore_files = []
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('DIR:'):
                    ignore_dirs.append(line[4:])
                elif line.startswith('FILE:'):
                    ignore_files.append(line[5:])
    return ignore_dirs, ignore_files

def backup_files(source_dir, backup_dir, ignore_dirs, ignore_files):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    total_files = sum([len(files) for r, d, files in os.walk(source_dir)])
    with tqdm(total=total_files, desc="Kopiere Dateien", unit="Dateien") as pbar:
        for root, dirs, files in os.walk(source_dir):
            relative_root = os.path.relpath(root, source_dir)
            if any(relative_root.startswith(ignore_dir) for ignore_dir in ignore_dirs):
                continue
            for file_name in files:
                if os.path.relpath(os.path.join(root, file_name), source_dir) in ignore_files:
                    continue
                full_file_name = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_file_name, source_dir)
                backup_file_name = os.path.join(backup_dir, relative_path)
                backup_file_dir = os.path.dirname(backup_file_name)
                if not os.path.exists(backup_file_dir):
                    os.makedirs(backup_file_dir)
                shutil.copy(full_file_name, backup_file_name)
                pbar.update(1)
