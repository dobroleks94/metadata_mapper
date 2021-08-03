import os.path
import json
from .cameraData import CameraDataFields


def extract_metadata(metadata):
    print('Extracting and mapping metadata')
    metadata_map = {}
    for key, value in metadata.items():
        metadata_map[key] = value
    return metadata_map


def grab_camera_data(metadata, fields):
    camera_data_map = {}
    print('Filtering metadata with camera info')
    for k, v in metadata:
        if ('QuickTime' in k) and (k.split(':')[1] in fields):
            camera_data_map[str(k).replace('QuickTime:', '')] = str(v)
    return camera_data_map


def create_metadata_json(file, data, outfilepath, metadata):
    print('Saving camera metadata')
    shortFileName = get_file_name(file, metadata)
    output = outfilepath + '{filename}.json'
    with open(output.format(filename=shortFileName), "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_file_name(file, metadata):
    shortFileName = os.path.basename(metadata['SourceFile'].replace(file, ""))
    shortFileName = shortFileName[0:shortFileName.find('.')]
    return shortFileName


def process_video_files(metadata_list, videos, outpath):
    for md in metadata_list:
        print('Processing video {video}'.format(video=get_file_name(videos, md)))
        print('------------------------------')
        metadata_map = extract_metadata(md)
        fieldsList = [f.value for f in CameraDataFields]
        camera_data_map = grab_camera_data(metadata=metadata_map.items(), fields=fieldsList)
        create_metadata_json(file=videos, data=camera_data_map, outfilepath=outpath, metadata=md)
        print('------------------------------')


def process_image_files(metadata_list, images, outpath):
    for md in metadata_list:
        metadata_map = extract_metadata(md)
        create_metadata_json(file=images, data=metadata_map, outfilepath=outpath, metadata=md)

