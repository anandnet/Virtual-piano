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
<ListItem>:
    orientation:"vertical"
    size_hint_y:None
    height:"50dp"
    BoxLayout:
        BoxLayout:
            padding:20,0,0,0
            MDLabel:
                color:1,1,1,1
                text:root.text
        BoxLayout:
            Widget:
            DropItem:
                size_hint_x:None
                width:"170dp"
                icon_color:1,1,1,1
                icon:"chevron-down"
                id: dropdown_item
                text: "None"
                transparent:True
                on_release: root.menu.open(self)
            Widget:

    MDSeparator:

<MusicMapping>:
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
                            text:"Left Hand"
                            color:1,1,1,1
                            font_size:"23sp"
                            bold:True
                    MDSeparator:
                    BoxLayout:
                        id:lefthand
                        orientation:"vertical"
                        size_hint_y:None
                        height:self.minimum_height
                        
                    BoxLayout:
                        size_hint_y:None
                        height:"60dp"
                        MDLabel:
                            text:"Right Hand"
                            color:1,1,1,1
                            font_size:"23sp"
                            bold:True
                    MDSeparator:
                    BoxLayout:
                        id:righthand
                        orientation:"vertical"
                        size_hint_y:None
                        height:self.minimum_height
                        
                    
""")


class ListItem(BoxLayout):
    index = ListProperty()
    text = StringProperty()

    def __init__(self, selected_instr, finger_name, index, selected_text, notes, **kwargs):
        self.initial_selected_text = "None" if(
            selected_text == "") else selected_text
        self.text = finger_name
        self.index = index
        self.menu_items = notes
        self.selected_instr = selected_instr
        Clock.schedule_once(self.buildDropDown, 0)
        super(ListItem, self).__init__(**kwargs)

    def buildDropDown(self, args):
        self.ids.dropdown_item.text = self.initial_selected_text
        self.menu = DropDown()
        for each in self.menu_items:
            btn = DropItem(text=each.split(".")[0], icon="music-note",
                           icon_color=random.choice(clr))
            btn.bind(on_release=lambda btn: self.set_item(self.menu, btn))
            self.menu.add_widget(btn)
            self.menu.spacing = 0
            self.menu.add_widget(MDSeparator())

    def set_item(self, instance_menu, instance_menu_item):
        self.ids.dropdown_item.text = instance_menu_item.text
        import json
        with open('utils/map_data.json', 'r') as file:
            data = json.load(file)

        data[self.selected_instr][int(self.index[0])
                                  ][self.index[1]] = instance_menu_item.text

        with open('utils/map_data.json', 'w') as json_file:
            json.dump(data, json_file)
        instance_menu.dismiss()


class MusicMapping(BoxLayout):
    selected_instr = "piano"

    def __init__(self, **kwargs):
        from utils.instrument import selected_instr
        self.selected_instr=selected_instr
        Clock.schedule_once(self.buildDropDown, 0)
        super(MusicMapping, self).__init__(**kwargs)

    def buildDropDown(self, args):
        # Load All Notes
        with open('utils/notes.json', 'r') as file:
            self.music_notes = json.load(file)
        self.add_mapping_table()

    

    def add_mapping_table(self, *args):
        
        with open('utils/map_data.json', 'r') as file:
            mapped_data = json.load(file)
        lh_current_map = mapped_data[self.selected_instr][0]
        rh_current_map = mapped_data[self.selected_instr][1]
        

        # building current mapped list for left hand
        if(len(self.ids.lefthand.children) > 0):
            self.ids.lefthand.clear_widgets()
        self.build_list(
            0, self.music_notes[self.selected_instr], lh_current_map)

        # building current mapped list for right hand
        if(len(self.ids.righthand.children) > 0):
            self.ids.righthand.clear_widgets()
        self.build_list(
            1, self.music_notes[self.selected_instr], rh_current_map)

    def build_list(self, hand_index, music_note, current_map):
        wid = self.ids.lefthand if(hand_index == 0) else self.ids.righthand

        for i in range(1, 6):
            wid.add_widget(ListItem(self.selected_instr, finger_name[i-1], [
                           str(hand_index), str(i)], current_map[str(i)], music_note))
