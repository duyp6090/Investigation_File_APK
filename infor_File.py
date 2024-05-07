import subprocess

def get_file_info(file_path):
    """
    Lấy thông tin chi tiết cho tệp tin được chỉ định trên thiết bị Android.

    Args:
        file_path: Đường dẫn đến tệp tin trên thiết bị Android.

    Returns:
        Dictionary chứa thông tin chi tiết về tệp tin.
    """
    try:
        # Loại bỏ ký tự \r từ cuối đường dẫn
        file_path = file_path.rstrip()
        
        # Lấy ra thông tin trong file
        adb_command = f"adb shell stat '{file_path}'"
        output = subprocess.check_output(adb_command, shell=True).decode().split("\n")

        # Xử lý thông tin chi tiết
        file_info = {}
        for line in output:
            if ":" in line:
                key, value = line.split(":", 1)
                file_info[key.strip()] = value.strip()
        return file_info
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi lấy thông tin chi tiết tệp tin: {e}")
        return None
    
def list_file_to_get_infor(directory):
    # Duyệt qua danh sách tệp tin trong thư mục
    try:
        adb_command = f"adb shell ls -p '{directory}'"
        file_list = subprocess.check_output(adb_command, shell=True).decode().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi liệt kê tệp tin: {e}")
        return None

    for file_name in file_list:
        file_path = f"{directory}/{file_name}"

        # Lấy thông tin chi tiết cho tệp tin
        file_info = get_file_info(file_path)

        # In ra thông tin chi tiết
        if file_info:
            print(f"**Thông tin chi tiết tệp tin:** {file_name}")
            for key, value in file_info.items():
                print(f" {key}: {value}")
            print()


