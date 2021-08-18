from scripts.metadata.metadataExtractor import process_video_files
from scripts.splitVideo import split_video
from scripts.metadata import metadataCreator
import exiftool
import os
import shutil

from scripts.paths import Paths


def clear_output_directories():
    print('Clearing output directories')
    for path in os.listdir(str(Paths.OUTPUT_DIR)):
        shutil.rmtree(str(Paths.OUTPUT_DIR) + path)
    make_subdirectories()


def make_subdirectories():
    os.mkdir(str(Paths.VIDEO_CAMERA_METADATA_JSON_OUTPUT))
    os.mkdir(str(Paths.VIDEO_FRAMES_OUTPUT))
    os.mkdir(str(Paths.IMAGE_METADATA_JSON_OUTPUT))
    os.mkdir(str(Paths.FRAME_SUBTITLES))


def make_all_directories():
    os.mkdir(str(Paths.OUTPUT_DIR))
    os.mkdir(str(Paths.INPUT_DIR))
    os.mkdir(str(Paths.VIDEOS_INPUT))
    os.mkdir(str(Paths.IMAGES_INPUT))
    os.mkdir(str(Paths.SUBTITLES))
    make_subdirectories()


def grab_all_frames(path_from, path_into):
    count = 1
    for folder in os.listdir(path_from):
        for file in os.listdir(path_from + folder):
            old_file = path_from + folder + '/' + file
            new_file = path_into + '{filename}.jpg'.format(filename=count)
            shutil.copy(old_file, new_file)
            count += 1


def convert_videos_to_frames(path_to_videos, path_to_frames_output, path_to_camera_metadata_output):
    clear_output_directories()
    with exiftool.ExifTool() as et:
        video_metadata = et.get_metadata_batch([path_to_videos])
        print('Fetched video metadata for pipeline')

    process_video_files(video_metadata, path_to_videos, path_to_camera_metadata_output)
    split_video(path_to_videos, path_to_frames_output)
    metadataCreator.fetch_and_bind_metadata_to_frames(path_to_videos)


