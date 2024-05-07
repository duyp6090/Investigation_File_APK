# cần cài đặt thư viện flask, và adb để truy xuất thông tin file trên android
from flask import Flask, request, redirect, url_for, render_template
import os
import loop_File
import count_File
import total_File
import check_content_File
import app_installed
import directory_Information
import sqlite_data

# Đường dẫn đến thư mục gốc của ứng dụng Flask
root_path = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn đến thư mục template
template_dir = os.path.join(root_path, 'frontend\\templates')

# Đường dẫn đến thư mục static
static_dir = os.path.join(root_path, 'frontend\\static')

# Khởi tạo ra app
app = Flask(__name__, template_folder = template_dir, static_folder = static_dir)

@app.route("/loop_file/<path:direction>")
def loop_file(direction):
    if direction == "System":
        direction ="/"
    # Hướng dẫn sửa đường link nếu có direction / và tách đường link thành mảng
    spearate_Link = direction.strip('/').split('/')
    # Lấy ra tên file
    getNameFile_Folder = spearate_Link[-1]
    # Tạo title in ra page
    page_Title = "Cây thư mục của " + getNameFile_Folder + ":\n\n\n"
    # Duyệt link lấy tệp tin
    linkFiles = loop_File.Loop_File_Folder(direction)
    print(linkFiles)
    if type(linkFiles) == str:
        return render_template("handle_Error.html", error = linkFiles)
    else: 
        return render_template('loop_File.html', page_Title = page_Title, linkFiles = linkFiles)

@app.route('/total_file/<path:direction>')
def total_file(direction):
    # Đếm tổng sô file có trong thư mục
    num_directories, num_subdirectories = total_File.count_files_and_directories(direction)
    return render_template('total_File.html', num_directories = num_directories, num_subdirectories=  num_subdirectories)

@app.route('/count_file/<path:direction>')
def count_file(direction):
    # Phân loại file có trong thư mục
    type_file = count_File.count_type_file(direction)
    return render_template('count_File.html', type_file = type_file)

@app.route('/directory_detail/<path:direction>')
def directory_detail(direction):
    # Lấy ra thông tin chi tiết của 1 tệp tin
    directory_Info = directory_Information.get_directory_details(direction)
    return render_template('directory_Infor.html', directory_Info = directory_Info)


@app.route('/infor_advanced_file/<path:direction>')
def infor_advanced_file(direction):
    # Lấy tên tệp tin, loại tệp tin
    open_file, type_file = check_content_File.process_link_file(direction)
    # Mở tệp tin
    if type_file == 1:   # Chạy video
        return render_template('mp4.html', open_file = open_file)
    elif type_file == 2: # Chạy audio
        return render_template('audio.html', open_file = open_file)
    elif type_file == 3: # In ảnh
        return render_template('image.html', open_file = open_file)
    elif type_file == 4: # Trả về trang chọn Table trong SQLite
        return render_template('sql_table.html', open_file = open_file, direction = direction )
    elif type_file == 5: # Trả về trang text
        return render_template("text.html", open_file = open_file)
    else: # Báo lỗi
        return render_template("handle_Error.html", error = open_file)

@app.route('/count_app_install')
def count_app_install():
    # Lây ra số app và danh sách app đã cài đặt trong tài khoản
    installed_apps, num_apps = app_installed.list_installed_apps()
    return render_template('count_app.html', installed_apps = installed_apps, num_apps = num_apps)

@app.route('/get_data_from_sql/<path:direction>')
def get_data_from_sql(direction):
    # Lấy ra data trong app đã cài đặt
    open_file = sqlite_data.process_link_file(direction)
    return render_template('sqlite.html', open_file = open_file )

# route chính của chương trình, tiếp nhận các thông tin từ web và redirect route để thực thi
@app.route('/', methods=["POST", "GET"])
def display_tool():
    if request.method == "POST":
        # Option cho việc lựa chọn
        option = request.form['handle-option']
        # Tên đường dẫn
        direction = request.form['link-file']
        # Đếm app thì ko cần link đường dẫn
        if option == "count_app_install":
            return redirect(url_for(option))
        # Xử lí nêu lấy tệp tin gốc (thư mục root trong android)
        if direction == "/":
            direction = "System" 
        return redirect(url_for(option, direction = direction))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
