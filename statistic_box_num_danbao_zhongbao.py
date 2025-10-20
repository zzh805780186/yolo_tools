#  读取yolo的标签txt，将目标裁剪，并存放到类对应的文件夹中。方便查看目标的标签是否正确
import os
import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

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

def check_folder_exists(folder_path):
    """检查指定路径的文件是否存在"""
    return os.path.isdir(folder_path)

def gen_empty_txt(txt_path):
    with open(txt_path, "w") as f:
        pass

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

def get_everylevel_foldername(path):
    levels = []

    # 规范化路径并分割
    normalized_path = os.path.normpath(path)
    current_path = normalized_path

    while True:
        head, tail = os.path.split(current_path)
        if not tail:  # 到达根目录
            levels.insert(0, head)
            break
        levels.insert(0, tail)
        current_path = head
    # # 打印结果
    # for i, level in enumerate(levels, 1):
    #     print(f"层级 {i}: {level}")

    # 也可以返回列表
    print(levels)
    return levels

def integration_dict_of_list(data):
    result = {}
    for item in data:
        for key, value in item.items():
            if key in result:
                result[key] += value
            else:
                result[key] = value
    sorted_data = dict(sorted(result.items()))
    return sorted_data

def draw_bar(data, title_describe, x_describe , y_describe):
    # 提取键和值
    x = list(data.keys())
    y = list(data.values())

    # 创建柱状图
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x, y, color='skyblue')

    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height}', ha='center', va='bottom')

    # 设置图表标题和坐标轴标签
    plt.title(title_describe, fontsize=14)
    plt.xlabel(x_describe, fontsize=12)
    plt.ylabel(y_describe, fontsize=12)

    # 调整x轴刻度
    plt.xticks(x)

    # 显示网格线
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()
    # 保存为JPG文件
    # plt.savefig('output.jpg', dpi=300, quality=90, bbox_inches='tight')
    # plt.close()  # 关闭图形释放内存


def read_yolo_txt(file_path):
    # 存储类别信息的列表
    classes = []

    # 打开文件并读取每一行
    with open(file_path, 'r') as file:
        for line in file:
            # 去除行尾的换行符并按空格分割
            parts = line.strip().split()

            # 第一个元素是类别ID
            class_id = int(parts[0])

            # # 如果类别ID不在列表中，则添加
            # if class_id not in classes:
            #     classes.append(class_id)
            classes.append(class_id)

    return classes


def accord_txt_statistic_num_danbao(labels_path):
    # print('开始统计...')

    total_class_list = []

    box_num_list = []
    box_image_num_list = []

    labels = get_files(labels_path)

    num_id = 0
    for label in labels:
        name, ext = split_to_name_ext(label)
        if name == 'classes':
            continue
        if ext not in ['.txt']:
            continue
        # print(label)
        num_id += 1
        full_label_path = os.path.join(labels_path, label)
        classes_list = read_yolo_txt(full_label_path)
        classes_set = set(classes_list)
        for i in range(len(classes_list)):
            if classes_list[i] not in total_class_list:
                total_class_list.append(classes_list[i])
                box_num_list.append(0)
                box_image_num_list.append(0)

        for i in range(len(classes_list)):
            idx = total_class_list.index(classes_list[i])
            box_num_list[idx] += 1

        for i in range(len(classes_set)):
            idx = total_class_list.index(list(classes_set)[i])
            box_image_num_list[idx] += 1


    print(f' * {labels_path} 总共统计 {num_id} 个标签文件：')
    # for i in range(len(total_class_list)):
    #     print(f'  |-- 第 {total_class_list[i]} 类标签：总共有 {box_num_list[i]} 个标注框')
    #
    # for i in range(len(total_class_list)):
    #     print(f'  |-- 含有第 {total_class_list[i]} 类标签的图像，总共有 {box_image_num_list[i]} 张')
    # print('完成统计...')

    box_result = dict(zip(total_class_list, box_num_list))
    image_result = dict(zip(total_class_list, box_image_num_list))
    print(f"   |-- 类别:标注框数 {box_result}")
    print(f"   |-- 类别:图像数 {image_result}")
    return num_id, box_result, image_result



def accord_txt_statistic_num_zhongbao(root_path):
    son_folder_list = get_folder_names(root_path)

    if son_folder_list == []:
        print(f"{root_path} 下无众包数据")
        return
    print('----开始扫描文件夹-----')

    folder_num = 0
    for son_folder in son_folder_list:
        if son_folder == 'WG16问题数据20251011':
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
    print(f"----开始统计数据-----")

    idx = 0
    txt_num_total, box_result_total, image_result_total = [], [], []
    for son_folder in son_folder_list:
        num = 0
        if son_folder == 'WG16问题数据20251011':
            continue
        idx += 1
        son_folder_full_path = os.path.join(root_path, son_folder)
        txt_folder_path = os.path.join(son_folder_full_path, 'labels')
        flag = check_folder_exists(txt_folder_path)
        if not flag:
            print(f"{txt_folder_path}下无labels文件夹")

        txt_num, box_result, image_result = accord_txt_statistic_num_danbao(txt_folder_path)
        txt_num_total.append(txt_num)
        box_result_total.append(box_result)
        image_result_total.append(image_result)


    print(f"----总计-----")
    txt_num_summary = sum(txt_num_total)
    box_result_summary = integration_dict_of_list(box_result_total)
    image_result_summary = integration_dict_of_list(image_result_total)
    print(f"所有数据中 总计 {txt_num_summary} 个标签文件")
    print(f"所有数据中 类别:标注框数 {box_result_summary}")
    print(f"所有数据中 类别:图像数 {image_result_summary}")

    return txt_num_summary, box_result_summary, image_result_summary





if __name__ == '__main__':



    # labels_path = r'F:\ZZH\DATA\count\Line_16_IN_20250917080308_20250917091257_284\labels'
    # txt_num, box_result, image_result = accord_txt_statistic_num_danbao(labels_path)

    root_path = r'F:\ZZH\DATA\count'
    txt_num_summary, box_result_summary, image_result_summary = accord_txt_statistic_num_zhongbao(root_path)

    #画出众包结果
    draw_bar(box_result_summary, 'cls:box' , 'cls' , 'box_num')
    # draw_bar(image_result_summary, 'cls:image' , 'cls' , 'image_num')

