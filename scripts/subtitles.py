class Subtitles:

    def __init__(self, frame_number, datetime, latitude, longitude, altitude):
        self.frame_number = frame_number
        self.datetime = datetime
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = altitude
        # self.barometer = barometer
