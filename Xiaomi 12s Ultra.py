import os
import time
from ppadb.client import Client as AdbClient
import argparse

parser = argparse.ArgumentParser(description='Input Y position ')
parser.add_argument('--ypos', type=str, required=True)
args = parser.parse_args()
distance = str((10330 - int(args.ypos))/10)
client = AdbClient(host='127.0.0.1', port=5037)
devices = client.devices()
mydevice = devices[0]
mydevice.shell("rm -rf /sdcard/DCIM/Camera/")

##### Setting ###########
Phone = "Mi12sUltra"
shot = 1
savedir ="D:\Result\MF\DOF\Mi12sUltra"
##########################
time.sleep(10)
for s in range(shot):

    mydevice.shell(f"input keyevent KEYCODE_CAMERA")  # 촬영
    time.sleep(8)
    Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split()
    jpglist = [s for s in Camera if ".jpg" in s]
    if len(jpglist) == 1:
        mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}', f'{savedir}{os.sep}{Phone}_{distance}_{jpglist[0]}')
    else:
        print("JPG파일 개수를 확인하세요 ")
        break

    dnglist = mydevice.shell("ls /sdcard/DCIM/Camera/RAW").split()
    if len(dnglist) == 1:
        mydevice.pull(f'/sdcard/DCIM/Camera/RAW/{dnglist[0]}', f'{savedir}{os.sep}{Phone}_{distance}_{dnglist[0]}')
    else:
        print("DNG파일 개수를 확인하세요 ")
        break

    time.sleep(5)

    mydevice.shell("rm -rf /sdcard/DCIM/Camera/")

