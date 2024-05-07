import sqlite3
import subprocess

def read_sqlite(directory, file, table):
    # Lệnh liệt kê sql ra một table
    result = ["sqlite3", file,".mode box --wrap 30 ",f"select * from {table};"]
    # ?
    data_query = subprocess.Popen(result, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory)
    stdout, stderr = data_query.communicate()
    
    if data_query.returncode != 0:
        # Nếu có lỗi
        print("Error:", stderr.decode('utf-8'))
        return None
    # Không có lỗi
    output = stdout.decode('utf-8')
    return output

def process_link_file(directory):
    # Đường dẫn thư mục đích (Nơi lưu trữ file video, ảnh, audio)
    directory_path = r"D:\Hidden\File-investigation-tool\frontend\static\media"
    # Lấy ra tên của file trong đường dẫn
    data = directory.split()
    nameOfFile = data[0].split('/')[-1]
    table = data[1]
    sqlite_file = read_sqlite(directory_path, nameOfFile,table)
    return  sqlite_file