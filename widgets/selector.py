__all__ = ("Selector")
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    HoverBehavior)
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    StringProperty,
)
from utils.instrument import selected_instr


Builder.load_string("""
<InstrumentSelector>:
    #radius:[40,40,40,40]
    #elevation:0
    size_hint:None,None
    height:"150dp"
    width:"130dp"
    padding:0,15,0,0
    orientation:"vertical"
    canvas:
        Color:
            rgba:[1,0,0,1] if self.active else self.color if self.hovered else [0.7,.7,.7,.5]   #[1,0,1,.5]
        RoundedRectangle:
            pos:self.pos
            size:self.size
            #radius:root.radius
    Image:
        source:('assets/icons/drums_white.png' if root.active else 'assets/icons/drums.png') if root.source=="" else root.source
        size: self.texture_size
    MDLabel:
        halign:"center"
        text: root.text
        #theme_text_color:"Primary" if root.active else "Secondary"
        color:(1,1,1,1) if root.active else (0.9,.9,.9,1)
""")


class InstrumentSelector(ToggleButtonBehavior, HoverBehavior, ThemableBehavior,  BoxLayout):
    active = BooleanProperty(False)
    source = StringProperty()
    text = StringProperty()
    color = ColorProperty([.9, .9, .9, .3])

    def __init__(self, text="", source="", **kwargs):
        self.text = text
        self.source = source
        super(InstrumentSelector, self).__init__(**kwargs)

    def on_state(self,  widget, value):
        if value == "down":
            self.active = True
            _list = ToggleButtonBehavior.get_widgets('x')
            for each in _list:
                if each is not widget:
                    each.active = False
                    each.color =  [.7, .7, .7, .5]
            del _list
            name = widget.text.lower()
            import utils.instrument as ut
            ut.selected_instr = name
            st = "selected_instr = '{}'".format(name)

            with open('utils/instrument.py', 'w') as file:
                file.write(st)

    def on_enter(self):
        if(not self.active):
            self.color =  [.3, .3, .3, .5]
            pass

    def on_leave(self):
        if(not self.active):
            self.color =  [.7, .7, .7, .5]
            pass
