import os


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

def check_and_create_file(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        # 创建空的txt文件
        with open(file_path, 'w') as file:
            pass
        print(f"文件 {file_path} 不存在，已创建一个空的txt文件")
    else:
        print(f"文件 {file_path} 已存在")


def check_and_create_empty_txt(image_path):
    images = get_files(image_path)

    save_path = os.path.join(image_path,'empty_txt')
    create_folder(save_path)
    for image in images:
        name ,ext  = os.path.splitext(image)
        if ext not in ['.jpg' , '.png' , '.BMP', '.PNG' ,'.bmp' , '.jpeg']:
            continue
        print(image)
        save_full_path = os.path.join(save_path, name+'.txt')
        with open(save_full_path, 'w') as file:
            pass

# if __name__ == '__main__':
#     image_path = r'E:\ZZH\DATA\Anomaly_Detection\zhongyi_data20230710_segment\anomally_data_for_roi_crop\images'
#     label_path = r'E:\ZZH\DATA\Anomaly_Detection\zhongyi_data20230710_segment\anomally_data_for_roi_crop\labels'
#
#     image_path = r'C:\Users\zhaozihao\Desktop\exp_crop2'
#     label_path = r'C:\Users\zhaozihao\Desktop\exp_crop2\labels'
#
#     image_path = r'E:\ZZH\DATA\Anomaly_Detection\zhongyi_data20230721_segment\anomally_data_for_roi_crop\images'
#     label_path = r'E:\ZZH\DATA\Anomaly_Detection\zhongyi_data20230721_segment\anomally_data_for_roi_crop\labels_empty'
#
#
#     image_path = r'E:\ZZH\DATA\Anomaly_Detection\zhongyi_data_segment\anomally_data_for_roi_crop\images'
#     label_path = r'E:\ZZH\DATA\Anomaly_Detection\zhongyi_data_segment\anomally_data_for_roi_crop\labels'
#
#     image_path = r'E:\ZZH\DATA\Anomaly_Detection\result\predict\exp_myself4'
#     label_path = r'E:\ZZH\DATA\Anomaly_Detection\result\predict\exp_myself4\labels'
#
#     image_path = r'E:\ZZH\DATA\A_light\xu_NG_angle2_20230911\NG\1\raw_data_english_png'
#     label_path = r'E:\ZZH\DATA\A_light\xu_NG_angle2_20230911\NG\1\raw_data_english_png\铆钉有监督标签'
#
#
#     image_path = r'F:\ZZH\DATA\A_light\2023.10.30\2023.10.30\body\2023-10-30\raw_data\select_good_tmp'
#     label_path = r'F:\ZZH\DATA\A_light\2023.10.30\2023.10.30\body\2023-10-30\raw_data\select_good_tmp\labels'
#
#     image_path = r'F:\ZZH\DATA\A_light\test_data\no_rivet1'
#     label_path = r'F:\ZZH\DATA\A_light\test_data\no_rivet1'
#
#     image_path = r'F:\ZZH\DATA\A_light\2023.11.24\2023.11.24\thread\2023-11-24\raw_data\new_crop'
#     label_path = r'F:\ZZH\DATA\A_light\2023.11.24\2023.11.24\thread\2023-11-24\raw_data\new_crop'
#
#     image_path = r'F:\ZZH\DATA\A_light\2023.11.29\thread\2023-11-29\raw_data\new_crop'
#     label_path = r'F:\ZZH\DATA\A_light\2023.11.29\thread\2023-11-29\raw_data\new_crop'
#
#
#     image_path = r'D:\ZZH\package_detect\result\package_work\exp_package4_fix\img_select'
#     label_path = r'D:\ZZH\package_detect\result\package_work\exp_package4_fix\img_select'
#
#     image_path = r'F:\ZZH\DATA\bar\FP_data\frame\20250826_f11_5line1'
#     label_path = r'F:\ZZH\DATA\bar\FP_data\frame\20250826_f11_5line1'
#
#     images = get_files(image_path)
#     for image in images:
#         name ,ext  = os.path.splitext(image)
#         if ext not in ['.jpg' , '.png' , '.BMP', '.PNG']:
#             continue
#
#         check_and_create_file(os.path.join(label_path ,name+'.txt' ))
#
#         pass



