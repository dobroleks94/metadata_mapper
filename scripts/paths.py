from enum import Enum


class Paths(Enum):
    OUTPUT_DIR = './output/'
    INPUT_DIR = './input/'
    VIDEOS_INPUT = './input/videos/'
    IMAGES_INPUT = './input/images/'
    SUBTITLES = './input/video-subtitles/'
    IMAGE_METADATA_JSON_OUTPUT = './output/image-result/'
    VIDEO_CAMERA_METADATA_JSON_OUTPUT = './output/video-result/'
    VIDEO_FRAMES_OUTPUT = './output/video-frames/'
    FRAME_SUBTITLES = './output/frame-subtitles/'

    def __str__(self):
        return self.value

