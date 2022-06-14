from kivy.app import App
from kivy.resources import resource_add_path, resource_find
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
import os, sys, re
import shutil
import win32timezone
from pytube import YouTube
import random
import subprocess
import threading


class YRloader_GUI(Screen):
    """ YRloader functional gui """
    dowload_folder = f"{os.environ['USERPROFILE']}\\Downloads"
    def get_shref(self):
        r_shref = [r'https://www.youtube.com', r'https://youtu.be']
        shref = self.ids.video_shref.text
        for i in r_shref:
            result = re.match(i, shref)
            if result is not None:
                yt = YouTube(shref)
                self.ids.img_previvev.background_color = (24/255, 35/255, 55/255, 0)
                self.ids.img_previvev.source = yt.thumbnail_url
                return core_activate(shref, self.ids.video_res.text, YRloader_GUI.dowload_folder)

    def spinner_clicked(self, value):
        self.ids.video_res.text = f'{value}'


def core_activate(a, b, c):
    tread_core = YRloader_core(a, b, c)
    return lambda: threading.Thread(target = tread_core, args = ()).start()


class SecondScreen(Screen):
    def selected(self, filename):
        try:
            self.folder_pass = filename[0]
        except:
            pass

    def back(self):
        self.ids.filechooser.selection = []

    def ok(self):
        try:
            YRloader_GUI.dowload_folder = self.folder_pass
        except:
            YRloader_GUI.dowload_folder = f"{os.environ['USERPROFILE']}\\Downloads"


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('yrloader_desinger.kv')

def convert(fil1, fil2, rname, path_f):
    codec = "copy"
    subprocess.run(f"ffmpeg -i {fil1} -i {fil2} -c {codec} {rname}")
    os.remove(fil1)
    os.remove(fil2)
    shutil.move(rname, path_f)

class YRloader_core:
    """ YRloader dowloander functional """
    def __init__(self, video_url, video_res, filename):
        self.video_url = video_url
        self.video_res = video_res
        self.filename = filename
        not_full = ["480p", "1080p", "1440p", "2160p"]
        yt = YouTube(self.video_url )
        if self.video_res in not_full:
            self.go()
        else:
            try:
                yt.streams.filter(res=self.video_res).first().download(self.filename)
            except Exception:
                yt.streams.first().download(self.filename)

    def go(self):
        yt = YouTube(self.video_url )
        file1 = yt.streams.filter(only_audio=True).first().download(filename="video.mp3")


        try:
            file2 = yt.streams.filter(res=self.video_res).first().download(filename="video.mp4")
        except Exception:
            file2 = yt.streams.first().download()

        raname = (f"video{str(random.randint(1, 100))}.mp4")
        return convert(file1, file2, raname, self.filename)



class YRloader(App):
    def build(self):
        self.icon = 'ico.png'
        Window.clearcolor = (24/255, 35/255, 55/255, 1)
        Window.size = (1020, 720)
        return kv



if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    YRloader().run()
