from scripts import UtilsFunctions
from scripts.paths import Paths

if __name__ == '__main__':
    # UtilsFunctions.make_all_directories()

    # UtilsFunctions.grab_all_frames(str(Paths.VIDEO_FRAMES_OUTPUT),
    #                                str(Paths.IMAGE_METADATA_JSON_OUTPUT))
    UtilsFunctions.convert_videos_to_frames(str(Paths.VIDEOS_INPUT),
                                            str(Paths.VIDEO_FRAMES_OUTPUT),
                                            str(Paths.VIDEO_CAMERA_METADATA_JSON_OUTPUT))
