
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




def extract_crop(root_path, extract_num = 10000000):
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
    print(f"----开始抽取数据-----")

    save_path = os.path.join(root_path, 'extract_crop')
    # if check_folder_exists(save_path):
    #     delete_folder_file(save_path)
    # else:
    #     create_folder(save_path)
    create_folder(save_path)


    idx = 0
    for son_folder in son_folder_list:
        num = 0
        if son_folder == 'extract_crop':
            continue
        idx += 1
        son_folder_full_path = os.path.join(root_path, son_folder)
        grand_son_folder_list = get_files(os.path.join(son_folder_full_path , 'images'))

        # 随机打乱list
        random.shuffle(grand_son_folder_list)

        extract_num_actually = len(grand_son_folder_list) if len(grand_son_folder_list) < extract_num  else extract_num

        # save_up_images_path = os.path.join(save_path,  son_folder, 'images')
        # save_up_labels_path = os.path.join(save_path,  son_folder, 'labels')
        # create_folder(save_up_images_path)
        # create_folder(save_up_labels_path)

        for i  in range(extract_num_actually):
            name ,ext  = os.path.splitext(grand_son_folder_list[i])

            image_full_path = os.path.join(root_path, son_folder , 'images' , grand_son_folder_list[i])
            txt_full_path = os.path.join(root_path, son_folder , 'labels' , name+'.txt')

            img = cv2.imdecode(np.fromfile(image_full_path, dtype=np.uint8), -1)
            img_height, img_width = img.shape[0], img.shape[1]

            line_num = 0
            with open(txt_full_path, "r") as lines:
                for line in lines:
                    line_num+=1
                    line = line.rstrip('\n')
                    line_list = line.split(' ')

                    cls = line_list[0]
                    center_x = float(line_list[1])
                    center_y = float(line_list[2])
                    width = float(line_list[3])
                    height = float(line_list[4])
                    width_half = width * img_width / 2
                    height_half = height * img_height / 2
                    x0 = center_x * img_width - width_half
                    x1 = center_x * img_width + width_half
                    y0 = center_y * img_height - height_half
                    y1 = center_y * img_height + height_half

                    # img_crop = img[int(x0):int(x1),int(y0):int(y1)]
                    img_crop = img[int(y0):int(y1), int(x0):int(x1)]

                    cls_output_path = os.path.join(save_path, cls)
                    create_folder(cls_output_path)

                    # cv2.imwrite(os.path.join(cls_output_path, name + '_'+str(num) +'.png' ),    img_crop)
                    cv2.imencode('.jpg', img_crop)[1].tofile(os.path.join(cls_output_path, name + '_[' + str(line_num) + ']_'+'.jpg'))
            num +=1


            # image_output_path = os.path.join(save_up_images_path, grand_son_folder_list[i])
            # txt_output_path = os.path.join(save_up_labels_path,  name + '.txt')
            #
            #
            # if check_file_exists(image_full_path) and check_file_exists(txt_full_path):
            #     num += 1
            #     shutil.copy(image_full_path, image_output_path)
            #     shutil.copy(txt_full_path, txt_output_path)
            # else:
            #     print(f"{os.path.join(root_path, son_folder , 'images' , grand_son_folder_list[i])} 无image或对应的txt ！！！")

        print(f"{idx}: {son_folder} 抽取 {num} 张数据")
    print(f"----完成抽取数据-----")



if __name__ == '__main__':

    extract_crop(r'\\172.25.102.12\test\wjw\赵子豪\WG线体数据集\WG_Line14', 10)