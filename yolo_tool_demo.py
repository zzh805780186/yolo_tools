import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
from tkinter import PhotoImage
from PIL import ImageTk, Image
import os
import math
import ast
from accord_txt_select_image import accord_txt_select_img
from batch_modify_box_class_label import batch_modify_txt_class
from gen_empty_txt import  check_and_create_empty_txt
from video2frame import  read_videos
from batch_read_yololabel_crop_image  import accord_yololabel_crop_image_and_joint
from  batch_read_cropimage_modify_yololabel import batch_modify_box_class
from  create_train_val_dataset_same_num_3 import build_dataset

from tran_ge import dataset_process_random_danbao,dataset_process_random_zhongbao

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YOLO处理工具 版本：V0.0.5")
        self.geometry("1000x1000")

        # 左侧导航栏
        nav_frame = tk.Frame(self, width=150, bg="#f0f0f0")
        nav_frame.pack(side="left", fill="y")
        nav_frame.pack_propagate(False)

        # 主内容区
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

        # 创建导航按钮
        buttons = [
            ("首页", StartPage),
            ("批量修改类别", PageOne),
            ("根据txt筛选图像", PageTwo),
            ("负样本生成空txt", PageThree),
            ("视频拆帧", PageFour),
            ("根据标签裁剪图像小图", PageFive),
            ("根据图像小图修正标签", PageSix),
            ("数据集划分(图像版)", PageSeven),
            ("数据集划分(标签版)", PageEight)
        ]

        for text, page in buttons:
            tk.Button(
                nav_frame,
                text=text,
                width=15,
                relief="flat",
                bg="#e0e0e0",
                activebackground="#d0d0d0",
                command=lambda p=page: self.show_page(p)
            ).pack(pady=10, padx=10, ipady=5)

        # 初始化所有页面
        self.pages = {}
        for F in (StartPage, PageOne, PageTwo,PageThree,PageFour,PageFive,PageSix,PageSeven,PageEight):
            page = F(self.main_frame)
            self.pages[F] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(StartPage)

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent):
        # tk.Frame.__init__(self, parent, bg="white")
        tk.Frame.__init__(self, parent)
        tk.Label(self,
                 text="彦祖亦菲你来啦 ^_^",
                 font=("Arial", 24),
                 bg="white").pack(pady=200)





class PageOne(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="批量修改txt类别",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 图像文件夹选择相关控件
        # tk.Label(self, text="选择图像文件夹路径:").pack()
        self.entry_txt_path = tk.Entry(self, width=100)
        self.entry_txt_path.pack(pady=10)

        tk.Button(
            self,
            text="选择txt文件夹",
            command=self.browse_folder_txt
        ).pack(pady=10)

        self.entry_mapping = tk.Entry(self, width=100)
        self.entry_mapping.pack(pady=5)
        label = tk.Label(self, text="类别转换：所有类别都转换为统一值，则输入整数,例如3。指定类转换，则输入字典，例如{'0':'1','3':'5'}", font=("Arial", 10))
        label.pack(pady=50)

        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_txt_path.delete(0, tk.END)
        self.entry_mapping.delete(0, tk.END)


    def browse_folder_txt(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_txt_path.delete(0, tk.END)
            self.entry_txt_path.insert(0, folder_selected)


    def process(self):
        """读取所选文件夹中的txt文件"""
        folder_txt_path = self.entry_txt_path.get()  # 获取之前选择的文件夹路径
        if not folder_txt_path:
            messagebox.showwarning("警告", "请先选择txt文件夹路径")
            return
        everylevel_foldername = self.get_everylevel_foldername(folder_txt_path)
        if everylevel_foldername[-1] == 'labels_class':
            messagebox.showwarning("警告", "输入的txt文件夹不允许起名labels_class，请换一个名字再试")
            return

        mapping = self.entry_mapping.get()

        mapping_type =   self.check_string_type(mapping)
        if mapping_type == 'other':
            messagebox.showwarning("警告", "类别转换关系有误")
            return

        txt_files = []
        txt_test_names = self.get_files(folder_txt_path)
        for txt_test_name in txt_test_names:
            name_tmp, ext_tmp = os.path.splitext(txt_test_name)
            if ext_tmp not in ['.txt']:
                continue
            txt_files.append(os.path.join(folder_txt_path, txt_test_name))


        if not txt_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关txt")
            return
        batch_modify_txt_class(folder_txt_path, mapping)

        result_str = folder_txt_path
        messagebox.showinfo("提示", "转换完成,保存至:"+result_str)

    def get_everylevel_foldername(self, path):
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
        return levels

    def is_non_negative_integer(self,value):
        return isinstance(value, int) and value >= 0 and math.isfinite(value)

    def is_non_negative_dict(self,value):
        return isinstance(value, dict)
    def get_files(self,path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files

    def check_string_type(self,s):
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

class PageTwo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="根据txt筛选图像",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 图像文件夹选择相关控件
        # tk.Label(self, text="选择图像文件夹路径:").pack()
        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择图像文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)





        # 标签文件夹选择相关控件
        # tk.Label(self, text="选择标签文件夹路径:").pack()
        self.entry_txt_path = tk.Entry(self, width=100)
        self.entry_txt_path.pack(pady=40)

        tk.Button(
            self,
            text="选择txt文件夹",
            command=self.browse_folder_txt
        ).pack(pady=20)

        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)
        self.entry_txt_path.delete(0, tk.END)

    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)

    def browse_folder_txt(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_txt_path.delete(0, tk.END)
            self.entry_txt_path.insert(0, folder_selected)


    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        if not folder_path:
            messagebox.showwarning("警告", "请先图像选择文件夹路径")
            return

        everylevel_foldername = self.get_everylevel_foldername(folder_path)
        if everylevel_foldername[-1] == 'img_select':
            messagebox.showwarning("警告", "输入的图像文件夹不允许起名img_select，请换一个名字再试")
            return

        jpg_files = []
        image_test_names = self.get_files(folder_path)
        for image_test_name in image_test_names:
            name_tmp, ext_tmp = os.path.splitext(image_test_name)
            if ext_tmp not in ['.png','.jpg','.bmp']:
                continue
            jpg_files.append(os.path.join(folder_path, image_test_name))

        # # 遍历文件夹中的JPG文件
        # jpg_files = []
        # for root, dirs, files in os.walk(folder_path):
        #     for file in files:
        #         if file.lower().endswith(('.jpg', '.jpeg')):
        #             jpg_files.append(os.path.join(root, file))

        if not jpg_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关图像")
            return


        folder_txt_path = self.entry_txt_path.get()  # 获取之前选择的文件夹路径
        if not folder_txt_path:
            messagebox.showwarning("警告", "请先选择txt文件夹路径")
            return

        everylevel_foldername = self.get_everylevel_foldername(folder_txt_path)
        if everylevel_foldername[-1] == 'txt_select':
            messagebox.showwarning("警告", "输入的标签文件夹不允许起名txt_select，请换一个名字再试")
            return


        txt_files = []
        txt_test_names = self.get_files(folder_txt_path)
        for txt_test_name in txt_test_names:
            name_tmp, ext_tmp = os.path.splitext(txt_test_name)
            if ext_tmp not in ['.txt']:
                continue
            txt_files.append(os.path.join(folder_txt_path, txt_test_name))


        if not txt_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关txt")
            return


        # 显示读取结果（示例：打印到控制台）
        print(f"找到 {len(jpg_files)} 个JPG文件:")
        for file in jpg_files:
            print(file)

        accord_txt_select_img(folder_path, folder_txt_path)

        result_str = folder_path
        messagebox.showinfo("提示", "转换完成,保存至:"+result_str)

    def get_files(self,path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files

    def get_everylevel_foldername(self, path):
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
        return levels



class PageThree(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="负样本生成空txt",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 图像文件夹选择相关控件
        # tk.Label(self, text="选择图像文件夹路径:").pack()
        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择图像文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)

        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)


        # # 输出日志文本框
        # self.log_text = scrolledtext.ScrolledText(
        #     self,
        #     width=80,
        #     height=15,
        #     wrap=tk.WORD,
        #     bg="#f0f0f0",
        #     font=("Consolas", 10)
        # )
        # self.log_text.pack(pady=10)


    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)



    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        if not folder_path:
            messagebox.showwarning("警告", "请先图像选择文件夹路径")
            return

        jpg_files = []
        image_test_names = self.get_files(folder_path)
        for image_test_name in image_test_names:
            name_tmp, ext_tmp = os.path.splitext(image_test_name)
            if ext_tmp not in ['.png', '.jpg', '.bmp']:
                continue
            jpg_files.append(os.path.join(folder_path, image_test_name))


        if not jpg_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关图像")
            return

        # self.log_text.delete(1.0, tk.END)  # 清空日志
        #
        # try:
        #     # 重定向print输出
        #     original_print = print
        #
        #     def custom_print(*args):
        #         original_print(*args)
        #         self.log_text.insert(tk.END, ''.join(str(arg) for arg in args) + '\n')
        #         self.log_text.yview(tk.END)
        #
        #     import sys
        #     sys.stdout = custom_print
        #
        #     # 调用处理函数
        #     check_and_create_empty_txt(folder_path)
        #
        #     # 恢复print
        #     sys.stdout = sys.__stdout__
        #     self.log_text.insert(tk.END, "\n处理完成！", "success")
        #     self.log_text.yview(tk.END)
        #
        # except Exception as e:
        #     self.log_text.insert(tk.END, f"错误: {str(e)}\n", "error")
        #     self.log_text.yview(tk.END)
        #
        # # 配置日志样式
        # self.log_text.tag_configure("success", foreground="green")
        # self.log_text.tag_configure("error", foreground="red")
        # self.log_text.config(state=tk.DISABLED)  # 防止误编辑



        check_and_create_empty_txt(folder_path)

        result_str = folder_path
        messagebox.showinfo("提示", "转换完成,保存至:" + result_str)

    def get_files(self, path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files


class PageFour(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="视频拆帧",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择视频文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)

        self.entry_interval = tk.Entry(self, width=100)
        self.entry_interval.pack(pady=5)
        label = tk.Label(self, text="抽帧间隔 3 50 等...", font=("Arial", 10))
        label.pack(pady=50)

        self.entry_frame_num = tk.Entry(self, width=100)
        self.entry_frame_num.pack(pady=5)
        label = tk.Label(self, text="最大拆帧图像张数 400 张等... 不输入数值则默认全拆", font=("Arial", 10))
        label.pack(pady=50)

        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)
        self.entry_frame_num.delete(0, tk.END)
        self.entry_interval.delete(0, tk.END)

    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)

    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        if not folder_path:
            messagebox.showwarning("警告", "请先选择视频文件夹路径")
            return

        jpg_files = []
        image_test_names = self.get_files(folder_path)
        for image_test_name in image_test_names:
            name_tmp, ext_tmp = os.path.splitext(image_test_name)
            if ext_tmp not in ['.mp4', '.avi']:
                continue
            jpg_files.append(os.path.join(folder_path, image_test_name))

        if not jpg_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关视频")
            return

        interval = self.entry_interval.get()

        interval_type = self.is_positive_integer(interval)

        if not interval_type:
            messagebox.showinfo("提示", "抽帧输入错误")
            return

        entry_frame_num = self.entry_frame_num.get()
        entry_frame_num_type = self.is_positive_integer(entry_frame_num)
        if entry_frame_num != '':
            if not entry_frame_num_type:
                messagebox.showinfo("提示", "图像总张数输入错误")
                return

        #
        # # 显示读取结果（示例：打印到控制台）
        # print(f"找到 {len(jpg_files)} 个JPG文件:")
        # for file in jpg_files:
        #     print(file)

        read_videos(folder_path,int(interval), entry_frame_num)

        result_str = folder_path
        messagebox.showinfo("提示", "转换完成,保存至:" + result_str)

    def get_files(self, path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files

    def is_positive_integer(self,s):
        """
        判断字符串是否为正整数
        :param s: 输入字符串
        :return: 如果是正整数返回True，否则返回False
        """
        if not s:
            return False
        if s.startswith('0') and len(s) > 1:
            return False
        if s == '0':
            return False
        return s.isdigit()



class PageFive(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="根据标签裁剪图像小图",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 图像文件夹选择相关控件
        # tk.Label(self, text="选择图像文件夹路径:").pack()
        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择图像文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)





        # 标签文件夹选择相关控件
        # tk.Label(self, text="选择标签文件夹路径:").pack()
        self.entry_txt_path = tk.Entry(self, width=100)
        self.entry_txt_path.pack(pady=40)

        tk.Button(
            self,
            text="选择txt文件夹",
            command=self.browse_folder_txt
        ).pack(pady=20)

        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)
        self.entry_txt_path.delete(0, tk.END)


    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)

    def browse_folder_txt(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_txt_path.delete(0, tk.END)
            self.entry_txt_path.insert(0, folder_selected)


    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        if not folder_path:
            messagebox.showwarning("警告", "请先图像选择文件夹路径")
            return

        jpg_files = []
        image_test_names = self.get_files(folder_path)
        for image_test_name in image_test_names:
            name_tmp, ext_tmp = os.path.splitext(image_test_name)
            if ext_tmp not in ['.png','.jpg','.bmp']:
                continue
            jpg_files.append(os.path.join(folder_path, image_test_name))

        # # 遍历文件夹中的JPG文件
        # jpg_files = []
        # for root, dirs, files in os.walk(folder_path):
        #     for file in files:
        #         if file.lower().endswith(('.jpg', '.jpeg')):
        #             jpg_files.append(os.path.join(root, file))

        if not jpg_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关图像")
            return


        folder_txt_path = self.entry_txt_path.get()  # 获取之前选择的文件夹路径
        if not folder_txt_path:
            messagebox.showwarning("警告", "请先选择txt文件夹路径")
            return

        txt_files = []
        txt_test_names = self.get_files(folder_txt_path)
        for txt_test_name in txt_test_names:
            name_tmp, ext_tmp = os.path.splitext(txt_test_name)
            if ext_tmp not in ['.txt']:
                continue
            txt_files.append(os.path.join(folder_txt_path, txt_test_name))

            if txt_test_name =='classes.txt':
                continue
            if txt_test_name ==  r'Line_16_OUT_WG_NVR_20251007152833_20251007162834_1094406_700.txt':
                a = 1
            with open(os.path.join(folder_txt_path, txt_test_name), "r") as lines:
                for line in lines:
                    line = line.rstrip('\n')
                    line_list = line.split(' ')
                    cls = line_list[0]
                    center_x = float(line_list[1])
                    center_y = float(line_list[2])
                    width = float(line_list[3])
                    height = float(line_list[4])
                    if width == 0 or height ==0:
                        messagebox.showwarning("警告", txt_test_name + " 中宽高不能为0，请检测处理后再试！")
                        return



        if not txt_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关txt")
            return


        # 显示读取结果（示例：打印到控制台）
        print(f"找到 {len(jpg_files)} 个JPG文件:")
        for file in jpg_files:
            print(file)

        accord_yololabel_crop_image_and_joint(folder_path, folder_txt_path)

        result_str = folder_path
        messagebox.showinfo("提示", "转换完成,保存至:"+result_str)

    def get_files(self,path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files





class PageSix(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="根据裁剪小图修正标签",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 图像文件夹选择相关控件
        # tk.Label(self, text="选择图像文件夹路径:").pack()
        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择裁剪小图文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)





        # 标签文件夹选择相关控件
        # tk.Label(self, text="选择标签文件夹路径:").pack()
        self.entry_txt_path = tk.Entry(self, width=100)
        self.entry_txt_path.pack(pady=40)

        tk.Button(
            self,
            text="选择txt文件夹",
            command=self.browse_folder_txt
        ).pack(pady=20)

        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)
        self.entry_txt_path.delete(0, tk.END)

    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)

    def browse_folder_txt(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_txt_path.delete(0, tk.END)
            self.entry_txt_path.insert(0, folder_selected)


    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        if not folder_path:
            messagebox.showwarning("警告", "请先图像选择文件夹路径")
            return

        folder_txt_path = self.entry_txt_path.get()  # 获取之前选择的文件夹路径
        if not folder_txt_path:
            messagebox.showwarning("警告", "请先选择txt文件夹路径")
            return

        txt_files = []
        txt_test_names = self.get_files(folder_txt_path)
        for txt_test_name in txt_test_names:
            name_tmp, ext_tmp = os.path.splitext(txt_test_name)
            if ext_tmp not in ['.txt']:
                continue
            txt_files.append(os.path.join(folder_txt_path, txt_test_name))


        if not txt_files:
            messagebox.showinfo("提示", "所选文件夹中没有相关txt")
            return


        # # 显示读取结果（示例：打印到控制台）
        # print(f"找到 {len(jpg_files)} 个JPG文件:")
        # for file in jpg_files:
        #     print(file)

        batch_modify_box_class(folder_path, folder_txt_path)

        result_str = folder_txt_path
        messagebox.showinfo("提示", "转换完成,保存至:"+result_str)

    def get_files(self,path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files






class PageSeven(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="数据集划分(图像版)",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 创建主框架
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建左右子框架
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 界面布局
        tk.Label(
            self.left_frame,
            text='''
            输入 目录结构
            my_data/
            ├── line1/
            │   ├── images/       # .jpg 图像
            │   └── labels/      # .txt 标签 + classes.txt
            ├── line2/
            │   ├── images/
            │   └── labels/
            └── ...
            ''',
            font = ("Arial", 8),
            bg = "#fff2e6",
            justify=tk.LEFT  # 添加左对齐参数
        ).pack(fill=tk.BOTH, expand=True)

        # 界面布局
        tk.Label(
            self.right_frame,
            text='''
            输出结果目录结构
            train_and_val_data/
            ├── train/
            │   ├── images/          # 训练图像
            │   └── labels/            # 训练标签
            ├── val/
            │   ├── images/          # 验证图像
            │   └── labels/            # 验证标签
            └── data.yaml           # YOLO 配置文件
                   ''',
            font=("Arial", 8),
            bg="#fff2e6",
            justify=tk.LEFT  # 添加左对齐参数
        ).pack(fill=tk.BOTH, expand=True)



        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择输入数据文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)

        self.train_dataset = tk.Entry(self, width=100)
        self.train_dataset.pack(pady=5)
        label = tk.Label(self, text="训练集数量占比=训练集数量/总数量*100 [0,100]，例如90", font=("Arial", 10))
        label.pack(pady=50)

        self.val_dataset = tk.Entry(self, width=100)
        self.val_dataset.pack(pady=5)
        label = tk.Label(self, text="验证集数量占比=验证集数量/总数量*100 [0,100]，例如10 （注意：训练集+验证集=100）", font=("Arial", 10))
        label.pack(pady=50)


        self.max_linex_num = tk.Entry(self, width=100)
        self.max_linex_num.pack(pady=5)
        label = tk.Label(self, text="每条LineX划分的最多数量，不输入值默认=1000000000000", font=("Arial", 10))
        label.pack(pady=50)

        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)
        self.train_dataset.delete(0, tk.END)
        self.val_dataset.delete(0, tk.END)
        self.max_linex_num.delete(0, tk.END)

    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)

    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        if not folder_path:
            messagebox.showwarning("警告", "请先选择视频文件夹路径")
            return

        folders = self.get_subdirectories(folder_path)
        if folders == []:
            messagebox.showwarning("警告", "所选的路径下无数据")
            return
        else:
            for folder_i in folders:
                folders_sub = self.get_subdirectories(os.path.join(folder_path, folder_i))
                if "images" in folders_sub and "labels" in folders_sub :
                    pass
                else:
                    error_str = os.path.join(folder_path, folder_i)
                    messagebox.showwarning("警告", error_str +"下无图像或标签文件")
                    return

            for folder_i in folders:
                folders_sub = self.get_subdirectories(os.path.join(folder_path, folder_i))

                images_full_path = os.path.join(folder_path, folder_i, "images")
                files_list = self.get_files(images_full_path)
                if files_list == []:
                    messagebox.showwarning("警告", images_full_path +"下无数据")
                    return

                txt_full_path = os.path.join(folder_path, folder_i, "labels")
                txt_list = self.get_files(txt_full_path)
                if txt_list == []:
                    messagebox.showwarning("警告", txt_full_path +"下无数据")
                    return



        train_dataset_ratio = self.train_dataset.get()
        train_dataset_type = self.is_positive_integer(train_dataset_ratio)
        if not train_dataset_type:
            messagebox.showinfo("提示", "训练集占比输入错误")
            return

        val_dataset_ratio = self.val_dataset.get()
        val_dataset_type = self.is_positive_integer(val_dataset_ratio)
        if not val_dataset_type:
            messagebox.showinfo("提示", "验证集占比输入错误")
            return

        max_linex_num = self.max_linex_num.get()
        max_linex_num_type = self.is_positive_integer(max_linex_num)
        if max_linex_num != '':
            if not max_linex_num_type:
                messagebox.showwarning("警告", "LineX最大值输入有问题")
                return
        if max_linex_num !='':
            build_dataset(folder_path,  int(train_dataset_ratio)/100, int(val_dataset_ratio)/100, int(max_linex_num))
        else:
            build_dataset(folder_path, int(train_dataset_ratio) / 100, int(val_dataset_ratio) / 100)

        result_str = folder_path
        messagebox.showinfo("提示", "转换完成,保存至:" + result_str)

    def get_files(self, path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files

    def get_subdirectories(self, folder_path):
        """
        获取指定路径下的所有文件夹名称列表
        参数:
            folder_path (str): 目标路径字符串

        返回:
            list: 包含所有子目录名称的列表（按字母顺序排序）
        """
        try:
            return sorted([entry.name for entry in os.scandir(folder_path) if entry.is_dir()])
        except FileNotFoundError:
            print(f"错误：路径不存在 '{folder_path}'")
            return []
        except PermissionError:
            print(f"错误：无权限访问 '{folder_path}'")
            return []

    def is_positive_integer(self,s):
        """
        判断字符串是否为正整数
        :param s: 输入字符串
        :return: 如果是正整数返回True，否则返回False
        """
        if not s:
            return False
        if s.startswith('0') and len(s) > 1:
            return False
        if s == '0':
            return False
        return s.isdigit()



class PageEight(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 界面布局
        tk.Label(
            self,
            text="数据集划分(标签版)",
            font=("Arial", 24),
            bg="#fff2e6"
        ).pack(pady=20)

        # 创建主框架
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建左右子框架
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 界面布局
        tk.Label(
            self.left_frame,
            text='''
            输入 (众包)目录结构
            众包路径：my_data/
            ├── line1/
            │   ├── images/       # .jpg 图像
            │   └── labels/      # .txt 标签 + classes.txt
            ├── line2/
            │   ├── images/
            │   └── labels/
            └── ...
            ''',
            font = ("Arial", 8),
            bg = "#fff2e6",
            justify=tk.LEFT  # 添加左对齐参数
        ).pack(fill=tk.BOTH, expand=True)

        # 界面布局
        tk.Label(
            self.right_frame,
            text='''
            输出(众包)目录结构
            众包路径：my_data/
            ├── line1/
            │   ├── images/       # .jpg 图像
            │   └── labels/      # .txt 标签 + classes.txt
            ├── line2/
            │   ├── images/
            │   └── labels/
            └── train.txt 、 val.txt           # 生成划分好的（众包）txt文件
                   ''',
            font=("Arial", 8),
            bg="#fff2e6",
            justify=tk.LEFT  # 添加左对齐参数
        ).pack(fill=tk.BOTH, expand=True)



        self.entry_image_path = tk.Entry(self, width=100)
        self.entry_image_path.pack(pady=10)

        tk.Button(
            self,
            text="选择输入（众包）数据文件夹",
            command=self.browse_folder_image
        ).pack(pady=10)

        # 创建主框架
        self.main_frame_dan = tk.Frame(self)
        self.main_frame_dan.pack(fill=tk.BOTH, expand=True)

        # 创建左右子框架
        self.left_frame_dan = tk.Frame(self.main_frame_dan)
        self.left_frame_dan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.right_frame_dan = tk.Frame(self.main_frame_dan)
        self.right_frame_dan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 界面布局
        tk.Label(
            self.left_frame_dan,
            text='''
                  输入 (单包)目录结构
                  单包路径：my_data/
                      ├── images/       # .jpg 图像
                      └── labels/      # .txt 标签 + classes.txt
                  ''',
            font=("Arial", 8),
            bg="#fff2e6",
            justify=tk.LEFT  # 添加左对齐参数
        ).pack(fill=tk.BOTH, expand=True)

        # 界面布局
        tk.Label(
            self.right_frame_dan,
            text='''
                  输出(单包)目录结构
                  单包路径：my_data/
                      ├── images/       # .jpg 图像
                      └── labels/      # .txt 标签 + classes.txt
                      └── train.txt 、 val.txt           # 生成划分好的（单包）txt文件
                  ''',
            font=("Arial", 8),
            bg="#fff2e6",
            justify=tk.LEFT  # 添加左对齐参数
        ).pack(fill=tk.BOTH, expand=True)

        self.entry_image_path_dan = tk.Entry(self, width=100)
        self.entry_image_path_dan.pack(pady=10)

        tk.Button(
            self,
            text="选择输入（单包）数据文件夹",
            command=self.browse_folder_image_dan
        ).pack(pady=10)

        self.train_dataset = tk.Entry(self, width=100)
        self.train_dataset.pack(pady=5)
        label = tk.Label(self, text="训练集数量占比=训练集数量/总数量*100 [0,100]，例如90", font=("Arial", 10))
        label.pack(pady=50)

        self.val_dataset = tk.Entry(self, width=100)
        self.val_dataset.pack(pady=5)
        label = tk.Label(self, text="验证集数量占比=验证集数量/总数量*100 [0,100]，例如10 （注意：训练集+验证集=100）", font=("Arial", 10))
        label.pack(pady=50)


        # 新增JPG读取按钮
        tk.Button(
            self,
            text="开始（众包/单包）处理",
            command=self.process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).pack(pady=20)

        # 创建清空按钮
        self.clear_button = tk.Button(
            self,
            text="Clear",
            command=self.clear_entry
        )
        self.clear_button.pack(pady=5)

    def clear_entry(self):
        """清空Entry控件内容"""
        self.entry_image_path.delete(0, tk.END)
        self.entry_image_path_dan.delete(0, tk.END)
        self.val_dataset.delete(0, tk.END)
        self.train_dataset.delete(0, tk.END)

    def browse_folder_image(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, folder_selected)

    def browse_folder_image_dan(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory(
            title="请选择文件夹",
            mustexist=True
        )
        if folder_selected:
            self.entry_image_path_dan.delete(0, tk.END)
            self.entry_image_path_dan.insert(0, folder_selected)

    def process(self):
        """读取所选文件夹中的JPG文件"""
        folder_path = self.entry_image_path.get()  # 获取之前选择的文件夹路径
        folder_path_dan = self.entry_image_path_dan.get()

        if  folder_path =='' and folder_path_dan=='':
            messagebox.showwarning("警告", "请先选择众包/单包数据路径")
            return

        if folder_path != '':
            folders = self.get_subdirectories(folder_path)
            if folders == []:
                messagebox.showwarning("警告", "所选的路径下无数据")
                return
            else:
                for folder_i in folders:
                    folders_sub = self.get_subdirectories(os.path.join(folder_path, folder_i))
                    if "images" in folders_sub and "labels" in folders_sub :
                        pass
                    else:
                        error_str = os.path.join(folder_path, folder_i)
                        messagebox.showwarning("警告", error_str +"下无图像或标签文件")
                        return

                for folder_i in folders:
                    folders_sub = self.get_subdirectories(os.path.join(folder_path, folder_i))

                    images_full_path = os.path.join(folder_path, folder_i, "images")
                    files_list = self.get_files(images_full_path)
                    if files_list == []:
                        messagebox.showwarning("警告", images_full_path +"下无数据")
                        return

                    txt_full_path = os.path.join(folder_path, folder_i, "labels")
                    txt_list = self.get_files(txt_full_path)
                    if txt_list == []:
                        messagebox.showwarning("警告", txt_full_path +"下无数据")
                        return
        else:
            images_full_path_dan = os.path.join(folder_path_dan,  "images")
            if not os.path.isdir(images_full_path_dan):
                messagebox.showwarning("警告", images_full_path_dan + "下无images数据")
                return
            files_list_dan = self.get_files(images_full_path_dan)
            if files_list_dan == []:
                messagebox.showwarning("警告", images_full_path_dan + "下无数据")
                return
            txt_full_path_dan = os.path.join(folder_path_dan,  "labels")
            if not os.path.isdir(txt_full_path_dan):
                messagebox.showwarning("警告", txt_full_path_dan + "下无txt数据")
                return
            txt_list_dan = self.get_files(txt_full_path_dan)
            if txt_list_dan == []:
                messagebox.showwarning("警告", txt_full_path_dan + "下无数据")
                return


        train_dataset_ratio = self.train_dataset.get()
        train_dataset_type = self.is_positive_integer(train_dataset_ratio)
        if not train_dataset_type:
            messagebox.showwarning("出错", "训练集占比输入错误")
            return

        val_dataset_ratio = self.val_dataset.get()
        val_dataset_type = self.is_positive_integer(val_dataset_ratio)
        if not val_dataset_type:
            messagebox.showwarning("出错", "验证集占比输入错误")
            return

        train_dataset_ratio_float = float(train_dataset_ratio)
        val_dataset_ratio_float = float(val_dataset_ratio)
        train_add_val = train_dataset_ratio_float + val_dataset_ratio_float
        if train_add_val != 100:
            messagebox.showwarning("出错", f"{train_dataset_ratio} + {val_dataset_ratio} != 100")
            return

        if folder_path != '':
            dataset_process_random_zhongbao(folder_path, int(train_dataset_ratio), int(val_dataset_ratio))
            result_str = folder_path
        else:
            dataset_process_random_danbao(folder_path_dan, int(train_dataset_ratio), int(val_dataset_ratio))
            result_str = folder_path_dan
        messagebox.showinfo("提示", "转换完成,保存至:" + result_str)

    def get_files(self, path):
        files = []
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                files.append(filename)
        return files

    def get_subdirectories(self, folder_path):
        """
        获取指定路径下的所有文件夹名称列表
        参数:
            folder_path (str): 目标路径字符串

        返回:
            list: 包含所有子目录名称的列表（按字母顺序排序）
        """
        try:
            return sorted([entry.name for entry in os.scandir(folder_path) if entry.is_dir()])
        except FileNotFoundError:
            print(f"错误：路径不存在 '{folder_path}'")
            return []
        except PermissionError:
            print(f"错误：无权限访问 '{folder_path}'")
            return []

    def is_positive_integer(self,s):
        """
        判断字符串是否为正整数
        :param s: 输入字符串
        :return: 如果是正整数返回True，否则返回False
        """
        if not s:
            return False
        if s.startswith('0') and len(s) > 1:
            return False
        if s == '0':
            return False
        return s.isdigit()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
