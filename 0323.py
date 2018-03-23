# -*- coding:utf-8 -*-

# psutil 为第三方模块

from ctypes import *
import subprocess
import win32api
import time
import errno
import psutil

def drire_label():  # 获取U盘卷标
    label = []
    for i in psutil.disk_partitions():
        if "removable" in i.opts:
            label.append(i.device.strip('\\'))
    return label

def myFmtCallback(command, modifier, arg):
    # print(command)
    return 1  # TRUE

def format_drive(Drive, Format, Title):  # 格式化U盘
    fm = windll.LoadLibrary('fmifs.dll')
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_HARDDISK = 0
    fm.FormatEx(c_wchar_p(Drive), FMIFS_HARDDISK, c_wchar_p(Format),
                c_wchar_p(Title), True, c_int(0), FMT_CB_FUNC(myFmtCallback))

def document_record(doc):  # 记录格式化的时间，U盘卷名，耗时
    with open("USB记录.txt", "a", encoding="utf-8") as f:
        f.write(doc + "\n")

def file_fill(drive_file):
    write_str = "!" * 1024 * 1024 * 5  # 5MB
    with open(drive_file, "a") as f:
        while True:
            try:
                f.write(write_str)
                f.flush()
            except Exception :
                break

def main(): # 主函数
    for label in drire_label():
        start_time = time.time()  # 开始时间
        now_time = time.strftime("%F %T", time.localtime())  # 格式化时间
        volume_name, _, _, _, volume_filesystem = win32api.GetVolumeInformation(label)  # 获取卷名和文件系统
        format_drive(label, "NTFS", volume_name)  # 第一次格式化

        free_space = psutil.disk_usage(label).free # 获取磁盘可用空间
        # subprocess.Popen("fsutil file createnew " + label + "\\test.tmp " + str(free_space),
        #                            shell=True,
        #                            stderr=subprocess.PIPE,
        #                            stdout=subprocess.PIPE).communicate() # 填充磁盘
        # file_fill(label + "\\test.tmp")
        format_drive(label, volume_filesystem, volume_name)  # 第二次格式化
        end_time = time.time()  # 结束时间
        log_info =  "%s %s 格式化完成，耗时 %.2f 秒。" % (now_time, volume_name, end_time - start_time)
        document_record(log_info)
        print(log_info)

if __name__ == '__main__':
    main()
