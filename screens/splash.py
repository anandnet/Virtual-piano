from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
Builder.load_string("""
<SplashScreen>:
    BoxLayout:
        canvas:
            Color:
                rgba:0,0,0,1
            Rectangle:
                pos:self.pos
                size:self.size

        orientation:"vertical"
        BoxLayout:
            size_hint_y:.20
            
        BoxLayout:
            size_hint_y:.55
            AnchorLayout:
                Image:
                    size_hint_y:1
                    source:'assets/icons/treble-clef 12.png'
        
        BoxLayout:
            size_hint_y:.25
            AnchorLayout:
                Loader:
                    size_hint_x:None
                    width:"400dp"
                    bg_color:[0.7,.7,.7,1]
                    fill_color:.5,1,.5,1
                    value:0
            
""")
class SplashScreen(Screen):
    pass