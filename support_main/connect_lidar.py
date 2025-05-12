import numpy as np
from rplidar import RPLidar
import time
import serial.tools.list_ports
import threading


def get_com_ports():
    """
    Lấy danh sách các cổng COM hiện có.
    
    Returns:
    list: Danh sách các cổng COM.
    """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def check_com_port(port_name):
    """
    Kiểm tra xem cổng COM đầu vào có tồn tại hay không.
    
    Parameters:
    port_name (str): Tên cổng COM cần kiểm tra.
    
    Returns:
    bool: True nếu cổng COM tồn tại, False nếu không tồn tại.
    """
    return port_name in get_com_ports()



class main_lidar:
    def __init__(self, com, bau):
        self.com = com
        self.bau = bau
        self.lidar = ""
        self.connect_lidar = False
        try:
            self.lidar = RPLidar(self.com, baudrate=self.bau)
            self.connect_lidar = True
        except:
            self.connect_lidar = False
            self.load_data = 0
        
        self.scan = [[0],[0],[0]]
        self.ouput = [[0],[0],[0]]
        self.check_scan = 0
        self.load_data = 0
        self.close_lidar = 0
        self.time_close = time.time()

        
        

    def connect(self):
        if self.close_lidar == 0:
            if check_com_port(self.com):
                if self.connect_lidar == False:
                    try:
                        self.lidar = RPLidar(self.com, baudrate=self.bau)
                        self.connect_lidar = True
                    except:
                        self.connect_lidar = False
                        self.load_data = 0
            if self.connect_lidar == True:
                if self.load_data == 0:
                    self.load_data = 1
                    threading.Thread(target=self.load_data_lidar).start()
    def check_close(self):
        if time.time() - self.time_close > 10:
            self.close_lidar = 1
            self.connect_lidar = False
    def disconnect(self):
        if self.connect_lidar == True:
            self.close_lidar = 1
            self.connect_lidar = False
    def load_data_lidar(self):
        if self.connect_lidar == True:
            try:
                for i, scan0 in enumerate(self.lidar.iter_scans()):
                    if len(scan0) > 0 and self.check_scan == 0:
                        self.upload_scan(scan0)
                    self.check_close()
                    if self.close_lidar == 1:
                        self.lidar.stop()
                        self.lidar.stop_motor()
                        self.lidar.disconnect()
                        break
                    # if off_lidar == 1:
                    #     off_lidar = 0
                    #     self.connect_lidar = False
                    #     self.lidar.stop()
                    #     self.lidar.stop_motor()
                    #     self.lidar.disconnect()
                    #     break
            except:
                print("RPLidar exception:")
                self.connect_lidar = False
    def return_data(self):
        check = False
        if self.check_scan == 1:
            self.check_scan = 0
            self.ouput = self.scan
            check = True
        return self.ouput, check

    def upload_scan(self,data):
        self.scan = data
        self.check_scan = 1


# def main_lidar(com, bau):
#     scan_thread = threading.Thread(target=lidar_scan_thread, args=(com, bau))
#     scan_thread.start()

# # Ví dụ sử dụng
# if __name__ == "__main__":
#     com_port = 'COM4'  # Thay đổi theo cổng COM của bạn
#     baud_rate = 256000
#     scan_lidar = main_lidar(com_port, baud_rate)
#     scan_lidar.connect()

# #     # Xử lý dữ liệu trong thread chính
#     while True:
#         data = scan_lidar.return_data()
#         if data is not None:
#             # Xử lý dữ liệu từ LIDAR
#             print(data)