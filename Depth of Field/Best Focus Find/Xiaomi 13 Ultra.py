### 미사용 ######



import os
import time
from ppadb.client import Client as AdbClient
client = AdbClient(host='127.0.0.1', port=5037)
devices = client.devices()
mydevice = devices[0]
mydevice.shell("rm -rf /sdcard/DCIM/Camera/")


##### Setting ###########
# 프로 모드로 켜놓고 시작해야함. 주의
Phone = "Xiaomi 13 Ultra"
shot = 1
# battery_limit = 15
# savedir ="D:\Result\MF\DOF\Xiaomi 13 Ultra"
savedir ="D:\Result"
##########################
fnumbername = ["F1.9", "F4.0"]
xpos = [427, 400]
ypos = [1402, 1402]

for fnumber, x, y in zip(fnumbername, xpos, ypos):

    time.sleep(1)
    mydevice.shell("input tap 617 1617")  # F# 버튼 클릭
    time.sleep(1)
    mydevice.shell("input swipe 548 1402 850 1402 300 ")  # F# 초기화
    time.sleep(1)
    mydevice.shell(f"input swipe 548 1402 {x} {y} 300") # 원하는  F# 로 drag
    time.sleep(1)
    mydevice.shell("input tap 551 946")  # 화면 중앙 세팅
    time.sleep(1)

    for i in range(2):

        mydevice.shell("input tap 289 1611")  # MF setting 클릭
        time.sleep(1)
        mydevice.shell("input swipe 555 1506 240 1506 500")  # MF 초기화
        time.sleep(1)
        mydevice.shell("input tap 551 946")  # 화면 중앙 세팅
        time.sleep(1)
    mydevice.shell("input tap 289 1611")  # MF setting 클릭
    time.sleep(1)
    mydevice.shell(f"input swipe 555 1506 990 1506 30000")  # MF 초기화
    time.sleep(1)

    mydevice.shell("input tap 289 1611")  # MF setting 클릭
    time.sleep(1)
    mydevice.shell(f"input swipe 555 1506 990 1506 30000")  # MF 초기화
    time.sleep(3)

    # for dac in range(40):
    #     d = 555+8*15
    #     print(dac, d)
    #     for i in range(2):
    #
    #         mydevice.shell("input tap 289 1611")  # MF setting 클릭
    #         time.sleep(1)
    #         mydevice.shell("input swipe 555 1506 240 1506 500")  # MF 초기화
    #         time.sleep(1)
    #         mydevice.shell("input tap 551 946")  # 화면 중앙 세팅
    #         time.sleep(1)
    #     mydevice.shell("input tap 289 1611")  # MF setting 클릭
    #     time.sleep(1)
    #     mydevice.shell(f"input swipe 555 1506 {d} 1506 300")  # MF 초기화
    #     time.sleep(3)
    #     # mydevice.shell("input tap 568 992")  # 화면 중앙 터치
    #     # time.sleep(1)
    #     # # battery_check = int(mydevice.shell("dumpsys battery | grep temperature").split(':')[-1].split('\n')[0].strip())
    #     # mydevice.shell("input tap 1860 542")
    #     # time.sleep(1)
    #     mydevice.shell(f"input keyevent KEYCODE_CAMERA")
    #     time.sleep(7)
    #     Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split() # JPG 저장 폴더
    #     raw = mydevice.shell("ls /sdcard/DCIM/Camera/Raw").split() # DNG 저장 폴더
    #     jpglist = [s for s in Camera if ".jpg" in s]
    #     if len(jpglist) == 1:
    #         mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}',
    #                       f'{savedir}{os.sep}{"SFRplus"}_LD65-6500-2000-X-X_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{fnumber}-{d}_{jpglist[0]}')
    #     else:
    #         print("JPG파일 개수를 확인하세요 ")
    #         break
    #     dnglist = [s for s in raw if ".dng" in s]
    #     time.sleep(3)
    #     if len(dnglist) == 1:
    #         mydevice.pull(f'/sdcard/DCIM/Camera/Raw/{dnglist[0]}',
    #                       f'{savedir}{os.sep}{"SFRplus"}_LD65-6500-2000-X-X_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{fnumber}-{d}_{dnglist[0]}')
    #         # time.sleep(3)
    #     else:
    #         print("DNG파일 개수를 확인하세요 ")
    #         break
    #     mydevice.shell("rm -rf /sdcard/DCIM/Camera/")


