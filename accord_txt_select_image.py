#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 根据文件夹中的标签txt，在对应的图像文件夹中找对应的图像



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

def split_to_name_ext(image_name_ext):
    name, ext = os.path.splitext(image_name_ext)
    return name, ext

def gen_empty_txt(txt_path):
    with open(txt_path, "w") as f:
        pass

def accord_txt_select_img(dir_path, txt_path):
    print('处理开始')
    # print(opt.image_path)
    #dir_path = opt.image_path
    #txt_path = opt.txt_path

    #output_path = opt.output_path
    output_path = os.path.join(dir_path , 'img_select')
    create_folder(output_path)
    #parent_dir = os.path.dirname(os.path.dirname(dir_path))

    txt_output_path = os.path.join(dir_path, 'txt_select')
    create_folder(txt_output_path)

    num = 0
    txt_list = get_files(txt_path)
    for txt in txt_list:
        name , ext = split_to_name_ext(txt)

        if ext in  ['.txt']:
            print(txt)
            # tmp_path = r'F:\ZZH\DATA\execel_anylase\models\download\barcoda_dataset\yolo\archive (7)\valid\images'
            # image_full_path = os.path.join(tmp_path, name + '.jpg')

            image_full_path = os.path.join(dir_path , name+'.jpg')

            if os.path.exists(image_full_path):
                shutil.copy(image_full_path  , output_path)

                txt_full_path = os.path.join(txt_path, txt)
                shutil.copy(txt_full_path, txt_output_path)





#if __name__ == '__main__':
    #parser = argparse.ArgumentParser()



    #parser.add_argument('--input_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\挑选脏污数据', help='*.cfg path')
    #parser.add_argument('--output_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\挑选脏污数据', help='*.cfg path')

    # parser.add_argument('--input_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\泡体脏污', help='*.cfg path')

    # parser.add_argument('--input_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.17\2023.11.17\thread\2023-11-17\raw_data', help='*.cfg path')
    # parser.add_argument('--input_path', type=str, default=r'D:\ZZH\2024-03-25\2024-03-25\raw_data', help='*.cfg path')

    # parser.add_argument('--input_path', type=str, default=r'D:\ZZH\package_detect\result\package_work', help='*.cfg path')
    # parser.add_argument('--input_path', type=str, default=r'D:\ZZH\package_detect\result\package_work\exp_package4_fix',help='*.cfg path')
    # parser.add_argument('--input_path', type=str, default=r'D:\ZZH\package_detect\result\package_work\exp_package2_fix\select',help='*.cfg path')

    #parser.add_argument('--input_path', type=str,default=r'D:\ZZH\A2500_data\20240514\body_NG', help='*.cfg path')

    # parser.add_argument('--input_path', type=str, default=r'D:\ZZH\A2500_data\20240607\4工位   眼片\2024-06-07   左眼片划伤右漏眼片', help='*.cfg path')
    #parser.add_argument('--input_path', type=str, default=r'D:\ZZH\A2500_data\20240607\4工位   眼片\2024-06-07  左绝缘层脏污右中线外漏', help='*.cfg path')

    # parser.add_argument('--input_path', type=str,default=r'D:\ZZH\A2500_data\20240607\2工位   灯头\2024-06-07左灯头间隙  右右灯头划伤', help='*.cfg path')
    # parser.add_argument('--input_path', type=str,default=r'D:\ZZH\A2500_data\20240607\2工位   灯头\2024-06-07   左灯头凹陷右边线外漏', help='*.cfg path')


    # parser.add_argument('--input_path', type=str,default=r'D:\ZZH\A1200_data\2024-06-13\5\thread\raw_data\supervised_thread', help='*.cfg path')

    # parser.add_argument('--input_path', type=str,default=r'F:\ZZH\DATA\A_light\2025-01-21\camera4\1535_1613\supervised_cup', help='*.cfg path')

    #parser.add_argument('--image_path', type=str,default=r'\\172.25.102.12\test\wjw\datasets\shixishengbiaozhu917\Line_15_IN_20250917082959_20250917093002_745224021\Line_15_20250917082959_20250917093002_745224021\Line_15_20250917082959_20250917093002_745224021', help='*.cfg path')
    #parser.add_argument('--txt_path', type=str,default=r'\\172.25.102.12\test\wjw\datasets\shixishengbiaozhu917\Line_15_IN_20250917082959_20250917093002_745224021\line-15-in', help='*.cfg path')


    #opt = parser.parse_args()

    #accord_txt_select_img()

