import subprocess

def is_directory_with_root(directory):
    # Kiểm tra xem đường dẫn có phải là thư mục hay không
    command = ['adb', 'shell', 'su', '-c', 'test -d "{}" && echo exists'.format(directory)]
    # Nếu là thư mục, thêm exists vào chuỗi 
    result = subprocess.run(command, capture_output=True, text=True)
    if "exists" in result.stdout:
        return True
    else:
        return False


def Loop_File_Folder(directory_path):
    if not(is_directory_with_root(directory_path)):
        return f"Tệp không phải thư mục "
    adb_command = f"adb shell su -c 'ls -p '{directory_path}''"
    process = subprocess.Popen(adb_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()

    # Map để lưu lại tên file + đường dẫn đến file
    file_and_dir = {}
    if process.returncode == 0:
        # Lấy ra các file cần duyệt
        directory_content = output.decode().split("\n")
        for item in directory_content:
            item = item.replace('\r', '').strip()
            if directory_path =='/':
                file_and_dir[item] = f"{item}"
                continue
            if item:
                    file_and_dir[item] = f"{directory_path}/{item}"
        return file_and_dir
        