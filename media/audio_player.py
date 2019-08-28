import json
import re
import typing

import pafy
import vlc


class AudioClient:
    """
    example usage::

        audio = AudioClient('audio/song1.mp3')
        audio.play()
        while True:
            a = input('a')
            if a == 'p':
                audio.pause()
            elif a == 's':
                audio.stop()
            elif a == 'r':
                audio.play()
            elif a == 'n':
                audio.stop()
                song = input('URL: ')
                audio.new_song(song)
                audio.play()
    """
    file_name = None

    def __init__(self, file_name: str):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.new_song(file_name)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def new_song(self, file_name):
        self._handle_filename(file_name)
        self.player.set_mrl(self.file_name)

    def _handle_filename(self, file_name):
        if re.match('https://', file_name) or 'http://' in file_name:
            self.file_name = pafy.new(file_name).getbest().url
        else:
            self.file_name = file_name


class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)


class PlayList:
    __metaclass__ = GetAttr

    def __init__(self, filenames: typing.List):
        self.__dict__ = {num: filename for num, filename in enumerate(filenames)}
        self.index = 0

    @classmethod
    def parse_from_file(cls, filename: str) -> 'PlayList':
        if '.json' not in filename:
            raise Exception('file format wrong')

        with open(filename, 'r') as file:
            content = file.read()
            content = json.loads(content)

        content = content.get('songs', [])

        return cls(content)

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def __getitem__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            raise StopIteration
