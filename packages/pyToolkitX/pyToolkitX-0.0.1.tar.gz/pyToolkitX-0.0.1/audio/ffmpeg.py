#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 10:45 AM
# @Author  : wangdongming
# @Site    : 
# @File    : ffmpeg.py
# @Software: Hifive
import os
import re
from assents.utils import popen


class FFmpeg(object):

    def __init__(self, converter=None):
        self.ffmpeg = converter or 'ffmpeg'

    def check_ex(self, filename, extension):
        _, ex = os.path.splitext(filename)
        return ex.lstrip('.').lower() == extension.lstrip('.').lower()

    def is_pcm(self, filename):
        return self.check_ex(filename, 'pcm')

    def normdb(self, src, dst, ar=44100):
        _, ex = os.path.splitext(os.path.basename(dst))
        ex = ex.lower()
        if ex.endswith('wav'):
            acodec = "pcm_s16le"
        elif ex.endswith("mp3"):
            acodec = "libmp3lame"
        else:
            raise TypeError(f"This format:{ex} is not supported.")
        conversion_command = [
            "ffmpeg-normalize",
            "-f", src,
            "-nt", "peak",
            "-vn",
            "-ar", str(ar),
            "-c:a", acodec,
            "-o", dst
        ]
        return popen(conversion_command)

    def convert2wav(self, src_path, dst_path, ac=2, ar=44100):
        # cmd = '%s -y -loglevel error -vn -i %s %s'%(self.ffmpeg, src_path, dst_path)
        conversion_command = [
            self.ffmpeg,
            "-vn",
            "-y",
            "-loglevel", "error",
        ]
        if self.is_pcm(src_path):
            conversion_command.extend([
                '-f', 's16be',
                '-acodec', 'pcm_s16be',
            ])
        conversion_command.extend([
            "-i", src_path,
            "-ar", str(ar),
            "-ac", str(ac),
            dst_path
        ])
        return popen(conversion_command)

    def convert2mp3(self, src_path, dst_path, ac=2, br=320):
        conversion_command = [
            self.ffmpeg,
            "-y",
            "-loglevel", "error",
        ]
        conversion_command.extend([
            "-i", src_path,
            "-ac", str(ac),
            "-ab", "{}k".format(br),
            dst_path
        ])
        return popen(conversion_command)

    def convert2aac(self, src_path, dst_path, br=64, ar=44100):
        conversion_command = [
            self.ffmpeg,
            "-y",
            "-loglevel", "error",
        ]
        conversion_command.extend([
            "-i", src_path,
            '-acodec', 'aac',
            "-ab", "{}k".format(br),
            '-ar', str(ar),
            dst_path
        ])
        return popen(conversion_command)

    def detect_media_info(self, filename, fetch_key=None):
        cmd = [
            self.ffmpeg,
            "-i",
            filename
        ]
        p_code, p_out, p_err = popen(cmd)
        if fetch_key and callable(fetch_key):
            if isinstance(p_err, bytes):
                p_err = p_err.decode('utf8')
            return fetch_key(p_err)
        return p_err

    def media_duration(self, filename):

        def search_dur(info):
            m = re.search("Duration:\s*([\d.]+):([\d.]+):([\d.]+),", info)
            dur = 0
            if m:
                hours = float(m.group(1))
                minutes = float(m.group(2))
                seconds = float(m.group(3))
                dur = seconds + minutes * 60 + hours * 60 * 60
            return dur

        dur = self.detect_media_info(filename, search_dur)
        return dur

    def format_audio_info(self, filename):

        def format_info(info):
            ms = re.search("Audio:(.+?),\s+(\d+)\s+Hz,\s+(\w+),\s+(\w+),\s+(\w+)", info)
            if ms:
                return {
                    'format': ms.group(1),
                    'samplerate': ms.group(2),
                    'channel': 1 if 'mono' == ms.group(3) else 2,
                    'bitdepth': ms.group(4),
                    "bitrate": ms.group(5)
                }

        return self.detect_media_info(filename, format_info)

    def audio_samplerate(self, filename):

        def search_samplerate(info):
            m = re.search("Audio:.+?(\d+)\s+Hz", info)
            samplerate = 0
            if m:
                samplerate = int(m.group(1))
            return samplerate

        return self.detect_media_info(filename, search_samplerate)

    def resample(self, src_path, dst_path, ar):
        conversion_command = [
            self.ffmpeg,
            "-y",
            "-loglevel", "error",
        ]
        conversion_command.extend([
            "-i", src_path,
            "-ar", str(ar),
            dst_path
        ])
        return popen(conversion_command)

    @staticmethod
    def extract_cover(filename):
        _, ex = os.path.splitext(filename)
        if ex.lower().lstrip('.') not in ("mp3", "flac", "m4a", "mp4"):
            raise TypeError(f"cannot support this file extension:{ex}.")
        from mutagen import File
        from mutagen.mp4 import MP4, MP4Cover
        audio = File(filename)
        pic = audio.get("covr") or audio.get('APIC:')
        if not pic and hasattr(audio, "pictures"):
            pic = getattr(audio, "pictures")[0]
        if audio.get("covr") and isinstance(pic, list):
            pic = pic[0]
        if pic:
            if hasattr(pic, "mime"):
                ex = pic.mime.split('/')[-1]
            elif isinstance(pic, MP4Cover):
                ex = "jpg" if pic.imageformat == MP4Cover.FORMAT_JPEG else "png"
            else:
                raise ValueError(f"the format unspported:{type(pic)}.")

            if hasattr(pic, 'data'):
                pic = pic.data
            return pic, ex

    @staticmethod
    def add_flac_cover(filename, albumart):
        from mutagen.flac import Picture, FLAC
        audio = FLAC(filename)

        image = Picture()
        image.type = 3
        if albumart.lower().endswith('png'):
            mime = 'image/png'
        else:
            mime = 'image/jpeg'
        image.desc = 'front cover'
        image.mime = mime
        with open(albumart, 'rb') as f:
            image.data = f.read()

        audio.add_picture(image)
        audio.save()

    @staticmethod
    def add_mp4_cover(filename, albumart):
        from mutagen.mp4 import MP4, MP4Cover
        audio = MP4(filename)
        data = open(albumart, 'rb').read()

        covr = []
        if albumart.lower().endswith('png'):
            covr.append(MP4Cover(data, MP4Cover.FORMAT_PNG))
        else:
            covr.append(MP4Cover(data, MP4Cover.FORMAT_JPEG))

        audio.tags['covr'] = covr
        audio.save()

    def add_m4a_cover(self, filename, albumart):
        self.add_mp4_cover(filename, albumart)

    @staticmethod
    def add_mp3_cover(filename, albumart):
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC, error
        audio = MP3(filename, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass
        if albumart.lower().endswith('png'):
            mime = 'image/png'
        else:
            mime = 'image/jpeg'
        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime=mime,  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=open(albumart).read()
            )
        )
        audio.save()
