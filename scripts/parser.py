import datetime

from .subtitles import Subtitles
import re


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


def get_subtitle_object(text_obj):
    pattern = '(?P<frame_numb>\d+)(\n)(((\\d{2}\:){2}(\d{2},\d{3}))(\s\-{2}\>\s)((\d{2}\:){2}(\d{2},\d{3}))\n)(?P<date>\d{4}\.\d{2}\.\d{2})(\s)(?P<time>(\d{2}\:){2}\d{2})(\n)(GPS\()((?P<lat>\d+\.\d+)(\,))((?P<lon>\d+\.\d+)(\,))((?P<alt>\d+\.\d+)(M))(\))(\s)((BAROMETER:)((?P<barometer>\d+\.\d+)(M)))'
    match = re.search(pattern, text_obj)
    date = [int(i) for i in match.group('date').split('.')]
    time = [int(i) for i in match.group('time').split(':')]
    return Subtitles(
        int(match.group('frame_numb')),
        datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2]),
        float(match.group('lat')),
        float(match.group('lon')),
        float(match.group('alt')),
        float(match.group('barometer'))
    )


def parse_subtitles_file(file_name):
    lineList = read_lines(file_name)
    text_obj = grab_lines_to_text_obj(lineList)
    return [get_subtitle_object(text) for text in text_obj]