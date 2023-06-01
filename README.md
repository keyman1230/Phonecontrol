[ Ver. 2.9 (2022-07-26) ]
usage: PhoneControl_android.py [-h] [-ad] [-f] [-d | -i | -w | -p] -m MODE [-c CHART] -l LIGHT -lx LUX -s SETFILE

Android Camera App Mode Setting

optional arguments:
  -h, 		--help            			show this help message and exit
  -ad, 		--autodetection  			Enable Auto Detection Mode
  -f, 		--jsonformat      			Make PhoneSetting format json file
  -d, 		--logging_debug   			Logging Level set to DEBUG
  -i, 		--logging_info    			Logging Level set to INFO
  -w, 		--logging_warning			Logging Level set to WARNING
  -p, 		--logging_print   			Logging on console
  -m MODE, 	--mode MODE  				Preset name for preview mode setting
  -c CHART, 	--chart CHART	                        Chart Type
  -l LIGHT, 	--light LIGHT	                        Light Source Type [LD65 / HD65 / CWF / LDP65 / etc.]
  -lx LUX, 	--lux LUX    				Illumination [2000 / 1000 / 100 / 50 / etc.]
  -s SETFILE, 	--setfile SETFILE			App Mode Setting File [setting file (path + filename)]

ex) PhoneControl_android_v2p9.exe -ad -m W-24mm-RAW -l LD65 -lx 2000 -s ".\[Setting] Phone_Setting\PhoneSetting_Xperia1IV.json"


[ Ver. 2.8 ~ 2.2 (2022-07-26) ]
usage: PhoneControl_android.py [-h] [-ad] [-d | -i | -w | -p] -m MODE [-c CHART] -l LIGHT -lx LUX -s SETFILE

Android Camera App Mode Setting

optional arguments:
  -h, 		--help            			show this help message and exit
  -ad, 		--autodetection  			Enable Auto Detection Mode
  -d, 		--logging_debug   			Logging Level set to DEBUG
  -i, 		--logging_info    			Logging Level set to INFO
  -w, 		--logging_warning			Logging Level set to WARNING
  -p, 		--logging_print   			Logging on console
  -m MODE, 	--mode MODE  				Preset name for preview mode setting
  -c CHART, 	--chart CHART	                        Chart Type
  -l LIGHT, 	--light LIGHT	                        Light Source Type [LD65 / HD65 / CWF / LDP65 / etc.]
  -lx LUX, 	--lux LUX    				Illumination [2000 / 1000 / 100 / 50 / etc.]
  -s SETFILE, 	--setfile SETFILE			App Mode Setting File [setting file (path + filename)]

ex) PhoneControl_android_v2p3.exe -ad -m W-24mm-RAW -l LD65 -lx 2000 -s "C:\# Data\# Repository\PhoneControl\[Setting] Phone_Setting\PhoneSetting_Xperia1III.json"


[ Ver. 2.1 (2022-06-29) ]
usage: PhoneControl_android_v2p1.exe [-h] [-ad] [-d | -i | -w | -p] -m MODE [-c CHART] -l LIGHT -t CTEMP -lx LUX -s SETFILE
                                                                              
Android Camera App Mode Setting                                               

optional arguments:
  -h, 		--help            			show this help message and exit
  -ad, 		--autodetection  			Enable AutoDetection Mode
  -d, 		--logging_debug   			Logging Level set to DEBUG
  -i, 		--logging_info    			Logging Level set to INFO
  -w, 		--logging_warning			Logging Level set to WARNING
  -p, 		--logging_print   			Logging on console
  -m MODE, 	--mode MODE  				Preset name for preview mode setting
  -c CHART, 	--chart CHART				Chart Type
  -l LIGHT, 	--light LIGHT				Light Source Type [LD65 / HD65 / CWF / etc.]
  -t CTEMP, 	--ctemp CTEMP				Color Temperature[6500 / 4000 / 3000 / etc.]
  -lx LUX, 		--lux LUX    			Illumination [2000 / 1000 / 100 / 50 / etc.]
  -s SETFILE, 	--setfile SETFILE			App Mode Setting File [setting file (path + filename)]


[ Ver. 1.2 (2022-05-18) ]
usage: PhoneControl_android_v1p2.exe [-h] [-c CHART] -m MODE -l LIGHT -s SETFILE

Android Camera Control

optional arguments:
  -h, 		--help           			show this help message and exit
  -c CHART, 	--chart CHART				Chart Name
  -m MODE, 	--mode MODE  				App Mode Name
  -l LIGHT, 	--light LIGHT				Light Information (LightType_C.Temp_Lux)
  -s SETFILE, 	--setfile SETFILE			Phone Setting File

[ Ver. 1.1 (2022-05-18) ]
PhoneControl_android_v1p1.exe CHART MODE LIGHT CTEMP LUX SETFILE

Android Camera Control

optional arguments:
  CHART			Chart Type
  MODE			Preset name for preview mode setting
  LIGHT			Light Source Type [LD65 / HD65 / CWF / etc.]
  CTEMP			Color Temperature[6500 / 4000 / 3000 / etc.]
  LUX			Illumination [2000 / 1000 / 100 / 50 / etc.]
  SETFILE		App Mode Setting File [setting file (path + filename)]