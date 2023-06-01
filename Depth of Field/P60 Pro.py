import os
import time
from ppadb.client import Client as AdbClient
import argparse


def set_P60_Pro(f_num):
    MF = {
     1.4:{"fnum_x":298,
          "fnum_y":1593,
          "mf_x":792,
          "mf_y":1410},
     2.0:{"fnum_x":558,
          "fnum_y":1593,
          "mf_x":788,
          "mf_y":1410},
     2.8:{"fnum_x":813,
          "fnum_y":1593,
          "mf_x":800,
          "mf_y":1410},
     4.0:{"fnum_x":1069,
          "fnum_y":1593,
          "mf_x":802,
          "mf_y":1410}
    }
    time.sleep(1)
    mydevice.shell("input tap 444 1779")  # F# 버튼 클릭
    time.sleep(2)
    mydevice.shell(f"input tap {MF[f_num]['fnum_x']} {MF[f_num]['fnum_y']}") # 원하는  F# 터치
    time.sleep(2)
    mydevice.shell("input tap 568 992")  # 화면 중앙 세팅

    time.sleep(1)
    mydevice.shell("input tap 945 1775")  # MF 버튼 클릭
    time.sleep(2)
    mydevice.shell(f"input tap 1065 1395") # Dac 초기화
    time.sleep(2)
    mydevice.shell(f"input tap {MF[f_num]['mf_x']} {MF[f_num]['mf_y']}") # 원하는  Dac 터치
    time.sleep(3)



parser = argparse.ArgumentParser(description='Input Y position ')
parser.add_argument('--ypos', type=str, required=True)
parser.add_argument('--f', type=str, required=True)
parser.add_argument('--fset', type=str, required=False)
args = parser.parse_args()
distance = args.ypos
F_num = args.f
setting_fnumber = float(args.fset)
client = AdbClient(host='127.0.0.1', port=5037)
devices = client.devices()
mydevice = devices[0]
mydevice.shell("rm -rf /sdcard/DCIM/Camera/")
time.sleep(4)
##### Setting ###########
Phone = "P60 Pro"
shot = 1
savedir ="D:\Result\MF\DOF\P60 Pro"
##########################

if setting_fnumber:
    set_P60_Pro(setting_fnumber)


for s in range(shot):

    mydevice.shell(f"input keyevent KEYCODE_CAMERA")  # 촬영
    time.sleep(8)
    Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split()
    jpglist = [s for s in Camera if ".jpg" in s]
    if len(jpglist) == 1:
        mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}', f'{savedir}{os.sep}{Phone}_{F_num}_{distance}_{jpglist[0]}')
    else:
        print("JPG파일 개수를 확인하세요 ")
        break

    dnglist = mydevice.shell("ls /sdcard/DCIM/Camera/RAW").split()
    if len(dnglist) == 1:
        mydevice.pull(f'/sdcard/DCIM/Camera/RAW/{dnglist[0]}', f'{savedir}{os.sep}{Phone}_{F_num}_{distance}_{dnglist[0]}')
    else:
        print("DNG파일 개수를 확인하세요 ")
        break

    time.sleep(5)

    mydevice.shell("rm -rf /sdcard/DCIM/Camera/")

