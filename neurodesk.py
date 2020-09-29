import sys
import argparse
import configparser
import pathlib
import os
import signal
import sys
import xml.etree.ElementTree as et
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# CLI signal handler for safe Ctrl-C
def signal_handler(signal, frame):
        print('\nExiting ...')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Global settings
CONFIG_FILE = 'neurodesk.ini'
DEFAULT_PATHS = {}
DEFAULT_PATHS['lxde'] = {
    'appmenu': '/etc/xdg/menus/lxde-applications.menu',
    'appdir': '/usr/share/applications/',
    'deskdir': '/usr/share/desktop-directories/'
}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action="store_true", default=False)
    parser.add_argument('--installdir', action="store_true", default=False)
    parser.add_argument('--lxde', action="store_true", default=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    if os.name != 'posix':
        raise OSError

    args = get_args()
    config = configparser.ConfigParser()

    config['vnm'] = {'installdir': '', 'appmenu': '', 'appdir': '', 'deskdir': ''}
    config.read(CONFIG_FILE)


    if args.lxde:
        config['vnm']['appmenu'] = DEFAULT_PATHS['lxde']['appmenu']
        config['vnm']['appdir'] = DEFAULT_PATHS['lxde']['appdir']
        config['vnm']['deskdir'] = DEFAULT_PATHS['lxde']['deskdir']

    if args.init:
        config['vnm']['installdir'] = input(f'installdir: ') or config['vnm']['installdir']
        config['vnm']['appmenu'] = input(f'appmenu: ') or config['vnm']['appmenu']
        config['vnm']['appdir'] = input(f'appdir: ') or config['vnm']['appdir']
        config['vnm']['deskdir'] = input(f'deskdir: ') or config['vnm']['deskdir']

    try:
        installdir = pathlib.Path(config['vnm']['installdir']).resolve(strict=False)
        installdir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        logging.error(f'PermissionError creating installdir [{installdir}]')
        logging.error('Exiting ...')
        sys.exit()
    
    try:
        appmenu = pathlib.Path(config['vnm']['appmenu']).resolve(strict=True)
        et.parse(appmenu)
    except et.ParseError:
        logging.error(f'InvalidXMLError with appmenu [{appmenu}]')
        logging.error('Exiting ...')
        sys.exit()

    appdir = pathlib.Path(config['vnm']['appdir']).resolve(strict=True)
    try:
        appdir = pathlib.Path(config['vnm']['appdir']).resolve(strict=True)
        next(appdir.glob("*.desktop"))
    except StopIteration:
        logging.error(f'.desktop files not found in appdir [{appdir}]')
        logging.error('Exiting ...')
        sys.exit()

    try:
        deskdir = pathlib.Path(config['vnm']['deskdir']).resolve(strict=True)
        next(deskdir.glob("*.directory"))
    except StopIteration:
        logging.error(f'.directory files not found in deskdir [{deskdir}]')
        logging.error('Exiting ...')
        sys.exit()

    config['vnm']['installdir'] = str(installdir)
    config['vnm']['appmenu'] = str(appmenu)
    config['vnm']['appdir'] = str(appdir)
    config['vnm']['deskdir'] = str(deskdir)

    with open(CONFIG_FILE, 'w+') as fh:
        config.write(fh)
