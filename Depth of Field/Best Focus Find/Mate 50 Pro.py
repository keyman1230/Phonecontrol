import os
import time
from ppadb.client import Client as AdbClient
# scrcpy -m 1080
client = AdbClient(host='127.0.0.1', port=5037)
devices = client.devices()
mydevice = devices[0]
mydevice.shell("rm -rf /sdcard/DCIM/Camera/")


##### Setting ###########
# 프로 모드로 켜놓고 시작해야함. 주의
Phone = "Mate 50 Pro"
shot = 1
# battery_limit = 15
savedir ="D:\Result\MF\DOF\Mate 50 Pro"
##########################
# fnumbername = ["F1.4", "F1.6", "F1.8", "F2.0", "F2.2", "F2.5", "F2.8","F3.2","F3.5","F4.0"]
# xpos = [241, 324, 403, 488, 566, 647, 725, 808, 891, 967]
# ypos = [1472, 1472, 1472, 1472, 1472, 1472, 1472, 1472, 1472, 1472]

fnumbername = ["F4.0"]
xpos = [967]
ypos = [1472]

for fnumber, x, y in zip(fnumbername, xpos, ypos):

    time.sleep(1)
    mydevice.shell("input tap 403 1616")  # F# 버튼 클릭
    time.sleep(2)
    mydevice.shell(f"input tap {x} {y}") # 원하는  F# 터치
    time.sleep(2)
    mydevice.shell("input tap 553 960")  # 화면 중앙 세팅
    time.sleep(2)

    for dac in range(150):
        d = 600 + dac * 2
        mydevice.shell("input tap 833 1620")  # MF setting 클릭
        time.sleep(1)
        mydevice.shell("input tap 978 1292")  # MF 초기화
        time.sleep(1)
        mydevice.shell(f"input tap {d} 1292")  # 원하는 MF 선택
        time.sleep(3)
        # mydevice.shell("input tap 568 992")  # 화면 중앙 터치
        # time.sleep(1)
        # # battery_check = int(mydevice.shell("dumpsys battery | grep temperature").split(':')[-1].split('\n')[0].strip())
        # mydevice.shell("input tap 1860 542")
        # time.sleep(1)
        mydevice.shell(f"input keyevent KEYCODE_CAMERA")
        time.sleep(9)
        Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split() # JPG 저장 폴더
        raw = mydevice.shell("ls /sdcard/DCIM/Camera/RAW").split() # DNG 저장 폴더
        jpglist = [s for s in Camera if ".jpg" in s]
        if len(jpglist) == 1:
            mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}',
                          f'{savedir}{os.sep}{"SFRplus"}_LD65-6500-2000-X-X_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{fnumber}-{d}_{jpglist[0]}')
        else:
            print("JPG파일 개수를 확인하세요 ")
            continue
        dnglist = [s for s in raw if ".dng" in s]
        time.sleep(3)
        if len(dnglist) == 1:
            mydevice.pull(f'/sdcard/DCIM/Camera/RAW/{dnglist[0]}',
                          f'{savedir}{os.sep}{"SFRplus"}_LD65-6500-2000-X-X_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{fnumber}-{d}_{dnglist[0]}')
            # time.sleep(3)
        else:
            print("DNG파일 개수를 확인하세요 ")
            break
        mydevice.shell("rm -rf /sdcard/DCIM/Camera/")




