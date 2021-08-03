import json
import os
import piexif
from scripts.paths import Paths
from .cameraData import CameraDataFields
from ..parser import parse_subtitles_file
from PIL import Image


def to_deg(value, loc):
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
    return deg, min, sec, loc_value


def get_exif_lat_long(latitude, longitude):
    exiv_lat = ((int(latitude[0]*60+latitude[1]), 60), (int(latitude[2]*100), 6000), (0, 1))
    exiv_lng = ((int(longitude[0]*60+longitude[1]), 60), (int(longitude[2]*100), 6000), (0, 1))
    return {"latitude": exiv_lat, "longitude": exiv_lng}


def create_metadata_map(subtitle, camera_data):
    camera_metadata = json.dumps(camera_data)
    # image_ifd = {
    #     piexif.ImageIFD.CameraCalibration1: float(camera_data[CameraDataFields.YAW.value]),
    #     piexif.ImageIFD.CameraCalibration2: float(camera_data[CameraDataFields.PITCH.value])
    # }
    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: str(subtitle.datetime),
        piexif.ExifIFD.LensModel: camera_data[CameraDataFields.CAMERA_MODEL.value],
        piexif.ExifIFD.UserComment: camera_metadata.encode('ascii')
    }
    lat_deg = to_deg(subtitle.latitude, ["South", "North"])
    lng_deg = to_deg(subtitle.longitude, ["West", "East"])
    gps_coordinates = get_exif_lat_long(lat_deg, lng_deg)
    gps_ifd = {
        piexif.GPSIFD.GPSAltitude: int(subtitle.altitude).as_integer_ratio(),
        piexif.GPSIFD.GPSLongitude: gps_coordinates["longitude"],
        piexif.GPSIFD.GPSLatitude: gps_coordinates["latitude"],
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3]
    }
    return {"exif": exif_ifd, "gps": gps_ifd}


def fetch_and_bind_metadata_to_frames(input_folder):
    for file in os.listdir(input_folder):
        file_name = file[0:file.find('.')]
        print('Processing frames for {}'.format(file_name))
        print('------------------------------')
        camera_metadata = get_json_camera_metadata(file_name)
        subtitles = get_frames_subtitles(file_name)
        exifmetadata = frame_metadata_map(camera_metadata, subtitles)
        bind_metadata_to_frame_img(exifmetadata, file_name)
        print('------------------------------')


def bind_metadata_to_frame_img(exifmetadata, file_name):
    print('Binding metadata to frames ({} frames)'.format(len(exifmetadata.items())))
    for frame, data in exifmetadata.items():
        image_path = str(Paths.VIDEO_FRAMES_OUTPUT) + file_name + '/{image_name}.jpg'
        exif_dict = {"Exif": data["exif"], "GPS": data["gps"]}
        exif_bytes = piexif.dump(exif_dict)
        try:
            image = Image.open(image_path.format(image_name=frame))
            image.save(image_path.format(image_name=frame), exif=exif_bytes)
        except:
            print("Redundant frames where skipped for {}".format(file_name))


def frame_metadata_map(camera_metadata, subtitles):
    print('Converting subtitles to frame metadata --> binding camera metadata')
    exifmetadata = {}
    for subtitle in subtitles:
        exifmetadata[subtitle.frame_number] = create_metadata_map(subtitle, camera_metadata)
    return exifmetadata


def get_frames_subtitles(file_name):
    print('Getting video subtitles to process')
    subtitles_input = str(Paths.SUBTITLES) + "{subtitles}.srt"
    subtitles = parse_subtitles_file(subtitles_input.format(subtitles=file_name))
    return subtitles


def get_json_camera_metadata(file_name):
    print('Uploading camera metadata')
    json_md_path = str(Paths.VIDEO_CAMERA_METADATA_JSON_OUTPUT) + "{filename}.json"
    camera_metadata = json.load(open(json_md_path.format(filename=file_name)))
    return camera_metadata
