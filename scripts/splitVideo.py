import os
import shutil
import cv2


def get_frame(second, video, path, count):
    video.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
    hasFrames, image = video.read()
    if hasFrames:
        cv2.imwrite(path + '/' + str(count + 1) + ".jpg", image)
    return hasFrames


def get_video_duration(file_name):
    video = cv2.VideoCapture(file_name + os.listdir(file_name)[1])
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    return frame_count / fps


def make_dir_for_frames(file_name, output_path):
    subdir = file_name[0:file_name.find('.')]
    directory = output_path + subdir
    if not os.path.isdir(directory):
        os.mkdir(directory)
    return directory


def increment(count, sec):
    count += 1
    sec += 1
    return count, sec


def split_video(input, output):
    for file_name in os.listdir(input):
        print('Splitting video {}'.format(file_name[0:file_name.find('.')]))
        path_to_dir = make_dir_for_frames(file_name, output)
        count, sec = 0, 0

        video = cv2.VideoCapture(input + file_name)
        success = get_frame(sec, video, path_to_dir, count)
        count, sec = increment(count, sec)
        while success:
            success = get_frame(sec, video, path_to_dir, count)
            count, sec = increment(count, sec)
