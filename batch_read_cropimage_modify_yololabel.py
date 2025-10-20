#!/usr/bin/python
# -*- coding: UTF-8 -*-

#用来批量修改txt中每个box的类别




import os
import argparse
import shutil


def get_folders(path):
    """ 获取指定路径下所有文件夹名称 """
    folders = []
    for foldername in os.listdir(path):
        if os.path.isdir(os.path.join(path, foldername)):
            folders.append(foldername)
    return folders
def get_files(path):
    """ 获取指定路径下所有文件名称 """
    files = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            files.append(filename)
    return files

def create_folder(folder_path):
    """ 判断文件夹是否存在，不存在则创建 """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)





def batch_modify_box_class(crop_image_path, txt_path):
    # crop_image_path = opt.crop_image_path
    # txt_path = opt.txt_path

    save_txt_path = os.path.join(txt_path, 'modify_txt')
    create_folder(save_txt_path)

    entries = os.listdir(crop_image_path)
    folders = [entry for entry in entries if os.path.isdir(os.path.join(crop_image_path, entry))]

    files = get_files(txt_path)

    for file in files:
        #print(file)

        name , ext = os.path.splitext(file)
        if ext not in ['.txt']:
            continue

        if file == 'classes.txt':  #非标签内容的txt跳过
            continue


        with open(os.path.join(txt_path, file), "r") as lines:
            f_class = open(os.path.join(save_txt_path, file), 'w')
            line_num = 0
            for line in lines:
                pass
                line_list = line.split(' ')
                cls = line_list[0]
                center_x = float(line_list[1])
                center_y = float(line_list[2])
                width = float(line_list[3])
                height = float(line_list[4])

                flag = -1

                for folder in folders:
                    folder_path = os.path.join(crop_image_path, folder)
                    uncertain_crop_image_path = os.path.join(folder_path, name+'_'+str(line_num)+'.jpg')
                    if os.path.exists(uncertain_crop_image_path):
                        flag = str(folder)
                        break

                if int(flag) >= 0:
                    pass
                    line_str = flag + ' ' + line_list[1] + ' ' + line_list[2] + ' ' + line_list[3] + ' ' + line_list[4]
                    f_class.writelines(line_str)  # 写入新txt

                line_num += 1
            f_class.close()








# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#
#
#     parser.add_argument('--crop_image_path', type=str, default=r'F:\ZZH\DATA\downlight\A8_3line\NJ30K\images\crop_image_manual', help='*.labels path')
#     parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\downlight\A8_3line\NJ30K\labels', help=r'output path')
#
#
#     opt = parser.parse_args()
#
#
#     batch_modify_box_class()
#
#     print('process over')