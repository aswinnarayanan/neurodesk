import sys
import argparse
import configparser
import pathlib


class SystemPath:
    def __init__(self, path, ):
        self.path = path
        self.display()

    def __str__(self):
        return self.path

    @classmethod
    def user_input(cls, description="File or Dir path"):
        while True:
            try:
                user_input_path = pathlib.Path(input(f'Enter {description}: ')).resolve(strict=True) 
                cls.is_valid(user_input_path)               
                return cls(user_input_path)
            except FileNotFoundError:
                print('Path Not Found. Please enter valid path')
                continue
            except NotADirectoryError:
                print('Path not Dir. Please enter valid dir')
                continue

    def display(self):
        print(f'Found {self.path}')

    @staticmethod
    def is_valid(path):
        if not path.exists():
            raise FileNotFoundError

class SystemFile(SystemPath):
    @staticmethod
    def is_valid(path):
        if not path.is_file():
            raise FileNotFoundError

class SystemDir(SystemPath):
    @staticmethod
    def is_valid(path):
        if not path.is_dir():
            raise NotADirectoryError


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action="store_true", default=False)
    parser.add_argument('--install', action="store_true", default=False)
    args = parser.parse_args()
    return args


def write_config():
    config = configparser.ConfigParser()
    config['neurodesk'] = {'InstallationDir': pathlib.Path.cwd()}
    with open('neurodesk.ini', 'w') as configfile:
        config.write(configfile)


def read_config():
    config = configparser.ConfigParser()
    config.read('neurodesk.ini')
    print(config['neurodesk']['InstallationDir'])


def user_config():
    while True:
        try:
            local_applications_menu = pathlib.Path(input('/etc/xdg/menus/lxde-applications.menu')).resolve(strict=True)
            break
        except FileNotFoundError:
            print('File Not Found. Please enter valid file')
            continue


if __name__ == "__main__":
    args = get_args()
    # user_config()
    # write_config()
    # read_config()

    if args.init:
        local_applications_menu = SystemFile.user_input('Local Application Menu')
        local_applications_dir = SystemDir.user_input('Local Applications Directory')
        local_desktop_directories_dir = SystemDir.user_input('Local Desktop Directory')
