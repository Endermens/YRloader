from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.resources import resource_add_path, resource_find
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
    fold_img = "1_1.png"
    def get_shref(self):
        r_shref = [r'https://www.youtube.com', r'https://youtu.be']
        shref = self.ids.video_shref.text
        for i in r_shref:
            result = re.match(i, shref)
            if result is not None:
                yt = YouTube(shref)
                self.ids.img_previvev.background_color = (24/255, 35/255, 55/255, 0)
                self.ids.img_previvev.source = yt.thumbnail_url
                return core_activate(shref, self.ids.video_res.text, YRloader_GUI.dowload_folder, self.ids.video_music.text)

    def init_img(self, value):
        self.ids.fold_pass_img.source = '1_1.png'

    def spinner_clicked(self, value):
        self.ids.video_res.text = f'{value}'

    def music_spinner(self, value):
        self.ids.video_music.text = f'{value}'


def core_activate(a, b, c, d):
    if d == "mp4":
        tread_core = YRloader_core(a, b, c)
        return lambda mv: threading.Thread(target = tread_core, args = ()).start()
    else:
        tread_core = Fast_music(a, c)
        return lambda ms: threading.Thread(target = tread_core, args = ()).start()



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

kv = Builder.load_string("""WindowManager:
  YRloader_GUI:
  SecondScreen:

#  shablon
<Label>
  font_size: 16
  font_name: "Roboto-Regular.ttf"
  background_color: (24/255, 35/255, 55/255, 1)
  canvas.before:
    Color:
      rgba: self.background_color
    Rectangle:
      size: self.size
      pos: self.pos
  bold: True
  italic: True
  outline_color: 0, 0, 0
# <cLabel@Label>


<YRloader_GUI>
  name: "main"
  #Parent box
  BoxLayout:
    orientation: "vertical"
    size: root.width, root.height

    #block 1
    BoxLayout:
      orientation: "vertical"
      size_hint_y: None
      height: 80
      Label:
        id: greeting
        text: "Вcтавьте ссылку на видео!"
        font_size: 24
        size_hint_y: None
        width: 200

    #block 2
    BoxLayout:
      orientation: "horizontal"
      pos_hint: {'center_x':0.5, 'y':0}
      size_hint_y: None
      height: 60
      size_hint_x: 0.6

      Spinner:
        id: video_music
        pos_hint: {'center_x':0.1, 'y':0}
        size_hint: (0.1, 1)
        background_color: (252/255, 254/255, 249/255, 0.5)
        text: "mp4"
        font_size: 18
        values: ["mp3", "mp4"]
        on_text: root.spinner_clicked(video_res.text)


      TextInput:
        id: video_shref
        pos_hint: {'center_x':0.5, 'y':0}
        multiline: False
        size_hint: (0.75, 1)
        font_size: 26

      Spinner:
        id: video_res
        pos_hint: {'center_x':0.75, 'y':0}
        size_hint: (0.1, 1)
        background_color: (252/255, 254/255, 249/255, 0.5)
        text: "720p"
        font_size: 18
        values: ["144p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
        on_text: root.spinner_clicked(video_res.text)

      Button:
        id: fold_pass
        pos_hint: {'center_x':0.1, 'y':0}
        size_hint: (0.1, 1)
        background_color: (252/255, 254/255, 249/255, 0.5)
        on_release:
          app.root.current = "folder"
          root.manager.transition.direction = "up"

        Image:
          id: fold_pass_img
          source: root.fold_img
          center_x: self.parent.center_x
          center_y: self.parent.center_y

    BoxLayout:
      orientation: "vertical"
      padding: 10
      size_hint_y: None
      height: 80
      Button:
        id: download_button
        pos_hint: {'center_x':0.5, 'y':0}
        text: "Download"
        font_size: 24
        size_hint: (0.2, 0.25)
        # background_normal: ""
        background_color: (1, 228/255, 37/255, 0.5)
        on_release: root.get_shref()

    # block 3
    BoxLayout:
      orientation: "horizontal"
      background_color: (0, 1, 0, 1)
      canvas.before:
        Color:
          rgba: self.background_color
        Rectangle:
          size: self.size
          pos: self.pos

      BoxLayout:
        orientation: "vertical"
        size_hint: (0.2, 1)
        background_color: (24/255, 35/255, 55/255, 1)
        canvas.before:
          Color:
            rgba: self.background_color
          Rectangle:
            size: self.size
            pos: self.pos

      BoxLayout:
        orientation: "vertical"
        size_hint: (0.6, 1)
        background_color: (24/255, 35/255, 55/255, 1)
        canvas.before:
          Color:
            rgba: self.background_color
          Rectangle:
            size: self.size
            pos: self.pos
        # Image:
        AsyncImage:
          id: img_previvev
          background_color: (24/255, 35/255, 55/255, 1)
          canvas:
            Color:
              rgba: self.background_color
            Rectangle:
              size: self.size
              pos: self.pos
          allow_stretch: True
          keep_ratio: True

      BoxLayout:
        orientation: "vertical"
        size_hint: (0.2, 1)
        background_color: (24/255, 35/255, 55/255, 1)
        canvas.before:
          Color:
            rgba: self.background_color
          Rectangle:
            size: self.size
            pos: self.pos


<SecondScreen>:
  name: "folder"

  BoxLayout:
    orientation: "vertical"
    size: root.width, root.height
    padding: 50
    spacing: 20

    FileChooserIconView:
      id: filechooser
      dirselect: True
      filters: ['']
      on_selection: root.selected(filechooser.selection)

    BoxLayout:
      orientation: "horizontal"
      size_hint: (1, .4)
      canvas.before:
        Rectangle:
          size: self.size
          pos: self.pos


      Button:
        size_hint: (.1, .2)
        background_color: (252/255, 254/255, 249/255, 0.5)
        text: "Back"
        font_size: 32
        on_release:
          app.root.current = "main"
          root.manager.transition.direction = "down"
          root.back()

      Button:
        size_hint: (.1, .2)
        background_color: (252/255, 254/255, 249/255, 0.5)
        text: "ok"
        font_size: 32
        on_release:
          app.root.current = "main"
          root.manager.transition.direction = "down"
          root.ok()
""")

def convert(fil1, fil2, rname, path_f):
    codec = "copy"
    subprocess.run(f"ffmpeg -i {fil1} -i {fil2} -c {codec} {rname}", creationflags=subprocess.CREATE_NO_WINDOW)
    os.remove(fil1)
    os.remove(fil2)
    shutil.move(rname, path_f)

def extract(fil1, rname, path_f):
    codec = "copy"
    subprocess.run(f"ffmpeg -i {fil1} -q:a 0 -map a {rname}", creationflags=subprocess.CREATE_NO_WINDOW)
    os.remove(fil1)
    shutil.move(rname, path_f)

class YRloader_core:
    """ YRloader dowloander functional """
    def __init__(self, video_url, video_res, filename):
        self.video_url = video_url
        self.video_res = video_res
        self.filename = filename
        not_full = ["480p", "1080p", "1440p", "2160p"]
        yt = YouTube(self.video_url)
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

        raname = (f"video{str(random.randint(1, 100))}{str(random.randint(1, 100))}.mp4")
        return convert(file1, file2, raname, self.filename)

class Fast_music:
    def __init__(self, video_url, filename):
        self.video_url = video_url
        self.filename = filename
        yt = YouTube(self.video_url)
        raname = (f"music{str(random.randint(1, 100))}{str(random.randint(1, 100))}.mp3")
        file1 = yt.streams.filter(only_audio=True).first().download(filename="muve.mp4")
        return extract(file1, raname, self.filename)


class YRloader(App):
    icon = 'ico.png'
    def build(self):
        Window.clearcolor = (24/255, 35/255, 55/255, 1)
        Window.size = (1020, 720)
        return YRloader_GUI()



if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    YRloader().run()
