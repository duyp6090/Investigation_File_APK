import subprocess
import imghdr

def adb_preview_file(file_path):
    # Sử dụng lệnh adb để đọc nội dung của tệp tin
    adb_command = f"adb shell cat '{file_path}' "
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)

    # Kiểm tra kết quả trả về từ lệnh adb
    if result.returncode == 0:
        encoded_output = result.stdout.encode('utf-8', 'ignore')
        return encoded_output.decode('utf-8')
    else:
        print(f"Lỗi khi xem trước nội dung của tệp tin {file_path}.")

def adb_pull_file(file_path, directory_path):
    # Nhận dạng link tệp tin khi có khoảng trắng
    if " " in file_path:
        file_path = f'"{file_path}"'
    if " " in directory_path:
        directory_path = f'"{directory_path}"'
    # Sử dụng adb để sao chép file từ thiết bị Android về máy tính
    adb_command = f"adb pull  {file_path} {directory_path}"
    subprocess.run(adb_command, shell=True)

def copy_file_to_sdcard(directory):
    # Tải file db của app về thư mục scard
    command = f"adb shell su -c 'cp {directory} /sdcard/Download/data'"
    subprocess.run(command, shell=True)

def read_sqlite(directory, file):
    # Hiển thị danh sách các bảng trong tệp tin sqlite
    result = f"sqlite3 {file} .table"
    data_query = subprocess.run(result, shell=True, capture_output=True, cwd=directory, text=True)
    # Chuẩn hóa đầu ra đường dẫn với các khoảng trắng
    encoded_output = data_query.stdout.encode('utf-8', 'ignore') 
    return encoded_output.decode('utf-8').split()

def list_files(directory):
    try:
        # Sử dụng adb shell ls để liệt kê các tệp tin trong thư mục
        adb_command = f"adb shell su -c 'ls '{directory}''"
        output = subprocess.check_output(adb_command, shell=True).decode()
        # In ra danh sách các tệp tin
        result = [line.strip() for line in output.split("\n") if line.strip()]
        return result
    
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi liệt kê tệp tin: {e}")


def process_link_file(directory):
    # Đường dẫn thư mục đích (Nơi lưu trữ file video, ảnh, audio)
    directory_path = r"D:\Hidden\File-investigation-tool\frontend\static\media"

    # Lấy ra đuôi file để check xem là video, audio, text, ...
    typeOfFile = directory.split('/')[-1].split('.')[-1] 
    # Lấy ra tên của file trong đường dẫn
    nameOfFile = directory.split('/')[-1]
    
    # Sao chép file về bộ nhớ cấp phép của điện thoại
    copy_file_to_sdcard(directory)

    # Đường dẫn mới của file
    new_directory = "/sdcard/Download/data/" + nameOfFile

    # Sao chép file từ Android về máy tính
    adb_pull_file(new_directory, directory_path )

    if typeOfFile == 'mp4':
        # Trả về tên file video
        return nameOfFile, 1
    elif typeOfFile == 'mp3':
        # Trả về tên file audio
        return nameOfFile, 2
    elif typeOfFile in ['img','jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
        # Trả về tên file ảnh
        return nameOfFile, 3    
    elif typeOfFile == 'db':
        # Trả về data của app 
        sqlite_file = read_sqlite(directory_path, nameOfFile)
        return  sqlite_file, 4
    elif typeOfFile in ['text','txt']:
        # Trả về file text
        data_txt = adb_preview_file(directory)
        return data_txt, 5
    else:
        return "Lỗi khi mở tệp tin", 0

