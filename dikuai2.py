import os
import re
from tkinter import Tk, filedialog

def select_folder():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    folder_path = filedialog.askdirectory()  # 打开文件夹选择对话框
    return folder_path

def find_files_with_prefix(folder_path, prefix):
    # 使用正则表达式确保只检索以该前缀开头且完整的文件名
    pattern = re.compile(rf'^{re.escape(prefix)}\w*\.txt$')
    files = [f for f in os.listdir(folder_path) if pattern.match(f)]
    return files

def modify_file(file_path, old_tag, new_tag):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # 使用正则表达式替换第一个匹配项
    modified_content = re.sub(r'owner\s*=\s*[A-Z]{3}', f'owner = {new_tag}', content, count=1)
    
    with open(file_path, 'w') as file:
        file.write(modified_content)

def find_files_with_prefix(folder_path, prefix):
    # 使用正则表达式限定以prefix开头并跟随非数字或直接结束
    pattern = re.compile(rf"^{prefix}(?!\d)")
    files = [f for f in os.listdir(folder_path) if pattern.match(f)]
    return files

def main():
    folder_path = select_folder()
    if not folder_path:
        print("没有选择文件夹")
        return
    
    prefixes = input("请输入需要修改的地块前缀（用逗号分隔）：").strip().split(',')
    prefixes = [prefix.strip() for prefix in prefixes]
    
    all_files = []
    for prefix in prefixes:
        files = find_files_with_prefix(folder_path, prefix)
        all_files.extend(files)
    
    if not all_files:
        print(f"没有找到以 {prefixes} 开头的文件")
        return
    
    new_tag = input("请输入新的标签（三个大写字母）：").strip().upper()
    if len(new_tag) != 3 or not new_tag.isalpha() or not new_tag.isupper():
        print("输入的标签无效，必须是三个大写字母")
        return
    
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as f:
            content = f.read()
        
        match = re.search(r'owner\s*=\s*([A-Z]{3})', content)
        if match:
            old_tag = match.group(1)
            print(f"在文件 {file} 中找到标签 {old_tag}")
            modify_file(file_path, old_tag, new_tag)
            print(f"文件 {file} 已更新")
        else:
            print(f"在文件 {file} 中未找到 owner 标签")

if __name__ == "__main__":
    main()
