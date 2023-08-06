#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 10:48 AM
# @Author  : wangdongming
# @Site    :
# @File    : ffmpeg.py
# @Software: Hifive
import os
import wavio
import numpy as np
from assents.utils import popen
from encryptor.md5 import md5
from pydub import AudioSegment
from pydub.utils import audioop


def readfile(filename, ar=44100, mandatory=True, norm_db=False, ac=None):
    '''
    format and load file.
    :param ac:
    :param filename: file path
    :param mandatory:
    :return:
    '''
    temporary = normalize(filename, mandatory=mandatory, ar=ar, norm_db=norm_db, ac=ac)
    audiofile = AudioSegment.from_file(temporary)
    return audiofile, temporary


def read(filename, limit=None):
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within. If file reading fails due to input being a 24-bit wav file,
    wavio is used as a backup.
    Can be optionally limited to a certain amount of seconds from the start
    of the file by specifying the `limit` parameter. This is the amount of
    seconds from the start of the file.
    returns: (channels, samplerate)
    """
    # pydub does not support 24-bit wav files, use wavio when this occurs
    try:
        audiofile, temporary = readfile(filename, mandatory=True, norm_db=True)

        if limit:
            audiofile = audiofile[:limit * 1000]

        data = np.fromstring(audiofile._data, np.int16)

        channels = []
        for chn in range(audiofile.channels):
            channels.append(data[chn::audiofile.channels])

        fs = audiofile.frame_rate
        if temporary != filename and os.path.isfile(temporary):
            os.remove(temporary)
    except audioop.error:
        fs, _, audiofile = wavio.read(filename)

        if limit:
            audiofile = audiofile[:limit * 1000]

        audiofile = audiofile.T
        audiofile = audiofile.astype(np.int16)

        channels = []
        for chn in audiofile:
            channels.append(chn)

    return channels, fs


def normwave(wave, bitwidth):
    return np.asarray(wave) / (2 ** bitwidth)


def write(data, filename, frame_rate):
    outdata = np.array(data).astype(np.short)
    wavio.write(filename, outdata, frame_rate)


def get_temporary_file(filename, ex):
    parentdir = os.path.dirname(filename) or 'temp'
    if not os.path.isdir(parentdir):
        os.mkdir(parentdir)
    basename = os.path.basename(filename)
    unique_name = str(md5(basename))
    return os.path.join(parentdir, unique_name + ex)


def normalize(filename, ar=44100, ac=None, acodec='pcm_s16le', mandatory=False, norm_db=False):

    # TODO: FFMPEG -> FFMPEG-NORMALIZE
    conversion_command = [
        AudioSegment.converter,
        "-i", filename,
        "-vn",  # Drop any video streams if there are any
        "-f", "wav",  # output options (filename last)
        "-ar", str(ar),
        "-acodec", acodec,
        "-y"
    ]
    if ac:
        conversion_command.extend(
            ["-ac", str(ac)]
        )
    without_ex, _ex = os.path.splitext(filename)
    if _ex.lower() == '.wav' and os.path.isfile(filename) and not mandatory:
        return filename
    temporary_file = get_temporary_file(filename, '.wav')
    if not os.path.isfile(temporary_file):
        conversion_command.append(temporary_file)
        returncode, p_out, p_err = popen(conversion_command)
        if not os.path.isfile(temporary_file) or os.path.getsize(temporary_file) < 2 ** 12:
            raise OSError(
                "Decoding failed. ffmpeg returned error code: {0}\n\nOutput from ffmpeg/avlib:\n\n{1}"
                    .format(returncode, p_err))
    if norm_db:
        file_path, ex = os.path.splitext(temporary_file)
        dst = f"{file_path}_norm.wav"
        normalizedb(temporary_file, dst, ar)
        os.remove(temporary_file)
        temporary_file = dst
    return temporary_file


def normalizedb(src, dst, ar):
    conversion_command = [
        'ffmpeg-normalize',
        "-f", src,
        "-vn",  # Drop any video streams if there are any
        "-nt", "peak",  # output options (filename last)
        "-t", "-0",
        "-ar", str(ar),
        "-o", dst
    ]
    returncode, p_out, p_err = popen(conversion_command)
    if not os.path.isfile(dst) or os.path.getsize(dst) < 2 ** 12:
        raise OSError(
            "normalize failed. ffmpeg returned error code: {0}\n\nOutput from ffmpeg/avlib:\n\n{1}"
                .format(returncode, p_err))


def detect_audio_duration(filename, fast=False):
    """
    detect media duration.
    extract audio stream and detect it when filename is a video.
    :param filename: media full path.
    :param fast: fast mode is enabled.
    :return: audio stream duration(sec).
    """
    if fast:
        from .ffmpeg import FFmpeg
        converter = FFmpeg()
        return converter.media_duration(filename)
    else:
        channels, fs = read(filename)
        if not channels:
            raise OSError(f"cannot read audio stream from {filename}.")
        shape = np.asarray(channels[0]).shape
        return shape[0] / fs
