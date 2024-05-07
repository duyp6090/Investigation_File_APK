import subprocess

def get_directory_details(directory_path):
    # Lấy ra thông tin file
    adb_command = f"adb shell stat '{directory_path}'"
    process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # Nểu gặp lỗi
    if stderr:
        return "Error: " + stderr.decode().strip()
    # Lấy ra thông tin thành công
    else:
        # Chia thành mảng các thông tin
        output = stdout.decode().split("\n")
        # Bỏ phần tử trống
        output.pop()
        return output