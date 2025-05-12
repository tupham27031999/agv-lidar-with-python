from flask import Flask, send_file, request
import requests
from flask import Response
from PIL import Image, ImageDraw
from flask import jsonify
import cv2, os, shutil
import signal
import sys
import math
import path
from support_main.lib_main import remove, edit_csv_tab
from flask import render_template
import numpy as np
from io import BytesIO
import time
from support_main import edit_file_json
import threading

# # start-L0-P1, P1-L1-P2 # P2-L2-P3,P3-L3-P4
# l = np.array([[["start","L0","P1"],["P1","L1","P2"]],[["P2","L2","P3"],["P3","L3","P4"]]])
# np.save("duong_di.npy", l)
# data_duong_di = np.load("duong_di.npy", allow_pickle=True)
# print(data_duong_di[0,0])
def thap_phan_sang_nhi_phan(n): 
    return list(bin(n).replace("0b", ""))[::-1]
tien_max = 3000
re_max = 1000
grid_size = 5
agv_size = 5
host = "192.168.11.1"
port = 5000

path_phan_mem = path.path_phan_mem
path_data_input_output = path_phan_mem + "/data_input_output"
path_admin = path_phan_mem + "/setting/admin_window.csv"
if os.name == "nt":
    print("Hệ điều hành là Windows")
    # Đọc file cài đặt cho Windows
    path_admin = path_phan_mem + "/setting/admin_window.csv"
elif os.name == "posix":
    print("Hệ điều hành là Ubuntu (Linux)")
    # Đọc file cài đặt cho Ubuntu
    path_admin = path_phan_mem + "/setting/admin_ubuntu.csv"
data_admin = edit_csv_tab.load_all_stt(path_admin)

for i in range(0,len(data_admin)):
    if len(data_admin[i]) > 1:
        if data_admin[i][0] == "tien_max":
            tien_max = int(float(data_admin[i][1]))
        if data_admin[i][0] == "re_max":
            re_max = int(float(data_admin[i][1]))
        if data_admin[i][0] == "grid_size":
            grid_size = int(float(data_admin[i][1]))
        if data_admin[i][0] == "agv_size":
            agv_size = int(float(data_admin[i][1]))
        if data_admin[i][0] == "host":
            host = data_admin[i][1]
        if data_admin[i][0] == "port":
            port = int(float(data_admin[i][1]))


path_project_all = remove.tao_folder(path_data_input_output + "/project")
path_project = ""
path_map = ""
path_duong_di = ""
file_duong_di = ""
project_name = ""
path_map_chon_ban_do = ""

# Dữ liệu giả lập
x_size = 5000
y_size = 5000
w_size = 1000
h_size = 1000
map_all = np.full((5000, 5000, 4), (150, 150, 150, 0), np.uint8)
img1 = map_all.copy()
h_goc, w_goc, _ = map_all.shape
x_goc = 0
y_goc = 0
angle_goc = 0

x_crop_min = w_goc // 2 - w_size // 2
y_crop_min = h_goc // 2 - h_size // 2

data_cai_dat = {"tien_max": tien_max, "re_max": re_max, "grid_size": grid_size, "agv_size": agv_size, "path_project":""}
# lay map cu
data_chon_ban_do = {"update": 0, "map_file_path": "", "add_all_point": 0,"name_map": ""}
data_ban_do_moi = {"reset": 0, "start_stop": "stop", "path_new_map": "", "save": 0, "name_map": ""}
data_vi_tri_agv = {"x": 0, "y": 0, "angle": 0, "update_vi_tri_agv": 0, "update": 0}


# Danh sách giá trị cho các combobox
list_tien_max = [7000, 6500, 6000, 5500, 5000, 4500, 4000, 3500, 3000, 2500, 2000, 1500, 1000, 500]  # Giá trị vận tốc tiến max
list_re_max = [1000, 900, 800, 700, 600, 500]  # Giá trị vận tốc rẽ max
list_grid_size = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # Giá trị grid size
list_agv_size = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # Giá trị AGV size


stt_id = 0
stt_id_duong = 0
data_duong_di = ""
data_text_box = ""
run_stop = "stop" # Trạng thái chạy hoặc dừng
danh_sach_diem = {} # danh_sach_diem[str(stt_id)] = {"point_name":"P" + str(stt_id),"point_coord":[x, y], "direction":"", "alpha":""}
danh_sach_duong = {} # {"ten_duong": line_name, "diem_1": id_diem_1, "diem_2": id_diem_2, "loai_duong": line_type, "C1": c1, "C2": c2}

loai_lap = "lien_tuc"
so_lan_lap = 0

list_name_map = []  # Danh sách tên bản đồ
point_end = []
list_point_star = []

sent_esp_new  = str(int("100000001", 2))
sent_esp= ""
connect_esp = True
input_esp = {"IN1":0,"IN2":0,"IN3":0,"IN4":0,"IN5":0,"IN6":0,"IN7":0,"IN8":0,"IN9":0,"IN10":0,"IN11":0,"IN12":0}


# dk ban phim
dk_agv_thu_cong = 0
data_dk_tay = {"tien": 0, "lui": 0, "trai": 0, "phai": 0, "stop": 1}

def release_camera_and_exit(signal, frame):
    print("Đang giải phóng camera...")
    # video_capture.release()  # Giải phóng camera
    # cv2.destroyAllWindows()  # Đóng tất cả cửa sổ OpenCV
    sys.exit(0)  # Thoát chương trình

# Bắt tín hiệu Ctrl + C
signal.signal(signal.SIGINT, release_camera_and_exit)

app = Flask(__name__)
# Tạo ảnh kích thước 1000x1000 pixel
def create_image():
    img = Image.new('RGB', (1000, 1000), color=(0, 0, 0))  # Tạo ảnh nền trắng
    draw = ImageDraw.Draw(img)
    draw.text((400, 500), "Hello, World!", fill=(255, 255, 255))  # Thêm text vào ảnh
    return img

@app.route('/')
def display_image():
    image_path = create_image()  # Gọi hàm tạo ảnh và lưu đường dẫn ảnh vào biến `image_path`
    
    # Kiểm tra nếu đường dẫn tồn tại, lấy danh sách tệp từ thư mục
    if os.path.exists(path_duong_di):
        list_duong_di = os.listdir(path_duong_di)
    else:
        list_duong_di = []  # Nếu không tồn tại, đặt danh sách rỗng

    # Trả về nội dung HTML để hiển thị trang web
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AGV LIDAR BROTHER</title>
        <style>
            body {{
                font-family: Arial, sans-serif;  /* Đặt phông chữ cho toàn bộ trang */
                margin: 0;  /* Loại bỏ khoảng cách mặc định của trình duyệt */
                padding: 0;  /* Loại bỏ khoảng cách mặc định của trình duyệt */
                display: flex;
                flex-direction: column;  /* Sắp xếp các phần tử theo chiều dọc */
                height: 100vh;  /* Chiều cao toàn màn hình */
            }}
            .header {{
                background-color: #f0f0f0;  /* Đặt màu nền xám nhạt cho tiêu đề */
                padding: 20px;  /* Thêm khoảng cách bên trong tiêu đề */
                text-align: center;  /* Căn giữa nội dung theo chiều ngang */
                font-size: 2.5em;  /* Đặt kích thước chữ lớn cho tiêu đề */
                margin: 0;  /* Loại bỏ khoảng cách mặc định */
            }}
            .content {{
                display: flex;  /* Sử dụng Flexbox để chia bố cục thành hai phần: ảnh và khung bên phải */
                flex: 1;  /* Chiếm toàn bộ không gian còn lại */
            }}
            .image-container {{
                flex: 1.1;  /* Chiếm 2 phần không gian của bố cục */
                display: flex;
                justify-content: center;  /* Căn giữa ảnh theo chiều ngang */
                align-items: center;  /* Căn giữa ảnh theo chiều dọc */
                background-color: #f9f9f9;  /* Đặt màu nền xám nhạt cho khung ảnh */
            }}
            .image-container img {{
                max-width: 90%;  /* Đặt chiều rộng tối đa của ảnh là 90% chiều rộng khung */
                height: auto;  /* Đảm bảo tỷ lệ khung hình của ảnh không bị méo */
            }}
            .right-container {{
                flex: 1;  /* Chiếm 1 phần không gian của bố cục */
                display: flex;
                flex-direction: column;  /* Sắp xếp các phần tử theo chiều dọc */
                background-color: #e0e0e0;  /* Đặt màu nền xám nhạt cho khung bên phải */
                padding: 10px;  /* Thêm khoảng cách bên trong khung */
            }}
            .box-cai-dat {{
                flex: 1;  /* Đặt khung chiếm 1 phần không gian trong container Flexbox */
                display: flex;  /* Sử dụng Flexbox để sắp xếp các phần tử bên trong khung */
                justify-content: flex-start;  /* Căn các phần tử bên trong khung về phía bên trái theo chiều ngang */
                align-items: flex-start;  /* Căn các phần tử bên trong khung về phía trên theo chiều dọc */
                margin: 10px;  /* Thêm khoảng cách 10px xung quanh khung */
                background-color: #ffffff;  /* Đặt màu nền của khung là màu trắng */
                border: 1px solid #ccc;  /* Thêm viền 1px màu xám nhạt cho khung */
                border-radius: 5px;  /* Bo tròn các góc của khung với bán kính 5px */
                font-size: 1.2em;  /* Đặt kích thước chữ bên trong khung là 1.2 lần kích thước mặc định */
                font-weight: bold;  /* Đặt chữ bên trong khung in đậm */
                padding-left: 20px;  /* Thêm khoảng cách 10px bên trái nội dung bên trong khung */
                padding-top: 25px;  /* Thêm khoảng cách 25px bên trên nội dung bên trong khung (dành riêng cho khung "Điều chỉnh vị trí AGV") */
            }}
            .name_project {{
                width: 200px;
            }}

            .delete_project_button, #upload_project_button {{
                transition: background-color 0.3s ease;
            }}

            .box-ve-ban-do {{
                flex: 1;
                display: flex;
                justify-content: flex-start;
                align-items: flex-start;
                margin: 10px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1.2em;
                font-weight: bold;
                padding-left: 10px;
                padding-top: 5px; /* Padding riêng cho khung "Vẽ bản đồ" */
            }}

            .box-dieu-chinh-agv {{
                flex: 1;
                display: flex;
                justify-content: flex-start;
                align-items: flex-start;
                margin: 10px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1.2em;
                font-weight: bold;
                padding-left: 10px;
                padding-top: 25px; /* Padding riêng cho khung "Điều chỉnh vị trí AGV" */
            }}

            .box-dieu-khien-agv {{
                flex: 1;
                display: flex;
                justify-content: flex-start;
                align-items: flex-start;
                margin: 10px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1.2em;
                font-weight: bold;
                padding-left: 10px;
                padding-top: 15px; /* Padding riêng cho khung "Điều khiển AGV" */
            }}

            .box-khac {{
                flex: 1;
                display: flex;
                justify-content: flex-start;
                align-items: flex-start;
                margin: 10px;
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1.2em;
                font-weight: bold;
                padding-left: 10px;
                padding-top: 10px; /* Padding riêng cho khung "Khác" */
            }}
            .box-label {{
                position: absolute;  /* Đặt vị trí tuyệt đối để nhãn nằm bên ngoài khung */
                top: -15px;  /* Đặt nhãn sát mép trên của khung */
                left: 10px;  /* Căn nhãn sang bên trái */
                background-color: #90ee90;  /* Đặt màu nền xám nhạt cho nhãn */
                padding: 2px 5px;  /* Thêm khoảng cách bên trong nhãn */
                font-size: 1em;  /* Đặt kích thước chữ cho nhãn */
                font-weight: bold;  /* Đặt chữ in đậm */
                border-radius: 3px;  /* Bo tròn các góc của nhãn */
            }}
            .combobox-container {{
                display: flex;  /* Sử dụng Flexbox để căn chỉnh combobox và nhãn */
                align-items: center;  /* Căn giữa combobox và nhãn theo chiều dọc */
                justify-content: flex-start;  /* Căn sát mép trái */
                margin: 10px 0;  /* Thêm khoảng cách giữa các dòng */
            }}
            .pro_name {{
                font-size: 20px; /* Điều chỉnh cỡ chữ, thay đổi giá trị này theo nhu cầu */
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                height: 60px;
                width: 250px;
            }}

            .combobox-row {{
                display: flex;  /* Sử dụng Flexbox để sắp xếp các phần tử theo hàng ngang */
                flex-wrap: wrap;  /* Cho phép xuống dòng nếu không đủ không gian */
                justify-content: space-between;  /* Căn đều các phần tử trong dòng */
                gap: 20px;  /* Thêm khoảng cách giữa các phần tử */
                margin-bottom: 20px;  /* Thêm khoảng cách giữa các dòng */
            }}

            .combobox-container label {{
                margin-right: 10px;  /* Thêm khoảng cách giữa nhãn và combobox */
                font-size: 1em;  /* Đặt kích thước chữ cho nhãn */
                font-weight: normal;  /* Đặt chữ thường cho nhãn */
                white-space: nowrap;  /* Đảm bảo nhãn không xuống dòng */
            }}

            .combobox-container select {{
                padding: 5px;  /* Thêm khoảng cách bên trong combobox */
                font-size: 1em;  /* Đặt kích thước chữ cho combobox */
                height: 40px;  /* Đặt chiều cao cho combobox */
                width: auto;  /* Đặt chiều rộng tự động cho combobox */
            }}
            .sub-box-container-horizontal {{
                display: flex;  /* Sử dụng Flexbox để sắp xếp các khung con theo chiều ngang */
                justify-content: space-between;  /* Căn đều khoảng cách giữa các khung con */
                align-items: stretch;  /* Đảm bảo các khung con có chiều cao bằng nhau */
                gap: 10px;  /* Thêm khoảng cách giữa các khung con */
                width: 100%;  /* Đặt chiều rộng của container là 100% */
                margin-top: 30px;  /* Thêm khoảng cách giữa container và mép trên của khung "Vẽ bản đồ" */
                padding-left: 20px;  /* Thêm khoảng cách với mép trái */
                padding-right: 20px;  /* Thêm khoảng cách với mép phải */
                margin-bottom: 20px;  /* Thêm khoảng cách giữa container và mép dưới của khung "Vẽ bản đồ" */
                box-sizing: border-box;  /* Đảm bảo padding không làm tăng kích thước container */
            }}

            .sub-box {{
                position: relative;  /* Đặt vị trí tương đối để căn chỉnh nhãn */
                background-color: #ffffff;  /* Đặt màu nền trắng cho khung con */
                border: 1px solid #ccc;  /* Thêm viền cho khung con */
                border-radius: 5px;  /* Bo tròn các góc của khung con */
                padding: 10px;  /* Thêm khoảng cách bên trong khung con */
                flex: 1;  /* Đặt các khung con có kích thước bằng nhau */
                height: 120px;  /* Đặt chiều cao cho khung con */
                max-width: 48%;  /* Đặt chiều rộng tối đa cho mỗi khung con là 48% để chúng nằm gọn trong container */
                box-sizing: border-box;  /* Đảm bảo padding không làm tăng kích thước khung */
            }}

            .sub-box-label {{
                position: absolute;  /* Đặt vị trí tuyệt đối để nhãn nằm bên ngoài khung con */
                top: -15px;  /* Đặt nhãn sát mép trên của khung con */
                left: 10px;  /* Căn nhãn sang bên trái */
                background-color: #e0e0e0;  /* Đặt màu nền xám nhạt cho nhãn */
                padding: 2px 5px;  /* Thêm khoảng cách bên trong nhãn */
                font-size: 0.9em;  /* Đặt kích thước chữ cho nhãn */
                font-weight: bold;  /* Đặt chữ in đậm */
                border-radius: 3px;  /* Bo tròn các góc của nhãn */
            }}

            .sub-box-content {{
                height: 100%;  /* Chiếm toàn bộ chiều cao của khung con */
                display: flex;  /* Sử dụng Flexbox để căn chỉnh nội dung */
                justify-content: center;  /* Căn giữa nội dung theo chiều ngang */
                align-items: center;  /* Căn giữa nội dung theo chiều dọc */
                margin-right: 10px;  /* Thêm khoảng cách giữa nhãn và ô nhập liệu */
                white-space: nowrap;  /* Đảm bảo nhãn không xuống dòng */
                font-weight: normal;  /* Đặt chữ in thường */
            }}
            .sub-box-chon_ban_do {{
                height: 100%;  /* Chiếm toàn bộ chiều cao của khung con */
                display: flex;  /* Sử dụng Flexbox để căn chỉnh nội dung */
                margin-right: 10px;  /* Thêm khoảng cách giữa nhãn và ô nhập liệu */
                white-space: nowrap;  /* Đảm bảo nhãn không xuống dòng */
                font-weight: normal;  /* Đặt chữ in thường */
            }}


            /* CSS cho các entry trong khung Điều chỉnh vị trí AGV */
            .box-dieu-chinh-agv .sub-box-content {{
                display: flex;  /* Sử dụng Flexbox để căn chỉnh nội dung */
                flex-direction: column;  /* Sắp xếp các phần tử theo chiều dọc */
                justify-content: space-between;  /* Căn đều khoảng cách giữa các phần tử */
                height: 100%;  /* Chiếm toàn bộ chiều cao của khung */
                padding-bottom: 15px;  /* Thêm khoảng cách 15px giữa nút và mép dưới của khung */
                box-sizing: border-box;  /* Đảm bảo padding không làm tăng kích thước khung */
            }}

            .box-dieu-chinh-agv .sub-box-content button {{
                margin-bottom: 0;  /* Đảm bảo nút không có khoảng cách mặc định bên dưới */
            }}
            .box-dieu-chinh-agv .sub-box-content input {{
                width: 100%;  /* Đặt chiều rộng của entry */
                height: 35px;  /* Đặt chiều cao cho entry */
                padding: 5px;  /* Thêm khoảng cách bên trong entry */
                border: 1px solid #ccc;  /* Thêm viền màu xám nhạt */
                border-radius: 5px;  /* Bo tròn các góc của entry */
                box-sizing: border-box;  /* Đảm bảo padding không làm tăng kích thước entry */
            }}

            .box-dieu-chinh-agv .sub-box-content label {{
                margin-right: 10px;  /* Thêm khoảng cách giữa nhãn và entry */
                white-space: nowrap;  /* Đảm bảo nhãn không xuống dòng */
                font-size: 1em;  /* Đặt kích thước chữ cho nhãn */
                width: 100px;  /* Đặt chiều rộng cố định cho nhãn */
            }}

            .box-dieu-chinh-agv .sub-box-content button {{
                padding: 7px 15px;  /* Thêm khoảng cách bên trong nút */
                border: none;  /* Loại bỏ viền nút */
                border-radius: 5px;  /* Bo tròn các góc của nút */
                cursor: pointer;  /* Thay đổi con trỏ khi hover */
            }}

            #agv_position_button {{
                background-color: #f44336;  /* Màu nền đỏ cho nút Vị trí AGV */
                color: black;  /* Màu chữ trắng */
            }}

            #agv_position_button:hover {{
                background-color: #d32f2f;  /* Màu nền khi hover cho nút Vị trí AGV */
            }}

            #update_button {{
                background-color: #4CAF50;  /* Màu nền xanh lá cho nút Update */
                color: black;  /* Màu chữ trắng */
            }}

            #update_button:hover {{
                background-color: #388E3C;  /* Màu nền khi hover cho nút Update */
            }}

            /* Container chứa hai khung con */
            .box-dieu-khien-agv .sub-box-container-horizontal {{
                display: flex;  /* Sử dụng Flexbox để sắp xếp các khung con theo chiều ngang */
                justify-content: space-between;  /* Căn đều khoảng cách giữa các khung con */
                align-items: stretch;  /* Đảm bảo các khung con có chiều cao bằng nhau */
                gap: 10px;  /* Thêm khoảng cách giữa các khung con */
                width: 100%;  /* Đặt chiều rộng của container là 100% */
                margin-top: 10px;  /* Thêm khoảng cách phía trên container */
            }}

            /* Khung con */
            .box-dieu-khien-agv .sub-box {{
                position: relative;  /* Đặt vị trí tương đối để căn chỉnh nhãn */
                background-color: #ffffff;  /* Đặt màu nền trắng cho khung con */
                border: 1px solid #ccc;  /* Thêm viền cho khung con */
                border-radius: 5px;  /* Bo tròn các góc của khung con */
                padding: 10px;  /* Thêm khoảng cách bên trong khung con */
                flex: 1;  /* Đặt các khung con có kích thước bằng nhau */
                height: 120px;  /* Đặt chiều cao cho khung con */
                box-sizing: border-box;  /* Đảm bảo padding không làm tăng kích thước khung */
                margin-top: 10px;  /* Thêm khoảng cách phía trên container */
                margin-bottom: 30px;  /* Thêm khoảng cách phía dưới container */
            }}

            /* Nhãn của khung con */
            .box-dieu-khien-agv .sub-box-label {{
                position: absolute;  /* Đặt vị trí tuyệt đối để nhãn nằm bên ngoài khung con */
                top: -15px;  /* Đặt nhãn sát mép trên của khung con */
                left: 10px;  /* Căn nhãn sang bên trái */
                background-color: #e0e0e0;  /* Đặt màu nền xám nhạt cho nhãn */
                padding: 2px 5px;  /* Thêm khoảng cách bên trong nhãn */
                font-size: 0.9em;  /* Đặt kích thước chữ cho nhãn */
                font-weight: bold;  /* Đặt chữ in đậm */
                border-radius: 3px;  /* Bo tròn các góc của nhãn */
            }}

            /* Nội dung bên trong khung con */
            .box-dieu-khien-agv .sub-box-content {{
                height: 100%;  /* Chiếm toàn bộ chiều cao của khung con */
                display: flex;  /* Sử dụng Flexbox để căn chỉnh nội dung */
                justify-content: center;  /* Căn giữa nội dung theo chiều ngang */
                align-items: center;  /* Căn giữa nội dung theo chiều dọc */
                margin-right: 10px;  /* Thêm khoảng cách giữa nhãn và ô nhập liệu */
                white-space: normal;  /* Cho phép xuống dòng nếu nội dung quá dài */
                word-wrap: break-word;  /* Tự động xuống dòng khi từ quá dài */
                word-break: break-word;  /* Ngắt từ nếu cần thiết */
                font-weight: normal;  /* Đặt chữ in thường */
                text-align: center;  /* Căn giữa nội dung theo chiều ngang */
                overflow-wrap: break-word;  /* Đảm bảo từ dài sẽ được ngắt dòng */
            }}
            
            .edit-loai_lap{{
                display: flex;
                align-items: center;
                margin-top: 15px;
            }}

            #loop_type {{
                width: auto;
            }}

            #loop_count {{
                width: 100px;
            }}

            #edit_button {{
                padding: 7px 15px;  /* Khoảng cách bên trong nút */
                background-color: #4CAF50;  /* Màu nền xanh lá */
                color: black;  /* Màu chữ trắng */
                border: none;  /* Loại bỏ viền nút */
                border-radius: 5px;  /* Bo tròn các góc nút */
                cursor: pointer;  /* Thay đổi con trỏ khi hover */
                transition: background-color 0.3s ease;  /* Hiệu ứng chuyển đổi màu */
            }}

            #run_button {{
                padding: 7px 15px;  /* Khoảng cách bên trong nút */
                background-color: #4CAF50;  /* Màu nền xanh lá */
                color: black;  /* Màu chữ trắng */
                border: none;  /* Loại bỏ viền nút */
                border-radius: 5px;  /* Bo tròn các góc nút */
                cursor: pointer;  /* Thay đổi con trỏ khi hover */
                transition: background-color 0.3s ease;  /* Hiệu ứng chuyển đổi màu */
            }}

            .save-run-button-container {{
                display: flex;  /* Sử dụng Flexbox để căn chỉnh nội dung */
                justify-content: flex-start;  /* Căn nút sang bên phải */
                align-items: center;  /* Căn giữa theo chiều dọc */
                margin-top: -30px;  /* Thêm khoảng cách phía trên container */
            }}

            #save_button {{
                padding: 7px 15px;  /* Khoảng cách bên trong nút */
                background-color: #4CAF50;  /* Màu nền xanh lá */
                color: black;  /* Màu chữ trắng */
                border: none;  /* Loại bỏ viền nút */
                border-radius: 5px;  /* Bo tròn các góc nút */
                cursor: pointer;  /* Thay đổi con trỏ khi hover */
                transition: background-color 0.3s ease;  /* Hiệu ứng chuyển đổi màu */
            }}

            #btn_up, #btn_down, #btn_left, #btn_right, #btn_stop, #btn_toggle {{
                font-size: 15px;
                font-weight: bold;
                color: white;
                transition: background-color 0.3s ease;
            }}
        </style>
    </head>
    <body>
        <div class="header">AGV LIDAR BROTHER</div>
        <div class="content">
            <div class="image-container">
                <!-- Thay ảnh bằng video -->
                <!-- <img src="/video_feed" alt="Video Stream" style="width: 100%; height: auto;" onclick="getPixelCoordinates(event)"> -->
                <img src="/video_feed" alt="Video Stream" style="width: 100%; height: auto;" onclick="getPixelCoordinates(event)">
            </div>
            <div class="right-container">
                <div class="box box-cai-dat" style="position: relative;">
                    <label class="box-label">Cài đặt</label>
                    <div class="combobox-row">
                        <div class="combobox-container">
                            <label for="tien_max">Vận tốc tiến max:</label>
                            <select id="tien_max" name="tien_max" style="height: 40px;" onchange="updateSettings()">
                                {''.join([f'<option value="{v}" {"selected" if v == data_cai_dat["tien_max"] else ""}>{v}</option>' for v in list_tien_max])}
                            </select>
                        </div>
                        <div class="combobox-container">
                            <label for="re_max">Vận tốc rẽ max:</label>
                            <select id="re_max" name="re_max" style="height: 40px;" onchange="updateSettings()">
                                {''.join([f'<option value="{v}" {"selected" if v == data_cai_dat["re_max"] else ""}>{v}</option>' for v in list_re_max])}
                            </select>
                        </div>
                    </div>
                    <div class="combobox-row">
                        <div class="combobox-container">
                            <label for="grid_size">Grid size:</label>
                            <select id="grid_size" name="grid_size" style="height: 40px;" onchange="updateSettings()">
                                {''.join([f'<option value="{v}" {"selected" if v == data_cai_dat["grid_size"] else ""}>{v}</option>' for v in list_grid_size])}
                            </select>
                        </div>
                        <div class="combobox-container">
                            <label for="agv_size">AGV size:</label>
                            <select id="agv_size" name="agv_size" style="height: 40px;" onchange="updateSettings()">
                                {''.join([f'<option value="{v}" {"selected" if v == data_cai_dat["agv_size"] else ""}>{v}</option>' for v in list_agv_size])}
                            </select>
                        </div>
                    </div>
                    <div class="combobox-row">
                        <!-- Combobox Project Name -->
                        <div class="pro_name">
                            <label for="project_name">Project name:</label>
                            <input list="project_list" id="project_name" name="project_name" style="font-size: 20px;" placeholder="Enter or select project">
                            <datalist id="project_list">
                                {''.join([f'<option value="{project}">{project}</option>' for project in os.listdir(path_project_all)])}
                            </datalist>
                        </div>
                        <!-- Buttons -->
                        <div class="button-container">
                            <button id="delete_project_button" style="font-size: 20px;" onclick="deleteProject()">Delete</button>
                            <button id="upload_project_button" style="font-size: 20px;" onclick="uploadProject()">Upload</button>
                        </div>
                    </div>
                </div>
                <div class="box box-ve-ban-do" style="position: relative;">
                    <label class="box-label">Vẽ bản đồ</label>
                    <div class="sub-box-container-horizontal">
                        <div class="sub-box">
                            <label class="sub-box-label">Chọn bản đồ</label>
                            <div class="sub-box-chon_ban_do" style="flex-direction: column;">
                                    <div class="combobox-container">
                                        <label for="map_name">Tên bản đồ:</label>
                                        <select id="map_name" name="map_name" style="height: 40px; width: 100%;">
                                            {''.join([f'<option value="{name}">{name}</option>' for name in list_name_map])}
                                        </select>
                                    </div>
                                    <div style="margin-top: 7px; text-align: right; width: 100%; align-items: flex-end;">
                                        <select id="update_mode" name="update_mode" style="height: 30px; padding: 5px; border: 1px solid #ccc; border-radius: 5px; margin-left: 10px;">
                                            <option value="no_update">No update</option>
                                            <option value="update">Update</option>
                                        </select>
                                        <button id="update" type="submit" onclick="chon_ban_do_handleUpdateButton()" style="padding: 7px 15px;background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer;">Update</button>
                                    </div>
                            </div>
                        </div>
                        <div class="sub-box">
                            <label class="sub-box-label">Bản đồ mới</label>
                            <div class="sub-box-content" style="flex-direction: column; justify-content: space-between;">
                                <!-- Thanh nhập tên bản đồ cùng hàng với nhãn -->
                                <div style="display: flex; align-items: center; width: 100%; margin-bottom: 10px;">
                                    <label for="new_map_name" style="margin-right: 10px; white-space: nowrap;">Tên bản đồ:</label>
                                    <input type="text" id="new_map_name" name="new_map_name" style="flex: 1; height: 40px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;" placeholder="Nhập tên bản đồ">
                                </div>
                                <!-- Nút Save và Reset -->
                                <div style="display: flex; justify-content: space-between; width: 100%; margin-top: auto;">
                                    <button id="reset_button" onclick="ban_do_moi_handleResetButton()"  style="padding: 7px 15px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer;">Reset</button>
                                    <button id="start_stop_button" onclick="ban_do_moi_handleStartButton()" style="padding: 7px 15px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer;">Start</button>
                                    <button id="save_button" onclick="ban_do_moi_handleSaveButton()"  style="padding: 7px 15px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer;">Save</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="box box-dieu-chinh-agv" style="position: relative;">
                    <label class="box-label">Điều chỉnh vị trí AGV</label>
                    <div class="sub-box-content" style="flex-direction: column; justify-content: space-between; height: 100%; padding-bottom: 15px;">
                        <!-- Entry Tọa độ X -->
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <label for="x_coord" style="margin-right: 10px; white-space: nowrap; width: 100px;">Tọa độ X:</label>
                            <input type="text" id="x_coord" name="x_coord" style="flex: 1; height: 35px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;" placeholder="Nhập tọa độ X">
                        </div>
                        <!-- Entry Tọa độ Y -->
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <label for="y_coord" style="margin-right: 10px; white-space: nowrap; width: 100px;">Tọa độ Y:</label>
                            <input type="text" id="y_coord" name="y_coord" style="flex: 1; height: 35px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;" placeholder="Nhập tọa độ Y">
                        </div>
                        <!-- Entry Góc Alpha -->
                        <div style="display: flex; align-items: center; margin-bottom: 20px;">
                            <label for="alpha_angle" style="margin-right: 10px; white-space: nowrap; width: 100px;">Góc Alpha:</label>
                            <input type="text" id="alpha_angle" name="alpha_angle" style="flex: 1; height: 35px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;" placeholder="Nhập góc Alpha">
                        </div>
                        <!-- Nút Vị trí AGV và Update -->
                        <div style="display: flex; justify-content: space-between; width: 100%; margin-top: auto;">
                            <button id="agv_position_button" onclick="dieu_chinh_agv_position_button();" style="padding: 7px 15px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer;">Vị trí AGV</button>
                            <button id="update_button" onclick="dieu_chinh_agv_handleUpdateButton();" style="padding: 7px 15px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer;">Update</button>
                        </div>
                    </div>
                    <!-- Khung Điều khiển tay cầm -->
                    <div class="sub-box-content" style="flex-direction: column; justify-content: space-between; height: 100%; padding-bottom: 5px; margin-top: 0px;">
                        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px; margin-left: 100px;">
                            <button id="btn_up" style="width: 50px; height: 30px; background-color: #4CAF50; border: none; border-radius: 5px; cursor: pointer;">↑</button>
                        </div>
                        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px; margin-left: 100px;">
                            <button id="btn_left" style="width: 50px; height: 30px; background-color: #4CAF50; border: none; border-radius: 5px; cursor: pointer;">←</button>
                            <button id="btn_stop" style="width: 50px; height: 30px; background-color: #4CAF50; border: none; border-radius: 5px; cursor: pointer;">■</button>
                            <button id="btn_right" style="width: 50px; height: 30px; background-color: #4CAF50; border: none; border-radius: 5px; cursor: pointer;">→</button>
                        </div>
                        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px; margin-left: 100px;">
                            <button id="btn_down" style="width: 50px; height: 30px; background-color: #4CAF50; border: none; border-radius: 5px; cursor: pointer;">↓</button>
                        </div>
                        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px; margin-left: 100px;">
                            <button id="btn_toggle" onclick="toggleControlMode();" style="width: 100px; height: 30px; background-color: #4CAF50; border: none; border-radius: 5px; cursor: pointer;">OFF</button>
                        </div>
                    </div>
                </div>
                <div class="box box-dieu-khien-agv" style="position: relative;">
                    <label class="box-label">Điều khiển AGV</label>
                    <div class="sub-box-container-horizontal">
                        <!-- Khung Chỉnh sửa đường đi -->
                        <div class="sub-box">
                            <label class="sub-box-label">Chỉnh sửa đường đi</label>  <!-- Nhãn của ô -->
                            <div class="sub-box-content" style="display: flex; flex-direction: column; gap: 10px;">
                                <!-- Hàng đầu tiên -->
                                <div style="display: flex; justify-content: space-between; gap: 10px;">
                                    <button id="add_point" onclick="toggle_add_point();" style="flex: 1; height: 30px; width: 130px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer; white-space: nowrap;">Thêm điểm</button>
                                    <button id="edit_point" onclick="toggle_edit_point();" style="flex: 1; height: 30px; width: 130px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer; white-space: nowrap;">Chỉnh sửa điểm</button>
                                </div>
                                <!-- Hàng thứ hai -->
                                <div style="display: flex; justify-content: space-between; gap: 10px;">
                                    <button id="them_duong" onclick="toggle_btn_straight_line();" style="flex: 1; height: 30px; width: 130px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer; white-space: nowrap;">Thêm đường</button>
                                    <button id="chinh_sua_duong" onclick="toggle_btn_curve();" style="flex: 1; height: 30px; width: 130px; background-color: #4CAF50; color: black; border: none; border-radius: 5px; cursor: pointer; white-space: nowrap;">Chỉnh sửa đường</button>
                                </div>
                            </div>
                            <!-- Nút Edit/Close edit -->
                            <div class="edit-loai_lap">
                                <select id="loop_type" style="height: 35px; padding: 5px; border: 1px solid #ccc; border-radius: 5px;" onchange="updateLoopType()">
                                    <option value="lien_tuc">Lặp liên tục</option>
                                    <option value="so_luong">Lặp số lượng</option>
                                </select>
                                <input type="text" id="loop_count" placeholder="Số lần lặp (nếu có)" style="height: 20px; padding: 5px; border: 1px solid #ccc; border-radius: 5px; margin-left: 10px; width: 150px;" oninput="updateLoopCount()">
                            </div>
                        </div>
                        <!-- Khung Danh sách đường đi -->
                        <div class="sub-box">
                            <label class="sub-box-label">Danh sách đường đi</label>
                            <div class="sub-box-content">
                                <!-- Thêm khung nhập liệu dạng textarea -->
                                <textarea id="duong_di_input" placeholder="NAME: DUONG_DI_1 \nX1: START-L0-P1-NONE \nX2: P1-L1-P2-O1, P2-L1-P1-O1 \nALL: P1-L1-P2-O1, P2-L2-P3-O1"
                                        style="width: 100%; height: 100px; padding: 5px; border: 1px solid #ccc; border-radius: 5px; resize: none; overflow-wrap: break-word;"></textarea>
                            </div>
                            <div class="save-run-button-container">
                                <button id="save_button" onclick="danh_sach_duong_di_toggleSave()" style="margin-top: 50px; display: flex; justify-content: flex-start; align-items: center;">Save</button>
                                <button id="upload_button" onclick="handleUploadClick()" style="margin-top: 50px; margin-left: 50px; display: flex; justify-content: flex-start; align-items: center; font-size: 16px; height:30px;">Upload</button>
                                <!-- Combobox thêm vào -->
                                <select id="list_duong_di_combobox" style="margin-top: 50px; margin-left: 5px; height: 30px; width: 150px; text-align: center; text-align-last: center; justify-content: center;">
                                    {''.join([f'<option value="{duong}">{duong}</option>' for duong in list_duong_di])}
                                </select>
                                <button id="run_button" onclick="danh_sach_duong_di_toggleRunStop()" style="margin-top: 50px; display: flex; justify-content: flex-end; align-items: center; margin-left: auto;">Run</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="box box-khac" style="position: relative;">
                    <label class="box-label">Khác</label>
                </div>
            </div>
        </div>

    <script>
        


//////////////////////////////////////////////////////////// cai dat  ////////////////////////////////////////////////////////////
        function updateSettings() {{
            // Lấy giá trị từ các combobox
            const tien_max = document.getElementById('tien_max').value;
            const re_max = document.getElementById('re_max').value;
            const grid_size = document.getElementById('grid_size').value;
            const agv_size = document.getElementById('agv_size').value;

            // Tạo dữ liệu để gửi
            const data = {{
                tien_max: tien_max,
                re_max: re_max,
                grid_size: grid_size,
                agv_size: agv_size
            }};

            // Gửi dữ liệu qua AJAX
            fetch('/update_settings', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Cập nhật thành công:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi cập nhật:', error);
            }});
        }}
        function deleteProject() {{
        const projectName = document.getElementById('project_name').value;

        if (!projectName) {{
            alert('Vui lòng chọn hoặc nhập tên project để xóa.');
            return;
        }}

        fetch('/delete_project', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ project_name: projectName }})
        }})
        .then(response => response.json())
        .then(result => {{
            alert(result.message);
            if (result.status === 'success') {{
                location.reload(); // Làm mới trang để cập nhật danh sách
            }}
        }})
        .catch(error => {{
            console.error('Lỗi khi xóa project:', error);
        }});
        }}

        function uploadProject() {{
            const projectName = document.getElementById('project_name').value;

            if (!projectName) {{
                alert('Vui lòng chọn hoặc nhập tên project để upload.');
                return;
            }}

            fetch('/upload_project', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ project_name: projectName }})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    // Lưu giá trị project_name vào localStorage
                    localStorage.setItem('selectedProjectName', projectName);

                    const mapSelect = document.getElementById('map_name');
                    mapSelect.innerHTML = ''; // Xóa các giá trị cũ
                    result.list_name_map.forEach(mapName => {{
                        const option = document.createElement('option');
                        option.value = mapName;
                        option.textContent = mapName;
                        mapSelect.appendChild(option); // Thêm các lựa chọn mới
                    
                    }});
                    location.reload(); // Làm mới trang để cập nhật danh sách
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi upload project:', error);
            }});
        }}


//////////////////////////////////////////////////////////// ve ban do  ////////////////////////////////////////////////////////////
        function ban_do_moi_handleResetButton() {{
            const resetButton = document.getElementById('reset_button');
            const mapName = document.getElementById('new_map_name').value; // Lấy thanh entry "Bản đồ mới"

            if (!mapName || "{ path_project }" === "") {{
                alert('Vui lòng điền tên bản đồ và đảm bảo dự án đã được chọn trước khi bắt đầu!');
                return; // Dừng thực hiện nếu tên bản đồ rỗng hoặc chưa chọn dự án
            }}

            // Gửi dữ liệu về server
            fetch('/map_action', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(['reset', mapName]) // Gửi hành động "reset" và tên bản đồ
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Phản hồi từ server:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi dữ liệu:', error);
            }});

            // Đổi màu sang xanh dương (Dodger Blue)
            resetButton.style.backgroundColor = '#1E90FF'; // Mã màu xanh dương Dodger Blue

            // Sau 1 giây, đổi lại màu xanh lá
            setTimeout(() => {{
                resetButton.style.backgroundColor = '#4CAF50'; // Mã màu xanh lá
            }}, 1000); // 1000ms = 1 giây
        }}

        let text_button = "stop"; // Biến toàn cục để lưu trạng thái Start/Stop
        function ban_do_moi_handleStartButton() {{
            const startButton = document.getElementById('start_stop_button');
            const mapName = document.getElementById('new_map_name').value; // Lấy tên bản đồ từ ô nhập liệu
            
            if (!mapName || "{ path_project }" === "") {{
                alert('Vui lòng điền tên bản đồ và đảm bảo dự án đã được chọn trước khi bắt đầu!');
                return; // Dừng thực hiện nếu tên bản đồ rỗng hoặc chưa chọn dự án
            }}

            const button = document.getElementById('start_stop_button');
            if (text_button === "stop") {{
                text_button = "start";
                button.innerText = "Stop"; // Đổi chữ trên nút thành "Stop"
                button.style.backgroundColor = "#1E90FF"; // Đổi màu nút sang xanh dương
            }} else {{
                text_button = "stop";
                button.innerText = "Start"; // Đổi chữ trên nút thành "Start"
                button.style.backgroundColor = "#4CAF50"; // Đổi màu nút sang xanh lá
            }}
            // Gửi dữ liệu về server
            fetch('/map_action', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify([text_button, mapName]) // Gửi hành động "save" và tên bản đồ
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Phản hồi từ server:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi dữ liệu:', error);
            }});
        }}
        function ban_do_moi_handleSaveButton() {{
            const saveButton = document.getElementById('save_button');
            const mapName = document.getElementById('new_map_name').value; // Lấy tên bản đồ từ ô nhập liệu
            
            if (!mapName || "{ path_project }" === "") {{
                alert('Vui lòng điền tên bản đồ và đảm bảo dự án đã được chọn trước khi bắt đầu!');
                return; // Dừng thực hiện nếu tên bản đồ rỗng hoặc chưa chọn dự án
            }}

            // Gửi dữ liệu về server
            fetch('/map_action', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(['save', mapName]) // Gửi hành động "save" và tên bản đồ
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Phản hồi từ server:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi dữ liệu:', error);
            }});

            // Đổi màu sang xanh dương (Dodger Blue)
            saveButton.style.backgroundColor = '#1E90FF'; // Mã màu xanh dương Dodger Blue

            // Sau 1 giây, đổi lại màu xanh lá
            setTimeout(() => {{
                saveButton.style.backgroundColor = '#4CAF50'; // Mã màu xanh lá
            }}, 1000); // 1000ms = 1 giây
        }}
        
        function chon_ban_do_handleUpdateButton() {{
            const resetButton = document.getElementById('update');
            const mapSelect = document.getElementById('map_name'); // Lấy combobox tên bản đồ
            const selectedMap = mapSelect.value; // Lấy giá trị được chọn trong combobox
            const ModeSelect = document.getElementById('update_mode'); // Lấy combobox Update/No Update
            const selectMode = ModeSelect.value; // Lấy giá trị được chọn trong combobox Update/No Update

            if ("{ path_project }" === "") {{
                alert('Vui lòng chọn dự án đã được chọn trước khi bắt đầu!');
                return; // Dừng thực hiện nếu tên bản đồ rỗng hoặc chưa chọn dự án
            }}

            if (selectedMap) {{ // Kiểm tra nếu giá trị không rỗng
                // Gửi dữ liệu về server để cập nhật trạng thái
                fetch('/update_map_action', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        selectMode: selectMode,
                        selectedMap: selectedMap
                    }})
                }})
                .then(response => response.json())
                .then(result => {{
                    console.log('Phản hồi từ server:', result);
                    if (result.status === 'success') {{
                        alert(`Đã load thành công bản đồ: ${{selectedMap}}`);
                    }} else {{
                        alert(`Lỗi: ${{result.message}}`);
                    }}
                }})
                .catch(error => {{
                    console.error('Lỗi khi gửi dữ liệu:', error);
                    alert('Đã xảy ra lỗi khi load bản đồ.');
                }});
            }} else {{
                alert('Vui lòng chọn một bản đồ!');
            }}

            // Đổi màu sang xanh dương (Dodger Blue)
            resetButton.style.backgroundColor = '#1E90FF'; // Mã màu xanh dương Dodger Blue

            // Sau 1 giây, đổi lại màu xanh lá
            setTimeout(() => {{
                resetButton.style.backgroundColor = '#4CAF50'; // Mã màu xanh lá
            }}, 1000); // 1000ms = 1 giây
        }}
///////////////////////////////////////////////////// điều chỉnh vị trí agv  ////////////////////////////////////////////////////////////
        function dieu_chinh_agv_position_button() {{
            const button = document.getElementById('agv_position_button');
            const backgroundColor = window.getComputedStyle(button).backgroundColor;
            // Lấy giá trị từ các entry
            const x = document.getElementById('x_coord').value;
            const y = document.getElementById('y_coord').value;
            const alphaAngle = document.getElementById('alpha_angle').value;

            let update_vi_tri_agv = 0;
                if (backgroundColor === 'rgb(30, 144, 255)'){{
                    update_vi_tri_agv = 0;
                }}
                else{{
                    update_vi_tri_agv = 1;
                }}

            // Kiểm tra nếu màu nền là màu xanh (mã RGB: rgb(76, 175, 80))
            if (backgroundColor === 'rgb(76, 175, 80)') {{
                button.style.backgroundColor = '#1E90FF';  // Đổi màu sang xanh dương
                console.log('Nút có màu xanh.');
            }} else {{
                console.log('Nút không có màu xanh.');
                button.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
            }}
            // Gửi tọa độ pixel về server qua AJAX
            fetch('/get_pixel_coordinates', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ x: x, y: y, alpha: alphaAngle, update_vi_tri_agv: update_vi_tri_agv}})
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Phản hồi từ server:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi tọa độ pixel:', error);
            }});
        }}
        function dieu_chinh_agv_handleUpdateButton() {{
            const button = document.getElementById('agv_position_button');
            button.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh

            // Lấy giá trị từ các entry
            const xCoord = document.getElementById('x_coord').value;
            const yCoord = document.getElementById('y_coord').value;
            const alphaAngle = document.getElementById('alpha_angle').value;

            if (xCoord === "" || yCoord === "" || alphaAngle === "") {{
                alert('Vui lòng chọn các tọa độ và góc anpha!');
                return;
            }}

            // Gửi dữ liệu về server
            fetch('/chon_ban_do_update', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    x: xCoord,
                    y: yCoord,
                    alpha: alphaAngle
                }})
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Phản hồi từ server:', result);
                if (result.status === 'success') {{
                    alert('Đã cập nhật thành công vị trí AGV!');
                }} else {{
                    alert(`Lỗi: ${{result.message}}`);
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi dữ liệu:', error);
            }});

            const updateButton = document.getElementById('update_button');

            // Đổi màu sang xanh dương (Dodger Blue)
            updateButton.style.backgroundColor = '#1E90FF'; // Mã màu xanh dương Dodger Blue

            // Sau 1 giây, đổi lại màu xanh lá
            setTimeout(() => {{
                updateButton.style.backgroundColor = '#4CAF50'; // Mã màu xanh lá
            }}, 1000); // 1000ms = 1 giây
        }}
        // Hàm chuyển đổi trạng thái ON/OFF
        function toggleControlMode() {{
            const btnToggle = document.getElementById("btn_toggle");

            // Gửi yêu cầu đến route để thay đổi giá trị của data_dk_tay
            fetch('/toggle_control_mode', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }}
            }})
            .then(response => response.json())
            .then(result => {{
                if (result.status === 'success') {{
                    const newValue = result.data_dk_tay; // Lấy giá trị mới của data_dk_tay từ server
                    if (newValue === 1) {{
                        btnToggle.style.backgroundColor = "#1E90FF"; // Xanh dương
                        btnToggle.innerText = "ON";
                    }} else {{
                        btnToggle.style.backgroundColor = "#4CAF50"; // Xanh lá
                        btnToggle.innerText = "OFF";
                        resetControlButtons();
                    }}
                }} else {{
                    console.error('Lỗi khi cập nhật trạng thái:', result.message);
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi yêu cầu:', error);
            }});
        }}

        // Hàm reset màu các nút
        function resetControlButtons() {{
            document.getElementById("btn_up").style.backgroundColor = "#4CAF50";
            document.getElementById("btn_down").style.backgroundColor = "#4CAF50";
            document.getElementById("btn_left").style.backgroundColor = "#4CAF50";
            document.getElementById("btn_right").style.backgroundColor = "#4CAF50";
        }}

        // Bắt sự kiện nhấn phím
        document.addEventListener("keydown", (event) => {{
            // Kiểm tra trạng thái của nút "btn_toggle"
            const btnToggle = document.getElementById("btn_toggle");
            if (btnToggle.innerText === "ON") {{ // Nếu nút đang ở trạng thái ON
                switch (event.key) {{
                    case "ArrowUp":
                        document.getElementById("btn_up").style.backgroundColor = "#1E90FF"; // Đổi màu nút
                        updateDataDkTay({{ tien: 1, lui: 0, trai: 0, phai: 0, stop: 0 }}); // Gửi dữ liệu
                        break;
                    case "ArrowDown":
                        document.getElementById("btn_down").style.backgroundColor = "#1E90FF";
                        updateDataDkTay({{ tien: 0, lui: 1, trai: 0, phai: 0, stop: 0 }});
                        break;
                    case "ArrowLeft":
                        document.getElementById("btn_left").style.backgroundColor = "#1E90FF";
                        updateDataDkTay({{ tien: 0, lui: 0, trai: 1, phai: 0, stop: 0 }});
                        break;
                    case "ArrowRight":
                        document.getElementById("btn_right").style.backgroundColor = "#1E90FF";
                        updateDataDkTay({{ tien: 0, lui: 0, trai: 0, phai: 1, stop: 0 }});
                        break;
                }}
            }}
        }});

        // Bắt sự kiện nhả phím
        document.addEventListener("keyup", (event) => {{
            // Kiểm tra trạng thái của nút "btn_toggle"
            const btnToggle = document.getElementById("btn_toggle");
            if (btnToggle.innerText === "ON") {{ // Nếu nút đang ở trạng thái ON
                switch (event.key) {{
                    case "ArrowUp":
                        document.getElementById("btn_up").style.backgroundColor = "#4CAF50"; // Trả lại màu ban đầu
                        break;
                    case "ArrowDown":
                        document.getElementById("btn_down").style.backgroundColor = "#4CAF50";
                        break;
                    case "ArrowLeft":
                        document.getElementById("btn_left").style.backgroundColor = "#4CAF50";
                        break;
                    case "ArrowRight":
                        document.getElementById("btn_right").style.backgroundColor = "#4CAF50";
                        break;
                }}
                updateDataDkTay({{ tien: 0, lui: 0, trai: 0, phai: 0, stop: 1 }}); // Reset trạng thái
            }}
        }});

        // Hàm gửi yêu cầu cập nhật data_data_dk_tay
        function updateDataDkTay(data) {{
            fetch('/update_data_dk_tay', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Cập nhật data_data_dk_tay:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi cập nhật data_data_dk_tay:', error);
            }});
        }}

        // Bắt sự kiện nhả phím
        document.addEventListener("keyup", (event) => {{
            if ({dk_agv_thu_cong} === 1) {{
                switch (event.key) {{
                    case "ArrowUp":
                        document.getElementById("btn_up").style.backgroundColor = "#4CAF50";
                        break;
                    case "ArrowDown":
                        document.getElementById("btn_down").style.backgroundColor = "#4CAF50";
                        break;
                    case "ArrowLeft":
                        document.getElementById("btn_left").style.backgroundColor = "#4CAF50";
                        break;
                    case "ArrowRight":
                        document.getElementById("btn_right").style.backgroundColor = "#4CAF50";
                        break;
                }}
                resetControlButtons();
            }}
        }});
//////////////////////////////////////////////////////////// điều khiển agv  ////////////////////////////////////////////////////////////
        
        function toggle_btn_curve() {{
            const button_btn_curve = document.getElementById('chinh_sua_duong');
            const backgroundColor = window.getComputedStyle(button_btn_curve).backgroundColor;

            const button_straight_line = document.getElementById('them_duong');
            const button_edit_point = document.getElementById('edit_point');
            const button_add_point = document.getElementById('add_point');

            // Kiểm tra nếu màu nền là màu xanh (mã RGB: rgb(76, 175, 80))
            if (backgroundColor === 'rgb(76, 175, 80)') {{
                button_btn_curve.style.backgroundColor = '#1E90FF';  // Đổi màu sang xanh dương
                button_straight_line.style.backgroundColor = '#4CAF50';
                button_edit_point.style.backgroundColor = '#4CAF50';
                button_add_point.style.backgroundColor = '#4CAF50';
                console.log('Nút có màu xanh.');
                showEditLineModal();
            }} else {{
                console.log('Nút không có màu xanh.');
                button_btn_curve.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
            }}
        }}
        // danh sach duong di
        function danh_sach_duong_di_toggleRunStop() {{
            const button = document.getElementById('run_button');

            const inputValue = document.getElementById('duong_di_input').value; // Lấy giá trị từ textarea

            if (!inputValue.trim()) {{
                alert("Vui lòng nhập dữ liệu đường đi trước khi chạy!");
                return;
            }}

            // Kiểm tra trạng thái của nút
            let run_stop = "";
            if (button.innerText === 'Run') {{
                button.innerText = 'Stop';
                button.style.backgroundColor = '#1E90FF';  // Đổi màu sang xanh dương
                run_stop = "run";
            }} else {{
                button.innerText = 'Run';
                button.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
                run_stop = "stop";
            }}

            // Gửi dữ liệu về server
            fetch('/toggle_run_stop', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    data_text_box: inputValue,
                    run_stop: run_stop
                }})
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Phản hồi từ server:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi gửi dữ liệu:', error);
            }});

        }}
        function danh_sach_duong_di_toggleSave() {{
            const button = document.getElementById('save_button');
            const inputValue = document.getElementById('duong_di_input').value; // Lấy giá trị từ textarea
            
            if ("{ path_project }" === "") {{
                alert('Vui lòng chọn dự án đã được chọn trước khi bắt đầu!');
                return; // Dừng thực hiện nếu tên bản đồ rỗng hoặc chưa chọn dự án
            }}

            if (!inputValue.trim()) {{
                alert("Vui lòng nhập dữ liệu đường đi trước khi lưu!");
                return;
            }}

            // Gửi dữ liệu đến server
            fetch('/save_duong_di', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ duong_di: inputValue }}) // Gửi giá trị đường đi
            }})
            .then(response => response.json())
            .then(result => {{
                if (result.status === 'success') {{
                    alert("Đã lưu dữ liệu đường đi thành công!");
                }} else {{
                    alert(`Lỗi: ${{result.message}}`);
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi lưu dữ liệu đường đi:', error);
            }});
        }}
        function toggle_btn_straight_line() {{
            const button_straight_line = document.getElementById('them_duong');
            const backgroundColor = window.getComputedStyle(button_straight_line).backgroundColor;

            const button_btn_curve = document.getElementById('chinh_sua_duong');
            const button_edit_point = document.getElementById('edit_point');
            const button_add_point = document.getElementById('add_point');

            // Kiểm tra nếu màu nền là màu xanh (mã RGB: rgb(76, 175, 80))
            if (backgroundColor === 'rgb(76, 175, 80)') {{
                button_straight_line.style.backgroundColor = '#1E90FF';  // Đổi màu sang xanh dương
                button_btn_curve.style.backgroundColor = '#4CAF50';
                button_edit_point.style.backgroundColor = '#4CAF50';
                button_add_point.style.backgroundColor = '#4CAF50';
                console.log('Nút có màu xanh.');

                showStraightLineModal()
            }} else {{
                console.log('Nút không có màu xanh.');
                button_straight_line.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
            }}
        
        }}
        
        function toggle_edit_point() {{
            const button_edit_point = document.getElementById('edit_point');
            const backgroundColor = window.getComputedStyle(button_edit_point).backgroundColor;

            const button_add_point = document.getElementById('add_point');
            const button_straight_line = document.getElementById('them_duong');
            const button_btn_curve = document.getElementById('chinh_sua_duong');

            // Kiểm tra nếu màu nền là màu xanh (mã RGB: rgb(76, 175, 80))
            if (backgroundColor === 'rgb(76, 175, 80)') {{
                button_edit_point.style.backgroundColor = '#1E90FF';  // Đổi màu sang xanh dương
                button_add_point.style.backgroundColor = '#4CAF50';
                button_btn_curve.style.backgroundColor = '#4CAF50';
                button_straight_line.style.backgroundColor = '#4CAF50';
                console.log('Nút có màu xanh.');
            }} else {{
                console.log('Nút không có màu xanh.');
                button_edit_point.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
            }}
        }}
        
        function toggle_add_point() {{
            const button_add_point = document.getElementById('add_point');
            const backgroundColor = window.getComputedStyle(button_add_point).backgroundColor;

            const button_edit_point = document.getElementById('edit_point');
            const button_straight_line = document.getElementById('them_duong');
            const button_btn_curve = document.getElementById('chinh_sua_duong');

            // Kiểm tra nếu màu nền là màu xanh (mã RGB: rgb(76, 175, 80))
            if (backgroundColor === 'rgb(76, 175, 80)') {{
                button_add_point.style.backgroundColor = '#1E90FF';  // Đổi màu sang xanh dương
                button_edit_point.style.backgroundColor = '#4CAF50';
                button_straight_line.style.backgroundColor = '#4CAF50';
                button_btn_curve.style.backgroundColor = '#4CAF50';
                console.log('Nút "Thêm điểm" được kích hoạt.');
            }} else {{
                console.log('Nút "Thêm điểm" không được kích hoạt.');
                button_add_point.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
            }}
        }}

        function updateLoopType() {{
        const loopType = document.getElementById('loop_type').value;
        fetch('/update_loop_type', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{ loai_lap: loopType }})
        }})
        .then(response => response.json())
        .then(result => {{
            console.log('Cập nhật loại lặp:', result);
        }})
        .catch(error => {{
            console.error('Lỗi khi cập nhật loại lặp:', error);
        }});
        }}

        function updateLoopCount() {{
            const loopCount = document.getElementById('loop_count').value;
            fetch('/update_loop_count', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ so_lan_lap: loopCount }})
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Cập nhật số lần lặp:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi cập nhật số lần lặp:', error);
            }});
        }}

        function handleUploadClick() {{
            const uploadButton = document.getElementById('upload_button');
            const combobox = document.getElementById('list_duong_di_combobox');
            const selectedValue = combobox.value;

            if ("{path_project}" === "") {{
                alert('Vui lòng chọn dự án đã được chọn trước khi bắt đầu!');
                return; // Dừng thực hiện nếu tên bản đồ rỗng hoặc chưa chọn dự án
            }} 
            else {{
                fetch('/upload_duong_di', {{
                method: 'POST',
                headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ name_duong_di: selectedValue }})
                }})
                .then(response => response.json())
                .then(result => {{
                    console.log('Cập nhật số lần lặp:', result);
                    if (result.status === 'success') {{
                        // Nhập giá trị của data_duong_di vào khung text
                        document.getElementById('duong_di_input').value = result.data_duong_di;
                        alert('Đã tải lên đường di chuyển cho AGV!');
                    }} else {{
                        alert(`Lỗi: ${{result.message}}`);
                    }}
                    
                }})
                .catch(error => {{
                    console.error('Lỗi khi cập nhật số lần lặp:', error);
                }});
            }}
        }}



////////////////////////////////////////////////////////// cửa sổ tạm thời ///////////////////////////////////////////////////////////
        function showEditPointModal(id, point_data) {{
            // Tạo nội dung HTML cho cửa sổ tạm thời
            const modalContent = `
                <div id="edit-modal" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 1px solid #ccc; border-radius: 10px; z-index: 1000;">
                <h3>Chỉnh sửa điểm ID: "${{id}}"</h3>
                <div>
                    <label for="point_name">Tên điểm:</label>
                    <input type="text" id="point_name" value="${{point_data.point_name}}" style="width: 100%; margin-bottom: 10px;">
                </div>
                <div>
                    <label for="x_edit">Tọa độ X:</label>
                    <input type="text" id="x_edit" value="${{point_data.point_coord[0]}}" style="width: 100%; margin-bottom: 10px;">
                </div>
                <div>
                    <label for="y_edit">Tọa độ Y:</label>
                    <input type="text" id="y_edit" value="${{point_data.point_coord[1]}}" style="width: 100%; margin-bottom: 10px;">
                </div>
                <div>
                    <label for="direction">Hướng:</label>
                    <select id="direction" style="width: 100%; margin-bottom: 10px;">
                        <option value="có hướng" ${{point_data.direction === "có hướng" ? "selected" : ""}}>Có hướng</option>
                        <option value="không hướng" ${{point_data.direction === "không hướng" || point_data.direction === "" ? "selected" : ""}}>Không hướng</option>
                    </select>
                </div>
                <div>
                    <label for="alpha_ang">Góc Alpha:</label>
                    <input type="text" id="alpha_ang" value="${{point_data.alpha}}" style="width: 100%; margin-bottom: 10px;">
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <button onclick="deletePoint('${{id}}')" style="background: red; color: white; padding: 10px; border: none; border-radius: 5px;">Xóa điểm</button>
                    <button onclick="addPoint('${{id}}')" style="background: blue; color: white; padding: 10px; border: none; border-radius: 5px;">Add</button>
                    <button onclick="savePoint('${{id}}')" style="background: green; color: white; padding: 10px; border: none; border-radius: 5px;">Lưu</button>
                </div>
            </div>
            `;
            // Hiển thị cửa sổ tạm thời
            const modal = document.createElement('div');
            modal.innerHTML = modalContent;
            document.body.appendChild(modal);
        }}

        function deletePoint(id) {{
            fetch('/delete_point', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ id: id }})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    document.getElementById('edit-modal').remove();
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi xóa điểm:', error);
            }});
        }}

        function savePoint(id) {{
            // Lấy giá trị từ các trường nhập liệu
            const name = document.getElementById('point_name').value;
            const x = parseFloat(document.getElementById('x_edit').value);
            const y = parseFloat(document.getElementById('y_edit').value);
            const direction = document.getElementById('direction').value;
            const alpha = parseFloat(document.getElementById('alpha_ang').value);

            // Gửi dữ liệu về server
            fetch('/save_point', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{id: id, point_name:name, x:x, y:y, direction:direction, alpha:alpha}})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    document.getElementById('edit-modal').remove(); // Đóng modal sau khi lưu thành công
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi lưu điểm:', error);
            }});
        }}

        function addPoint(id) {{
            // Lấy giá trị từ các trường nhập liệu
            const name = document.getElementById('point_name').value;
            const x = parseFloat(document.getElementById('x_edit').value);
            const y = parseFloat(document.getElementById('y_edit').value);
            const direction = document.getElementById('direction').value;
            const alpha = parseFloat(document.getElementById('alpha_ang').value);

            // Gửi dữ liệu về server
            fetch('/adds_point', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{id: id, point_name:name, x:x, y:y, direction:direction, alpha:alpha}})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    document.getElementById('edit-modal').remove(); // Đóng modal sau khi lưu thành công
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi lưu điểm:', error);
            }});
        }}

        function showStraightLineModal() {{
            const modalContent = `
                <div id="straight-line-modal" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 1px solid #ccc; border-radius: 10px; z-index: 1000; width: 300px;">
                    <h3>Thông tin đường</h3>
                    <div>
                        <label for="line_name">Tên đường:</label>
                        <input type="text" id="line_name" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập tên đường">
                    </div>
                    <div>
                        <label for="point_1">Điểm 1:</label>
                        <input type="text" id="point_1" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập tên điểm 1">
                    </div>
                    <div>
                        <label for="point_2">Điểm 2:</label>
                        <input type="text" id="point_2" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập tên điểm 2">
                    </div>
                    <div>
                        <label for="line_type">Loại đường:</label>
                        <select id="line_type" style="width: 100%; margin-bottom: 10px;">
                            <option value="đường thẳng">Đường thẳng</option>
                            <option value="đường cong">Đường cong</option>
                        </select>
                    </div>
                    <div>
                        <label for="c1">C1:</label>
                        <input type="text" id="c1" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập giá trị C1">
                    </div>
                    <div>
                        <label for="c2">C2:</label>
                        <input type="text" id="c2" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập giá trị C2">
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <button onclick="closeStraightLineModal()" style="background: red; color: white; padding: 10px; border: none; border-radius: 5px;">Close</button>
                        <button onclick="saveStraightLine()" style="background: green; color: white; padding: 10px; border: none; border-radius: 5px;">Lưu</button>
                    </div>
                </div>
            `;
            const modal_them_duong = document.createElement('div');
            modal_them_duong.innerHTML = modalContent;
            document.body.appendChild(modal_them_duong);
        }}

         function closeStraightLineModal() {{
            // Đóng cửa sổ tạm thời mà không lưu dữ liệu
            const modal = document.getElementById('straight-line-modal');
            if (modal) {{
                modal.remove();
                // Đổi màu nút "Thêm đường" sang xanh lá
                const buttonStraightLine = document.getElementById('them_duong');
                buttonStraightLine.style.backgroundColor = '#4CAF50'; // Màu xanh lá
            }}
        }}
        function saveStraightLine() {{
            // Lấy giá trị từ các entry và combobox
            const lineName = document.getElementById('line_name').value;
            const point1 = document.getElementById('point_1').value;
            const point2 = document.getElementById('point_2').value;
            const lineType = document.getElementById('line_type').value;
            const c1 = document.getElementById('c1').value;
            const c2 = document.getElementById('c2').value;

            // Gửi dữ liệu về server để cập nhật danh_sach_duong
            fetch('/add_straight_line', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    line_name: lineName,
                    point_1: point1,
                    point_2: point2,
                    line_type: lineType,
                    c1: c1,
                    c2: c2
                }})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    // Xóa cửa sổ tạm thời sau khi lưu thành công
                    document.getElementById('straight-line-modal').remove();

                    // Đổi màu nút "Thêm đường" sang xanh lá
                    const buttonStraightLine = document.getElementById('them_duong');
                    buttonStraightLine.style.backgroundColor = '#4CAF50'; // Màu xanh lá
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi lưu đường thẳng:', error);
            }});
        }}
    
        function showEditLineModal() {{
            const modalContent = `
            <div id="edit-line-modal" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 1px solid #ccc; border-radius: 10px; z-index: 1000; width: 400px;">
                <h3>Chỉnh sửa đường</h3>
                <div>
                    <label for="edit_line_name">Tên đường:</label>
                    <input type="text" id="edit_line_name" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập tên đường">
                </div>
                <div>
                    <label for="edit_point_1">Điểm 1:</label>
                    <input type="text" id="edit_point_1" style="width: 100%; margin-bottom: 10px;" placeholder="Tên điểm 1">
                </div>
                <div>
                    <label for="edit_point_2">Điểm 2:</label>
                    <input type="text" id="edit_point_2" style="width: 100%; margin-bottom: 10px;" placeholder="Tên điểm 2">
                </div>
                <div>
                    <label for="edit_line_type">Loại đường:</label>
                    <select id="edit_line_type" style="width: 100%; margin-bottom: 10px;">
                        <option value="đường thẳng">Đường thẳng</option>
                        <option value="đường cong">Đường cong</option>
                    </select>
                </div>
                <div>
                    <label for="edit_c1">C1:</label>
                    <input type="text" id="edit_c1" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập giá trị C1">
                </div>
                <div>
                    <label for="edit_c2">C2:</label>
                    <input type="text" id="edit_c2" style="width: 100%; margin-bottom: 10px;" placeholder="Nhập giá trị C2">
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <button onclick="closeEditLineModal()" style="background: red; color: white; padding: 10px; border: none; border-radius: 5px;">Close</button>
                    <button onclick="deleteLine()" style="background: orange; color: white; padding: 10px; border: none; border-radius: 5px;">Delete</button>
                    <button onclick="saveLine()" style="background: green; color: white; padding: 10px; border: none; border-radius: 5px;">Save</button>
                </div>
            </div>
        `;
        const modal = document.createElement('div');
        modal.innerHTML = modalContent;
        document.body.appendChild(modal);
    }}
    
    function closeEditLineModal() {{
        const modal = document.getElementById('edit-line-modal');
        if (modal) {{
            modal.remove();
            const button_btn_curve = document.getElementById('chinh_sua_duong');
            const backgroundColor = window.getComputedStyle(button_btn_curve).backgroundColor;
            button_btn_curve.style.backgroundColor = '#4CAF50';  // Đổi màu sang xanh
        }}
    }}

    function populateLineDetails() {{
        const lineName = document.getElementById('edit_line_name').value;

        // Kiểm tra nếu tên đường không rỗng và tồn tại trong danh_sach_duong
        if (lineName && danh_sach_duong) {{
            for (const key in danh_sach_duong) {{
                const line = danh_sach_duong[key];
                if (line.ten_duong === lineName) {{
                    // Điền thông tin vào các trường
                    document.getElementById('edit_point_1').value = danh_sach_diem[line.diem_1]?.point_name || '';
                    document.getElementById('edit_point_2').value = danh_sach_diem[line.diem_2]?.point_name || '';
                    document.getElementById('edit_line_type').value = line.loai_duong;
                    document.getElementById('edit_c1').value = line.C1 || '';
                    document.getElementById('edit_c2').value = line.C2 || '';
                    break;
                }}
            }}
        }}
    }}

    function deleteLine() {{
        const lineName = document.getElementById('edit_line_name').value;

        if (lineName) {{
            fetch('/delete_line', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ ten_duong: lineName }})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    closeEditLineModal();
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi xóa đường:', error);
            }});
        }} else {{
            alert('Vui lòng nhập tên đường để xóa.');
        }}
    }}

    function saveLine() {{
        const lineName = document.getElementById('edit_line_name').value;
        const point1 = document.getElementById('edit_point_1').value;
        const point2 = document.getElementById('edit_point_2').value;
        const lineType = document.getElementById('edit_line_type').value;
        const c1 = document.getElementById('edit_c1').value;
        const c2 = document.getElementById('edit_c2').value;

        if (lineName) {{
            fetch('/save_line', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    ten_duong: lineName,
                    diem_1: point1,
                    diem_2: point2,
                    loai_duong: lineType,
                    C1: c1,
                    C2: c2
                }})
            }})
            .then(response => response.json())
            .then(result => {{
                alert(result.message);
                if (result.status === 'success') {{
                    closeEditLineModal();
                }}
            }})
            .catch(error => {{
                console.error('Lỗi khi lưu đường:', error);
            }});
        }} else {{
            alert('Vui lòng nhập tên đường để lưu.');
        }}
    }}


////////////////////////////////////////////////////////// su kien chuot ///////////////////////////////////////////////////////////
        let x_crop_min = {x_crop_min};
        let y_crop_min = {y_crop_min};
        function getPixelCoordinates(event) {{
            // Danh sách các nút cần kiểm tra
            const buttons = [
                'agv_position_button',
                'add_point',
                'edit_point',
                'them_duong',
                'chinh_sua_duong',
                'edit_button'
            ];

            const button_add_point = document.getElementById('add_point');
            const backgroundColor_add_point = window.getComputedStyle(button_add_point).backgroundColor;

            const button_edit_point = document.getElementById('edit_point');
            const backgroundColor_edit_point = window.getComputedStyle(button_edit_point).backgroundColor;

            let isActive = false;
            // Kiểm tra nếu bất kỳ nút nào đang có màu xanh dương
            for (const buttonId of buttons) {{
                const button = document.getElementById(buttonId);
                const backgroundColor = window.getComputedStyle(button).backgroundColor;

                if (backgroundColor === 'rgb(30, 144, 255)') {{ // Mã màu xanh dương Dodger Blue
                    isActive = true;
                    break;
                }}
            }}
            if (isActive) {{
                const img = event.target;
                const rect = img.getBoundingClientRect();

                // Lấy kích thước ảnh hiển thị trên web
                const w_web = rect.width;
                const h_web = rect.height;

                // Tính tọa độ pixel dựa trên vị trí chuột và vị trí ảnh
                const x = x_crop_min + Math.floor(event.clientX - rect.left) * {w_size} / w_web; // Làm tròn xuống
                const y = y_crop_min + Math.floor(event.clientY - rect.top) * {h_size} / h_web; // Làm tròn xuống

                // Chỉ xử lý khi nút "Chỉnh sửa điểm" đang có màu xanh dương
                if (backgroundColor_edit_point === 'rgb(30, 144, 255)') {{ // Mã màu xanh dương
                    // Gửi tọa độ về server để kiểm tra và tìm điểm gần nhất
                    fetch('/edit_points', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{ x: x, y: y}})
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        console.log('Phản hồi từ server:', result);
                        if (result.status === 'success') {{
                            const data = result.data;
                            const id = result.id;
                            showEditPointModal(id, data);
                        }} else {{
                            alert(result.message);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Lỗi khi gửi tọa độ:', error);
                    }}); 
                }}                              
                // Chỉ xử lý khi nút "Thêm điểm" đang có màu xanh dương
                if (backgroundColor_add_point === 'rgb(30, 144, 255)') {{
                    // Gửi tọa độ về server để lưu vào danh_sach_diem
                    fetch('/add_points', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{ x: x, y: y}})
                    }})
                }}
                
                // Hiển thị tọa độ vào các entry
                document.getElementById('x_coord').value = parseInt(x, 10); // Chuyển đổi x thành số nguyên
                document.getElementById('y_coord').value = parseInt(y, 10); // Chuyển đổi x thành số nguyên
                // Nếu entry góc alpha rỗng, đặt giá trị mặc định là 0
                const alphaEntry = document.getElementById('alpha_angle');
                if (!alphaEntry.value) {{
                    alphaEntry.value = 0;
                }}
                const button_agv_position = document.getElementById('agv_position_button');
                const backgroundColor_agv_position = window.getComputedStyle(button_agv_position).backgroundColor;
                // Xác định giá trị update_vi_tri_agv dựa trên màu sắc của nút "Vị trí AGV"
                let update_vi_tri_agv = 0;
                if (backgroundColor_agv_position === 'rgb(30, 144, 255)'){{
                    update_vi_tri_agv = 1;
                }}
                else{{
                    update_vi_tri_agv = 0;
                }}
                const alphaAngle = document.getElementById('alpha_angle').value;
                // Gửi tọa độ pixel về server qua AJAX
                fetch('/get_pixel_coordinates', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ x: x, y: y, alpha: alphaAngle, update_vi_tri_agv: update_vi_tri_agv}})
                }})
                .then(response => response.json())
                .then(result => {{
                    console.log('Phản hồi từ server:', result);
                }})
                .catch(error => {{
                    console.error('Lỗi khi gửi tọa độ pixel:', error);
                }});
            }} else {{
                console.log('Không có nút nào đang hoạt động (màu xanh dương).');
            }}
        }}

        

        let isDragging = false; // Biến để kiểm tra trạng thái kéo thả
        let startX = 0; // Tọa độ X khi bắt đầu kéo
        let startY = 0; // Tọa độ Y khi bắt đầu kéo
        let zoomLevel = 1; // Mức độ zoom (1 = 100%)

        const imgElement = document.querySelector('.image-container img'); // Lấy phần tử ảnh

        // Ngăn hành vi kéo thả mặc định của trình duyệt
        imgElement.addEventListener('dragstart', (event) => {{
            event.preventDefault(); // Ngăn trình duyệt kéo ảnh
        }});
        // Sự kiện khi nhấn chuột trái
        imgElement.addEventListener('mousedown', (event) => {{
            if (event.button === 0) {{ // Chỉ xử lý chuột trái
                isDragging = true;
                startX = event.clientX;
                startY = event.clientY;
            }}
        }});

        // Sự kiện khi di chuyển chuột
        imgElement.addEventListener('mousemove', (event) => {{
            if (isDragging) {{
                const deltaX = - event.clientX + startX;
                const deltaY = - event.clientY + startY;

                // Gửi giá trị mới về server
                fetch('/update_crop', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ deltaX: deltaX, deltaY: deltaY }})
                }})
                .then(response => response.json())
                .then(result => {{
                    console.log('Cập nhật crop thành công:', result);
                    x_crop_min = result.x_crop_min; // Cập nhật giá trị x_crop_min từ server
                    y_crop_min = result.y_crop_min; // Cập nhật giá trị y_crop_min từ server
                }})
                .catch(error => {{
                    console.error('Lỗi khi cập nhật crop:', error);
                }});

                // Cập nhật tọa độ bắt đầu
                startX = event.clientX;
                startY = event.clientY;
            }}
        }});

        // Sự kiện khi thả chuột
        imgElement.addEventListener('mouseup', () => {{
            isDragging = false;
        }});
        // Sự kiện khi chuột rời khỏi ảnh
        imgElement.addEventListener('mouseleave', () => {{
            isDragging = false; // Ngừng kéo thả nếu chuột rời khỏi ảnh
        }});

        // Sự kiện khi cuộn chuột
        imgElement.addEventListener('wheel', (event) => {{
            event.preventDefault(); // Ngăn cuộn mặc định của trình duyệt

            // Cập nhật mức độ zoom
            if (event.deltaY < 0) {{
                zoomLevel *= 1.1; // Phóng to
            }} else {{
                zoomLevel /= 1.1; // Thu nhỏ
            }}

            // Gửi giá trị zoom mới về server
            fetch('/update_zoom', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{ zoom: zoomLevel }})
            }})
            .then(response => response.json())
            .then(result => {{
                console.log('Cập nhật zoom thành công:', result);
            }})
            .catch(error => {{
                console.error('Lỗi khi cập nhật zoom:', error);
            }});
        }});
        window.onload = function() {{
            const savedProjectName = localStorage.getItem('selectedProjectName');
            const projectNameInput = document.getElementById('project_name');
            

            if (savedProjectName) {{
                const projectNameInput = document.getElementById('project_name');
                projectNameInput.value = savedProjectName;
            }}
            localStorage.removeItem('selectedProjectName');


            fetch('/get_data')
            .then(response => response.json())
            .then(data => {{
                // Hiển thị lại dữ liệu trên web
                document.getElementById('duong_di_input').value = data.data_duong_di || '';
                document.getElementById('project_name').value = data.project_name || '';
                // chon ban do
                document.getElementById('map_name').value = data.chon_ban_do.name_map || '';
                 // Cập nhật giá trị combobox
                document.getElementById('tien_max').value = data.data_cai_dat.tien_max || '';
                document.getElementById('re_max').value = data.data_cai_dat.re_max || '';
                document.getElementById('grid_size').value = data.data_cai_dat.grid_size || '';
                document.getElementById('agv_size').value = data.data_cai_dat.agv_size || '';

                document.getElementById('new_map_name').value = data.ban_do_moi.name_map || '';
                // Cập nhật các phần khác nếu cần
                console.log('Dữ liệu đã tải lại:', data);
            }})
            .catch(error => {{
                console.error('Lỗi khi tải lại dữ liệu:', error);
            }});
        }};
    </script>
    <script>
        // Hàm gửi yêu cầu keep-alive đến server
        function keepAlive() {{
            fetch('/keep_alive', {{ method: 'GET' }})
                .then(response => {{
                    if (!response.ok) {{
                        console.error('Keep-alive failed:', response.statusText);
                    }}
                }})
                .catch(error => console.error('Error in keep-alive:', error));
        }}

        // Gửi yêu cầu keep-alive mỗi 30 giây
        setInterval(keepAlive, 10000); // 30 giây
    </script>
    </body>
    </html>
    '''
# Route để phục vụ ảnh
############################################################## IMAGES ###########################################################################
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
def draw_text(image, text, x, y, color=(255, 255, 255), font_scale=0.5, thickness=1, offset=(0, 0)):
    """
    Vẽ văn bản (tên điểm) lên ảnh tại tọa độ (x, y) với một khoảng offset.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = x + offset[0]
    text_y = y + offset[1]
    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)
def draw_arrow(image, x, y, angle, color=(0, 0, 255), length=25, thickness=2):
    """
    Vẽ một mũi tên nhỏ tại tọa độ (x, y) với góc `angle` (đơn vị: độ).
    """
    # Chuyển đổi góc từ độ sang radian
    angle_rad = math.radians(angle)

    # Tính toán điểm kết thúc của mũi tên
    end_x = int(x + length * math.cos(angle_rad))
    end_y = int(y - length * math.sin(angle_rad))  # Trừ vì trục y của ảnh ngược

    # Vẽ mũi tên
    cv2.arrowedLine(image, (x, y), (end_x, end_y), color, thickness, tipLength=0.3)

def draw_point_on_image(image, x, y, color, radius=25):
    cv2.circle(image, (x, y), radius, color, -1)  # -1 để tô đầy hình tròn
    return image

def draw_all_points_on_image(image, danh_sach_diem0, color=(0, 255, 0), radius=7, line_color=(255, 0, 0), line_thickness=2, text_color = (0,255,0)):
    # print("------------cvvvv-------------", len(list_point_star))
    danh_sach_diem = danh_sach_diem0.copy()
    danh_sach_duong0 = danh_sach_duong.copy()
    for i in range(len(list_point_star)):
        if i == 0:
            cv2.line(image, (x_goc, y_goc), (list_point_star[i][0], list_point_star[i][1]), (2550, 0, 255), 2)  # Vẽ đường thẳng giữa các điểm
        else:
            cv2.line(image, (list_point_star[i-1][0], list_point_star[i-1][1]), (list_point_star[i][0], list_point_star[i][1]), (255, 0, 255), 2)
    cv2.rectangle(image, (x_crop_min + 10, y_crop_min + 10), (x_crop_min + 60, y_crop_min + 60), (0, 255, 0), -1)  # Tô đen toàn bộ ảnh
    cv2.circle(image, (x_goc, y_goc), 5, (255, 0, 0), -1)  # Vẽ điểm gốc
    draw_arrow(image, x_goc, y_goc, angle_goc, color = (255, 0, 0))  # Vẽ mũi tên với góc alpha
    if len(point_end) >= 2:
        cv2.line(image, (x_goc, y_goc), (point_end[0], point_end[1]), (0, 0, 255), 2)  
        cv2.circle(image, point_end, 5, (255, 0, 255), -1) 
    # Vẽ các đường thẳng nếu danh_sach_duong không rỗng
    for key, value in danh_sach_duong0.items():
        point_1_id = value["diem_1"]
        point_2_id = value["diem_2"]
        line_name = value["ten_duong"]

        # Lấy tọa độ của điểm 1 và điểm 2
        if point_1_id in danh_sach_diem and point_2_id in danh_sach_diem:
            x1, y1 = danh_sach_diem[point_1_id]["point_coord"]
            x2, y2 = danh_sach_diem[point_2_id]["point_coord"]
            x1, y1 = int(float(x1)), int(float(y1))
            x2, y2 = int(float(x2)), int(float(y2))

            # Vẽ đường thẳng nối giữa điểm 1 và điểm 2
            cv2.line(image, (x1, y1), (x2, y2), line_color, line_thickness)

            # Tính trung điểm của đường thẳng
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2

            # Vẽ tên đường tại trung điểm
            draw_text(image, line_name, mid_x, mid_y, color=text_color, font_scale=0.7, thickness=2)
    for key, value in danh_sach_diem.items():
        x, y = danh_sach_diem[key]["point_coord"]  # Lấy tọa độ của điểm
        x = int(float(x))
        y = int(float(y))

        # Kiểm tra nếu điểm có hướng
        if danh_sach_diem[key]["direction"] == "có hướng":
            alpha = float(danh_sach_diem[key]["alpha"])
            draw_arrow(image, x, y, alpha)  # Vẽ mũi tên với góc alpha

            # Tính toán vị trí tên điểm ở phía đối diện mũi tên
            arrow_length = 40  # Độ dài mũi tên
            offset_x = int(arrow_length * math.cos(math.radians(alpha)))
            offset_y = int(-arrow_length * math.sin(math.radians(alpha)))  # Trừ vì trục y ngược
            text_offset = (-offset_x, -offset_y)  # Đặt tên ở phía đối diện mũi tên
        else:
            # Nếu không có mũi tên, đặt tên ngay cạnh điểm
            text_offset = (10, -10)
        # Vẽ điểm
        image = draw_point_on_image(image, x, y, color, radius)
        # Vẽ tên điểm
        name = danh_sach_diem[key]["point_name"]
        draw_text(image, name, x, y, offset=text_offset, color=text_color, font_scale=0.7, thickness=2)
    return image
def generate_frames():
    global w_goc, h_goc, x_crop_min, y_crop_min
    current_frame = None  # Ảnh đang xử lý
    next_frame = None  # Ảnh ngay sau ảnh đang xử lý
    while True:
        # print("fff")
        h1 = y_goc - h_size // 2
        h2 = y_goc + h_size // 2
        w1 = x_goc - w_size // 2
        w2 = x_goc + w_size // 2
        if h1 < 0:
            h1 = 0
            h2 = h_size
        if h2 > y_size:
            h1 = y_size - h_size
            h2 = y_size
        if w1 < 0:
            w1 = 0
            w2 = w_size
        if w2 > x_size:
            w1 = x_size - w_size
            w2 = x_size
        if img1 is not None:
            processed_frame = draw_all_points_on_image(img1.copy(), danh_sach_diem)
            # print(img1.shape, y_crop_min,y_crop_min+h_size, x_crop_min,x_crop_min+w_size)
            processed_frame = processed_frame[y_crop_min:y_crop_min+h_size, x_crop_min:x_crop_min+w_size]
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            # Giải phóng bộ nhớ
            del buffer
            del frame_bytes
        else:
            print("Frame không có giá trị. Đợi cập nhật...")
            time.sleep(0.1)
        # Giới hạn tốc độ khung hình (30 FPS)
        time.sleep(1 / 30)

############################################################## CAI DAT ###########################################################################
@app.route('/update_settings', methods=['POST'])
def update_settings():
    global data_cai_dat
    # Lấy dữ liệu JSON từ client
    data = request.get_json()

    # Lấy các giá trị từ dữ liệu
    data_cai_dat["tien_max"] = data.get('tien_max')
    data_cai_dat["re_max"] = data.get('re_max')
    data_cai_dat["grid_size"] = data.get('grid_size')
    data_cai_dat["agv_size"] = data.get('agv_size')


    # In ra terminal để kiểm tra
    print("Vận tốc tiến max:" + str(data_cai_dat["tien_max"]))
    print("Vận tốc rẽ max:" + str(data_cai_dat["re_max"]))
    print("Grid size:" + str(data_cai_dat["grid_size"]))
    print("AGV size:" + str(data_cai_dat["agv_size"]))

    # Trả về phản hồi JSON
    return jsonify({
        'status': 'success',
        'message': 'Cập nhật thành công',
        'data': data
    })

@app.route('/upload_project', methods=['POST'])
def upload_project():
    global path_project, project_name, path_map, list_name_map, data_cai_dat, path_duong_di
    data = request.get_json()
    project_name = data.get('project_name')
    path_project = remove.tao_folder(path_project_all + "/" + project_name)
    data_cai_dat["path_project"] =  path_project

    path_map = remove.tao_folder(path_project_all + "/" + project_name + "/map")
    path_duong_di = remove.tao_folder(path_project_all + "/" + project_name + "/duong_di")

    list_name_map = [os.path.splitext(file)[0] for file in os.listdir(path_map) if file.endswith('.npy')]
    return jsonify({
        'status': 'success',
        'message': f'Project "{project_name}" đã được upload. Path upload: {path_project}',
        'list_name_map': list_name_map  # Trả về danh sách file .npy
    })

@app.route('/delete_project', methods=['POST'])
def delete_project():
    global path_project, project_name, path_map
    data = request.get_json()
    project_name = data.get('project_name')
    project_path = os.path.join(path_project, project_name)
    data_cai_dat["path_project"] = ""

    if os.path.exists(project_path) and os.path.isdir(project_path):
        try:
            shutil.rmtree(project_path)  # Xóa folder
            project_name = ""
            path_project = ""
            path_map = ""
            return jsonify({
                'status': 'success',
                'message': f'Project "{project_name}" đã được xóa.'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Lỗi khi xóa project "{project_name}": {str(e)}'
            })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Project "{project_name}" không tồn tại.'
        })
    
############################################################# VẼ BẢN ĐỒ ############################################################################

                                    ######################### BẢN ĐỒ MỚI #################### 

@app.route('/map_action', methods=['POST'])
def map_action():
    global path_map, data_ban_do_moi, data_chon_ban_do
    data = request.get_json()

    action = data[0]  # "save" hoặc "reset"
    map_name = data[1]  # Tên bản đồ
    path_new_map = path_map + "/" + map_name + ".npy"
    print("path_new_map", path_new_map, data)

    if not map_name:
        return jsonify({
                    'status': 'error',
                    'message': 'Tên bản đồ không được để trống.'
                })
    else:
        data_ban_do_moi['name_map'] = map_name
        data_ban_do_moi['path_new_map'] = path_new_map
        data_chon_ban_do = {"update": 0, "map_file_path": "", "add_all_point": 0,"name_map": ""}
        if action == "save":
            if not os.path.exists(path_map):
                return jsonify({
                    'status': 'error',
                    'message': 'Thư mục path_map không tồn tại.'
                })

            try:
                # Lưu mảng dưới dạng file .npy
                np.save(path_new_map, map_all)
                data_ban_do_moi['save'] = 1
                print("data_ban_do_moi", data_ban_do_moi)
                return jsonify({
                    'status': 'success',
                    'message': f'Bản đồ "{map_name}" đã được lưu tại {path_new_map}.'
                })
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Lỗi khi lưu bản đồ: {str(e)}'
                })

        elif action == "reset":
            data_ban_do_moi['reset'] = 1
            print("data_ban_do_moi", data_ban_do_moi)
            return jsonify({
                'status': 'success',
                'message': 'Đã reset bản đồ mới.',
            })
        else:
            data_ban_do_moi['start_stop'] = action
            print("data_ban_do_moi", data_ban_do_moi)
            return jsonify({
                'status': 'success',
                'message': 'Đã bắt đầu hoặc dừng bản đồ mới.',
            })

                                    ######################### CHỌN BẢN ĐỒ #################### 

@app.route('/update_map_action', methods=['POST'])
def update_map_action():
    global path_map_chon_ban_do, data_chon_ban_do,data_ban_do_moi
    data = request.get_json()
    selectMode = data.get('selectMode')
    selectedMap = data.get('selectedMap')

    if selectedMap:
        # Đường dẫn đầy đủ đến file bản đồ
        map_file_path = os.path.join(path_map, f"{selectedMap}.npy")

        if os.path.exists(map_file_path):  # Kiểm tra nếu file tồn tại
            path_map_chon_ban_do = map_file_path
            print("path_map_chon_ban_do", path_map_chon_ban_do)

            # Đường dẫn đầy đủ đến file bản đồ
            if selectMode == "update":
                data_chon_ban_do["add_all_point"] = 1
            else:
                data_chon_ban_do["add_all_point"] = 0

            try:
                # Cập nhật frame bằng cách load dữ liệu từ file .npy
                data_chon_ban_do["map_file_path"] = path_map_chon_ban_do
                data_chon_ban_do["update"] = 1
                data_chon_ban_do["name_map"] = selectedMap
                data_ban_do_moi = {"reset": 0, "start_stop": "stop", "path_new_map": "", "save": 0, "name_map": ""}
                print(data_chon_ban_do)
                print(f"Đã cập nhật: path_map_chon_ban_do = {path_map_chon_ban_do}, frame được load thành công.")
                return jsonify({
                    'status': 'success',
                    'message': f'Bản đồ "{selectedMap}" đã được cập nhật.',
                    'path_map_chon_ban_do': path_map_chon_ban_do,
                })
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Lỗi khi load bản đồ: {str(e)}'
                })
        else:
            return jsonify({
                'status': 'error',
                'message': f'File bản đồ "{selectedMap}.npy" không tồn tại.'
            })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Tên bản đồ không hợp lệ hoặc không được chọn.'
        })

############################################################# ĐIỀU CHỈNH VỊ TRÍ AGV ############################################################################

@app.route('/chon_ban_do_update', methods=['POST'])
def chon_ban_do_update():
    global data_vi_tri_agv
    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    x = int(float(data.get('x')))
    y = int(float(data.get('y')))
    alpha = data.get('alpha')

    if x != "" and y != "" and alpha != "":
        data_vi_tri_agv["x"] = int(float(x))
        data_vi_tri_agv["y"] = int(float(y))
        data_vi_tri_agv["angle"] = int(float(alpha))
        data_vi_tri_agv["update"] = 1

    # In ra terminal để kiểm tra
    print("data_vi_tri_agv", data_vi_tri_agv)

    # Trả về phản hồi JSON
    return jsonify({
        'status': 'success',
        'message': 'Cập nhật vị trí AGV thành công',
        'data': {
            'x': x,
            'y': y,
            'alpha': alpha
        }
    })

@app.route('/toggle_run_stop', methods=['POST'])
def toggle_run_stop():
    global data_text_box, run_stop

    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    data_text_box = data.get('data_text_box')
    run_stop = data.get('run_stop')

    # In ra terminal để kiểm tra
    print(f"data_text_box: {data_text_box}")
    print(f"run_stop: {run_stop}")

    # Trả về phản hồi JSON
    return jsonify({
        'status': 'success',
        'message': f'Trạng thái đã được cập nhật thành "{run_stop}".'
    })







############################################################# ĐIỀU KHIEN AGV ############################################################################
@app.route('/get_pixel_coordinates', methods=['POST'])
def update_agv_position():
    global data_vi_tri_agv
    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    alpha = data.get('alpha')
    # print("alpha", alpha)+
    update_vi_tri_agv = data.get('update_vi_tri_agv')

    if x != "" and y != "" and alpha != "" and alpha != "-":
        data_vi_tri_agv["x"] = int(float(x))
        data_vi_tri_agv["y"] = int(float(y))
        data_vi_tri_agv["angle"] = int(float(alpha))
        data_vi_tri_agv["update_vi_tri_agv"] = int(float(update_vi_tri_agv))
        

    # In ra terminal để kiểm tra
    # print("data_vi_tri_agv", data_vi_tri_agv)

    # Trả về phản hồi JSON
    return jsonify({
        'status': 'success',
        'message': 'Cập nhật vị trí AGV thành công',
        'data': {
            'x': x,
            'y': y,
            'alpha': alpha
        }
    })

@app.route('/add_points', methods=['POST'])
def add_points():
    global stt_id, danh_sach_diem, w_goc, h_goc

    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    x = int(float(data.get('x')))
    y = int(float(data.get('y')))

    # Lưu tọa độ vào danh_sach_diem
    if str(str(stt_id)) not in danh_sach_diem:
        danh_sach_diem[str(stt_id)] = {"point_name":"P" + str(stt_id),"point_coord":[x, y], "direction":"", "alpha":""}
        print(danh_sach_diem)
        # Tăng stt_id
        stt_id += 1
    # Trả về phản hồi JSON
    return jsonify({
        'status': 'success',
        'message': 'Đã thêm 1 điểm mới',
        'id': stt_id,
        'data': danh_sach_diem
    })


@app.route('/edit_points', methods=['POST'])
def edit_points():
    global danh_sach_diem

    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    x = int(float(data.get('x')))
    y = int(float(data.get('y')))

    min_distance = float('inf')

    id = None
    # Tìm điểm trong danh_sach_diem có khoảng cách nhỏ nhất đến (x, y)
    for key, value in danh_sach_diem.items():
        point_x, point_y = danh_sach_diem[key]["point_coord"]
        point_x = int(float(point_x))
        point_y = int(float(point_y))
        distance = ((point_x - x) ** 2 + (point_y - y) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            id = key

    if id is None:
        return jsonify({
            'status': 'error',
            'message': 'Không tìm thấy điểm gần nhất trong danh_sach_diem'
        })

    # Trả về thông tin điểm gần nhất
    point_data = danh_sach_diem[str(id)]
    return jsonify({
        'status': 'success',
        'message': 'Hãy chỉnh sửa điểm',
        'id': id,
        'data': point_data
    })


@app.route('/delete_point', methods=['POST'])
def delete_point():
    global danh_sach_diem

    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    id = data.get('id')

    # Xóa điểm khỏi danh_sach_diem
    if str(id) in danh_sach_diem:
        del danh_sach_diem[str(id)]
        return jsonify({
            'status': 'success',
            'message': f'Điểm với ID = {id} đã được xóa'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Không tìm thấy điểm với ID = {id}'
        })


@app.route('/save_point', methods=['POST'])
def save_point():
    global danh_sach_diem
    # "point_name":name,"point_coord":[x, y], "direction":direction, "alpha":alpha?
    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    id = data.get('id')
    point_name = data.get('point_name')
    x = int(float(data.get('x')))
    y = int(float(data.get('y')))
    direction = data.get('direction')
    alpha = data.get('alpha')

    print(direction, alpha, "---------------")

    # Cập nhật thông tin điểm trong danh_sach_diem
    if id in danh_sach_diem:
        danh_sach_diem[id] = {"point_name":point_name,"point_coord":[x, y], "direction":direction, "alpha":alpha}
        print(danh_sach_diem)
        return jsonify({
            'status': 'success',
            'message': f'Điểm với ID = {id} đã được cập nhật'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Không tìm thấy điểm với ID = {id}'
        })
    
@app.route('/toggle_control_mode', methods=['POST'])
def toggle_control_mode():
    global dk_agv_thu_cong
    # Thay đổi giá trị của data_dk_tay
    dk_agv_thu_cong = 1 if dk_agv_thu_cong == 0 else 0
    print(f"data_dk_tay đã được cập nhật: {dk_agv_thu_cong}")
    return jsonify({
        'status': 'success',
        'message': 'Trạng thái data_dk_tay đã được cập nhật.',
        'data_dk_tay': dk_agv_thu_cong
    })

@app.route('/update_data_dk_tay', methods=['POST'])
def update_data_dk_tay():
    global data_dk_tay
    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    data_dk_tay = data  # Cập nhật giá trị
    print(f"data_data_dk_tay đã được cập nhật: {data_dk_tay}")
    return jsonify({
        'status': 'success',
        'message': 'data_data_dk_tay đã được cập nhật.',
        'data_data_dk_tay': data_dk_tay
    })

@app.route('/adds_point', methods=['POST'])
def adds_point():
    global danh_sach_diem
    # "point_name":name,"point_coord":[x, y], "direction":direction, "alpha":alpha?
    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    id = data.get('id')
    point_name = data.get('point_name')
    x = int(x_goc)
    y = int(y_goc)
    direction = "không hướng"
    alpha = angle_goc

    print(direction, alpha, "---------------")

    # Cập nhật thông tin điểm trong danh_sach_diem
    if id in danh_sach_diem:
        danh_sach_diem[id] = {"point_name":point_name,"point_coord":[x, y], "direction":direction, "alpha":alpha}
        print(danh_sach_diem)
        return jsonify({
            'status': 'success',
            'message': f'Điểm với ID = {id} đã được cập nhật'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f'Không tìm thấy điểm với ID = {id}'
        })
    
@app.route('/add_straight_line', methods=['POST'])
def add_straight_line():
    global danh_sach_duong, stt_id_duong

    # Lấy dữ liệu JSON từ client
    data = request.get_json()
    line_name = data.get('line_name')
    point_1 = data.get('point_1')
    point_2 = data.get('point_2')
    line_type = data.get('line_type')
    c1 = data.get('c1')
    c2 = data.get('c2')

    # Tìm ID của diem_1 và diem_2 trong danh_sach_diem
    id_diem_1 = None
    id_diem_2 = None

    for key, value in danh_sach_diem.items():
        if value["point_name"] == point_1:
            id_diem_1 = key
        if value["point_name"] == point_2:
            id_diem_2 = key

    # Tạo đường thẳng mới
    new_line = {"ten_duong": line_name, "diem_1": id_diem_1, "diem_2": id_diem_2, "loai_duong": line_type, "C1": c1, "C2": c2}

    # Thêm vào danh_sach_duong
    danh_sach_duong[str(stt_id_duong)] = new_line

    print(f"Đã thêm đường thẳng: {new_line}")

    stt_id_duong = stt_id_duong + 1
    # Trả về phản hồi JSON
    return jsonify({
        'status': 'success',
        'message': 'Đường thẳng đã được thêm.',
        'data': new_line
    })

@app.route('/delete_line', methods=['POST'])
def delete_line():
    global danh_sach_duong

    data = request.get_json()
    ten_duong = data.get('ten_duong')

    for key, value in list(danh_sach_duong.items()):
        if value["ten_duong"] == ten_duong:
            del danh_sach_duong[key]
            return jsonify({
                'status': 'success',
                'message': f'Đường "{ten_duong}" đã được xóa.'
            })

    return jsonify({
        'status': 'error',
        'message': f'Không tìm thấy đường với tên "{ten_duong}".'
    })
@app.route('/save_line', methods=['POST'])
def save_line():
    global danh_sach_duong, danh_sach_diem

    data = request.get_json()
    ten_duong = data.get('ten_duong')
    diem_1 = data.get('diem_1')
    diem_2 = data.get('diem_2')
    loai_duong = data.get('loai_duong')
    c1 = data.get('C1')
    c2 = data.get('C2')

    for key, value in danh_sach_duong.items():
        if value["ten_duong"] == ten_duong:
            value["diem_1"] = next((k for k, v in danh_sach_diem.items() if v["point_name"] == diem_1), None)
            value["diem_2"] = next((k for k, v in danh_sach_diem.items() if v["point_name"] == diem_2), None)
            value["loai_duong"] = loai_duong
            value["C1"] = c1
            value["C2"] = c2
            return jsonify({
                'status': 'success',
                'message': f'Đường "{ten_duong}" đã được cập nhật.'
            })

    return jsonify({
        'status': 'error',
        'message': f'Không tìm thấy đường với tên "{ten_duong}".'
    })
@app.route('/update_loop_type', methods=['POST'])
def update_loop_type():
    global loai_lap
    data = request.get_json()
    loai_lap = data.get('loai_lap')
    print(f"Loại lặp được cập nhật: {loai_lap}")
    return jsonify({
        'status': 'success',
        'message': f'Loại lặp được cập nhật thành {loai_lap}'
    })

@app.route('/update_loop_count', methods=['POST'])
def update_loop_count():
    global so_lan_lap
    data = request.get_json()
    so_lan_lap = data.get('so_lan_lap')
    print(f"Số lần lặp được cập nhật: {so_lan_lap}")
    return jsonify({
        'status': 'success',
        'message': f'Số lần lặp được cập nhật thành {so_lan_lap}'
    })

@app.route('/upload_duong_di', methods=['POST'])
def upload_duong_di():
    global file_duong_di, data_duong_di, danh_sach_diem, danh_sach_duong
    data = request.get_json()
    name_duong_di = data.get('name_duong_di')
    if os.path.exists( path_duong_di + "/" + name_duong_di + "/" + name_duong_di + ".json") == True:
        file_duong_di = path_duong_di + "/" + name_duong_di + "/" + name_duong_di + ".json"
        duong_di = edit_file_json.read_from_json_file(file_duong_di)
        data_duong_di = edit_file_json.convert_dict_to_data(duong_di)
        danh_sach_diem = edit_file_json.read_from_json_file(path_duong_di + "/" + name_duong_di + "/" + "danh_sach_diem.json")
        danh_sach_duong = edit_file_json.read_from_json_file(path_duong_di + "/" + name_duong_di + "/" + "danh_sach_duong.json")
        return jsonify({
            'status': 'success',
            'message': 'Đã tải lên đường đi thành công',
            "data_duong_di": data_duong_di,
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Dữ liệu đường đi không hợp lệ.'
        })

@app.route('/save_duong_di', methods=['POST'])
def save_duong_di():
    global data_duong_di
    data = request.get_json()
    duong_di = data.get('duong_di')

    ket_qua_check, error = edit_file_json.check_data(path_duong_di, duong_di, danh_sach_diem, danh_sach_duong)
    if ket_qua_check:
        data_duong_di = duong_di  # Gán giá trị vào biến toàn cục
        print("Dữ liệu đường đi đã được lưu:", data_duong_di)
        return jsonify({
            'status': 'success',
            'message': 'Dữ liệu đường đi đã được lưu thành công.'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Dữ liệu đường đi không hợp lệ: ' + error
        })
    
#############################################################################################################

@app.route('/update_crop', methods=['POST'])
def update_crop():
    global x_crop_min, y_crop_min
    data = request.get_json()
    print(int(data.get('deltaX')),int(data.get('deltaY')),x_crop_min,y_crop_min)
    x_crop_min = int(data.get('deltaX')) + x_crop_min
    y_crop_min = int(data.get('deltaY')) + y_crop_min
    if x_crop_min < 0:
        x_crop_min = 0
    if x_crop_min > w_goc - w_size:
        x_crop_min = w_goc - w_size
    if y_crop_min < 0:
        y_crop_min = 0
    if y_crop_min > h_goc - h_size:
        y_crop_min = h_goc - h_size

    print(f"x_crop_min: {x_crop_min}, y_crop_min: {y_crop_min}")
    return jsonify({
        'status': 'success',
        'message': 'Cập nhật crop thành công',
        'x_crop_min': x_crop_min,
        'y_crop_min': y_crop_min
    })
@app.route('/update_zoom', methods=['POST'])
def update_zoom():
    global w_goc, h_goc, new_width, new_height
    data = request.get_json()
    zoom = float(data.get('zoom', 1))

    # Cập nhật kích thước ảnh map_all
    new_width = int(w_goc * zoom)
    new_height = int(h_goc * zoom)

    print(f"Zoom: {zoom}, New size: {new_width}x{new_height}")
    return jsonify({
        'status': 'success',
        'message': 'Cập nhật zoom thành công',
        'zoom': zoom
    })

@app.route('/get_data', methods=['GET'])
def get_data():
    global data_duong_di, danh_sach_diem, danh_sach_duong
    # Trả về dữ liệu cần thiết để hiển thị lại
    return jsonify({
        'data_duong_di': data_duong_di,
        'danh_sach_diem': danh_sach_diem,
        'danh_sach_duong': danh_sach_duong,
        'project_name': project_name,
        'chon_ban_do': data_chon_ban_do,
        'data_cai_dat': data_cai_dat,  # Thêm dữ liệu combobox
        'ban_do_moi': data_ban_do_moi,
    })

@app.route('/esp_sent_py', methods=['POST', 'GET'])
def esp_sent_py():
    if request.method == 'POST':
        data = request.get_json()  # Lấy dữ liệu JSON từ ESP
        if data:
            new_data = data["data"]
            if len(str(new_data).split("#")) >= 3:
                list_data = list(bin(int(float(str(new_data).split("#")[2]))).replace("0b", ""))
                for i in range(1, len(list_data)):
                    input_esp["IN" + str(13 - i)] = int(list_data[i])
                print(f"Đã nhận dữ liệu từ ESP: {input_esp}")
            return jsonify({'status': 'success', 'message': 'Dữ liệu đã được nhận'})
        else:
            return jsonify({'status': 'error', 'message': 'Dữ liệu không hợp lệ'})
    elif request.method == 'GET':
        return jsonify({'status': 'success', 'message': 'GET request received'})
    
@app.route('/py_sent_esp', methods=['POST', 'GET'])
def py_sent_esp():
    if request.method == 'POST':
        data = request.get_json()  # Lấy dữ liệu JSON từ ESP
        print(f"Dữ liệu nhận được từ ESP (POST): {data}")
        return jsonify({'status': 'success', 'message': 'Dữ liệu đã được nhận qua POST'})
    elif request.method == 'GET':
        # Trả về dữ liệu cho ESP
        return jsonify({'status': 'success', 'message': 'Dữ liệu từ server', 'data': sent_esp_new})
# Hàm gửi dữ liệu sent_esp lên ESP
def send_sent_esp():
    global sent_esp, sent_esp_new
    while connect_esp:
        if sent_esp != sent_esp_new:  # Kiểm tra nếu sent_esp có giá trị
            try:
                # response = requests.post('http://192.168.11.1:5000/py_sent_esp', json={'sent_esp': sent_esp_new})
                response = requests.post('http://' + host + ':' + str(port) + '/py_sent_esp', json={'sent_esp': sent_esp_new})
                if response.status_code == 200:
                    print(f"Đã gửi dữ liệu sent_esp: {sent_esp_new}")
                    sent_esp = sent_esp_new
                else:
                    print(f"Lỗi khi gửi dữ liệu: {response.status_code}")
            except Exception as e:
                print(f"Lỗi khi gửi dữ liệu sent_esp: {e}")
        time.sleep(1)  # Gửi dữ liệu mỗi giây
# Khởi chạy luồng gửi dữ liệu
threading.Thread(target=send_sent_esp, daemon=True).start()       
@app.route('/')
def index():
    global path_project
    # Lấy danh sách các thư mục trong `path_project_all`
    project_list = os.listdir(path_project_all)
    return render_template('index.html', project_list=project_list, path_project=path_project)
@app.route('/keep_alive', methods=['GET'])
def keep_alive():
    return "OK", 200
# host = '172.26.76.151'
# port = 5000
# #http://172.26.76.151:5000
# if __name__ == '__main__':
#     app.run(host=host, port=port, debug=True)