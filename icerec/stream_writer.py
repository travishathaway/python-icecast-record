import requests, time
from pprint import pprint
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from datetime import datetime

class StreamWriter(object):
    """
    server_url:
        url of the icecast radio stream

    file_size:
        used to keep track of the file size

    bitrate:
        used in conjuction with file_size to calculate
        the playing length in seconds

    stream_length: 
        playing length of file in seconds

    metadata:
        HTTP headers we get from the icecast server

    timestamp:
        Used to help give the files unique names.
    """

    server_url = ''
    file_size = 0.0
    bitrate = 128.0
    stream_length = 0.0
    metadata = {}
    timestatmp = ''

    def __init__(self, server_url, seconds, destination='./', filename='output.mp3'):
        self.server_url = server_url
        self.seconds = seconds
        self.destination = destination
        self.filename = filename

    def record(self):
        """
        This method records the file stream until the stream_length has been reached
        """
        self.timestatmp = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')

        while True:
            with open(self.destination+self.filename, 'wb') as handle:
                request = requests.get(self.server_url, stream=True)
                self.metadata = request.headers

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
        self.write_metadata()

        return True

    def write_metadata(self):
        """
        This method adds metadata to the stream file
        """
        mp3 = MP3(self.destination+self.filename, ID3=EasyID3)

        mp3['title'] = self.metadata.get('icy-name')+' '+self.timestatmp
        mp3['genre'] = self.metadata.get('icy-genre')
        mp3['artist'] = 'Various Artists'

        mp3.save()

    def calc_length(self):
        self.stream_length = ( ( self.file_size/1024.0 ) * 8.0 )/128.0
