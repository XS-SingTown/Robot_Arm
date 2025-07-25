# Untitled - By: Admin - Wed Jun 25 2025

import sensor
import time

import Robot_arm as rb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)

clock = time.clock()

robot = rb.Robot(3) #初始化，设置串口3为机械臂通讯串口。
print(robot)

robot.home_seting()   #机械臂复位，复位运行时若有异常请重启机械臂后再次运行

# robot.get_key_val()

# robot.get_xyz_point() #获取当前XYZE坐标

# robot.set_xyz_point(0,174,222,0,0)    #给XYZE坐标，坐标系为平面直角坐标系，（X，Y，Z，E,F），#
# #                                     # E为滑轨坐标，不带滑轨给0即可，F为机械臂运行速度，值小于5为自动插值。#
# #                                     # x=0,y=174，z=222为复位后初始坐标#

# robot.relay(False)    #控制继电器（机械臂主板）

# robot.Servo(False)    #控制舵机（接机械臂主板）

# robot.mv_servo(50)   #给定抓夹舵机角度（接OPENMV拓展板）

while True:
    clock.tick()
    img = sensor.snapshot()
    # print(clock.fps())
