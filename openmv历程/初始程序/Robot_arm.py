from pyb import UART,Servo,ADC
import time , re
import sensor

base_h = 277 - 120

Actuator = 0

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
    def ad_key_control(self):
        """
        通过ADC模拟按键控制机械臂动作
        """
        ad = ((self.adc.read() * 3.3) / 4095)
        # print(ad)
        # 可根据实际需求调用机械臂动作方法
        if 0.2 > ad > 0.1:
            # print("Z+")
            self.z = self.z + 2

        elif ad < 0.1:
            # print("Z-")
            self.z = self.z - 2

        elif 1.7 > ad > 1.3:
            # print("Y+")
            self.y = self.y + 2

        elif 1.3 > ad > 1:
            # print("Y-")
            self.y = self.y - 2

        elif 0.7 > ad > 0.4:
            # print("X+")
            self.x = self.x - 2

        elif 1 > ad > 0.7:
            # print("X-")
            self.x = self.x + 2

        elif 2 > ad > 1.7:
            # print("Open")
            self.mv_servo(0)  # 示例：张开夹爪
        elif 2.4 > ad > 2:
            # print("Close")
            self.mv_servo(60)   # 示例：闭合夹爪
        elif 2.7 > ad > 2.4:
            # print("Home")
            self.home_seting() # 示例：机械臂复位
            time.sleep_ms(1000)
        time.sleep_ms(100)
        self.set_xyz_point(self.x, self.y, self.z, 0, 0)
        # self.get_xyz_point()

    def __init__(self, nums):
        self.uart1 = UART(nums, 115200, timeout_char=1)
        self.servo = Servo(1)
        self.servo.angle(45)
        self.adc = ADC("P6")  # ADC初始化，必须为"P6"
        self.x = 0
        self.y = 174
        self.z = 277

    def home_seting(self):
        data_to_send = "G28\r\n"
        print(data_to_send, "复位......")
        self.uart1.write(data_to_send)
        start = time.ticks_ms()
        timeout = 12000  # 12秒超时
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                self.x = 0
                self.y = 174
                self.z = 277
                print(string_data)
                break
            if time.ticks_diff(time.ticks_ms(), start) > timeout:
                print("复位超时，无数据返回")
                break

    def get_xyz_point(self):
        data_to_send = "M114\r\n"
        # print(data_to_send, "查询当前坐标......")
        self.uart1.write(data_to_send)
        while True:
            if self.uart1.any():
                data = self.uart1.read()
                string_data = data.decode('utf-8').strip()
                # 串口可能返回多行数据，逐行处理
                for line in string_data.split('\n'):
                    line = line.strip()
                    if 'CURRENT POSITION' in line:
                        position = parse_position(line)
                        if 'error' in position:
                            print(f"坐标解析失败: {position['error']} 原始数据: {position['input']}")
                            continue
                        # print(f"X: {position['X']} Y: {position['Y']} Z: {position['Z']} E: {position['E']}")
                        self.x = position['X']
                        self.y = position['Y']
                        self.z = position['Z']
                        return self.x, self.y, self.z
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
        self.x = X
        self.y = Y
        self.z = Z
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

