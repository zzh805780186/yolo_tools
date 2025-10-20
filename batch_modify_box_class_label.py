#!/usr/bin/python
# -*- coding: UTF-8 -*-

#用来批量修改txt中每个box的类别




import os
import argparse
import shutil

import math
import ast





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


def check_string_type(s):
    """
    判断字符串类型：整数、字典或其他
    :param s: 输入字符串
    :return: 字符串类型标识 ('integer', 'dict', 'other')
    """
    if not isinstance(s, str):
        return 'other'

    # 检查是否为整数字符串
    if s.strip():
        stripped = s.strip()
        if stripped[0] in ('+', '-'):
            stripped = stripped[1:]
        if stripped.isdigit():
            return 'integer'

    # 检查是否为字典字符串
    stripped = s.strip()
    if stripped.startswith('{') and stripped.endswith('}'):
        try:
            ast.literal_eval(stripped)
            if isinstance(ast.literal_eval(stripped), dict):
                return 'dict'
        except (ValueError, SyntaxError):
            pass

    return 'other'


def batch_modify_txt_class(txt_path,  mapping):
    #mapping = opt.mapping

    #save_path = opt.save_path
    save_path_modify = os.path.join(txt_path , 'labels_class')
    create_folder(save_path_modify)

    #txt_path = opt.txt_path
    files = get_files(txt_path)

    for file in files:


        name , ext = os.path.splitext(file)
        if ext not in ['.txt']:
            continue

        if file == 'classes.txt':  #非标签内容的txt跳过
            continue

        if not file.endswith('txt'): #非txt的文件跳过
            continue
        print(os.path.join(txt_path, file))

        size = os.path.getsize(os.path.join(txt_path, file))
        if size != 0:
            pass
            with open(os.path.join(txt_path, file), "r") as lines:
                f_class = open(os.path.join(save_path_modify, file), 'w')
                for line in lines:
                    pass
                    line_list = line.split(' ')
                    # if int(line_list[0]) > 6 :
                    #     print('{}  {}'.format(file , line_list))
                    # else:
                    #     continue


                    # if line_list[0] not in mapping:
                    #     f_class.writelines(line)
                    #     continue

                    # line_list[0] = '0'  # 统一将txt中每个box的类别修改成第 x 类

                    mapping_type = check_string_type(mapping)
                    if mapping_type== 'dict':
                        mapping_tmp = ast.literal_eval(mapping)
                        if line_list[0] in mapping_tmp:
                            dst_class = mapping_tmp[line_list[0]]  #根据输入进来的字典，索引类别的对应关系 line_list[0] -> dst_class
                            line_list[0] = dst_class #类别修改
                    elif mapping_type == 'integer':
                        line_list[0] = mapping
                    else:
                        break

                    line_str = line_list[0] + ' ' + line_list[1] + ' ' + line_list[2] + ' ' + line_list[3] + ' ' + line_list[4]
                    f_class.writelines(line_str)  #写入新txt
                f_class.close()

        else:
            shutil.copyfile(os.path.join(txt_path, file) , os.path.join(save_path_modify, file))






# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()

    #parser.add_argument('--txt_path', type=str, default=r'F:\data\将要修改标签的图像\tmp1\labels', help='*.labels path')
    #parser.add_argument('--save_path', type=str, default=r'F:\data\将要修改标签的图像\tmp1\labels', help=r'output path')
    #parser.add_argument('--mapping', type=str, default={'0':"8"}, help=r'key mapping to value')


    # parser.add_argument('--txt_path', type=str, default=r'F:\data\vjshi\labels_available', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\data\vjshi\labels_available', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'0':"8"}, help=r'key mapping to value')

    #parser.add_argument('--txt_path', type=str, default=r'F:\data\tmp\baidu_01\labels_modify', help='*.labels path')
    #parser.add_argument('--save_path', type=str, default=r'F:\data\tmp\baidu_01\labels_modify', help=r'output path')
    #parser.add_argument('--mapping', type=str, default={'0':"8"}, help=r'key mapping to value')

    # parser.add_argument('--txt_path', type=str, default=r'/home/zhaozihao/Dataset/package_label_ok/AISS-CV/labels/', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'/home/zhaozihao/Dataset/package_label_ok/AISS-CV/', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'8':"0"}, help=r'key mapping to value')

    # parser.add_argument('--txt_path', type=str, default=r'F:\data\taipei_person_car_pet_package\package_test', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\data\taipei_person_car_pet_package\package_test', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'0':"4"}, help=r'key mapping to value')

    # parser.add_argument('--txt_path', type=str, default=r'F:\data\taipei_person_car_pet_package\package_train', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\data\taipei_person_car_pet_package\package_train', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'0':"4"}, help=r'key mapping to value')

    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\挑选铆钉yolo数据\labels', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\挑选铆钉yolo数据\labels_modify', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'4':"80"}, help=r'key mapping to value')


    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\threaded_laser\rivet_repeat', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\threaded_laser\rivet_repeat', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'4':"80"}, help=r'key mapping to value')

    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\threaded_laser\rag', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\threaded_laser\rag', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'4':"80"}, help=r'key mapping to value')


    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.24\2023.11.24\螺纹镭射\2023-11-24-1-重铆\raw_data\labels', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.24\2023.11.24\螺纹镭射\2023-11-24-1-重铆\raw_data\labels', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'4':"80"}, help=r'key mapping to value')

    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\exp_dirty3\labels', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\test_data\exp_dirty3\labels_modify', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'0':"2","1":"1","2":"2"}, help=r'key mapping to value')


    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.15\2023.11.15\thread\2023-11-15\raw_data\img_select\labels_dirty', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.15\2023.11.15\thread\2023-11-15\raw_data\img_select\labels_dirty\labels_modify', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'0':"3"}, help=r'key mapping to value')


    # parser.add_argument('--txt_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.29\thread\2023-11-29\raw_data', help='*.labels path')
    # parser.add_argument('--save_path', type=str, default=r'F:\ZZH\DATA\A_light\2023.11.29\thread\2023-11-29\raw_data\img_select', help=r'output path')
    # parser.add_argument('--mapping', type=str, default={'0':"3"}, help=r'key mapping to value')


    #parser.add_argument('--txt_path', type=str, default=r'\\172.25.102.12\test\wjw\datasets\shixishengbiaozhu917\Line_15_OUT_20250917083000_20250917093001_745510578\Line_15_OUT_20250917083000_20250917093001_745510578\txt_select(label0)', help='*.labels path')
    #parser.add_argument('--save_path', type=str, default=r'\\172.25.102.12\test\wjw\datasets\shixishengbiaozhu917\Line_15_OUT_20250917083000_20250917093001_745510578\Line_15_OUT_20250917083000_20250917093001_745510578\txt_select(label1)', help=r'output path')
    #parser.add_argument('--mapping', type=str, default={'0':"1"}, help=r'key mapping to value')

    #opt = parser.parse_args()


    #batch_modify_txt_class()

    #print('process over')


    