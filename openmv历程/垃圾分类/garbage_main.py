# main.py
import sensor, time

import sensor, image, time, ml, math, uos, gc
import Robot_arm as rb

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
# sensor.set_windowing((224, 224))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)
robot.home_seting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行


with open('labels_garbage.txt','r') as file:
    labels = [line.strip()for line in file if line.strip()]
    print(labels)
model = ml.Model("model_garbage.tflite", load_to_fb=True)
print(model)
norm = ml.Normalization(scale = (0.0,1.0))

Actuator = 55

ShiftX = 20
ShiftY = 5

w = 128
h = 128

roi = (int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h)


def garbage():
    results = []  # 存储识别结果

    # 进行10次识别
    for _ in range(10):
        img = sensor.snapshot()
        img.draw_rectangle(int((320-w)/2)+ShiftX,int((240-h)/2)+ShiftY,w,h,color = (0,0,255))
        img2 = img.copy(roi=roi)
        input = [norm(img2)]  # scale 0~255 to 0.0~1.0
        scores = model.predict(input)[0].flatten().tolist()

        # 找到最高分标签
        max_score = 0
        max_label = None
        for label, score in zip(labels, scores):
            if score > max_score:
                max_score = score
                max_label = label

        # 仅记录置信度高的结果
        if max_score > 0.8:
            results.append(max_label)

    # 计算众数（最频繁出现的标签）
    if not results:
        return None

    # 使用简单计数找出出现次数最多的标签
    count_dict = {}
    for label in results:
        count_dict[label] = count_dict.get(label, 0) + 1

    # 找出最高频率
    max_count = 0
    best_label = None
    for label, count in count_dict.items():
        if count > max_count:
            max_count = count
            best_label = label

    return best_label



while(True):
    labelb = garbage()
    print(labelb)
    if labelb == "kitchen_garbage":
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(10)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,18+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(46)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(-120,124,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(-120,124,150+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(20)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)

    if labelb == "other":
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(10)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,18+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(46)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(-120,220,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(-120,220,150+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(20)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)

    if labelb == "harmful_waste":
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(10)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,18+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(46)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(120,124,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(120,124,150+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(20)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)

    if labelb == "recyclable_garbage":
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,50+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(10)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,217,18+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(46)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(120,220,222+Actuator,0,0)
        time.sleep_ms(1000)
        robot.set_xyz_point(120,220,150+Actuator,0,0)
        time.sleep_ms(1000)
        robot.mv_servo(20)
        time.sleep_ms(1000)
        robot.set_xyz_point(0,174,222+Actuator,0,0)
        time.sleep_ms(1000)
