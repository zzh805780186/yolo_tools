
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




def merge_txt(root_path):
    save_path = root_path
    save_train_txt_path = os.path.join(root_path, 'train.txt')
    save_val_txt_path = os.path.join(root_path, 'val.txt')


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

        txt_files = get_files(son_folder_full_path)
        if "train.txt" in txt_files and  "val.txt" in  txt_files:
            folder_num += 1
        else:
            print(f"---- {son_folder} 下无train.txt/val.txt")
            print('----算法退出-----')
            return


    print(f"----文件夹扫描完成，共计{folder_num}包数据-----")


    if check_file_exists(save_train_txt_path):
        print(f"删除 {save_train_txt_path}")
        os.remove(save_train_txt_path)

    if check_file_exists(save_val_txt_path):
        print(f"删除 {save_val_txt_path}")
        os.remove(save_val_txt_path)

    print(f"----开始合并标签-----")




    f_train = open(save_train_txt_path, 'a')
    f_val = open(save_val_txt_path, 'a')

    idx = 0
    train_total_num = 0
    val_total_num = 0
    for son_folder in son_folder_list:
        num = 0
        if son_folder == 'extract_crop':
            continue
        idx += 1
        son_folder_full_path = os.path.join(root_path, son_folder)
        # grand_son_folder_list = get_files(os.path.join(son_folder_full_path , 'images'))

        train_num = 0
        with open(os.path.join(son_folder_full_path, 'train.txt'), "r") as lines:
            for line in lines:
                f_train.writelines(line)
                train_num+=1
        train_total_num += train_num

        val_num = 0
        with open(os.path.join(son_folder_full_path, 'val.txt'), "r") as lines:
            for line in lines:
                f_val.writelines(line)
                val_num+=1
        val_total_num += val_num
        print(f"{idx}: {son_folder_full_path} train/val合并完成, train {train_num} 张图，val {val_num} 张图")
    f_train.close()
    f_val.close()
    print(f"总计： train {train_total_num} 张图，val {val_total_num} 张图")
    print(f"----完成合并标签-----")



if __name__ == '__main__':

    merge_txt(r'F:\ZZH\DATA\count\test')