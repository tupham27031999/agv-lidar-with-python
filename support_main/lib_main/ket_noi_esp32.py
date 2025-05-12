import serial
import load_data_csv
from tkinter.messagebox import showerror, showwarning, showinfo
import time
import threading
import shutil,os
import path
import time
close_ser = 0
#remove file
def remove_file(path):
    if os.path.exists(path) == True:
        try:
            os.remove(path) 
        except OSError as e:
            pass
# remove folder
def remove_folder(path):
    if os.path.exists(path) == True:
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
# tao folder
def tao_folder(path):
    if os.path.exists(path) == False:
        try:
            os.mkdir(path)
        except OSError as e:
            showerror(title='Error',message='không có folder: '+ str(path))
    return path
# remove all (file, folder) trong folder
def remove_all(path):
    if os.path.exists(path) == True:
        for os_path in os.listdir(path):
            l = 0
            for i in (os_path):
                if i == ".":
                    l = 1
                    try:
                        os.remove(path+"/"+os_path) 
                    except OSError as e:
                        showerror(title='Error',message='Không xóa được file: ' + path+"/"+os_path)
                    break
            if l == 0:
                try:
                    shutil.rmtree(path+"/"+os_path)
                except OSError as e:
                    showerror(title='Error',message='Không xóa được file: ' + path+"/"+os_path)

tao_folder(path.esp_sent_py)
tao_folder(path.py_sent_esp)
remove_all(path.esp_sent_py)
remove_all(path.py_sent_esp)
com = load_data_csv.ds_admin()[2][0][0]
hz = load_data_csv.ds_admin()[2][0][1]
load_ok = 0
connected = False
stop, start, reset,nguon_off,nguon_on,co_sp,khong_sp,kenh_sp,nha,kep,err_kep,nang,ha,an_toan,ko_an_toan = ["","","","","","","","","","","","","","",""]
sent_data = ""
def thap_phan_sang_nhi_phan(n): 
    return list(bin(n).replace("0b", ""))[::-1]

class Python_Esp:
    def __init__(self):
        self.serial = serial.Serial()
        self.connected = False
        self.data_esp_sent = []
        self.check_reset = "0"
        self.reset = "0"
        self.data_sent_esp = ""
        self.time_reset = 0
        self.data = ""
        self.new_data = ""
    def khai_bao_serial(self):
        try:
            self.serial.port = str(com)
            self.serial.baudrate = int(hz)
            self.serial.bytesize = serial.EIGHTBITS #number of bits per bytes
            self.serial.timeout = 1            #non-block read
            self.serial.writeTimeout = 2     #timeout for write
            self.serial.open()
            self.connected = True
            self.out = ""
            self.lay_du_lieu = 0
            self.data_old = ""
        except OSError as e:
            self.connected = False
    def check_connect(self):
        try:
            self.serial.inWaiting()
        except:
            self.connected = False
    def load_data(self):
        if self.connected == True:
            if len(self.data_esp_sent) != 0:
                if self.time_reset == 0:
                    self.time_reset = time.time()
                if len(self.data_esp_sent) == 0:
                    try:
                        if self.time_reset != 0 and time.time() - self.time_reset >=1:
                            self.time_reset = 0
                            # self.serial.write("8".encode())
                    except:
                        pass
            self.out = ""
            load = 0
            
            while self.serial.inWaiting() > 0:
                try:
                    self.data = self.serial.readline()
                    for ot in list(str(self.data)):
                        if ot == str("\\"):
                            break
                        if load == 1 and ot != str("'"):
                            self.out = self.out + ot
                        if ot == str("'"):
                            load = 1
                    if self.out != "":
                        # print("out = ",self.out)
                        if len(list(self.out)) == 4:
                            if self.out != self.data_old:
                                try:
                                    self.data=""
                                    self.data_old = self.out
                                    self.data_esp_sent = thap_phan_sang_nhi_phan(int(self.out))
                                except OSError as e:
                                    pass
                except OSError as e:
                    pass
        if len(self.data_esp_sent) != 0:
            # print(self.data_esp_sent)
            pass
                
    def sent_data(self,data):
        self.data = data
        self.serial.write(self.data.encode())
    def close_serial(self):
        self.serial.close()
def py_sent_esp(data):
    global sent_data
    sent_data = data
def esp_sent_py():
    global connected
    ds_esp_sent_py = os.listdir(path.esp_sent_py)
    connected = "False"
    sent = "0"
    for i in range(0,len(ds_esp_sent_py)):
        if str(ds_esp_sent_py[i]) == "connected":
            connected = "True"
    for i in range(0,len(ds_esp_sent_py)):
        if str(ds_esp_sent_py[i]) == "sent" and connected == "True":
            sent = "1"
    return connected,sent
def close_serial():
    global close_ser
    close_ser = 1
def python_esp32():
    global reset,connected, sent_data, close_ser
    py_esp = Python_Esp()
    py_esp.khai_bao_serial()

    # t0 = time.time()
    # t1 = time.time()

    while True:
        
        py_esp.check_connect()
        py_esp.load_data()

        # if py_esp.connected == True and time.time() - t0 > 3:
        #     t0 = time.time()
        #     py_sent_esp("0100")

        if py_esp.connected == False:
            py_esp.khai_bao_serial()
            # print(py_esp.connected)
        if py_esp.connected == True:
            tao_folder(path.esp_sent_py+"/connected")
            remove_folder(path.esp_sent_py+"/disconnected")
            if py_esp.data_esp_sent == "1":
                tao_folder(path.esp_sent_py+"/sent")
                remove_folder(path.esp_sent_py+"/close_sent")
            else:
                tao_folder(path.esp_sent_py+"/close_sent")
                remove_folder(path.esp_sent_py+"/sent")
        
        else:
            tao_folder(path.esp_sent_py+"/disconnected")
            remove_folder(path.esp_sent_py+"/connected")
        if sent_data != "":
            py_esp.sent_data(sent_data)
            print("Đã gửi: "+str(sent_data))
            sent_data = ""
        # if close_ser == 1 or time.time()-t1 > 15:
        if close_ser == 1:
            py_esp.close_serial()
            break

# while True:
# python_esp32()