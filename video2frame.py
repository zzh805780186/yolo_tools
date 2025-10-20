import cv2
import os
# import argparse
# import ffmpegcv




def video2frame(videos_path,frames_save_path,time_interval, entry_frame_num):
 
  '''
  :param videos_path: 视频的存放路径
  :param frames_save_path: 视频切分成帧之后图片的保存路径
  :param time_interval: 保存间隔
  :return:
  '''
  vidcap = cv2.VideoCapture(videos_path)
  #vidcap = ffmpegcv.VideoCaptureNV(videos_path)
  success, image = vidcap.read()
  count = 0
  entry_frame_num_counte = 0


  while success:
    # vidcap.set(cv2.CAP_PROP_POS_FRAMES, time_interval)
    success, image = vidcap.read()
    #image = cv2.rotate(image, cv2.ROTATE_180)

    if success is not True:
      continue
    count += 1
    if count % time_interval == 0:
    # if 1:
      #print(count)
      print(videos_path , '   ', str(count))
      entry_frame_num_counte += 1
      if entry_frame_num == '':
        pass
      else:
        if entry_frame_num_counte > int(entry_frame_num):
          break

      #以  framexxx.jpg名字保存
      #cv2.imencode('.jpg', image)[1].tofile(frames_save_path + "/frame%d.jpg" % count)

      base_name = os.path.split(frames_save_path)[1]
      #cv2.imencode('.jpg', image)[1].tofile(frames_save_path + '/'+base_name + "/frame%d.jpg" % count)
      #cv2.imencode('.jpg', image)[1].tofile('F:\data\customer_complaint\customer_data' + r'\' + base_name + "/frame%d.jpg" % count)
      #cv2.imencode('.jpg', image)[1].tofile(os.path.join('F:\data\customer_complaint\customer_data'  , base_name + "_frame%d.jpg" % count))

      #cv2.imencode('.jpg', image)[1].tofile(frames_save_path + '/' + base_name + "_frame%d.jpg" % count)

      cv2.imencode('.jpg', image)[1].tofile(frames_save_path + '/' + base_name + "_" + "%d.jpg" % count)
      #cv2.imencode('.jpg', image)[1].tofile(frames_save_path + '/' +   "%d.jpg" % count)

  print(count)


 
def read_videos(videos_path, time_interval, entry_frame_num):
 
  # videos_path = opt.videos_path
  # time_interval = opt.time_interval
  # frames_save_path = opt.save_path

  frames_save_path = os.path.join(videos_path,'frame')

  if not os.path.exists(frames_save_path):
    os.makedirs(frames_save_path)

  if not os.path.exists(videos_path):
    print('This video path is not exist!')
    return
  else:
    videos_lists = os.listdir(videos_path)
    for video in videos_lists:
      print('开始处理:{}'.format(video))
      base_name , ext = os.path.splitext(video)
      if ext not in ['.mp4','.avi']:
        continue

      #base_name=os.path.splitext(video)[0]
      if not os.path.exists(os.path.join(frames_save_path ,base_name)):
        os.makedirs(os.path.join(frames_save_path ,base_name))

      video2frame(os.path.join(videos_path,video),os.path.join(frames_save_path ,base_name),time_interval ,entry_frame_num)

      print('完成:{}'.format(os.path.join(videos_path, video)))
    




# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#
#
#     parser.add_argument('--videos_path', type=str, default=r'D:\Program Files (x86)\iVMS-4200 Site\UserData\Video\Line_8_产出_TH1_TH1_20250915095424', help='*.video path')
#     parser.add_argument('--time_interval', type=str, default=30, help='every time catch one frame')
#     parser.add_argument('--save_path', type=str, default=r'D:\Program Files (x86)\iVMS-4200 Site\UserData\Video\Line_8_产出_TH1_TH1_20250915095424', help='output path')
#
#     opt = parser.parse_args()
#
#     read_videos()


