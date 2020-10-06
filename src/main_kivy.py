from functools import partial

import kivy

from src.game_utils.game_logger import RkLogger

kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from src.settings.kivy import KivySettings
from src.event.command.scene import SceneChangeCommand
from src.event.command.scene import SceneChangeController
from kivy.core.window import Window
from src.screen.game import GameScreen
from src.screen.load_data import LoadDataScreen
from src.game_utils.game_logger import RkLogger
class MainWindow(ScreenManager):
    _mood_str = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        # Create a consumer of SceneChangeCommands.
        self.scene_change_controller = SceneChangeController()

        # Periodically add an update call.
        Clock.schedule_interval(partial(self.update), 1/60.0)

        self.logger = RkLogger.__call__().get_logger()

    def change_scene(self, scene_name, *args):
        """Queues an attempt to change the scene.
        """
        known_screens = (
            'splash_creen',
            'title_screen',
            'load_data_screen',
            'menu_screen',
            'game_screen',
        )
        # If it's not a known scene, ignore it
        if not scene_name in known_screens:
            return

        # if load screen pass the mood
        if scene_name == "load_data_screen":
            _mood_str = args[0]
        # Create a new SceneChangeCommand with the new scene.
        new_command = SceneChangeCommand(actor=self, scene=scene_name)

        # Add the new command to the contorller.
        self.scene_change_controller.add_command(new_command)


    def update(self, dt):
        """Tries to execute periodically.
        dt = The amount of time.
        """
        # Process all scene change commands.
        self.scene_change_controller.process_commands()

class TitleScreen(Screen):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def process_text(self):
        _mood_str = text = self.ids.input.text
        logger = RkLogger.__call__().get_logger()
        logger.info("mood_str " + _mood_str)
        self.switch_to_load_data_screen(_mood_str)

    def switch_to_load_data_screen(self,_mood_str):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("load_data_screen",_mood_str)

    def switch_to_game_screen(self):
        """Close this widget and open the Game Screen.
        """

        # Ask the parent to switch to the Game screen
        self.parent.change_scene("game_screen",None)


class MainKivyRKrApp(App):
    def build(self):
        screen_manager = MainWindow(transition=FadeTransition())
        screen_manager.add_widget(TitleScreen(name="title_screen"))
        screen_manager.add_widget(GameScreen(name="game_screen"))
        screen_manager.add_widget(LoadDataScreen(name="load_data_screen"))
        screen_manager.current = 'title_screen'
        return screen_manager

kv = Builder.load_file("kv_data/game_kv.kv")
if __name__ == '__main__':
    # First set up graphics settings.
    # Config.set('graphics', 'width', '200')
    # Config.set('graphics', 'height', '800')

    settings = KivySettings(filename="user/settings.ini")
    window_sizes = (600,800) #Window.size

    MainKivyRKrApp().run()
