from scripts.metadata.metadataExtractor import process_video_files
from scripts.splitVideo import split_video
from scripts.paths import Paths
from scripts.metadata import metadataCreator
import exiftool
import os
import shutil


def make_subdirs():
    os.mkdir(str(Paths.VIDEO_CAMERA_METADATA_JSON_OUTPUT))
    os.mkdir(str(Paths.VIDEO_FRAMES_OUTPUT))
    os.mkdir(str(Paths.IMAGE_METADATA_JSON_OUTPUT))
    os.mkdir(str(Paths.FRAME_SUBTITLES))


def clear_output_directories():
    print('Clearing output directories')
    for path in os.listdir(str(Paths.OUTPUT_DIR)):
        shutil.rmtree(str(Paths.OUTPUT_DIR) + path)
    make_subdirs()


if __name__ == '__main__':

    # count = 1
    # for folder in os.listdir(str(Paths.VIDEO_FRAMES_OUTPUT)):
    #     for file in os.listdir(str(Paths.VIDEO_FRAMES_OUTPUT) + folder):
    #         old_file = str(Paths.VIDEO_FRAMES_OUTPUT) + folder + '/' + file
    #         new_file = str(Paths.IMAGE_METADATA_JSON_OUTPUT) + '{filename}.jpg'.format(filename=count)
    #         shutil.copy(old_file, new_file)
    #         count += 1

    clear_output_directories()
    with exiftool.ExifTool() as et:
        video_metadata = et.get_metadata_batch([str(Paths.VIDEOS_INPUT)])
        print('Fetched video metadata for pipeline')

    process_video_files(video_metadata, str(Paths.VIDEOS_INPUT), str(Paths.VIDEO_CAMERA_METADATA_JSON_OUTPUT))
    split_video(str(Paths.VIDEOS_INPUT), str(Paths.VIDEO_FRAMES_OUTPUT))
    metadataCreator.fetch_and_bind_metadata_to_frames(str(Paths.VIDEOS_INPUT))

