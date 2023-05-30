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
fnumbername = ["F1.4", "F1.6", "F1.8", "F2.0", "F2.2", "F2.5", "F2.8","F3.2","F3.5","F4.0"]
# fpos = [640, 720, 800, 880, 960, 240, 320, 400, 480, 560]
xpos = [298, 388, 471, 558, 644, 722, 813, 888, 982, 1069]
ypos = [1593, 1593, 1593, 1593, 1593, 1593, 1593, 1593, 1593, 1593]

for fnumber, x, y in zip(fnumbername, xpos, ypos):

    time.sleep(1)
    mydevice.shell("input tap 444 1779")  # F# 버튼 클릭
    time.sleep(1)
    mydevice.shell(f"input tap {x} {y}") # 원하는  F# 터치
    time.sleep(1)
    mydevice.shell("input tap 568 992")  # 화면 중앙 세팅
    time.sleep(1)

    for dac in range(400):
        d = 600 + dac * 2
        mydevice.shell("input tap 940 1730")  # MF setting 클릭
        time.sleep(1)
        mydevice.shell("input tap 1060 1400")  # MF 초기화
        time.sleep(1)
        mydevice.shell(f"input tap {d} 1400")  # 원하는 MF 선택
        time.sleep(3)
        # mydevice.shell("input tap 568 992")  # 화면 중앙 터치
        # time.sleep(1)
        # # battery_check = int(mydevice.shell("dumpsys battery | grep temperature").split(':')[-1].split('\n')[0].strip())
        # mydevice.shell("input tap 1860 542")
        # time.sleep(1)
        mydevice.shell(f"input keyevent KEYCODE_CAMERA")
        time.sleep(7)
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



# for n in range(100, 271): #MF 0으로 셋팅
#     touchposition = 971-n
#     print(f"{touchposition = }, {f = }, {x = }")
#     # Phone_battery = int(mydevice.shell("dumpsys battery | grep level").split(':')[-1].split('\n')[0].strip())
#     # if Phone_battery > battery_limit:
#     time.sleep(1)
#     mydevice.shell("input tap 820 1623")  # MF 버튼 클릭
#     time.sleep(1)
#     mydevice.shell(f"input tap {touchposition} 1302")
#     for s in range(shot):
#         mydevice.shell("rm -rf /sdcard/DCIM/Camera/")
#         time.sleep(1)
#         mydevice.shell(f"input keyevent KEYCODE_CAMERA")  # 촬영
#         time.sleep(5)
#         Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split()
#         raw = mydevice.shell("ls /sdcard/DCIM/Camera/RAW").split()
#         jpglist = [s for s in Camera if ".jpg" in s]
#         if len(jpglist) == 1:
#             mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}',
#                           f'{savedir}{os.sep}{"SFRplus"}_{"LD65"}_{"6500"}_{"2000"}_{"6530"}_{"1998"}_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{"12MP"}_{fnumber}_{"50"}_{x}_{971-n}_{jpglist[0]}')
#         else:
#             print("JPG파일 개수를 확인하세요 ")
#             break
#         dnglist = [s for s in raw if ".dng" in s]
#         if len(dnglist) == 1:
#             mydevice.pull(f'/sdcard/DCIM/Camera/RAW/{dnglist[0]}',
#                           f'{savedir}{os.sep}{"SFRplus"}_{"LD65"}_{"6500"}_{"2000"}_{"6530"}_{"1998"}_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{"12MP"}_{fnumber}_{"50"}_{x}_{971-n}_{dnglist[0]}')
#         else:
#             print("DNG파일 개수를 확인하세요 ")
#             break
#             #
            #
            # time.sleep(1)
            # mydevice.shell("input tap 820 1623")  # MF 버튼 클릭
            # time.sleep(1)
            # mydevice.shell(f"input tap {971 - n} 1302")
            # for s in range(shot):
            #     mydevice.shell("rm -rf /sdcard/DCIM/Camera/")
            #     time.sleep(1)
            #     mydevice.shell(f"input keyevent KEYCODE_CAMERA")  # 촬영
            #     time.sleep(5)
            #     Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split()
            #     raw = mydevice.shell("ls /sdcard/DCIM/Camera/RAW").split()
            #     jpglist = [s for s in Camera if ".jpg" in s]
            #     if len(jpglist) == 1:
            #         mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}',
            #                       f'{savedir}{os.sep}{"SFRplus"}_{"LD65"}_{"6500"}_{"2000"}_{"6530"}_{"1998"}_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{"12MP"}_{fnumber}_{"50"}_{"xxxx"}_{971-n}_{jpglist[0]}')
            #     else:
            #         print("JPG파일 개수를 확인하세요 ")
            #         break
            #     dnglist = [s for s in raw if ".dng" in s]
            #     if len(dnglist) == 1:
            #         mydevice.pull(f'/sdcard/DCIM/Camera/RAW/{dnglist[0]}',
            #                       f'{savedir}{os.sep}{"SFRplus"}_{"LD65"}_{"6500"}_{"2000"}_{"6530"}_{"1998"}_{Phone}-{"W"}-{"x1.0"}-{"Default"}-{"Pro"}_{"12MP"}_{fnumber}_{"50"}_{"xxxx"}_{971-n}_{dnglist[0]}')
            #     else:
            #         print("DNG파일 개수를 확인하세요 ")
            #         break

# for i in range(250):
#     for s in range(shot):
#         mydevice.shell(f"input keyevent KEYCODE_CAMERA")  # 촬영
#         time.sleep(1)
#         Camera = mydevice.shell("ls /sdcard/DCIM/Camera").split()
#         jpglist = [s for s in Camera if ".jpg" in s]
#         if len(jpglist) == 1:
#             mydevice.pull(f'/sdcard/DCIM/Camera/{jpglist[0]}', f'{savedir}{os.sep}{Phone}_{i+1}-{s}_{jpglist[0]}')
#         else:
#             print("JPG파일 개수를 확인하세요 ")
#             break
#
#         dnglist = [s for s in Camera if ".dng" in s]
#         if len(dnglist) == 1:
#             mydevice.pull(f'/sdcard/DCIM/Camera/{dnglist[0]}', f'{savedir}{os.sep}{Phone}_{i+1}-{s}_{dnglist[0]}')
#         else:
#             print("DNG파일 개수를 확인하세요 ")
#             break
#
#         mydevice.shell(f"input tap 1839 537")  # 다음 덱으로 이동
#         time.sleep(2)
#


