import socket
import time
import path
from support_main.lib_main import edit_csv_tab
import numpy as np
import pyperclip
import struct
import os
# pyperclip.copy('The text to be copied to the clipboard.')
# import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets


UDP_IP = "192.168.1.10" # Nhận từ tất cả các địa chỉ IP
UDP_PORT = 2368

path_phan_mem = path.path_phan_mem
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
        if data_admin[i][0] == "host_lidar":
            host_lidar = data_admin[i][1]
        if data_admin[i][0] == "port_lidar":
            port_lidar = int(float(data_admin[i][1]))
print("host_lidar", host_lidar)
print("port_lidar", port_lidar, port_lidar == 2368)
UDP_IP = host_lidar
UDP_PORT = port_lidar


class LidarP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timer = QtCore.QTimer()
        self.final_data = np.array([[0],[0],[0]])
        self.final_data_old = np.array([[0],[0],[0]])
        self.final_data_new = []
        self.connect = True
        self.data_ok = 0
        # self.win = pg.GraphicsLayoutWidget()

        # self.plot = self.win.addPlot()
        self.setup()
        self.start = False


    def setup(self):
        self.sock.bind((UDP_IP, UDP_PORT))
        # self.timer.timeout.connect(self.process_data)
        self.timer.start(40)
        # self.win.show()
        # self.plot.setXRange(-1000, 1000)
        # self.plot.setYRange(-1000, 1000)

    def decode_data(self, data):
        """Giải mã dữ liệu từ LR-1BS3/5."""
        if len(data) != 8:
            raise ValueError("Dữ liệu đầu vào phải là 8 byte.")

        angle_raw, distance_raw, signal_raw, _ = struct.unpack("<HHHH", data)

        angle = angle_raw * 0.01

        distance = distance_raw  # Giả sử tỷ lệ khoảng cách là 1mm
        signal = signal_raw

        return angle, distance, signal, _
    def get_data(self):
        output = self.final_data_old
        if self.data_ok == 1:
            output = self.final_data
            self.final_data_old = self.final_data
            self.data_ok = 0
            
        return output
    # def process_data(self):
    #     start = False
    #     final_data = []
    #     try: 
    #         data, addr = self.sock.recvfrom(1240)
    #     except socket.timeout:
    #         self.connect = False
    #     if self.connect == True:
    #         body = data[40:]
    #         data_array = []
    #         for i in range(0, 1200, 8):
    #             eight_bytes = body[i:i + 8]
    #             angle, distance, signal, _ = self.decode_data(eight_bytes)
    #             data_array.append([angle, distance, signal])

    #         data_array = np.array(data_array)
    #         if np.min(data_array[:, 0]) == 0 and start == True:
    #             if self.data_ok == 0:
    #                 self.final_data = final_data
    #                 self.data_ok = 1
                    
    #             start = False

    #         if np.min(data_array[:, 0]) == 0:
    #             start = True

    #         if start:
    #             final_data = [*final_data, *data_array]
    def process_data(self):
        while self.connect:
            try: 
                data, addr = self.sock.recvfrom(1240)
            except socket.timeout:
                self.connect = False
                print("connect False")
                break
            body = data[40:]
            data_array = []

            # Chuyển toàn bộ body (1200 bytes) thành mảng NumPy
            data0 = np.frombuffer(body, dtype=np.uint16).reshape(-1, 4)

            

            data = data0[data0[:, 1] != 0]
            # print(data)
            # print("---------------")

            # Giải mã dữ liệu
            angles0 = data0[:, 0] * 0.01  # Góc quét (angle)
            angles = data[:, 0] * 0.01  # Góc quét (angle)
            # print(angles)
            distances = data[:, 1]      # Khoảng cách đo được (distance)
            signals = data[:, 2]        # Cường độ tín hiệu (signal)

            # Lọc bỏ các hàng có distance == 0
            # valid_indices = distances0 > 0
            # angles = angles0[valid_indices]
            # distances = distances0[valid_indices]
            # signals = signals[valid_indices]

            # Kết hợp các giá trị thành mảng dữ liệu
            # print("angles0[0],angles0[-1]",angles0[0],angles0[-1])
            # print(angles)
            # if angles.shape[0] != 0:
                # print("angles[0],angles[-1]",angles[0],angles[-1])
            # print(distances0)
            data_array = np.column_stack((signals, angles, distances))
            # print(data_array.shape)
            # data_array = np.array(data_array)

            

            if int(angles0[0]) == 0:
                if self.data_ok == 0:
                    self.final_data = self.final_data_new  # Ensure it's a NumPy array
                    # print(self.final_data_new, np.array(self.final_data_new).shape)
                    # Kiểm tra self.final_data chạy từ góc bao nhiêu đến bao nhiêu
                    # if self.final_data.size > 0:
                    #     min_angle = np.min(self.final_data[:, 1])
                    #     max_angle = np.max(self.final_data[:, 1])
                    #     print(f"self.final_data chạy từ góc {min_angle} đến {max_angle}")
                    self.data_ok = 1
                self.final_data_new = []
            else:
                self.final_data_new = [*self.final_data_new, *data_array]
                # self.final_data_new = data_array
                # print(np.array(self.final_data_new).shape)

