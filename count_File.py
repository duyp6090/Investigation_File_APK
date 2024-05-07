import subprocess

def count_type_file(directory):
    """
    Đệ quy để đếm số lượng các loại file trong thư mục và các thư mục con.
    """
    # Tạo một từ điển để lưu số lượng tệp tin cho mỗi loại
    type_file = {}

    try:
        # Sử dụng adb shell ls để liệt kê các tệp tin trong thư mục
        adb_command = f"adb shell su -c 'ls -p '{directory}''"
        file_list = subprocess.check_output(adb_command, shell=True).decode().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi liệt kê tệp tin: {e}")
        return type_file
    
    # Duyệt qua từng tên tệp hoặc thư mục
    for file_name in file_list:
        # Làm sạch ( Loại bỏ các khoảng trắng trong file_name)
        file_name = file_name.strip()

        # Kiểm tra xem có phải là thư mục không
        if file_name and file_name[-1] == '/':
            # Đệ quy để đếm số lượng tệp tin trong thư mục con
            sub_directory = directory + file_name
            sub_type_file = count_type_file(sub_directory)

            # Cộng số lượng tệp tin từ thư mục con vào type_file
            for ext, count in sub_type_file.items():
                type_file[ext] = type_file.get(ext, 0) + count
        elif "." in file_name:
            # Lấy ra đuôi của loại tệp tin
            file_extension = file_name.split(".")[-1]
            
            # Lưu thông tin vào type_file
            type_file[file_extension] = type_file.get(file_extension, 0) + 1

    return type_file