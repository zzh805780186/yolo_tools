
import os
import argparse
import random
from pathlib import Path
import shutil


import cv2
import numpy as np


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

def check_file_exists(file_path):
    """检查指定路径的文件是否存在"""
    return os.path.exists(file_path)

def check_folder_exists(folder_path):
    """检查指定路径的文件是否存在"""
    return os.path.isdir(folder_path)

def delete_folder_file(folder_path):
    shutil.rmtree(folder_path)

def change_extension(filename, new_extension):
    """将文件名后缀改为指定扩展名"""
    base = os.path.splitext(filename)[0]
    new_filename = base + new_extension
    return new_filename

def get_folder_names(path):
    """
    获取指定路径下的所有文件夹名称
    :param path: 目标路径
    :return: 文件夹名称列表
    """
    try:
        path = Path(path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"路径不存在: {path}")
        if not path.is_dir():
            raise NotADirectoryError(f"提供的路径不是文件夹: {path}")

        return [f.name for f in path.iterdir() if f.is_dir()]
    except Exception as e:
        print(f"错误: {str(e)}")
        return []




def delete_crop_image_folder(root_path):
    son_folder_list = get_folder_names(root_path)

    if son_folder_list == []:
        print(f"{root_path} 下无众包数据")
        return
    print('----开始扫描文件夹-----')

    folder_num = 0
    for son_folder in son_folder_list:
        if son_folder == 'extract_crop':
            continue

        son_folder_full_path = os.path.join(root_path, son_folder)
        grand_son_folder_list = get_folder_names(son_folder_full_path)
        if "images" in grand_son_folder_list and "labels" in grand_son_folder_list:
            folder_num += 1
            # print(f" ---- {son_folder}：train {len(sub_train_fullpath_list)} 条数据， val {len(sub_val_fullpath_list)} 条数据")
        else:
            print(f"---- {son_folder} 下无images/labels数据")
            print('----算法退出-----')
            return

    print(f"----文件夹扫描完成，共计{folder_num}包数据-----")
    print(f"----开始删除crop_image文件夹-----")

    # save_path = os.path.join(root_path, 'extract_crop')
    # if check_folder_exists(save_path):
    #     delete_folder_file(save_path)
    # else:
    #     create_folder(save_path)
    # create_folder(save_path)

    save_path = root_path

    idx = 0
    for son_folder in son_folder_list:
        num = 0
        if son_folder == 'extract_crop':
            continue
        idx += 1
        son_folder_full_path = os.path.join(root_path, son_folder)
        grand_son_folder_list = get_files(os.path.join(son_folder_full_path, 'images'))

        save_up_images_path = os.path.join(save_path, son_folder, 'images', 'crop_image')
        if check_folder_exists(save_up_images_path):
            delete_folder_file(save_up_images_path)
            print(f"删除{save_up_images_path} ")
    print("删除完成")


if __name__ == '__main__':

    delete_crop_image_folder(r'\\172.25.102.12\test\wjw\赵子豪\WG线体数据集\WG_Line25')
