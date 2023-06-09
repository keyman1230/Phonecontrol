import os
import time
from ppadb.client import Client as AdbClient
client = AdbClient(host='127.0.0.1', port=5037)
devices = client.devices()
mydevice = devices[0]
mydevice.shell("rm -rf /sdcard/DCIM/Camera/")





##### Setting ###########
# 프로 모드로 켜놓고 시작해야함. 주의
Phone = "P60 Pro"
shot = 1
# battery_limit = 15
savedir ="D:\Result\MF\DOF\P60 Pro"
##########################
# fnumbername = ["F1.4", "F1.6", "F1.8", "F2.0", "F2.2", "F2.5", "F2.8","F3.2","F3.5","F4.0"]
# xpos = [298, 388, 471, 558, 644, 722, 813, 888, 982, 1069]
# ypos = [1593, 1593, 1593, 1593, 1593, 1593, 1593, 1593, 1593, 1593]

fnumbername = ["F2.8", "F4.0", "F2.0"]
xpos = [ 813, 1069, 558]
ypos = [1593, 1593, 1593]

for fnumber, x, y in zip(fnumbername, xpos, ypos):

    time.sleep(1)
    mydevice.shell("input tap 444 1779")  # F# 버튼 클릭
    time.sleep(2)
    mydevice.shell(f"input tap {x} {y}") # 원하는  F# 터치
    time.sleep(2)
    mydevice.shell("input tap 568 992")  # 화면 중앙 세팅
    time.sleep(2)

    for dac in range(200):
        d = 600 + dac * 2
        mydevice.shell("input tap 940 1730")  # MF setting 클릭
        time.sleep(2)
        mydevice.shell("input tap 1060 1400")  # MF 초기화
        time.sleep(2)
        mydevice.shell(f"input tap {d} 1400")  # 원하는 MF 선택
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
            break
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




