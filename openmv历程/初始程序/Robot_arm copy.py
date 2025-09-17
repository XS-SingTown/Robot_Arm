from pyb import UART,Servo
import time , re

base_h = 162

Actuator = 60

ON = 1


def parse_position(data):
    """
    解析位置字符串并返回坐标字典
    :param data: 包含坐标信息的字符串 (格式: "INFO: CURRENT POSITION: [X:0.00 Y:174.00 Z:120.00 E:0.00]")
    :return: 包含X, Y, Z, E坐标的字典
    """
    try:
        # 找到方括号内的内容
        start_index = data.find('[') + 1
        end_index = data.find(']')

        # 验证字符串格式
        if start_index == -1 or end_index == -1 or start_index >= end_index:
            raise ValueError("无效的输入格式 - 缺少方括号")

        coordinates_str = data[start_index:end_index]

        # 分割键值对
        pairs = coordinates_str.split()

        # 验证元素数量
        if len(pairs) < 4:
            raise ValueError(f"无效的输入格式 - 需要4个元素，实际找到{len(pairs)}")

        # 提取每个值
        result = {
            'X': float(pairs[0].split(':')[1]),
            'Y': float(pairs[1].split(':')[1]),
            'Z': float(pairs[2].split(':')[1]) + base_h - Actuator,
            'E': float(pairs[3].split(':')[1])
        }

        return result

    except Exception as e:
        return {'error': str(e), 'input': data}



class Robot:
    def __init__(self,nums):
        self.uart1 = UART(nums, 115200, timeout_char=1)
        self.servo = Servo(1)
        self.servo.angle(45)

    def home_seting(self):
       data_to_send = "G28\r\n"
       print(data_to_send,"复位......")
       self.uart1.write(data_to_send)
       while(True):
        if self.uart1.any():
            data = self.uart1.read()
            string_data = data.decode('utf-8').strip()
            print(string_data)
            break

    def get_xyz_point(self):
        data_to_send = "M114\r\n"
        print(data_to_send,"查询当前坐标......")
        self.uart1.write(data_to_send)
        while(True):
            if self.uart1.any():
                 data = self.uart1.read()
                 string_data = data.decode('utf-8').strip()
                 position = parse_position(string_data)
                 print(f"X: {position['X']} Y: {position['Y']} Z: {position['Z']} E: {position['E']}")
                 break

    def get_key_val(self):
        data_to_send = "M119\r\n"
        print(data_to_send,"查询当前限位开关......")
        self.uart1.write(data_to_send)
        while(True):
            if self.uart1.any():
                 data = self.uart1.read()
                 string_data = data.decode('utf-8').strip()
                 print(string_data)
                 break

    def set_xyz_point(self,X,Y,Z,E,F):
        data_to_send = "G1 X{} Y{} Z{} E{} F{}\r\n".format(X, Y, Z-base_h+Actuator, E, F)
        self.uart1.write(data_to_send)
        time.sleep_ms(10)

    def relay(self,state):
        if state == ON :
            data_to_send = "M1\r\n"
        else:
            data_to_send = "M2\r\n"
        print(data_to_send)
        self.uart1.write(data_to_send)

    def Servo(self,state):
        if state == ON :
            data_to_send = "M3\r\n"
        else:
            data_to_send = "M5\r\n"
        print(data_to_send)
        self.uart1.write(data_to_send)

    def mv_servo(self,angle):
        self.servo.angle(angle)

