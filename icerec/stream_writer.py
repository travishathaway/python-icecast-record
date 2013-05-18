import requests, time
from pprint import pprint

class StreamWriter(object):

    server_url = ''
    file_size = 0.0
    bitrate = 128.0
    stream_length = 0.0
    meta_data = {}

    def __init__(self, server_url, seconds, destination='./', filename='output.mp3'):
        self.server_url = server_url
        self.seconds = seconds
        self.destination = destination
        self.filename = filename

    def record(self):
        while True:
            with open(self.destination+self.filename, 'wb') as handle:
                request = requests.get(self.server_url, stream=True)
                self.meta_data = request.headers

                for block in request.iter_content(1024):
                    self.file_size += 1024.0

                    if ( ( self.file_size/1024.0 ) * 8.0 ) / self.bitrate > self.seconds:
                        break_it_boy = True
                        break

                    if not block:
                        break

                    handle.write(block)

                if break_it_boy:
                    break

            if break_it_boy:
                break

        self.calc_length()

        return True

    def calc_length(self):
        self.stream_length = ( ( self.file_size/1024.0 ) * 8.0 )/128.0
