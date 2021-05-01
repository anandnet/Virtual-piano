import cv2
import random
from functools import partial
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix import boxlayout
from widgets.kivycamera import KivyCamera
from utils.constant import clr
from utils.play_music import Music
from handtracking.detect_hand import detect_hand
from kivy.properties import (
    ColorProperty,
    StringProperty,
    NumericProperty,
)
from screens.mapping import MusicMapping

Builder.load_string("""
<AnimIcon>:
    size_hint:None,None
    height:self.minimum_height
    width:self.minimum_width
    MDIcon:
        color:root.color
        icon:root.icon
        halign:"center"
        font_size:root.font_size
<HomeScreen>:
    #id:home
    AnchorLayout:
        anchor_x:"left"
        BoxLayout:
            id:feed
           

            #Something
        FloatLayout:
            id:float
            canvas:
                Color:
                    rgba:root.float_clr
                Rectangle:
                    pos:self.pos
                    size:self.size
            BoxLayout:   
                #size_hint_x:1 if root.width<1000  else .8
                FloatLayout:
                    id:music
            BoxLayout:

            BoxLayout:
                



            MDIconButton:
                icon:"tools"
                on_release:
                    root.add_mapping(self)
                md_bg_color:1,0,1,1
                pos:(10,20)
""")


class Camera(KivyCamera):

    def __init__(self, cap, **kwargs):
        super().__init__(cap, **kwargs)
        self.music = Music()

    def on_update(self, frame):
        left_status, right_status ,frame2= detect_hand(frame)
        #print(left_status, right_status)
        Clock.schedule_once(partial(self.play, left_status, 0))
        Clock.schedule_once(partial(self.play, right_status, 1))

        return cv2.flip(frame2,1)

    def play(self, status, hand_indx, interval):
        if(status):
            true_index = [i for i, each in enumerate(status) if each == True]
            if(len(true_index) == 1):
                self.music.play(hand_indx, true_index[0])
                if(true_index[0] != 0):
                    self.add_anim()

    def add_anim(self):
        icon = AnimIcon(
            color=random.choice(clr),
            icon=random.choice(
                ["music-clef-treble", "music", "music-note"]),
            pos_hint={"y": 0, "x": .45}
        )
        #print(self.parent.parent.ids)
        self.parent.parent.parent.ids.music.add_widget(icon)


class HomeScreen(Screen):
    mapping=False
    float_clr=[0.5,.5,.5,.3]
    cap = None

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.add_camera, 1/1000)
    

    

    def add_camera(self, *args):
        source = 0  # "https://192.168.43.1:8080/video"
        self.cap = cv2.VideoCapture(source)
        cam = Camera(self.cap)
        self.ids.feed.add_widget(cam)

    def on_pre_leave(self, *args):
        # print("hello")
        if(self.cap):
            self.cap.release()
    
    def add_mapping(self,button):
        x=MusicMapping()
        if(self.mapping):
            self.float_clr=[0.5,.5,.5,.3]
            self.mapping=False
            button.icon='tools'
            self.ids.float.remove_widget(self.ids.float.children[0])
        else:
            self.float_clr=[0.5,.5,.5,.0]
            button.icon='window-close'
            self.mapping=True
            self.ids.float.add_widget(x)
            
        


class AnimIcon(BoxLayout):
    color = ColorProperty()
    font_size = NumericProperty()
    icon = StringProperty()

    def __init__(self, icon, color=[0, 0, 1, 0], font_size="20sp", **kwargs):
        self.color = color
        self.font_size = font_size
        self.icon = icon
        super(AnimIcon, self).__init__(**kwargs)
        Clock.schedule_once(self.start_anim, 1/1000)

    def start_anim(self, *args):

        anim = Animation(color=random.choice(clr),
                         font_size=70,
                         pos_hint={"x": random.randrange(
                             25, 75, 5)/100, "y": .95},
                         duration=3
                         )
        anim.start(self)
        Clock.schedule_once(partial(self.remove_wid, self), 3)

    def remove_wid(self, inst, args):
        self.parent.remove_widget(inst)