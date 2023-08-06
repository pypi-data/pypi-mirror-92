#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 10:46 AM
# @Author  : wangdongming
# @Site    : 
# @File    : waveio.py
# @Software: Hifive
import os
import wave
import numpy as _np
from .ffmpeg import FFmpeg
from assents.utils import is_linuxos
from encryptor.md5 import md5 as hash


def convert2wav(input, export_folder, converter=None):
    fn = os.path.basename(input)
    hashname = '{}.wav'.format(hash(fn))
    temp_file = os.path.join(export_folder, hashname)
    if not os.path.isfile(temp_file):
        conv = converter or FFmpeg()
        returncode, p_out, p_err = conv.convert2wav(input, temp_file)
        if not os.path.isfile(temp_file):
            raise OSError(f"ffmepeg converter error, msg:{p_err}")
    return temp_file


def norm(wave, peak=30):
    positive = _np.abs(wave)
    maximum = _np.max(positive) or 1
    norm_wave = wave / float(maximum) * peak
    return norm_wave.astype(int)


def show_wave(file, ratio=0.01, draw=0, converter=None, clear=True, convert=True):
    wfile = convert2wav(file, converter) if convert else file
    f = wave.open(wfile, "rb")
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = f.readframes(nframes)
    wave_data = _np.fromstring(str_data, dtype=_np.short).reshape(-1, nchannels).T
    duration = nframes / framerate
    span = int(framerate * ratio)
    show_time = _np.arange(0, nframes, span) * (1.0 / framerate)
    data = norm(wave_data[0][::span])
    if draw and not is_linuxos:
        import pylab as pl
        pl.subplot(211)
        pl.plot(show_time, data, c='r')
        pl.xlabel("time (seconds)")
        pl.show()
    if clear and os.path.isfile(wfile):
        os.remove(wfile)
    return data.tolist(), int(duration)


def _wav2array(nchannels, sampwidth, data):
    """data must be the string containing the bytes from the wav file."""
    num_samples, remainder = divmod(len(data), sampwidth * nchannels)
    if remainder > 0:
        raise ValueError('The length of data is not a multiple of '
                         'sampwidth * num_channels.')
    if sampwidth > 4:
        raise ValueError("sampwidth must not be greater than 4.")

    if sampwidth == 3:
        a = _np.empty((num_samples, nchannels, 4), dtype=_np.uint8)
        raw_bytes = _np.fromstring(data, dtype=_np.uint8)
        a[:, :, :sampwidth] = raw_bytes.reshape(-1, nchannels, sampwidth)
        a[:, :, sampwidth:] = (a[:, :, sampwidth - 1:sampwidth] >> 7) * 255
        result = a.view('<i4').reshape(a.shape[:-1])
    else:
        # 8 bit samples are stored as unsigned ints; others as signed ints.
        dt_char = 'u' if sampwidth == 1 else 'i'
        a = _np.fromstring(data, dtype='<%s%d' % (dt_char, sampwidth))
        result = a.reshape(-1, nchannels)
    return result


def readwav(file):
    """
    Read a WAV file.

    Parameters
    ----------
    file : string or file object
        Either the name of a file or an open file pointer.

    Return Values
    -------------
    rate : float
        The sampling frequency (i.e. frame rate)
    sampwidth : float
        The sample width, in bytes.  E.g. for a 24 bit WAV file,
        sampwidth is 3.
    data : numpy array
        The array containing the data.  The shape of the array is
        (num_samples, num_channels).  num_channels is the number of
        audio channels (1 for mono, 2 for stereo).

    Notes
    -----
    This function uses the `wave` module of the Python standard libary
    to read the WAV file, so it has the same limitations as that library.
    In particular, the function does not read compressed WAV files.

    """
    wav = wave.open(file)
    rate = wav.getframerate()
    nchannels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    nframes = wav.getnframes()
    data = wav.readframes(nframes)
    wav.close()
    array = _wav2array(nchannels, sampwidth, data)
    return rate, sampwidth, array


def writewav24(filename, rate, data):
    """
    Create a 24 bit wav file.

    Parameters
    ----------
    filename : string
        Name of the file to create.
    rate : float
        The sampling frequency (i.e. frame rate) of the data.
    data : array-like collection of integer or floating point values
        data must be "array-like", either 1- or 2-dimensional.  If it
        is 2-d, the rows are the frames (i.e. samples) and the columns
        are the channels.

    Notes
    -----
    The data is assumed to be signed, and the values are assumed to be
    within the range of a 24 bit integer.  Floating point values are
    converted to integers.  The data is not rescaled or normalized before
    writing it to the file.

    Example
    -------
    Create a 3 second 440 Hz sine wave.

    >>> rate = 22050  # samples per second
    >>> T = 3         # sample duration (seconds)
    >>> f = 440.0     # sound frequency (Hz)
    >>> t = np.linspace(0, T, T*rate, endpoint=False)
    >>> x = (2**23 - 1) * np.sin(2 * np.pi * f * t)
    >>> writewav24("sine24.wav", rate, x)

    """
    a32 = _np.asarray(data, dtype=_np.int32)
    if a32.ndim == 1:
        # Convert to a 2D array with a single column.
        a32.shape = a32.shape + (1,)
    # By shifting first 0 bits, then 8, then 16, the resulting output
    # is 24 bit little-endian.
    a8 = (a32.reshape(a32.shape + (1,)) >> _np.array([0, 8, 16])) & 255
    wavdata = a8.astype(_np.uint8).tostring()

    w = wave.open(filename, 'wb')
    w.setnchannels(a32.shape[1])
    w.setsampwidth(3)
    w.setframerate(rate)
    w.writeframes(wavdata)
    w.close()
