# yolo_tools
关于YOLO周边的一些使用小工具

功能：
1.批量修改标签类别。 支持把txt中的所有box类别统一修改成指定类别，同时支持把某几类修改成指定类别；
2.根据txt筛选图像。 将txt同名的.png、.jpg、.bmp筛选出来；
3.负样本生成空txt。 根据图像生成对应的同名空txt；
4.视频拆帧。支持将视频文件按照每n帧取一帧的方式，拆帧成图像格式。支持设置拆帧上限；
5.根据标签裁剪图像小图。按照图像和标注好的txt标签，裁剪出小图，并按照类别整理；
6.根据小图修正标签。 支持对裁剪小图进行删除，修改类别等修正操作，来反向修正txt标签；
7.数据集划分。支持处理众包/单包数据，支持生成图像格式和txt格式。


exe生成方式：
方法1：   pyinstaller --onefile --hidden-import=模块1 --hidden-import=模块2 --hidden-import=模块3 主函数文件名.py
方法2：  首先生成基础.spec文件：
pyinstaller --onefile 主函数文件名.py
编辑生成的主函数文件名.spec文件，在Analysis部分的hiddenimports列表中添加所有模块：
a = Analysis(
    ['主函数文件名.py'],
    hiddenimports=['模块1', '模块2', '模块3'],  # 在此处集中添加
    ...
)
重新打包时直接使用.spec文件：
pyinstaller 主函数文件名.spec
