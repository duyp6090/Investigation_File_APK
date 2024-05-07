import subprocess

def count_files_and_directories(directory):
    # Liêt kê ra từng file trong thư mục
    adb_command = f"adb shell ls -p '{directory}'"
    process = subprocess.Popen(adb_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode == 0:
        # Lấy ra thông tin các file
        files = output.decode().split("\n")
        # Khởi tạo các biến chứa số lượng file, thư mục
        num_files = 0
        num_directories = 0
        # Duyệt qua thông tin các file rồi đếm
        for file_info in files:
            # Xử lí khoảng trống 2 đầu
            file_info = file_info.strip()
            if not file_info:
                continue
            # Check xem là thư mục
            if file_info and file_info[-1] == '/':
                num_directories += 1
                directory_name = file_info.split('/')[0]
                num_subfiles, num_subdirectories = count_files_and_directories(f"{directory}/{directory_name}")
                num_directories += num_subdirectories
                num_files += num_subfiles
            # Check xem là file
            elif "." in file_info:
                num_files += 1
        return num_directories, num_files
    else:
        return 0, 0