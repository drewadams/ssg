import shutil
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mdconverter import MDConverter

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
    md_file_data = open(from_path).read()
    converter = MDConverter()
    title = converter.extract_title(md_file_data)
    template = open(template_path)
    template_data = template.read()
    template.close()
    md_html = converter.markdown_to_html_node(md_file_data).to_html()
    html = template_data.replace("{{ Content }}", md_html)
    html = html.replace("{{ Title }}", title)
    html_file = open(dest_path, "x")
    html_file.write(html)
    print("File written.")

def generate_pages_recursive(dir_path_content, template_path, dir_path_dest):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Source directory {dir_path_content} does not exist")
    # if os.path.exists(dir_path_dest):
    #     shutil.rmtree(dir_path_dest)
    if not os.path.exists(dir_path_dest):
        os.makedirs(dir_path_dest) # Recreate the destination directory            
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dir_path_dest, item)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            generate_page(src_path, template_path, dest_path.replace(".md", ".html"))
        else:
            generate_pages_recursive(src_path, template_path, dest_path)


def main():
    cwd = os.getcwd()
    copy_dir(os.path.join(cwd, "static"), os.path.join(cwd, "public"))
    # generate page from md to html
    # generate_page(os.path.join(cwd, "content/index.md"), os.path.join(cwd, "template.html"), os.path.join(cwd, "public/index.html"))
    generate_pages_recursive(os.path.join(cwd, "content"), os.path.join(cwd, "template.html"), os.path.join(cwd, "public"))
main()