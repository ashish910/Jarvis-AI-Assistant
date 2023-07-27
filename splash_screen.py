from kivy.app import App
from kivy.uix.video import Video
from kivy.clock import Clock

class VideoWindow(App):
    def build(self):
        video = Video(source='a.mp4')
        video.state = "play"
        video.allow_stretch = True
        Clock.schedule_once(self.stop,80)
        return video
if __name__ == '__main__':
    window = VideoWindow()
    window.run()