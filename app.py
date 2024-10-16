from kivy.config import Config

Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from distutils.dir_util import copy_tree
from threading import Thread
import os

Window.size = (500, 500)


class MainScreen(Screen):
    pass


class DoneScreen(Screen):
    pass


class CopyingScreen(Screen):
    pass


class HelpScreen(Screen):
    pass


class ErrorScreen(Screen):
    pass


class Manager(ScreenManager):
    pass


def txt_handler(name, option, *args):
    """Read and write .txt files"""
    name += '.txt'
    with open(name, option) as file:
        if option == 'r':
            return file.read()
        elif option == 'w':
            file.write(args[0])
            return True
        else:
            return False


ASSETS_FOLDER = os.path.join(os.getcwd(), f'assets{os.path.sep}')
REMIX_FOLDER = 'Remix Mod'
BACKUP_FOLDER = 'Backup'
TXT_FILE = 'path'

try:
    blazblue_path = txt_handler(TXT_FILE, 'r')
except FileNotFoundError:
    blazblue_path = txt_handler(TXT_FILE, 'w', r'C:\Steam\steamapps\common\BlazBlue Centralfiction')


class RemixModManager(App):

    def build(self):
        self.icon = f'{ASSETS_FOLDER}app.ico'
        self.title = "BBCF Remix Mod Manager"
        self.bb_path = blazblue_path.replace('\\', '/')
        return Builder.load_file(f'style.kv')

    def screen_change(self, screen):
        """Facilitate screen change throughout the application"""
        self.root.current = screen

    def _copy(self, origin, target):
        """Does the main purpose: copy all files from source to destination"""
        txt_handler(TXT_FILE, 'w', self.root.get_screen('main_screen').ids.txt_in.text)
        copy_tree(origin, target)
        self.screen_change('done_screen')

    def mod(self, option):
        path = self.root.get_screen('main_screen').ids.txt_in.text
        if not os.path.isdir(path):
            self.screen_change('error_screen')
        else:
            self.screen_change('copying_screen')
            Thread(target=self._copy,
                   args=(REMIX_FOLDER if option == 'mod' else BACKUP_FOLDER, path + '\\data')).start()


RemixModManager().run()
