import os
import sys
import time
import datetime
import logging
from tqdm import tqdm
import exifread
import imghdr
import configparser
import tkinter
from tkinter import filedialog



def select_file(init_dir='./', file_type=(("All files", "*.*"),)):
    '''
    .. Note:: 1개의 파일 선택
    :return: filename (str) : 선택된 Filename (경로 포함)
    '''
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    filename = os.path.abspath(filedialog.askopenfilename(parent=tk_root,
                                                          initialdir=init_dir,
                                                          title='Please select a file',
                                                          filetypes=file_type))
    # print("Selected file: {}".format(filename))
    logging.info('Selected file: {}'.format(filename))
    return filename


def select_folder_location(init_dir='./'):
    '''
    .. Note:: Select folder location
    :param init_dir: Initial Directory (default = './')
    :return:
      selected_dir (str) : Selected folder location
    '''
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    selected_dir = os.path.abspath(filedialog.askdirectory(parent=tk_root,
                                                           initialdir=init_dir,
                                                           title='Please select a directory'))
    # print('Selected folder: {}'.format(select_dir))
    logging.info('Selected folder: {}'.format(selected_dir))
    return selected_dir


def make_filelist(target_dir, subdir=False, list_filetype=None):
    """
    .. Note:: 선택된 폴더와 하위 폴더까지의 파일 리스트와 폴더 리스트를 Return 하는 함수
    :param target_dir: 리스트로 작성하고자 하는 root 폴더
    :param subdir: 하위 디렉토리 검색 여부 (Default : False)
    :param list_filetype: 리스트로 작성할 파일의 확장자 ex. ['.csv', '.json'] (Default : None)
    :return:
        file_list - 파일 리스트 (list) (경로명 포함)
    """
    _filelist_all = []
    file_list = []

    if subdir:
        for path, direct, files in os.walk(target_dir):
            # file_path = [os.path.join(path, file) for file in files]
            file_path = [os.path.abspath(os.path.join(path, file)) for file in files]
            # print(file_path)
            _filelist_all.extend(file_path)
    else:
        _filelist_all = [os.path.join(os.path.abspath(target_dir), file) for file in os.listdir(target_dir) if
                         os.path.isfile(os.path.join(os.path.abspath(target_dir), file))]

    for _idx_file in tqdm(_filelist_all):
        if list_filetype != None:
            if os.path.splitext(_idx_file)[1].lower() in [idx.lower() for idx in list_filetype]:
                file_list.append(_idx_file)
        else:
            file_list.append(_idx_file)
    logging.info(
        'Extension : {}, Total files: {}, Selected files: {}'.format(list_filetype, len(_filelist_all), len(file_list)))
    return file_list
