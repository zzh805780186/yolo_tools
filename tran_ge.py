##############################################
# tran_ge.py
# 根据图片数据集，按照指定比例划分，生成标签train.txt、val.txt、test.txt、trainval.txt
# #按照顺序划分数据集
# def dataset_process():
# #按照乱序划分数据集
# def dataset_process_random():
##############################################





import os
import argparse
import random
from pathlib import Path

#train_p = 0.8
#test_p = 0.1
#val_p = 0.1

# train_p = 0.9
# test_p = 0
# val_p = 0.1

#train_p = 1
#test_p = 0
#val_p = 0


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


#按照顺序划分数据集
def dataset_process():
    #f_train = open(os.path.join(opt.path,'train.txt'), 'w')
    #f_trainval = open(os.path.join(opt.path,'trainval.txt'), 'w')
    #f_test = open(os.path.join(opt.path,'test.txt'), 'w')
    #f_val = open(os.path.join(opt.path,'val.txt'), 'w')


    if not os.path.exists(opt.output_path):
        os.makedirs(opt.output_path)

    f_train = open(os.path.join(opt.output_path,'train.txt'), 'w')
    f_trainval = open(os.path.join(opt.output_path,'trainval.txt'), 'w')
    f_test = open(os.path.join(opt.output_path,'test.txt'), 'w')
    f_val = open(os.path.join(opt.output_path,'val.txt'), 'w')


    img_dir = os.path.join(opt.input_path, 'images')
    img_list = os.listdir(img_dir)

    total = len(img_list)
    train_num = int(train_p * total)
    test_num  = int(test_p * total)
    val_num = total - train_num - test_num
    trainval_num = train_num + val_num
    count = 0

    for img in img_list:
        count += 1
        jpg_dir = os.path.join(img_dir, img)
        if count <= trainval_num:
            f_trainval.writelines(jpg_dir)
            f_trainval.write('\n')
            if count <= train_num:
                f_train.writelines(jpg_dir)
                f_train.write('\n')
                continue
            f_val.writelines(jpg_dir)
            f_val.write('\n')
        else:
            f_test.writelines(jpg_dir)
            f_test.write('\n')
    f_train.close()
    f_trainval.close()
    f_test.close()
    f_val.close()
    print('total: {}, trainval: {}, train: {}, val: {}, test: {}'.format(total, trainval_num, train_num, val_num, test_num))




#按照乱序划分数据集
def dataset_process_random():
    #f_train = open(os.path.join(opt.path,'train.txt'), 'w')
    #f_trainval = open(os.path.join(opt.path,'trainval.txt'), 'w')
    #f_test = open(os.path.join(opt.path,'test.txt'), 'w')
    #f_val = open(os.path.join(opt.path,'val.txt'), 'w')


    if not os.path.exists(opt.output_path):
        os.makedirs(opt.output_path)

    f_train = open(os.path.join(opt.output_path,'train.txt'), 'w')
    f_trainval = open(os.path.join(opt.output_path,'trainval.txt'), 'w')
    f_test = open(os.path.join(opt.output_path,'test.txt'), 'w')
    f_val = open(os.path.join(opt.output_path,'val.txt'), 'w')


    img_dir = os.path.join(opt.input_path, 'images')
    img_list = os.listdir(img_dir)

    #随机打乱list
    random.shuffle(img_list)


    total = len(img_list)
    train_num = int(train_p * total)
    test_num  = int(test_p * total)
    val_num = total - train_num - test_num
    trainval_num = train_num + val_num
    count = 0

    for img in img_list:
        count += 1
        jpg_dir = os.path.join(img_dir, img)
        if count <= trainval_num:
            f_trainval.writelines(jpg_dir)
            f_trainval.write('\n')
            if count <= train_num:
                f_train.writelines(jpg_dir)
                f_train.write('\n')
                continue
            f_val.writelines(jpg_dir)
            f_val.write('\n')
        else:
            f_test.writelines(jpg_dir)
            f_test.write('\n')
    f_train.close()
    f_trainval.close()
    f_test.close()
    f_val.close()
    print('total: {}, trainval: {}, train: {}, val: {}, test: {}'.format(total, trainval_num, train_num, val_num, test_num))

def dataset_process_random_danbao(root_path,train_ratio, val_ratio):

    f_train = open(os.path.join(root_path, 'train.txt'), 'w')
    f_val = open(os.path.join(root_path, 'val.txt'), 'w')

    img_dir = os.path.join(root_path, 'images')
    img_list = os.listdir(img_dir)

    # 随机打乱list
    random.shuffle(img_list)

    total = len(img_list)
    train_num = int((train_ratio/(train_ratio + val_ratio)) * total)
    val_num = total - train_num
    count = 0

    train_fullpath_list = []
    val_fullpath_list = []

    for img in img_list:
        count += 1
        jpg_dir = os.path.join(img_dir, img)
        if count <= train_num:
            f_train.writelines(jpg_dir)
            f_train.write('\n')
            train_fullpath_list.append(jpg_dir)
        else:
            f_val.writelines(jpg_dir)
            f_val.write('\n')
            val_fullpath_list.append(jpg_dir)
    f_train.close()
    f_val.close()
    # print('total: {}, trainval: {}, train: {}, val: {}, test: {}'.format(total, trainval_num, train_num, val_num,test_num))
    print('已处理文件夹：{},  total: {}, train: {}, val: {}'.format(root_path,total, train_num, val_num))
    return train_fullpath_list, val_fullpath_list



#按照乱序划分数据集 一包一包的数据
def dataset_process_random_zhongbao(root_path,train_ratio=90, val_ratio=10):
    #f_train = open(os.path.join(opt.path,'train.txt'), 'w')
    #f_trainval = open(os.path.join(opt.path,'trainval.txt'), 'w')
    #f_test = open(os.path.join(opt.path,'test.txt'), 'w')
    #f_val = open(os.path.join(opt.path,'val.txt'), 'w')

    son_folder_list = get_folder_names(root_path)

    if son_folder_list == []:
        print(f"{root_path} 下无众包数据")
        return

    print(f"✅ 数据集构建：共 {len(son_folder_list)} 个子目录")
    total_train_fullpath_list = []
    total_val_fullpath_list = []
    for son_folder in son_folder_list:
        son_folder_full_path = os.path.join(root_path, son_folder)
        grand_son_folder_list = get_folder_names(son_folder_full_path)
        if "images" in grand_son_folder_list and "labels" in grand_son_folder_list:
            pass
            sub_train_fullpath_list, sub_val_fullpath_list = dataset_process_random_danbao(son_folder_full_path,train_ratio, val_ratio )
            total_train_fullpath_list.append(sub_train_fullpath_list)
            total_val_fullpath_list.append(sub_val_fullpath_list)

            # print(f" ---- {son_folder}：train {len(sub_train_fullpath_list)} 条数据， val {len(sub_val_fullpath_list)} 条数据")
        else:
            print(f"---- {son_folder} 下无images/labels数据")
            return

    f_train = open(os.path.join(root_path, 'train.txt'), 'w')
    f_val = open(os.path.join(root_path, 'val.txt'), 'w')

    total_train_num = 0
    for train_fullpath_tmp  in total_train_fullpath_list:
        total_train_num += len(train_fullpath_tmp)
        for i_tmp in train_fullpath_tmp:
            f_train.writelines(i_tmp)
            f_train.write('\n')

    total_val_num = 0
    for val_fullpath_tmp  in total_val_fullpath_list:
        total_val_num += len(val_fullpath_tmp)
        for i_tmp in val_fullpath_tmp:
            f_val.writelines(i_tmp)
            f_val.write('\n')
    f_train.close()
    f_val.close()
    # print('total: {}, train: {}, val: {}'.format(total,  train_num, val_num))



    print(f"✅ 数据集构建完成：共 {len(son_folder_list)} 个子目录,共计： train {total_train_num} 条数据， val {total_val_num} 条数据")




if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    #
    #
    #
    # parser.add_argument('--input_path', type=str, default=r'D:\LF\ultralytics-main\train_data\taiguo\2025-09-20h10', help='*.cfg path')
    # parser.add_argument('--output_path', type=str, default=r'D:\LF\ultralytics-main\train_data\taiguo\2025-09-20h10', help='*.cfg path')
    # opt = parser.parse_args()



    #按照顺序划分数据集
    #dataset_process()



    #按照乱序划分数据集
    # dataset_process_random()

    dataset_process_random_danbao(r'F:\ZZH\DATA\count\2025-09-18-h10-out', 90,10)

    #按照乱序划分数据集 一包一包数据
    # dataset_process_random_zhongbao(r'F:\ZZH\DATA\count', 90,10)