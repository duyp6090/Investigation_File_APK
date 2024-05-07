import subprocess

def list_installed_apps():
    """
    Liệt kê tên và số lượng các ứng dụng đang được cài đặt trên thiết bị Android.
    """
    try:
        # Sử dụng lệnh pm list packages để liệt kê các gói ứng dụng đã cài đặt
        pm_command = "adb shell pm list packages -3"
        output = subprocess.check_output(pm_command, shell=True).decode()

        # Khởi tạo nơi lưu app và link
        app_packages = ""
        # Tách tên gói ứng dụng từ đầu ra
        for app in output.split("\n"):
            # Lấy tên app
            app_packages += app.split(":")[-1].strip() + " "
        # Tách ra thành mảng
        app_packages = app_packages.split()

        # Đếm số lượng ứng dụng
        num_apps = len(app_packages)
        print(app_packages)
        # Trả về danh sách các ứng dụng và tổng số lượng
        return app_packages, num_apps
    
    except subprocess.CalledProcessError as e:
        # Hiển thị lỗi
        print(f"Lỗi khi liệt kê ứng dụng: {e}")
        return {e}