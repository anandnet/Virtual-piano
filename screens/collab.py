from functools import partial
import json
import random
from widgets.dropitem import DropItem
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.card import MDSeparator
from kivy.properties import (
    ListProperty,
    StringProperty,
)
from utils.constant import  finger_name,clr


Builder.load_string("""
#:import DropItem widgets.dropitem 
<ListItem1>:
    orientation:"vertical"
    size_hint_y:None
    height:"50dp"
    BoxLayout:
        BoxLayout:
            padding:20,0,0,0
            MDLabel:
                color:1,1,1,1
                text:root.text

    MDSeparator:

<CollabWithFriends>:
    AnchorLayout:
        padding:80,20,20,20
        orientation:"vertical"
        canvas:
            Color:
                rgba:1,1,1,0
            Rectangle:
                pos:self.pos
                size:self.size

        BoxLayout:
            size_hint_x:.5 if app.root.width>1000 else .7
            padding:"20dp"
            canvas:
                Color:
                    rgba:[0.1,0.1,0.1,.6] 
                RoundedRectangle:
                    pos:self.pos
                    size:self.size
            ScrollView:
                do_scroll_y: True
                BoxLayout:
                    size_hint_y:None
                    height: self.minimum_height
                    orientation:"vertical"
                    BoxLayout:
                        size_hint_y:None
                        height:"60dp"
                        padding:5,0,0,0
                        MDLabel:
                            text:"Collab With Friends"
                            color:1,1,1,1
                            font_size:"27sp"
                            halign:"center"
                            bold:True
                    MDSeparator:
                        
                    BoxLayout:
                        size_hint_y:None
                        height:"60dp"
                        MDLabel:
                            text:"MyRecordings"
                            color:1,1,1,1
                            font_size:"22sp"
                            bold:True
                    MDSeparator:
                    BoxLayout:
                        id:recordings
                        orientation:"vertical"
                        size_hint_y:None
                        height:self.minimum_height
                        
                    
""")

class ListItem1(BoxLayout):
    text=StringProperty()
    def __init__(self,text, **kwargs):
        self.text=text
        super(ListItem1, self).__init__(**kwargs)


class CollabWithFriends(BoxLayout):

    def __init__(self, **kwargs):
        Clock.schedule_once(self.build_recording_list, 0)
        super(CollabWithFriends, self).__init__(**kwargs)
    
    def build_recording_list(self,*args):
        for i in range(10):
            self.ids.recordings.add_widget(ListItem1(text="Recording "+str(i)))


    