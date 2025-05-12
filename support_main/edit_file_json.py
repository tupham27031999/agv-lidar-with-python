import json
from support_main.lib_main import remove

# NAME: DUONG_DI_1
# X1: START-L0-P1
# X2: P1-L1-P2-O1, P2-L1-P1-O1
# XALL: P1-L1-P2-O1, P2-L2-P3-O1

dict_data = {"1": {"NAME": "DUONG_DI_1"}, "2": {"X1": [["START","L0","P1","NONE"]]}, "3": {"X2": [["P1","L1","P2","O1"], ["P2","L1","P1","O1"]]}, "4": {"XALL": [["P1","L1","P2","O1"], ["P2","L2","P3","O1"]]}}

data = "NAME: DUONG_DI_1 \nX1: START-L0-P1-NONE \nX2: P1-L1-P2-O1,\n P2-L1-P1-O1 \nXALL: P1-L1-P2-O1, P2-L2-P3-O1"
ds_diem = {"1": {"point_name":"P1","point_coord":[1, 1], "direction":"", "alpha":""},
           "2": {"point_name":"P2","point_coord":[1, 1], "direction":"", "alpha":""},
           "3": {"point_name":"P3","point_coord":[1, 1], "direction":"", "alpha":""}}
ds_duong = {"1": {"ten_duong": "L1", "diem_1": "P1", "diem_2": "P2", "loai_duong": "line_type", "C1": "c1", "C2": "c2"},
            "2": {"ten_duong": "L2", "diem_1": "P1", "diem_2": "P2", "loai_duong": "line_type", "C1": "c1", "C2": "c2"},
            "3": {"ten_duong": "L3", "diem_1": "P1", "diem_2": "P2", "loai_duong": "line_type", "C1": "c1", "C2": "c2"}}

def convert_dict_to_data(dict_data):
    result = []
    for key, value in dict_data.items():
        for sub_key, sub_value in value.items():
            if isinstance(sub_value, list):  # Nếu giá trị là danh sách (các đường đi)
                # Chuyển danh sách thành chuỗi với định dạng "A-B-C"
                paths = ", ".join(["-".join(item) for item in sub_value])
                result.append(f"{sub_key}: {paths}")
            else:  # Nếu giá trị là chuỗi (tên đường đi)
                result.append(f"{sub_key}: {sub_value}")
    return "\n".join(result)
def tach_du_lieu_dau_vao(data):
    """
    Tách dữ liệu đầu vào thành dictionary giống với dict_data.

    Args:
        data (str): Chuỗi dữ liệu đầu vào.

    Returns:
        dict: Dictionary chứa dữ liệu đã được tách.
    """
    result = {}
    lines = data.split("\n")  # Tách chuỗi thành các dòng
    for idx, line in enumerate(lines, start=0):
        line = line.strip()  # Loại bỏ khoảng trắng thừa ở đầu và cuối dòng
        if not line:  # Bỏ qua dòng trống
            continue
        if ":" not in line:  # Bỏ qua các dòng không chứa dấu ":"
            continue
        key, value = line.split(":", 1)  # Tách phần trước và sau dấu ":"
        key = key.strip()  # Loại bỏ khoảng trắng thừa
        value = value.strip()  # Loại bỏ khoảng trắng thừa
        if key == "NAME":
            result[str(idx)] = {key: value}
        else:
            # Tách các phần tử theo dấu "," và sau đó tách tiếp theo dấu "-"
            paths = [segment.strip().split("-") for segment in value.split(",")]
            result[str(idx)] = {key: paths}
    return result

# Hàm lưu dictionary vào file JSON
def save_to_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # Ghi dữ liệu vào file JSON với định dạng đẹp
    print(f"Dữ liệu đã được lưu vào file: {filename}")

# Hàm đọc dictionary từ file JSON
def read_from_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Đọc dữ liệu từ file JSON
        print(f"Dữ liệu đã được đọc từ file: {filename}")
        return data
    except FileNotFoundError:
        print(f"File {filename} không tồn tại.")
        return None


def check_name_in_parsed_dict(parsed_dict):
    # Kiểm tra index đầu tiên (key "0") có chứa key "NAME" và giá trị của "NAME" khác rỗng
    if "1" in parsed_dict and "NAME" in parsed_dict["0"] and parsed_dict["0"]["NAME"].strip():
        return True
    return False



def extract_points_and_lines(ds_diem, ds_duong):
    # Lấy danh sách các điểm từ ds_diem
    list_points = [value["point_name"] for value in ds_diem.values()]
    
    # Lấy danh sách các đường từ ds_duong
    list_lines = [value["ten_duong"] for value in ds_duong.values()]
    
    return list_points, list_lines




def extract_specific_points(parsed_dict):
    points = []
    # Duyệt qua các key từ "1" trở đi
    for key in parsed_dict:
        if key.isdigit() and int(key) >= 1:  # Chỉ xử lý các key số từ "2" trở đi
            for sublist in parsed_dict[key].values():
                for item in sublist:
                    # Chỉ lấy giá trị ở vị trí 1 và 3 (nếu tồn tại)
                    if len(item) > 2:  # Đảm bảo danh sách có ít nhất 3 phần tử
                        points.append(item[0])  # Lấy giá trị ở vị trí 1 (index 0)
                        points.append(item[2])  # Lấy giá trị ở vị trí 3 (index 2)
    return points

def extract_specific_lines(parsed_dict):
    lines = []
    # Duyệt qua các key từ "2" trở đi
    for key in parsed_dict:
        if key.isdigit() and int(key) >= 1:  # Chỉ xử lý các key số từ "2" trở đi
            for sublist in parsed_dict[key].values():
                for item in sublist:
                    # Chỉ lấy giá trị ở vị trí 2 (nếu tồn tại)
                    if len(item) > 1:  # Đảm bảo danh sách có ít nhất 2 phần tử
                        lines.append(item[1])  # Lấy giá trị ở vị trí 2 (index 1)
    return lines


def are_all_points_in_list(points, list_points):
    # Loại bỏ giá trị "START" khỏi danh sách points
    filtered_points = [point for point in points if point != "START"]
    
    # Kiểm tra tất cả các điểm trong filtered_points có trong list_points hay không
    return all(point in list_points for point in filtered_points)

def are_all_lines_in_list(specific_lines, list_lines):
    # Loại bỏ giá trị "L0" khỏi danh sách specific_lines
    filtered_lines = [line for line in specific_lines if line != "L0"]
    
    # Kiểm tra tất cả các đường trong filtered_lines có trong list_lines hay không
    return all(line in list_lines for line in filtered_lines)





def check_data(path_save, input_data, danh_sach_diem, danh_sach_duong):
    ket_qua_check = True
    error =  ""
    # tach du lieu dau vao
    parsed_dict = tach_du_lieu_dau_vao(input_data)
    if len(parsed_dict) < 2:
        ket_qua_check = False
        error = "E0" # Thiếu dữ liệu
    # print(len(parsed_dict))

    # Gọi hàm kiểm tra tên
    has_valid_name = check_name_in_parsed_dict(parsed_dict)
    if not has_valid_name:
        ket_qua_check = False
        error = "E1" # Thiếu tên đường đi


    # Gọi hàm lấy ra các điểm và đường
    list_points, list_lines = extract_points_and_lines(danh_sach_diem, danh_sach_duong)

    # Gọi hàm kiem tra diem
    points = extract_specific_points(parsed_dict)
    all_points_exist = are_all_points_in_list(points, list_points)
    if not all_points_exist:
        ket_qua_check = False
        error = "E2" # Điểm điền bị sai


    # Gọi hàm kiem tra duong
    specific_lines = extract_specific_lines(parsed_dict)
    all_lines_exist = are_all_lines_in_list(specific_lines, list_lines)
    if not all_lines_exist:
        ket_qua_check = False
        error = "E3" # Đường điền bị sai
    if ket_qua_check == True:
        # Lưu dữ liệu vào file JSON
        filename = f"{parsed_dict['0']['NAME']}"
        remove.tao_folder(path_save + "/" + str(filename))
        save_to_json_file(parsed_dict, path_save + "/" + str(filename) + "/" + filename + ".json")
        save_to_json_file(danh_sach_diem, path_save + "/" + str(filename) + "/danh_sach_diem.json")
        save_to_json_file(danh_sach_duong, path_save + "/" + str(filename) + "/danh_sach_duong.json")
    return ket_qua_check, error

# check_data(".",data, ds_diem, ds_duong)
