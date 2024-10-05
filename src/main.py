import shutil
import os
def copy_dir(src: str, dest: str):
    if not os.path.exists(src):
        raise ValueError(f"Source directory {src} does not exist")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)  # Recreate the destination directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_dir(src_path, dest_path)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
# left off here


def main():
    cwd = os.getcwd()
    copy_dir(os.path.join(cwd, "static"), os.path.join(cwd, "public"))

main()