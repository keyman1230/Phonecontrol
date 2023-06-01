from ppadb.client import Client as AdbClient
import os
# import sys
import datetime
import time
import logging
import re
import json
import numpy as np
# import pandas as pd
import argparse
import exifread
import inspect
import win32gui
from PIL import Image, ImageGrab


def set_logging_level(logging_lv):
    # import datetime
    # print('[{}] Current Logging Level : ({}) {}'.format(sys._getframe().f_code.co_name, self.logging_level, _log_level_ini))
    if not os.path.exists('./_pylog'):
        os.makedirs('./_pylog')
    _now = datetime.datetime.now()
    _log_file = './_pylog/Log_PhoneControl_android_' + _now.strftime('%Y%m%d') + '.log'

    # 로그 생성 (console)
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(logging_lv)
    # log 출력 형식
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-7s] [%(filename)s (%(lineno)4d)] [%(funcName)20s] %(message)s')
    # log format 설정
    # logger.handlers[0].formatter = formatter

    # log를 파일에 출력
    file_handler = logging.FileHandler(_log_file, 'a', 'utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def arg_parse():
    # 입력받을 인자값 설정
    parser = argparse.ArgumentParser(description='Android Camera App Mode Setting')

    parser.add_argument('-ad', '--autodetection', action='store_true', help='Enable Auto Detection Mode', required=False)
    parser.add_argument('-f', '--jsonformat', action='store_true', help='Make PhoneSetting format json file', required=False)

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-d', '--logging_debug', action='store_true', help='Logging Level set to DEBUG')
    group.add_argument('-i', '--logging_info', action='store_true', help='Logging Level set to INFO')
    group.add_argument('-w', '--logging_warning', action='store_true', help='Logging Level set to WARNING')
    group.add_argument('-p', '--logging_print', action='store_true', help='Logging on console')

    parser.add_argument('-m', '--mode', type=str, help='Preset name for preview mode setting', required=True)
    parser.add_argument('-c', '--chart', type=str, help='Chart Type', required=False)
    parser.add_argument('-l', '--light', type=str, help='Light Source Type [LD65 / HD65 / CWF / LDP65 / etc.]', required=True)
    parser.add_argument('-lx', '--lux', type=str, help='Illumination [2000 / 1000 / 100 / 50 / etc.]', required=True)
    parser.add_argument('-y', '--ypos', type=str, help='CTS Y positioin [9600 / 8600 / 5000 / 1000 / etc.]', required=False)
    parser.add_argument('-s', '--setfile', type=str, help='App Mode Setting File [setting file (path + filename)]', required=True)
    args = parser.parse_args()
    logging.warning('Input Arguments: {}'.format(args))
    return args


def log_info_function():
    # import inspect
    cf = inspect.currentframe()
    line_number = cf.f_back.f_lineno
    func_name = cf.f_back.f_code.co_name
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    file_name = module.__file__
    get_filename = file_name.split('/')[-1]
    return '[{}] [{} ({:>4})] [{:<20}] '.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), get_filename, line_number, func_name)


class androidCapture:
    def __init__(self, args, log):
        self.set_version_no = 2.9
        if args.autodetection:
            logging.warning('-=-=-=-=-=-=-=-=- Phone Control for Android v{} [AutoDetection Mode] -=-=-=-=-=-=-=-=-'.format(self.set_version_no))
        else:
            logging.warning('-=-=-=-=-=-=-=-=- Phone Control for Android v{} [Capture Mode] -=-=-=-=-=-=-=-=-'.format(self.set_version_no))
        self._log_to_file = log
        if self._log_to_file:
            logging.warning('Log is saved to file. (_pylog)')
        else:
            logging.warning('Log is not saved to file. (console print)')
            print(log_info_function() + 'Log is not saved to file. (console print)')

        self.lightLUT = {'LD100': '10000', 'LD65': '6500', 'LD51': '5100',  'LD41': '4100', 'LD32': '3200', 'LD24': '2400',
                         'HD65': '6500', 'H3200': '3200', 'INCA': '2856', 'HOR': '2380',
                         'FD75': '7500', 'FD50': '5000', 'CWF': '4150', 'TL84': '3950',
                         'LDP65': '6500', 'LDP51': '5100', 'LDP40': '4000', 'LDP31': '3100'}

        self.arg_autodetection_mode = args.autodetection
        # self.arg_screencapture_mode = args.screencapture
        self.arg_app_mode = args.mode
        self.arg_chart = args.chart
        self.arg_ypos = args.ypos
        self.arg_light = args.light
        self.arg_color_temperature = self.lightLUT[args.light]
        self.arg_lux = args.lux
        self.phone_setfile = args.setfile
        
        if self._log_to_file:
            logging.debug('arguments >> Enable Auto Detection Mode: [ {} ]'.format(self.arg_autodetection_mode))
            # logging.debug('arguments >> Enable Screen Capture Mode: [ {} ]'.format(self.arg_screencapture_mode))
            logging.debug('arguments >> Selected Camera App Mode: [ {} ]'.format(self.arg_app_mode))
            logging.debug('arguments >> Chart: [ {} ]'.format(self.arg_chart))
            logging.debug('arguments >> Light Source: [ {} ]'.format(self.arg_light))
            logging.debug('arguments >> Color Temperature (K): [ {} ]'.format(self.arg_color_temperature))
            logging.debug('arguments >> Illumination (Lux): [ {} ]'.format(self.arg_lux))
            logging.debug('arguments >> Setting File: [ {} ]'.format(self.phone_setfile))
        else:
            print(log_info_function() + 'arguments >> Enable Auto Detection Mode: [ {} ]'.format(self.arg_autodetection_mode))
            # print(log_info_function() + 'arguments >> Enable Screen Capture Mode: [ {} ]'.format(self.arg_screencapture_mode))
            print(log_info_function() + 'arguments >> Selected Camera App Mode: [ {} ]'.format(self.arg_app_mode))
            print(log_info_function() + 'arguments >> Chart: [ {} ]'.format(self.arg_chart))
            print(log_info_function() + 'arguments >> Light Source: [ {} ]'.format(self.arg_light))
            print(log_info_function() + 'arguments >> Color Temperature (K): [ {} ]'.format(self.arg_color_temperature))
            print(log_info_function() + 'arguments >> Illumination (Lux): [ {} ]'.format(self.arg_lux))
            print(log_info_function() + 'arguments >> Setting File: [ {} ]'.format(self.phone_setfile))

    def read_setting_file(self):
        if os.path.exists(self.phone_setfile):
            if self._log_to_file:
                logging.debug('Phone Setting File: [ {} ]'.format(self.phone_setfile))
            else:
                print(log_info_function() + 'Phone Setting File: [ {} ]'.format(self.phone_setfile))
            try:
                with open(self.phone_setfile, encoding='utf-8') as phoneSetting:
                    _dict_setting = json.load(phoneSetting)
                self.dict_phone_info = _dict_setting['phone_info']
                self.dict_execute_info = _dict_setting['execute_info']
                self.dict_delay_time = _dict_setting['delay_time']
                self.dict_modeset_operation = _dict_setting['modeset_operation']
                self.dict_close_operation = _dict_setting['close_operation']
            except Exception as err_msg:
                logging.error('Error while reading a setting file: [ {} ]'.format(err_msg))
                print(log_info_function() + 'Error while reading a setting file: [ {} ]'.format(err_msg))
                return False

            if self.dict_execute_info['set_version'] == self.set_version_no:
                if self._log_to_file:
                    logging.error('Setting File version: {}'.format(self.dict_execute_info['set_version']))
                else:
                    print(log_info_function() + 'Setting File version: {}'.format(self.dict_execute_info['set_version']))
            else:
                logging.error('Setting File version is different. [PhoneControl version: {}, Setting File version: {}]'.format(self.set_version_no, self.dict_execute_info['set_version']))
                print(log_info_function() + 'Setting File version is different. [PhoneControl version: {}, Setting File version: {}]'.format(self.set_version_no, self.dict_execute_info['set_version']))
                return False

            # Check Chart Type
            if args.chart == None:
                if os.path.exists(self.dict_execute_info['chart_save_file']):
                    f = open(self.dict_execute_info['chart_save_file'], 'r')
                    self.arg_chart = f.readline()
                    f.close()
                    logging.debug('Chart Name >> Chart name from {} : {}'.format(os.path.basename(self.dict_execute_info['chart_save_file']), self.arg_chart))
                else:
                    logging.error('Can\'t find {} file. set chart name to \'XXXXX\''.format(os.path.basename(self.dict_execute_info['chart_save_file'])))
                    self.arg_chart = 'XXXXX'
            if args.ypos == None:
                self.arg_ypos = 0

            if self._log_to_file:
                logging.debug('Phone Info >> Phone name: [ {} ], Maker: [ {} ], temp_batt_limit: [ {} ]'.format(self.dict_phone_info['phone_name'], self.dict_phone_info['maker'], self.dict_phone_info['temp_batt_limit']))
            else:
                print(log_info_function() + 'Phone Info >> Phone name: [ {} ], Maker: [ {} ], temp_batt_limit: [ {} ]'.format(self.dict_phone_info['phone_name'], self.dict_phone_info['maker'], self.dict_phone_info['temp_batt_limit']))

            # Check Light Cal Data Location
            if self.arg_autodetection_mode:
                if self._log_to_file:
                    logging.debug('This Scenario mode is [ AutoDetection ]. Do not need light calibration data.')
                else:
                    print(log_info_function() + 'This Scenario mode is [ AutoDetection ]. Do not need light calibration data.')
            else:
                if not os.path.exists(self.dict_execute_info['light_cal_data_dir']):
                    logging.error('Can not find arg_light cal data folder: [ {} ]'.format(self.dict_execute_info['light_cal_data_dir']))
                    print(log_info_function() + 'Can not find arg_light cal data folder: [ {} ]'.format(self.dict_execute_info['light_cal_data_dir']))
                    return False
                else:
                    if self._log_to_file:
                        logging.debug('Folder >> Light Cal. Data Location: [ {} ]'.format(self.dict_execute_info['light_cal_data_dir']))
                    else:
                        print(log_info_function() + 'Folder >> Light Cal. Data Location: [ {} ]'.format(self.dict_execute_info['light_cal_data_dir']))

            # Make Result Save Folder
            self.image_save_dir = self.dict_execute_info['result_save_dir'] + '_' + self.dict_phone_info['phone_name']
            if not os.path.exists(self.image_save_dir):
                os.makedirs(self.image_save_dir)
            if self._log_to_file:
                logging.debug('Folder >> Image Save: [ {} ]'.format(self.image_save_dir))
            else:
                print(log_info_function() + 'Folder >> Image Save: [ {} ]'.format(self.image_save_dir))
            return True
        else:
            logging.warning('Can not find setting file: {}'.format(self.phone_setfile))
            print(log_info_function() + 'Can not find setting file: {}'.format(self.phone_setfile))
            return False

    def check_device(self):
        try:
            # adb root
            os.system('adb start-server')
            # device 지정
            client = AdbClient(host='127.0.0.1', port=5037)
            devices = client.devices()
            if len(devices) < 1:
                logging.error('Can not find device.')
                print(log_info_function() + 'Can not find device.')
                return False
            else:
                for cnt_device, idx_device in enumerate(devices):
                    if self._log_to_file:
                        logging.debug('Detected Device ({}/{}) >>> Model: {}, Serial: {}'.format(cnt_device+1, len(devices), idx_device.shell('getprop ro.product.model').replace('\n', ''), idx_device.serial))
                    else:
                        print(log_info_function() + 'Detected Device ({}/{}) >>> Model: {}, Serial: {}'.format(cnt_device+1, len(devices), idx_device.shell('getprop ro.product.model').replace('\n', ''), idx_device.serial))
                self.device = devices[0]
                return True
        except Exception as err:
            logging.error('Can not find device. Error: [{}]'.format(err))
            print(log_info_function() + 'Can not find device. Error: [{}]'.format(err))
            return False

    def load_caldata(self):
        ## Load cal_data 가져오기
        # 광원_설정색온도_설정조도_측정색온도_측정조도
        # LD65_6500_2000_6500_2000
        if self.arg_autodetection_mode:
            if self._log_to_file:
                logging.debug('This Scenario mode is [ AutoDetection ]. Do not need light calibration data.')
            else:
                print(log_info_function() + 'This Scenario mode is [ AutoDetection ]. Do not need light calibration data.')
        else:
            if 'ldp' in self.arg_light.lower():
                self.light_info = "_".join([self.arg_light, self.arg_color_temperature, self.arg_lux, self.arg_color_temperature, self.arg_lux])
                if self._log_to_file:
                    logging.debug('Light Information (Uniformity): {}'.format(self.light_info))
                else:
                    print(log_info_function() + 'Light Information (Uniformity): {}'.format(self.light_info))
            else:
                cal_file = "_".join([self.arg_light.lower(), self.arg_color_temperature, self.arg_lux]) + ".csv"
                if os.path.exists(os.path.join(self.dict_execute_info['light_cal_data_dir'], cal_file)):
                    if self._log_to_file:
                        logging.debug('Find light cal data file: {}'.format(cal_file))
                    else:
                        print(log_info_function() + 'Find light cal data file: {}'.format(cal_file))
                    cal_data = open(os.path.join(self.dict_execute_info['light_cal_data_dir'], cal_file), 'r', encoding='utf-8').readline().split(",")
                    
                    if self.arg_light.lower() == 'hd65':    # Halogen
                        try:
                            measurement_lux = str(round(np.mean((list(map(float, cal_data[13:22]))))))
                            measurement_color_temperature = cal_data[22]
                        except Exception as err:
                            logging.error('Trouble while reading {} light cal data file: {} >> Error msg:[{}]'.format(self.arg_light, cal_file, err))
                            print(log_info_function() + 'Trouble while reading {} light cal data file: {} >> Error msg:[{}]'.format(self.arg_light, cal_file, err))
                            return False
                    else:   # LED / Fluorescent
                        try:
                            measurement_lux = str(round(np.mean((list(map(float, cal_data[9:18]))))))
                            measurement_color_temperature = cal_data[18]
                        except Exception as err:
                            logging.error('Trouble while reading {} light cal data file: {} >> Error msg:[{}]'.format(self.arg_light, cal_file, err))
                            print(log_info_function() + 'Trouble while reading {} light cal data file: {} >> Error msg:[{}]'.format(self.arg_light, cal_file, err))
                            return False
                    
                else:   # Can't find light cal data file
                    if self._log_to_file:
                        logging.warning('Can\'t find light cal data file: {}   >>> measured data set to \'XXXX\''.format(cal_file))
                    else:
                        print(log_info_function() + 'Can\'t find light cal data file: {}   >>> measured data set to \'XXXX\''.format(cal_file))
                    measurement_lux = 'XXXX'
                    measurement_color_temperature = 'XXXX'
                self.light_info = "_".join([self.arg_light, self.arg_color_temperature, self.arg_lux, measurement_color_temperature, measurement_lux])
            if self._log_to_file:
                logging.debug('Light Information: {}'.format(self.light_info))
            else:
                print(log_info_function() + 'Light Information: {}'.format(self.light_info))
        return True
    
    def check_batt_level(self):
        level_batt = 0
        # while check_batt:
        while True:
            for line in self.device.shell('dumpsys battery').split('\n'):
                if 'level' in line:
                    level_batt = int(re.findall("\d+", line)[0])

            if level_batt > self.dict_phone_info['level_batt_limit']:
                if self._log_to_file:
                    logging.warning('Current Battery Level is higher than limit level. (Current level.: {}, Limit level.: {}) !!'.format(level_batt, self.dict_phone_info['level_batt_limit']))
                else:
                    print(log_info_function() + 'Current Battery Level is higher than limit level. (Current level.: {}, Limit level.: {}) !!'.format(level_batt, self.dict_phone_info['level_batt_limit']))
                break
            else:
                self.device.shell('input keyevent KEYCODE_WAKEUP')
                time.sleep(0.3)
                self.device.shell('input keyevent KEYCODE_POWER')
                if self._log_to_file:
                    logging.warning('{} Battery level is low. (Current level: {}, Limit level.: {}) !! Wait {} secs!!'.format(self.dict_phone_info['phone_name'], level_batt, self.dict_phone_info['level_batt_limit'], self.dict_execute_info['level_recheck_period']))
                else:
                    print(log_info_function() + '{} Battery level is low. (Current level: {}, Limit level.: {}) !! Wait {} secs!!'.format(self.dict_phone_info['phone_name'], level_batt, self.dict_phone_info['level_batt_limit'], self.dict_execute_info['level_recheck_period']))
                time.sleep(self.dict_execute_info['level_recheck_period'])
                continue
                
    def check_batt_temp(self):
        # Check Temp. of Battery
        if self.arg_autodetection_mode:
            if self._log_to_file:
                logging.debug('This Scenario mode is [ AutoDetection ]. Do not need a temperature check.')
            else:
                print(log_info_function() + 'This Scenario mode is [ AutoDetection ]. Do not need a temperature check.')
        else:
            # check_batt = int(self.dict_execute_info['temp_check'])
            temp_batt = 0
            # while check_batt:
            while self.dict_execute_info['temp_check']:
                for line in self.device.shell('dumpsys battery').split('\n'):
                    if 'temperature' in line:
                        temp_batt = int(re.findall("\d+", line)[0])
                    elif 'level' in line:
                        level_batt = int(re.findall("\d+", line)[0])

                if temp_batt <= self.dict_phone_info['temp_batt_limit']:
                    if self._log_to_file:
                        logging.warning('Current temperature is lower than limit temperature. (Current temp.: {}, Limit temp.: {}) !!'.format(temp_batt, self.dict_phone_info['temp_batt_limit']))
                    else:
                        print(log_info_function() + 'Current temperature is lower than limit temperature. (Current temp.: {}, Limit temp.: {}) !!'.format(temp_batt, self.dict_phone_info['temp_batt_limit']))
                    break
                else:
                    self.device.shell('input keyevent KEYCODE_WAKEUP')
                    time.sleep(0.3)
                    self.device.shell('input keyevent KEYCODE_POWER')
                    if self._log_to_file:
                        logging.warning('{} Battery is hot (Current temp.: {}, Limit temp.: {}) !! Wait {} secs!!'.format(self.dict_phone_info['phone_name'], temp_batt, self.dict_phone_info['temp_batt_limit'], self.dict_execute_info['temp_recheck_period']))
                    else:
                        print(log_info_function() + '{} Battery is hot (Current temp.: {}, Limit temp.: {}) !! Wait {} secs!!'.format(self.dict_phone_info['phone_name'], temp_batt, self.dict_phone_info['temp_batt_limit'], self.dict_execute_info['temp_recheck_period']))
                    time.sleep(self.dict_execute_info['temp_recheck_period'])
                    continue

    def camera_preview(self):
        self.check_batt_level()
        if self._log_to_file:
            logging.warning('Start Camera Preview Setting: [{}]'.format(self.arg_app_mode))
        else:
            print(log_info_function() + 'Start Camera Preview Setting: [{}]'.format(self.arg_app_mode))
        # POWER ON & 잠금해제
        self.device.shell('input keyevent KEYCODE_WAKEUP')
        time.sleep(0.3)
        self.device.shell('input swipe 582 1900 582 100 1000')
        # self.device.shell('input keyevent KEYCODE_MENU')
        time.sleep(1)
        ############################################### 수정 필요함
        # CAMERA ON
        # try:
        #     if self.dict_modeset_operation[self.arg_app_mode]['cam_app']['name'].lower() == 'default':
        #         self.device.shell('am start -a android.media.action.STILL_IMAGE_CAMERA')
        #     else:
        #         self.device.shell('am start -n {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['name']))
        #     time.sleep(2)
        # except Exception as err_msg:
        #     if self._log_to_file:
        #         logging.error('Trouble while executing Camera App. >> Error msg:[{}]'.format(err_msg))
        #     else:
        #         print(log_info_function() + 'Trouble while executing Camera App. >> Error msg:[{}]'.format(err_msg))
        #     return False

        # Set Camera mode : modeset_operation
        if self.arg_app_mode in list(self.dict_modeset_operation.keys()):
            if self._log_to_file:
                logging.debug('Found the [{}] in modeset_operation'.format(self.arg_app_mode))
            else:
                print(log_info_function() + 'Found the [{}] in modeset_operation'.format(self.arg_app_mode))
            time.sleep(0.5)
            for order in list(self.dict_modeset_operation[self.arg_app_mode]['setting'].keys()):
                cmd = self.dict_modeset_operation[self.arg_app_mode]['setting'][order]
                if self._log_to_file:
                    logging.debug('adb command >> adb shell input {}'.format(cmd))
                else:
                    print(log_info_function() + 'adb command >> adb shell input {}'.format(cmd))
                self.device.shell('input {}'.format(cmd))
                time.sleep(self.dict_execute_info['modeset_operation_period'])
            if self._log_to_file:
                logging.debug('Finish Camera Preview Setting.: [{}]'.format(self.arg_app_mode))
            else:
                print(log_info_function() + 'Finish Camera Preview Setting.: [{}]'.format(self.arg_app_mode))
            return True
        else:
            if self._log_to_file:
                logging.error('Could not find the [{}] in modeset_operation'.format(self.arg_app_mode))
            else:
                print(log_info_function() + 'Could not find the [{}] in modeset_operation'.format(self.arg_app_mode))
            # KEYCODE_BACK
            for rep_cnt in range(3):
                self.device.shell('input keyevent KEYCODE_BACK')
                time.sleep(0.5)
                ########################################################################## 수정 필요함
            # # KEYCODE_HOME
            # self.device.shell('input keyevent KEYCODE_HOME')
            # # KEYCODE_POWER
            # self.device.shell('input keyevent KEYCODE_POWER')
            if self._log_to_file:
                logging.debug('Screen Off !!')
            else:
                print(log_info_function() + 'Screen Off !!')
            return False

    def read_exif(self, filename):
        f = open(filename, 'rb')  # Open image file for reading (binary mode)
        tags = exifread.process_file(f)  # Return Exif tags
        f.close()
        if len(tags) != 0:
            if not os.path.exists('_'.join(filename.split('_')[0:7])+'.csv'):
                f_image = open('_'.join(filename.split('_')[0:7]) + '.csv', 'a')
                _write_header = ','.join(['Capture Time', 'Filename', 'DateTime', 'Maker', 'Model', 'Width', 'Height', 'ExposureTime', 'F Number', 'ISO Speed', 'Focal Length', '\n'])
                f_image.write(_write_header)
                f_image.close()

            list_exif = ['DateTimeOriginal', 'Make', 'Model', 'ImageWidth', 'ImageLength', 'ExposureTime', 'FNumber', 'ISOSpeedRatings', 'FocalLength']
            exif_value = [self.capTime, os.path.basename(filename)]
            for idx_item in list_exif:
                _tmp_value = ''
                for idx_exif in tags:
                    if idx_item in idx_exif:
                        if idx_item in ['DateTimeOriginal', 'Make', 'Model']:
                            _tmp_value = str(tags[idx_exif])
                            break
                        else:
                            _tmp_value = str(eval(str(tags[idx_exif])))
                            break
                exif_value.append(_tmp_value)

            _write_str = ','.join(exif_value + ['\n'])
            f_image = open('_'.join(filename.split('_')[0:7]) + '.csv', 'a')
            f_image.write(_write_str)
            f_image.close()
            if self._log_to_file:
                logging.debug('Exif Information: [{}]'.format(_write_str[:-2]))
            else:
                print(log_info_function() + 'Exif Information: [{}]'.format(_write_str[:-2]))
        else:
            if self._log_to_file:
                logging.debug('Exif Data is empty. : {}'.format(os.path.basename(filename)))
            else:
                print(log_info_function() + 'Exif Data is empty. : {}'.format(os.path.basename(filename)))
        return tags

    def _pull_image(self):
        # Save File (adb pull)
        saved_filename = '_'.join([self.arg_chart, self.light_info, '-'.join([self.dict_phone_info['phone_name'], self.arg_app_mode]), self.arg_ypos])
        filelist_raw_dir = sorted(re.split('[\n ]', self.device.shell('ls \"{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir']))), reverse=True)
        filelist_raw = [idx_file for idx_file in filelist_raw_dir if idx_file.lower().endswith('.dng')]
        filelist_jpg_dir = sorted(re.split('[\n ]', self.device.shell('ls \"{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir']))), reverse=True)
        filelist_jpg = [idx_file for idx_file in filelist_jpg_dir if idx_file.lower().endswith('.jpg')]


        raw, jpg = False, False

        if (len(filelist_raw) > self.num_of_raw_before_capture):
            filename_raw = '{}{}{}_{}'.format(self.image_save_dir, os.sep, saved_filename, filelist_raw[0].replace('_', '-'))
            if self._log_to_file:
                logging.debug('adb command>> adb pull {}/{} {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir'], filelist_raw[0], filename_raw))
            else:
                print(log_info_function() + 'adb command>> adb pull {}/{} {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir'], filelist_raw[0], filename_raw))
            self.device.pull(r'{}/{}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir'], filelist_raw[0]), filename_raw)
            # os.system('adb pull \"{}/{}\" \"{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir'], filelist_raw[0], filename_raw))
            time.sleep(0.5)

            if self.dict_execute_info['delete_images_after_pull']:
                time.sleep(0.5)
                self.device.shell('rm -rf \"{}/{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir'], filelist_raw[0]))
            self.read_exif(filename=filename_raw)
            raw = True

        if (len(filelist_jpg) > self.num_of_jpg_before_capture):
            filename_jpg = '{}{}{}_{}'.format(self.image_save_dir, os.sep, saved_filename, filelist_jpg[0].replace('_', '-'))
            if self._log_to_file:
                logging.debug('adb command>> adb pull {}/{} {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir'], filelist_jpg[0], filename_jpg))
            else:
                print(log_info_function() + 'adb command>> adb pull {}/{} {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir'], filelist_jpg[0], filename_jpg))
            self.device.pull(r'{}/{}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir'], filelist_jpg[0]), filename_jpg)
            # os.system('adb pull \"{}/{}\" \"{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir'], filelist_jpg[0], filename_jpg))
            time.sleep(0.5)

            if self.dict_execute_info['delete_images_after_pull']:
                time.sleep(0.5)
                self.device.shell('rm -rf \"{}/{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir'], filelist_jpg[0]))
            self.read_exif(filename=filename_jpg)
            jpg = True

        if (raw == True or jpg == True):
            return True

        else:
            if self._log_to_file:
                logging.info('Can\'t find .dng or .jpg image in phone. [{}] [.dng :( {} >> {} ), .jpg: ( {} >> {} )]'.format(saved_filename, self.num_of_raw_before_capture, len(filelist_raw), self.num_of_jpg_before_capture, len(filelist_jpg)))
            else:
                print(log_info_function() + 'Can\'t find .dng or .jpg image in phone. [{}] [.dng :( {} >> {} ), .jpg: ( {} >> {} )]'.format(saved_filename, self.num_of_raw_before_capture, len(filelist_raw), self.num_of_jpg_before_capture, len(filelist_jpg)))
            time.sleep(1)
            return False



    def _record_capture_time(self, captureTime, tryCount):
        _now = datetime.datetime.now()
        self.result_save_dir = self.dict_execute_info['result_save_dir'] + '_' + self.dict_phone_info['phone_name']
        if not os.path.exists(self.result_save_dir):
            os.makedirs(self.result_save_dir)
        if self._log_to_file:
            logging.debug('Folder >> Capture Record Save: [ {} ]'.format(self.result_save_dir))
        else:
            print(log_info_function() + 'Folder >> Capture Record Save: [ {} ]'.format(self.result_save_dir))

        result_filename = os.path.join(self.result_save_dir, 'Capture_Record_{}.csv'.format(_now.strftime('%Y%m%d')))
        if not os.path.exists(result_filename):
            f_image = open(result_filename, 'a')
            _write_header = ','.join(['DateTime', 'Model', 'Chart', 'Light', 'C.Temp', 'Lux', 'Try Count.', 'Image Filename', '\n'])
            f_image.write(_write_header)
            f_image.close()
        _image_filename = '_'.join([self.arg_chart, self.light_info, '-'.join([self.dict_phone_info['phone_name'], self.arg_app_mode])])
        _write_str = ','.join([captureTime,
                               self.dict_phone_info['phone_name'],
                               self.arg_chart,
                               self.arg_light,
                               self.arg_color_temperature,
                               self.arg_lux,
                               str(tryCount),
                               _image_filename
                               ] + ['\n'])
        f_image = open(result_filename, 'a')
        f_image.write(_write_str)
        f_image.close()
        if self._log_to_file:
            logging.debug('Record of Capture : [{}]'.format(_write_str[:-2]))
        else:
            print(log_info_function() + 'Record of Capture: [{}]'.format(_write_str[:-2]))

    def capture_and_pull(self):
        for rep in range(int(self.dict_execute_info['repeat_capture'])):
            self.capTime = ''
            if self._log_to_file:
                logging.warning('<<<<< Check Phone Temperature !! >>>>>')
            else:
                print(log_info_function() + '<<<<< Check Phone Temperature !! >>>>>')
            self.check_batt_temp()

            if self._log_to_file:
                logging.warning('<<<<< Start Capture [ Try No.{} ] !! >>>>>'.format(rep + 1))
            else:
                print(log_info_function() + '<<<<< Start Capture [ Try No.{} ] !! >>>>>'.format(rep + 1))
            self.num_of_raw_before_capture = len([idx_file for idx_file in sorted(re.split('[\n ]', self.device.shell('ls \"{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['raw_dir']))), reverse=True) if idx_file.lower().endswith('.dng')])
            self.num_of_jpg_before_capture = len([idx_file for idx_file in sorted(re.split('[\n ]', self.device.shell('ls \"{}\"'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['jpg_dir']))), reverse=True) if idx_file.lower().endswith('.jpg')])

            # Preview & Mode setting
            if not self.camera_preview():

                return False
            else:  # Capture Sequence
                # SLEEP
                time.sleep(3)

                # Touch AF point
                self.device.shell('input tap {} {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['af_touch_x_position'], self.dict_modeset_operation[self.arg_app_mode]['cam_app']['af_touch_y_position']))
                if self._log_to_file:
                    logging.debug('Touch AF >> x: {}, y: {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['af_touch_x_position'], self.dict_modeset_operation[self.arg_app_mode]['cam_app']['af_touch_y_position']))
                else:
                    print(log_info_function() + 'Touch AF >> x: {}, y: {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['af_touch_x_position'], self.dict_modeset_operation[self.arg_app_mode]['cam_app']['af_touch_y_position']))

                # Delay time after touch AF
                if int(self.arg_lux) > 20:
                    if self._log_to_file:
                        logging.debug('Delay time over 20 lux after touch AF ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_AF_over_20lux']))
                    else:
                        print(log_info_function() + 'Delay time over 20 lux after touch AF ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_AF_over_20lux']))
                    time.sleep(self.dict_delay_time['delay_after_AF_over_20lux'])
                else:
                    if self._log_to_file:
                        logging.debug('Delay time under 20 lux after touch AF ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_AF_under_20lux']))
                    else:
                        print(log_info_function() + 'Delay time under 20 lux after touch AF ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_AF_under_20lux']))
                    time.sleep(self.dict_delay_time['delay_after_AF_under_20lux'])

                # Capture
                try:
                    if self.dict_modeset_operation[self.arg_app_mode]['cam_app']['capture'].lower() == 'default':
                        if self._log_to_file:
                            time.sleep(5)
                            logging.debug('Capture using KEYCODE_CAMERA')
                        else:
                            print(log_info_function() + 'Capture using KEYCODE_CAMERA')
                        time.sleep(5)
                        self.device.shell('input keyevent KEYCODE_CAMERA')
                    else:
                        if self._log_to_file:
                            logging.debug('Capture using Touch (adb shell input {})'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['capture']))
                        else:
                            print(log_info_function() + 'Capture using Touch (adb shell input {})'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['capture']))
                        self.device.shell('input {}'.format(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['capture']))
                    self.capTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    self._record_capture_time(captureTime=self.capTime, tryCount=rep+1)
                except Exception as err_msg:
                    if self._log_to_file:
                        logging.error('Trouble while capture image. >> Error msg:[{}]'.format(err_msg))
                    else:
                        print(log_info_function() + 'Trouble while capture image. >> Error msg:[{}]'.format(err_msg))
                    return False

                # Delay time after Capture
                if int(self.arg_lux) > 100:
                    if self._log_to_file:
                        logging.debug('Delay time over 100 lux after capture ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_capture_over_100lux']))
                    else:
                        print(log_info_function() + 'Delay time over 100 lux after capture ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_capture_over_100lux']))
                    time.sleep(self.dict_delay_time['delay_after_capture_over_100lux'])
                else:
                    if self._log_to_file:
                        logging.debug('Delay time under 100 lux after capture ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_capture_under_100lux']))
                    else:
                        print(log_info_function() + 'Delay time under 100 lux after capture ({} lux): {}s'.format(self.arg_lux, self.dict_delay_time['delay_after_capture_under_100lux']))
                    time.sleep(self.dict_delay_time['delay_after_capture_under_100lux'])
                if 'hires' in self.arg_app_mode.lower():
                    if self._log_to_file:
                        logging.debug('Additional Delay after capture in High Resolution Mode [{}]: {}s'.format(self.arg_app_mode, self.dict_delay_time['additional_delay_after_capture_HiRes']))
                    else:
                        print(log_info_function() + 'Additional Delay after capture in High Resolution Mode [{}]: {}s'.format(self.arg_app_mode, self.dict_delay_time['additional_delay_after_capture_HiRes']))
                    time.sleep(self.dict_delay_time['additional_delay_after_capture_HiRes'])

                if 'raw' in self.arg_app_mode.lower():
                    if self._log_to_file:
                        logging.debug('Additional Delay after capture in RAW Mode [{}]: {}s'.format(self.arg_app_mode, self.dict_delay_time['additional_delay_after_capture_RAW']))
                    else:
                        print(log_info_function() + 'Additional Delay after capture in RAW Mode [{}]: {}s'.format(self.arg_app_mode, self.dict_delay_time['additional_delay_after_capture_RAW']))
                    time.sleep(self.dict_delay_time['additional_delay_after_capture_RAW'])

                if 'additional_delay_after_capture' in self.dict_modeset_operation[self.arg_app_mode]['cam_app'].keys():
                    if self._log_to_file:
                        logging.debug('Additional Delay after capture. [{}]: {}s'.format(self.arg_app_mode, self.dict_modeset_operation[self.arg_app_mode]['cam_app']['additional_delay_after_capture']))
                    else:
                        print(log_info_function() + 'Additional Delay after capture. [{}]: {}s'.format(self.arg_app_mode, self.dict_modeset_operation[self.arg_app_mode]['cam_app']['additional_delay_after_capture']))
                    time.sleep(self.dict_modeset_operation[self.arg_app_mode]['cam_app']['additional_delay_after_capture'])

                # # KEYCODE_BACK
                # for rep_cnt in range(3):
                #     self.device.shell('input keyevent KEYCODE_BACK')
                #     time.sleep(0.5)

                # Execute Close Operation
                for order in list(self.dict_close_operation.keys()):
                    cmd = self.dict_close_operation[order]
                    if self._log_to_file:
                        logging.debug('adb command >> adb shell input {}'.format(cmd))
                    else:
                        print(log_info_function() + 'adb command >> adb shell input {}'.format(cmd))
                    self.device.shell('input {}'.format(cmd))
                    time.sleep(self.dict_execute_info['close_operation_period'])
                if self._log_to_file:
                    logging.debug('Finish to Close Camera App.')
                else:
                    print(log_info_function() + 'Finish to Close Camera App.')

                # pull Image from phone (adb pull)
                if self._pull_image():
                    if self._log_to_file:
                        logging.warning('Success to pull images. [Try No. {} / {}]'.format(rep+1, self.dict_execute_info['repeat_capture']))
                    else:
                        print(log_info_function() + 'Success to pull images. [Try No. {} / {}]'.format(rep+1, self.dict_execute_info['repeat_capture']))
                else:
                    if self._log_to_file:
                        logging.warning('Fail to pull images. [Try No. {} / {}]'.format(rep+1, self.dict_execute_info['repeat_capture']))
                    else:
                        print(log_info_function() + 'Fail to pull images. [Try No. {} / {}]'.format(rep+1, self.dict_execute_info['repeat_capture']))

                # SLEEP 1 sec
                time.sleep(1)
            
        # # KEYCODE_BACK
        # for rep_cnt in range(3):
        #     self.device.shell('input keyevent KEYCODE_BACK')
        #     time.sleep(0.5)

        #################################################################################### 수정 필요함
        # # KEYCODE_HOME
        # self.device.shell('input keyevent KEYCODE_HOME')
        # # KEYCODE_POWER
        # self.device.shell('input keyevent KEYCODE_POWER')
        if self._log_to_file:
            logging.info('Finish to Capture Image - Screen Off !!')
        else:
            print(log_info_function() + 'Finish to Capture Image - Screen Off !!')
        return True

    def make_PhoneSetting_json(self):
        # Variables
        phone_info = {'phone_name': 'PhoneName',
                      'maker': 'Maker',
                      'temp_batt_limit': 350,
                      'level_batt_limit': 50
                      }
        
        execute_info = {'set_version': self.set_version_no,
                        'repeat_capture': 3,
                        'chart_save_file': '..\\Result\\chart.txt',
                        'result_save_dir': '..\\Result\\20220726',
                        'light_cal_data_dir': '..\\[Data] Light_Cal_Data',
                        'temp_check': True,
                        'temp_recheck_period': 30,
                        'level_recheck_period': 300,
                        'modeset_operation_period': 1,
                        'close_operation_period': 1,
                        'delete_images_after_pull': True
                        }
        
        delay_time = {'delay_after_capture_over_100lux': 2.5,
                      'delay_after_capture_under_100lux': 4,
                      'additional_delay_after_capture_HiRes': 2,
                      'additional_delay_after_capture_RAW': 0,
                      'delay_after_AF_over_20lux': 1.5,
                      'delay_after_AF_under_20lux': 3
                      }
    
        modeset_operation = {'W-24mm-RAW': {'cam_app': {'name': 'default',
                                                        'capture': 'default',
                                                        'jpg_dir': '/sdcard/DCIM/PHOTOGRAPHY_PRO',
                                                        'raw_dir': '/sdcard/DCIM/PHOTOGRAPHY_PRO',
                                                        'af_touch_x_position': 585,
                                                        'af_touch_y_position': 865
                                                        },
                                            'setting': {'Mode1': 'tap 1000 100',
                                                        'Mode2': 'swipe 1000 100 100 100 800',
                                                        'Mode3': 'tap 240 270',
                                                        'Mode4': 'tap 585 865',
                                                        'cam1': 'tap 290 100',
                                                        'cam2': 'tap 580 100',
                                                        'cam3': 'tap 585 865',
                                                        'AF1': 'tap 385 1800',
                                                        'AF2': 'tap 830 1720',
                                                        'RAW1': 'tap 230 2134',
                                                        'RAW2': 'tap 830 2055'
                                                        }
                                            },
                             'T-70mm-RAW': {'cam_app': {'name': 'default',
                                                        'capture': 'default',
                                                        'jpg_dir': '/sdcard/DCIM/PHOTOGRAPHY_PRO',
                                                        'raw_dir': '/sdcard/DCIM/PHOTOGRAPHY_PRO',
                                                        'af_touch_x_position': 585,
                                                        'af_touch_y_position': 865
                                                        },
                                            'setting': {'Mode1': 'tap 1000 100',
                                                        'Mode2': 'swipe 1000 100 100 100 800',
                                                        'Mode3': 'tap 240 270',
                                                        'Mode4': 'tap 585 865',
                                                        'cam1': 'tap 290 100',
                                                        'cam2': 'tap 410 100',
                                                        'cam3': 'tap 585 865',
                                                        'AF1': 'tap 385 1800',
                                                        'AF2': 'tap 830 1720',
                                                        'RAW1': 'tap 230 2134',
                                                        'RAW2': 'tap 830 2055'
                                                        }
                                            }
                             }
    
        close_operation = {'Menu_Display1': 'swipe 700 2558 700 2400 300',
                           'multiwindow1': 'tap 870 2500',
                           'killwindow1': 'tap 950 2300'}
    
        dict_setting = {'phone_info': phone_info,
                        'execute_info': execute_info,
                        'delay_time': delay_time,
                        'modeset_operation': modeset_operation,
                        'close_operation': close_operation
                        }
        setting_folder = r'./[Setting] Phone_Setting'
        if not os.path.exists(setting_folder):
            os.makedirs(setting_folder)
        filename_setting = os.path.join(setting_folder, 'PhoneSetting_{}_{}.json'.format(phone_info['phone_name'],'v' + str(self.set_version_no).replace('.', 'p')))
        # Write json file
        with open(filename_setting, 'w') as setting_json:
            json.dump(dict_setting, setting_json, indent='\t')
    
        # Verify
        with open(filename_setting) as json_read:
            read_setting = json.load(json_read)
    
        if read_setting == dict_setting:
            print('Setting File is OK.: [{}]'.format(filename_setting))

if __name__ == "__main__":
    args = arg_parse()

    if args.logging_print:
        _log = False
        _logging_level = 'WARNING'
    elif args.logging_debug:
        _log = True
        _logging_level = 'DEBUG'
    elif args.logging_info:
        _log = True
        _logging_level = 'INFO'
    elif args.logging_warning:
        _log = True
        _logging_level = 'WARNING'
    else:
        _log = False
        _logging_level = 'WARNING'

    logging_level_list = {'NOTSET': logging.NOTSET,
                          'DEBUG': logging.DEBUG,
                          'INFO': logging.INFO,
                          'WARNING': logging.WARNING,
                          'ERROR': logging.ERROR,
                          'CRITICAL': logging.CRITICAL}
    set_logging_level(logging_lv=logging_level_list.get(_logging_level))
    logging.warning('Logging Level: {} ({})'.format(_logging_level, logging.root.level))
    
    PC = androidCapture(args=args, log=_log)
    
    if not args.jsonformat:
        logging.warning('---------- Start of Execution !! ----------')
        ts_start = datetime.datetime.now()          # Time Stamp
        
        ret = PC.read_setting_file()
        logging.warning('##### Result of read_setting_file: {} [{}]'.format(ret, args.setfile))
        ts_read_setting_file = datetime.datetime.now()  # Time Stamp
        
        if ret:
            ret = PC.check_device()
        logging.warning('##### Result of check_device: {}'.format(ret))
        ts_check_device = datetime.datetime.now()  # Time Stamp
        
        if ret:
            ret = PC.load_caldata()
        logging.warning('##### Result of Load_calData: {}'.format(ret))
        ts_load_caldata = datetime.datetime.now()  # Time Stamp
    
        if ret:
            if args.autodetection:
                ret = PC.camera_preview()
                # if args.screencapture:
                #     # os.system('scrcpy -m 1080 --window-title=ForCapture')
                #     # time.sleep(5)
                #     hWnd = win32gui.FindWindow(None, 'ForCapture')
                #     windowcor = win32gui.GetWindowRect(hWnd)
                #     # im = ImageGrab.grab()     # 전체화면 캡쳐
                #     im = ImageGrab.grab(windowcor)  # 창 캡쳐
                #     im.save('_'.join([PC.dict_phone_info['phone_name'], str(args.mode)]) + '.png')
            else:
                ret = PC.capture_and_pull()
        logging.warning('##### Result of Preview and Capture: {}'.format(ret))
        ts_end = datetime.datetime.now()  # Time Stamp
    
        logging.debug('--------------------------------------------------------------------')
        logging.debug('{:38s} : {}'.format('##### Execute Python Script', ts_start))
        logging.debug('--------------------------------------------------------------------')
        logging.debug('{:38s} : {}'.format('** Read Setting File', ts_read_setting_file - ts_start))
        logging.debug('{:38s} : {}'.format('** Check Device Connection', ts_check_device - ts_read_setting_file))
        logging.debug('{:38s} : {}'.format('** Load Light Cal. Data', ts_load_caldata - ts_check_device))
        logging.debug('{:38s} : {}'.format('** Capture & Pull Image ({} time(s))'.format(PC.dict_execute_info['repeat_capture']), ts_end - ts_load_caldata))
        logging.warning('--------------------------------------------------------------------')
        logging.warning('{:38s} : {}'.format('##### Total Processing Time', ts_end - ts_start))
        logging.warning('--------------------------------------------------------------------')
    
        logging.warning('End of Execution !!\n')
    else:
        PC.make_PhoneSetting_json()
        print('Complete to make PhoneSetting json file.')

