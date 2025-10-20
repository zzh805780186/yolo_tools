# -*- coding: utf-8 -*-
'''
构造训练集、验证集
'''
import os
import shutil
import random
import yaml


def get_files(path):
    """获取指定路径下的所有文件名列表"""
    if not os.path.exists(path):
        return []
    files = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            files.append(filename)
    return files


def find_classes_txt(root_dir):
    """
    遍历 root_dir 下的所有子目录，查找第一个存在的 classes.txt 并返回类别列表
    :param root_dir: 总根目录（如 test_data）
    :return: 类别名称列表
    """
    for subdir in sorted(os.listdir(root_dir)):
        sub_path = os.path.join(root_dir, subdir)
        if os.path.isdir(sub_path):
            labels_path = os.path.join(sub_path, 'labels')
            if os.path.isdir(labels_path):
                classes_file = os.path.join(labels_path, 'classes.txt')
                if os.path.exists(classes_file):
                    print(f"✅ 使用 {classes_file} 读取类别信息")
                    with open(classes_file, 'r', encoding='utf-8') as f:
                        names = [line.strip() for line in f if line.strip()]
                    return names
    raise FileNotFoundError("❌ 在任何子目录的 labels 中都未找到 classes.txt 文件！")


def create_data_yaml(output_root, class_names, train_path="./train", val_path="./val"):
    """
    生成 data.yaml 文件
    :param output_root: 输出根目录
    :param class_names: 类别名称列表
    :param train_path: 训练集路径（相对于 data.yaml）
    :param val_path: 验证集路径（相对于 data.yaml）
    """
    data = {
        'nc': len(class_names),  # number of classes
        'names': class_names,    # class names list
        'train': os.path.join(train_path, 'images'),  # YOLO 默认找 images
        'val': os.path.join(val_path, 'images'),
    }
    yaml_path = os.path.join(output_root, 'data.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"✅ data.yaml 已生成: {yaml_path}")


def build_dataset_bk(root_dir, output_root, num_per_folder, train_ratio=0.9, val_ratio=0.1, seed=42):
    """
    构建训练/验证数据集（基于新输入结构）
    :param root_dir: 总数据根目录（如 test_data），包含多个 lineX 子目录
    :param output_root: 输出数据集根目录
    :param num_per_folder: 每个子文件夹最多取多少张图
    :param train_ratio: 训练集比例
    :param val_ratio: 验证集比例
    :param seed: 随机种子
    """
    random.seed(seed)

    # 创建输出目录（新结构）
    train_img_dir = os.path.join(output_root, 'train', 'images')
    train_label_dir = os.path.join(output_root, 'train', 'labels')
    val_img_dir = os.path.join(output_root, 'val', 'images')
    val_label_dir = os.path.join(output_root, 'val', 'labels')

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    total_copied = 0
    total_folders = 0

    # 遍历 root_dir 下的每个子目录（如 line1, line2）
    for subdir in sorted(os.listdir(root_dir)):
        sub_path = os.path.join(root_dir, subdir)
        if not os.path.isdir(sub_path):
            continue

        image_dir = os.path.join(sub_path, 'images')
        label_dir = os.path.join(sub_path, 'labels')

        if not (os.path.exists(image_dir) and os.path.isdir(image_dir)):
            print(f"⚠️ 跳过 {subdir}：缺少 images 目录")
            continue
        if not (os.path.exists(label_dir) and os.path.isdir(label_dir)):
            print(f"⚠️ 跳过 {subdir}：缺少 labels 目录")
            continue

        total_folders += 1
        print(f"\n 处理文件夹: {subdir}")

        # 获取图像和标签文件（支持多种图像格式）
        image_files = [f for f in get_files(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        label_files = [f for f in get_files(label_dir) if f.lower().endswith('.txt') and f != 'classes.txt']

        # 构建 base_name 映射
        image_dict = {os.path.splitext(f)[0]: f for f in image_files}
        label_dict = {os.path.splitext(f)[0]: f for f in label_files}

        # 匹配图像和标签
        matched = []
        for base_name in image_dict:
            if base_name in label_dict:
                img_file = image_dict[base_name]
                label_file = label_dict[base_name]
                matched.append((base_name, img_file, label_file))

        if not matched:
            print(f"  ⚠️ 未找到匹配的图像-标签对")
            continue

        # 控制每文件夹最大数量
        if len(matched) > num_per_folder:
            random.shuffle(matched)
            selected = matched[:num_per_folder]
        else:
            selected = matched

        print(f"  ✅ 选中 {len(selected)} 个样本")

        # 划分训练/验证集
        random.shuffle(selected)
        n = len(selected)
        n_train = max(1, int(n * train_ratio))
        n_val = n - n_train

        train_set = selected[:n_train]
        val_set = selected[n_train:]

        # 复制训练集
        for base_name, img_file, label_file in train_set:
            shutil.copy2(
                os.path.join(image_dir, img_file),
                os.path.join(train_img_dir, img_file)
            )
            shutil.copy2(
                os.path.join(label_dir, label_file),
                os.path.join(train_label_dir, label_file)
            )

        # 复制验证集
        for base_name, img_file, label_file in val_set:
            shutil.copy2(
                os.path.join(image_dir, img_file),
                os.path.join(val_img_dir, img_file)
            )
            shutil.copy2(
                os.path.join(label_dir, label_file),
                os.path.join(val_label_dir, label_file)
            )

        total_copied += len(selected)

    print(f"\n✅ 数据集构建完成：共 {total_folders} 个子目录，复制 {total_copied} 个样本")

    # 读取 classes.txt
    try:
        class_names = find_classes_txt(root_dir)
        print(f"�� 检测到类别数: {len(class_names)}，类别名: {class_names}")
        create_data_yaml(output_root, class_names)
    except Exception as e:
        print(f"❌ 生成 data.yaml 失败: {e}")
        raise



def build_dataset(root_dir,  train_ratio=0.9, val_ratio=0.1, num_per_folder =1000000000, seed=42):
    """
    构建训练/验证数据集（基于新输入结构）
    :param root_dir: 总数据根目录（如 test_data），包含多个 lineX 子目录
    :param output_root: 输出数据集根目录
    :param num_per_folder: 每个子文件夹最多取多少张图
    :param train_ratio: 训练集比例
    :param val_ratio: 验证集比例
    :param seed: 随机种子
    """
    random.seed(seed)

    output_root = os.path.join(root_dir , 'counter_train')

    # 创建输出目录（新结构）
    train_img_dir = os.path.join(output_root, 'train', 'images')
    train_label_dir = os.path.join(output_root, 'train', 'labels')
    val_img_dir = os.path.join(output_root, 'val', 'images')
    val_label_dir = os.path.join(output_root, 'val', 'labels')

    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    total_copied = 0
    total_folders = 0

    # 遍历 root_dir 下的每个子目录（如 line1, line2）
    for subdir in sorted(os.listdir(root_dir)):
        sub_path = os.path.join(root_dir, subdir)
        if not os.path.isdir(sub_path):
            continue

        image_dir = os.path.join(sub_path, 'images')
        label_dir = os.path.join(sub_path, 'labels')

        if not (os.path.exists(image_dir) and os.path.isdir(image_dir)):
            print(f"⚠️ 跳过 {subdir}：缺少 images 目录")
            continue
        if not (os.path.exists(label_dir) and os.path.isdir(label_dir)):
            print(f"⚠️ 跳过 {subdir}：缺少 labels 目录")
            continue

        total_folders += 1
        print(f"\n 处理文件夹: {subdir}")

        # 获取图像和标签文件（支持多种图像格式）
        image_files = [f for f in get_files(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        label_files = [f for f in get_files(label_dir) if f.lower().endswith('.txt') and f != 'classes.txt']

        # 构建 base_name 映射
        image_dict = {os.path.splitext(f)[0]: f for f in image_files}
        label_dict = {os.path.splitext(f)[0]: f for f in label_files}

        # 匹配图像和标签
        matched = []
        for base_name in image_dict:
            if base_name in label_dict:
                img_file = image_dict[base_name]
                label_file = label_dict[base_name]
                matched.append((base_name, img_file, label_file))

        if not matched:
            print(f"  ⚠️ 未找到匹配的图像-标签对")
            continue

        # 控制每文件夹最大数量
        if len(matched) > num_per_folder:
            random.shuffle(matched)
            selected = matched[:num_per_folder]
        else:
            selected = matched

        print(f"  ✅ 选中 {len(selected)} 个样本")

        # 划分训练/验证集
        random.shuffle(selected)
        n = len(selected)
        n_train = max(1, int(n * train_ratio))
        n_val = n - n_train

        train_set = selected[:n_train]
        val_set = selected[n_train:]

        # 复制训练集
        for base_name, img_file, label_file in train_set:
            shutil.copy2(
                os.path.join(image_dir, img_file),
                os.path.join(train_img_dir, img_file)
            )
            shutil.copy2(
                os.path.join(label_dir, label_file),
                os.path.join(train_label_dir, label_file)
            )

        # 复制验证集
        for base_name, img_file, label_file in val_set:
            shutil.copy2(
                os.path.join(image_dir, img_file),
                os.path.join(val_img_dir, img_file)
            )
            shutil.copy2(
                os.path.join(label_dir, label_file),
                os.path.join(val_label_dir, label_file)
            )

        total_copied += len(selected)

    print(f"\n✅ 数据集构建完成：共 {total_folders} 个子目录，复制 {total_copied} 个样本")

    # 读取 classes.txt
    try:
        class_names = find_classes_txt(root_dir)
        print(f"�� 检测到类别数: {len(class_names)}，类别名: {class_names}")
        create_data_yaml(output_root, class_names)
    except Exception as e:
        print(f"❌ 生成 data.yaml 失败: {e}")
        raise


if __name__ == '__main__':
########################################
    '''
输入 目录结构
my_data/
├── line1/
│   ├── images/       # .jpg 图像
│   └── labels/      # .txt 标签 + classes.txt
├── line2/
│   ├── images/
│   └── labels/
└── ...
'''
#####################
    '''
输出结果目录结构
train_and_val_data/
├── train/
│   ├── images/          # 训练图像
│   └── labels/            # 训练标签
├── val/
│   ├── images/          # 验证图像
│   └── labels/            # 验证标签
└── data.yaml           # YOLO 配置文件
    '''
#####################################
    # ================== 参数配置 ==================
    ROOT_DIR = r"/home/zhaozihao/cuibin/yolo_project/yolo_data/19_line_without_doubletwo_kxn/"  # 只需输入这一个路径
    OUTPUT_ROOT = r"/home/zhaozihao/cuibin/yolo_project/yolo_data/counter_train_66666/"
    NUM_PER_FOLDER = 100000  # 每个 lineX 最多取多少样本
    TRAIN_RATIO = 0.9
    VAL_RATIO = 0.1
    RANDOM_SEED = 42

    # 执行构建
    build_dataset(
        root_dir=ROOT_DIR,
        output_root=OUTPUT_ROOT,
        num_per_folder=NUM_PER_FOLDER,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        seed=RANDOM_SEED
    )
