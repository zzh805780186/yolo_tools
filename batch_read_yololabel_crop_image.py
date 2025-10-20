#  读取yolo的标签txt，将目标裁剪，并存放到类对应的文件夹中。方便查看目标的标签是否正确
import os
import cv2
import numpy as np
import shutil
from pathlib import Path

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

def check_folder_exists(folder_path):
    """检查指定路径的文件是否存在"""
    return os.path.isdir(folder_path)

def delete_folder_file(folder_path):
    shutil.rmtree(folder_path)

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


def accord_yololabel_crop_image(images_path, labels_path):
    print('开始...')
    output_path = os.path.join(images_path, 'crop_image')
    create_folder(output_path)

    labels = get_files(labels_path)

    for label in labels:
        name, ext = split_to_name_ext(label)
        print(label)

        if ext not in ['.txt']:
            continue

        image_full_path = os.path.join(images_path, name+'.jpg')



        if not os.path.exists(image_full_path):
            print('{} 图像不存在'.format(image_full_path))
            continue

        img = cv2.imread(image_full_path, -1)
        img_height, img_width = img.shape[0], img.shape[1]

        num = 0
        with open(os.path.join(labels_path, label), "r") as lines:
            for line in lines:
                line = line.rstrip('\n')
                line_list = line.split(' ')

                cls = line_list[0]
                center_x = float(line_list[1])
                center_y = float(line_list[2])
                width = float(line_list[3])
                height = float(line_list[4])
                width_half = width * img_width / 2
                height_half = height * img_height /2
                x0 = center_x * img_width - width_half
                x1 = center_x * img_width + width_half
                y0 = center_y * img_height - height_half
                y1 = center_y * img_height + height_half

                # img_crop = img[int(x0):int(x1),int(y0):int(y1)]
                img_crop = img[int(y0):int(y1), int(x0):int(x1)]

                cls_output_path = os.path.join(output_path , cls)
                create_folder(cls_output_path)

                cv2.imwrite(os.path.join(cls_output_path, name + '_'+str(num) +'.png' ),    img_crop)



                num += 1

    print('完成...')


def accord_yololabel_crop_image_and_joint_zhongbao(root_path):
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



        save_up_images_path = os.path.join(save_path,  son_folder, 'images', 'crop_image')
        if check_folder_exists(save_up_images_path):
            delete_folder_file(save_up_images_path)
            print(f"删除{save_up_images_path}")



        # save_up_labels_path = os.path.join(save_path,  son_folder, 'labels')
        create_folder(save_up_images_path)
        # create_folder(save_up_labels_path)

        for i in range(len(grand_son_folder_list)):
            name, ext = os.path.splitext(grand_son_folder_list[i])

            image_full_path = os.path.join(root_path, son_folder, 'images', grand_son_folder_list[i])
            txt_full_path = os.path.join(root_path, son_folder, 'labels', name + '.txt')

            img = cv2.imdecode(np.fromfile(image_full_path, dtype=np.uint8), -1)
            img_height, img_width = img.shape[0], img.shape[1]

            print(txt_full_path)
            line_num = 0
            with open(txt_full_path, "r") as lines:
                for line in lines:

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

                    cls_output_path = os.path.join(save_up_images_path, cls)
                    create_folder(cls_output_path)

                    # cv2.imwrite(os.path.join(cls_output_path, name + '_'+str(num) +'.png' ),    img_crop)

                    cv2.imencode('.jpg', img_crop)[1].tofile(
                        os.path.join(cls_output_path, name + '_' + str(line_num) + '.jpg'))

                    line_num += 1

            num += 1
        print(f"{idx}: {son_folder} 抽取 {num} 张数据")
    print(f"----完成抽取数据-----")





def accord_yololabel_crop_image_and_joint(images_path, labels_path):
    print('开始...')


    output_path = os.path.join(images_path, 'crop_image')
    create_folder(output_path)

    labels = get_files(labels_path)

    num_id = 0
    for label in labels:
        crop_img_list = []

        name, ext = split_to_name_ext(label)
        print(label)

        if label ==r'WG_18_OUT__frame1200.txt':
            a=1


        if ext not in ['.txt']:
            continue

        # image_full_path = os.path.join(images_path, name+'.jpg')

        tmp_num = 0
        for ext_name in ['.jpg','.png','.bmp']:
            image_full_path = os.path.join(images_path, name + ext_name)

            if not os.path.exists(image_full_path):
                tmp_num += 1
                #print('{} 图像不存在'.format(image_full_path))
                continue
            break
        if tmp_num >= 3:
            print('{} 图像png,jpg,bmp都不存在'.format(image_full_path))
            continue

        num_id += 1
        #if num_id > 1000:
        #    continue

        #img = cv2.imread(image_full_path, -1)
        img = cv2.imdecode(np.fromfile(image_full_path, dtype=np.uint8), -1)
        img_height, img_width = img.shape[0], img.shape[1]

        num = 0
        with open(os.path.join(labels_path, label), "r") as lines:
            for line in lines:
                line = line.rstrip('\n')
                line_list = line.split(' ')

                cls = line_list[0]
                center_x = float(line_list[1])
                center_y = float(line_list[2])
                width = float(line_list[3])
                height = float(line_list[4])
                width_half = width * img_width / 2
                height_half = height * img_height /2
                x0 = center_x * img_width - width_half
                x1 = center_x * img_width + width_half
                y0 = center_y * img_height - height_half
                y1 = center_y * img_height + height_half

                # img_crop = img[int(x0):int(x1),int(y0):int(y1)]
                img_crop = img[int(y0):int(y1), int(x0):int(x1)]

                cls_output_path = os.path.join(output_path , cls)
                create_folder(cls_output_path)

                # cv2.imwrite(os.path.join(cls_output_path, name + '_'+str(num) +'.png' ),    img_crop)
                cv2.imencode('.jpg', img_crop)[1].tofile(os.path.join(cls_output_path, name + '_'+str(num) +'.jpg' ))


                cls_int = int(cls)
                if cls_int >= len(crop_img_list):
                    crop_img_list += [[] for _ in range(cls_int - len(crop_img_list) +1 )]
                crop_img_list[cls_int].append(img_crop)

                # crop_img_list[cls_int].append([1])


                num += 1

            # for crop_img_single_list in crop_img_list:
            for index, crop_img_single_list in enumerate(crop_img_list):
                if len(crop_img_single_list) == 0 :
                    continue
                resized_images_list = []
                # 初始化最大高度值为0
                max_height = 0

                # 遍历图像列表，获取最大高度值
                for image in crop_img_single_list:
                    height = image.shape[0]
                    if height > max_height:
                        max_height = height

                resized_images_list = [cv2.copyMakeBorder(img, 0, max_height - img.shape[0], 0, 50, cv2.BORDER_CONSTANT, value=(0, 0, 0)) for img in crop_img_single_list]


                # height = resized_images_list[0].shape[0]
                # widths = [img.shape[1] for img in resized_images_list]
                # total_width = sum(widths)
                # concatenated_image = np.zeros((height, total_width, 3), dtype=np.uint8)
                # # 将每张图像拼接到大图上
                # start_width = 0
                # for resized_image in resized_images_list:
                #     end_width = start_width + resized_image.shape[1]
                #     concatenated_image[:, start_width:end_width, :] = resized_image
                #     start_width = end_width
                #
                #
                # cls_joint_output_path = os.path.join(output_path , str(index) + '_joint')
                # create_folder(cls_joint_output_path)
                #
                # cv2.imwrite(os.path.join(cls_joint_output_path, name + r'.png' ),    concatenated_image)

    print('完成...')

if __name__ == '__main__':


    # images_path = r'F:\ZZH\DATA\count\counter_train_line6812_zzh\images'
    # labels_path = r'F:\ZZH\DATA\count\counter_train_line6812_zzh\labels'
    #
    # accord_yololabel_crop_image_and_joint(images_path, labels_path)
    # accord_yololabel_crop_image(images_path, labels_path)

    root_path = r'\\172.25.102.12\test\wjw\赵子豪\WG线体数据集\WG_Line25'
    accord_yololabel_crop_image_and_joint_zhongbao(root_path)


