from .subtitles import Subtitles
from .extensions import Extensions
import re
import datetime


def read_lines(filename):
    file = open(filename, 'r')
    return file.readlines()


def grab_lines_to_text_obj(lines):
    obj_list = []
    text = ''
    for line in lines:
        if line == '\n':
            obj_list.append(text)
            text = ''
            continue
        text = text + str(line)
    return obj_list


def get_subtitle_object(text_obj, extension):
    pattern_srt = '(?P<frame_numb>\d+)(\n)(((\d{2}\:){2}(\d{2},\d{3}))(\s\-{2}\>\s)((\d{2}\:){2}(\d{2},\d{3}))\n)(?P<date>\d{4}\.\d{2}\.\d{2})(\s)(?P<time>(\d{2}\:){2}\d{2})(\n)(GPS\()((?P<lat>\d+\.\d+)(\,))((?P<lon>\d+\.\d+)(\,))((?P<alt>\d+\.\d+)(M))(\))(\s)((BAROMETER:)((?P<barometer>\d+\.\d+)(M)))'
    pattern_SRT = '(?P<frame_numb>\d+)(\n)(((\d{2}\:){2}(\d{2}\,\d{3}))(\s\-{2}\>\s)((\d{2}\:){2}(\d{2}\,\d{3}))\n)(\<font size\=\"\d+\"\>FrameCnt\s*\:\s\d+\,\sDiffTime\s*\:\s\d+ms\n)((?P<date>\d{4}\-\d{2}\-\d{2})(\s)(?P<time>(\d{2}\:){2}\d{2})(\,\d+\,\d+)\n)((\[iso\s\:\s\d+\])\s(\[shutter\s\:\s\d+\/\d+\.\d+\])\s(\[fnum\s\:\s\d+\])\s(\[ev\s\:\s\d+\])\s(\[ct\s\:\s\d+\])\s(\[color_md\s\:\s[A-Za-z]+\])\s(\[focal_len\s\:\s\d+\])\s(\[latitude\s\:\s(?P<lat>\d+\.+\d+)\])\s((\[longtitude\s\:\s(?P<lon>\d+\.+\d+)\]))\s(((\[altitude\:\s(?P<alt>\d+\.+\d+)\])))\s)(\<\/font\>)'
    pattern_SRT2= '(?P<frame_numb>\d+)(\n)(((\d{2}\:){2}(\d{2}\,\d{3}))(\s\-{2}\>\s)((\d{2}\:){2}(\d{2}\,\d{3}))\n)(\<font size\=\"\d+\"\>FrameCnt\s*\:\s\d+\,\sDiffTime\s*\:\s\d+ms\n)((?P<date>\d{4}\-\d{2}\-\d{2})(\s)(?P<time>(\d{2}\:){2}\d{2})(\,\d+\,\d+)\n)((\[color_md\s*\:\s[A-Za-z]+\])\s(\[latitude\s*\:\s(?P<lat>\d+\.+\d+)\])\s((\[longtitude\s*\:\s(?P<lon>\d+\.+\d+)\]))\s(((\[rel_alt\:\s*(\d+\.+\d+))\s(abs_alt\:\s*(\d+\.+\d+)\])))\s(\[Drone:(\s*[A-Za-z]+:\-*\d+\.\d+(\,|\]))+)\s\<\/font)' 
    match = re.search(pattern_srt if extension == Extensions.srt else pattern_SRT, text_obj)
    date = [int(i) for i in re.split(pattern="[.-]", string=match.group('date'))]
    time = [int(i) for i in re.split(pattern=":", string=match.group('time'))]
    return Subtitles(
        int(match.group('frame_numb')),
        datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2]),
        float(match.group('lat')),
        float(match.group('lon')),
        float(match.group('alt'))
    )


def parse_subtitles_file(file_name):
    lineList = read_lines(file_name)
    text_obj = grab_lines_to_text_obj(lineList)
    extension = re.search("(?P<extension>\.[A-Za-z]{3})", file_name).group("extension")
    return [get_subtitle_object(text, Extensions(extension)) for text in text_obj]
