#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import shutil
import time
import random
import threading
import socket
import hashlib
import base64
import json
import re
import glob
import zipfile
import datetime
import getpass
import signal
import subprocess
import stat
import fnmatch
import shlex
import calendar
import csv
import urllib.request
import urllib.parse
import uuid
import secrets
import string
import binascii
import zlib
import gzip
import tarfile
import ftplib
import smtplib
import sqlite3
import webbrowser
import argparse
import queue
import enum
import copy
import math
import statistics
import itertools
import collections
import tempfile
import ctypes
import sysconfig
import importlib
import importlib.metadata
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.syntax import Syntax
    from rich import print as rprint
    from rich.markdown import Markdown
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.columns import Columns
    from rich.tree import Tree
    from rich.align import Align
    from rich.prompt import Prompt, Confirm
    from rich.status import Status
    from rich.console import Group
    from rich.box import Box, ROUNDED, DOUBLE, HEAVY, MINIMAL, SIMPLE
    from rich.style import Style
    from rich.color import Color
    from rich.padding import Padding
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from colorama import init, Fore, Back, Style as ColoramaStyle
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

if platform.system() != 'Windows':
    try:
        import pty
        import select
        import termios
        import tty
        UNIX_AVAILABLE = True
    except ImportError:
        UNIX_AVAILABLE = False
else:
    UNIX_AVAILABLE = False

try:
    import psutil
    PSUTIL = True
except ImportError:
    PSUTIL = False

try:
    import requests
    REQUESTS = True
except ImportError:
    REQUESTS = False

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL = True
except ImportError:
    PIL = False

try:
    import cryptography
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO = True
except ImportError:
    CRYPTO = False

class Installer:
    def __init__(self):
        self.required_packages = ['psutil', 'requests', 'Pillow', 'cryptography', 'colorama', 'rich']
        self.optional_packages = []
        self.python_version = sys.version_info
        self.install_path = Path.home() / '.kali_terminal'
        self.config_path = self.install_path / 'config.json'
        self.history_path = Path.home() / '.kali_terminal_history'
        
    def check_python_version(self):
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 7):
            print(f"\033[91m❌ Требуется Python 3.7 или выше (установлен {self.python_version.major}.{self.python_version.minor})\033[0m")
            sys.exit(1)
        return True
    
    def check_pip(self):
        try:
            import pip
            return True
        except ImportError:
            try:
                subprocess.run([sys.executable, '-m', 'pip', '--version'], capture_output=True, check=True)
                return True
            except:
                print("\033[93m⚠️ pip не найден. Установка библиотек может не работать\033[0m")
                return False
    
    def install_package(self, package):
        try:
            if package == 'Pillow':
                import_name = 'PIL'
            elif package == 'colorama':
                import_name = 'colorama'
            elif package == 'rich':
                import_name = 'rich'
            else:
                import_name = package.replace('-', '_')
            importlib.import_module(import_name)
            return True
        except ImportError:
            pass
        
        print(f"\033[96m📦 Установка {package}...\033[0m")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', package], check=True, capture_output=True)
            print(f"\033[92m✅ {package} успешно установлен\033[0m")
            return True
        except Exception as e:
            print(f"\033[91m❌ Ошибка установки {package}: {e}\033[0m")
            return False
    
    def install_all(self):
        terminal_width = shutil.get_terminal_size().columns
        border_char = '═'
        title = "УСТАНОВЩИК KALI TERMINAL v4.2"
        
        print("\033[95m")
        print(f"╔{border_char * (terminal_width - 2)}╗")
        print(f"║{title.center(terminal_width - 2)}║")
        print(f"╠{border_char * (terminal_width - 2)}╣")
        print(f"║{'ПРОВЕРКА И УСТАНОВКА НЕОБХОДИМЫХ БИБЛИОТЕК'.center(terminal_width - 2)}║")
        print(f"╚{border_char * (terminal_width - 2)}╝")
        print("\033[0m")
        
        self.check_python_version()
        has_pip = self.check_pip()
        
        installed = []
        failed = []
        
        for package in self.required_packages:
            if self.install_package(package):
                installed.append(package)
            else:
                failed.append(package)
        
        print("\n\033[95m")
        print(f"╔{border_char * (terminal_width - 2)}╗")
        if not failed:
            print(f"║{'✅ ВСЕ БИБЛИОТЕКИ УСПЕШНО УСТАНОВЛЕНЫ'.center(terminal_width - 2)}║")
        else:
            print(f"║{'⚠️ НЕКОТОРЫЕ БИБЛИОТЕКИ НЕ УСТАНОВЛЕНЫ'.center(terminal_width - 2)}║")
        print(f"╚{border_char * (terminal_width - 2)}╝")
        print("\033[0m")
        
        self.create_config()
        return len(failed) == 0
    
    def create_config(self):
        self.install_path.mkdir(exist_ok=True)
        config = {
            'version': '4.2',
            'install_date': datetime.datetime.now().isoformat(),
            'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
            'platform': platform.system(),
            'packages_installed': self.required_packages
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def run(self):
        if len(sys.argv) > 1 and sys.argv[1] == '--install':
            self.install_all()
            sys.exit(0)
        
        if not self.config_path.exists():
            print("\033[93m⚠️ Требуется установка библиотек. Запустите с --install\033[0m")
            response = input("\033[96mУстановить необходимые библиотеки? (y/n): \033[0m")
            if response.lower() == 'y':
                self.install_all()
            else:
                print("\033[91mНекоторые функции могут быть недоступны\033[0m")
                time.sleep(1)

class Colors:
    BLACK = '\033[30m'
    DARK_RED = '\033[31m'
    DARK_GREEN = '\033[32m'
    DARK_YELLOW = '\033[33m'
    DARK_BLUE = '\033[34m'
    DARK_MAGENTA = '\033[35m'
    DARK_CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'
    
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_DARK_GRAY = '\033[100m'
    BG_LIGHT_RED = '\033[101m'
    BG_LIGHT_GREEN = '\033[102m'
    BG_LIGHT_YELLOW = '\033[103m'
    BG_LIGHT_BLUE = '\033[104m'
    BG_LIGHT_MAGENTA = '\033[105m'
    BG_LIGHT_CYAN = '\033[106m'
    BG_LIGHT_WHITE = '\033[107m'
    
    @staticmethod
    def gradient_text(text: str, style: str = 'rainbow', single_color: str = None) -> str:
        if single_color:
            colors = []
            for i in range(len(text)):
                intensity = 30 + int((i / max(1, len(text)-1)) * 60)
                colors.append(f'\033[9{intensity//10}m')
        else:
            if style == 'rainbow':
                colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
            elif style == 'fire':
                colors = [Colors.RED, Colors.RED, Colors.YELLOW, Colors.YELLOW, Colors.RED, Colors.MAGENTA]
            elif style == 'ice':
                colors = [Colors.CYAN, Colors.CYAN, Colors.BLUE, Colors.BLUE, Colors.CYAN, Colors.WHITE]
            elif style == 'matrix':
                colors = [Colors.GREEN, Colors.GREEN, Colors.CYAN, Colors.GREEN, Colors.LIGHT_GRAY]
            elif style == 'sunset':
                colors = [Colors.RED, Colors.MAGENTA, Colors.YELLOW, Colors.RED, Colors.MAGENTA]
            elif style == 'ocean':
                colors = [Colors.BLUE, Colors.CYAN, Colors.BLUE, Colors.CYAN, Colors.BLUE]
            elif style == 'forest':
                colors = [Colors.GREEN, Colors.DARK_GREEN, Colors.GREEN, Colors.DARK_GREEN]
            elif style == 'neon':
                colors = [Colors.CYAN, Colors.MAGENTA, Colors.GREEN, Colors.YELLOW]
            elif style == 'pastel':
                colors = [Colors.GREEN, Colors.YELLOW, Colors.CYAN, Colors.MAGENTA]
            else:
                colors = [Colors.MAGENTA, Colors.CYAN, Colors.GREEN, Colors.YELLOW, Colors.RED]
        
        result = ""
        for i, char in enumerate(text):
            if single_color:
                color = colors[i % len(colors)]
            else:
                color = colors[i % len(colors)]
            result += f"{color}{char}{Colors.RESET}"
        return result
    
    @staticmethod
    def box(text: str, color: str = GREEN, border: str = CYAN, padding: int = 1) -> str:
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        padded_width = max_len + (padding * 2)
        
        top = f"{border}┌{'─' * padded_width}┐{Colors.RESET}"
        bottom = f"{border}└{'─' * padded_width}┘{Colors.RESET}"
        
        result = [top]
        for line in lines:
            padded_line = f"{' ' * padding}{line}{' ' * (max_len - len(line) + padding)}"
            result.append(f"{border}│{color}{padded_line}{Colors.RESET}{border}│{Colors.RESET}")
        result.append(bottom)
        return '\n'.join(result)
    
    @staticmethod
    def header(title: str, width: int = None, char: str = '═', style: str = 'double') -> str:
        if width is None:
            width = len(title) + 8
            if width < 60:
                width = 60
            if width > 120:
                width = 120
        
        if style == 'double':
            top_left = '╔'
            top_right = '╗'
            bottom_left = '╚'
            bottom_right = '╝'
            horizontal = '═'
            vertical = '║'
        elif style == 'single':
            top_left = '┌'
            top_right = '┐'
            bottom_left = '└'
            bottom_right = '┘'
            horizontal = '─'
            vertical = '│'
        elif style == 'heavy':
            top_left = '┏'
            top_right = '┓'
            bottom_left = '┗'
            bottom_right = '┛'
            horizontal = '━'
            vertical = '┃'
        else:
            top_left = '╔'
            top_right = '╗'
            bottom_left = '╚'
            bottom_right = '╝'
            horizontal = '═'
            vertical = '║'
        
        line = f"{Colors.CYAN}{top_left}{horizontal * width}{top_right}{Colors.RESET}"
        title_line = f"{Colors.CYAN}{vertical}{Colors.BOLD}{Colors.gradient_text(title.center(width), 'cyan', single_color=True)}{Colors.RESET}{Colors.CYAN}{vertical}{Colors.RESET}"
        bottom = f"{Colors.CYAN}{bottom_left}{horizontal * width}{bottom_right}{Colors.RESET}"
        return f"{line}\n{title_line}\n{bottom}"
    
    @staticmethod
    def gradient(text: str, colors: List[str] = None, single_color: str = 'cyan') -> str:
        if single_color:
            result = ""
            for i, char in enumerate(text):
                intensity = 30 + int((i / max(1, len(text)-1)) * 60)
                result += f"\033[9{intensity//10}m{char}{Colors.RESET}"
            return result
        if not colors:
            colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result += f"{color}{char}{Colors.RESET}"
        return result
    
    @staticmethod
    def glow(text: str, color: str = GREEN) -> str:
        return f"{color}{Colors.BOLD}{text}{Colors.RESET}"
    
    @staticmethod
    def neon(text: str, color: str = CYAN) -> str:
        return f"{color}{Colors.BOLD}{text}{Colors.RESET}"
    
    @staticmethod
    def shadow(text: str) -> str:
        return f"{Colors.DIM}{text}{Colors.RESET}"
    
    @staticmethod
    def blink(text: str) -> str:
        return f"{Colors.BLINK}{Colors.GREEN}{text}{Colors.RESET}"
    
    @staticmethod
    def rainbow(text: str) -> str:
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            result += f"{colors[i % len(colors)]}{char}{Colors.RESET}"
        return result
    
    @staticmethod
    def progress_bar(percent: int, width: int = 50, color: str = GREEN, show_percent: bool = True) -> str:
        filled = int(width * percent / 100)
        bar = f"{color}█{Colors.RESET}" * filled + f"{Colors.DIM}░{Colors.RESET}" * (width - filled)
        if show_percent:
            return f"{Colors.CYAN}[{bar}] {percent:3d}%{Colors.RESET}"
        return f"{Colors.CYAN}[{bar}]{Colors.RESET}"

class Icons:
    FOLDER = "📁"
    FILE = "📄"
    EXE = "⚙️"
    IMAGE = "🖼️"
    MUSIC = "🎵"
    VIDEO = "🎬"
    ARCHIVE = "📦"
    LINK = "🔗"
    ERROR = "❌"
    SUCCESS = "✅"
    WARNING = "⚠️"
    INFO = "ℹ️"
    QUESTION = "❓"
    STAR = "⭐"
    HEART = "❤️"
    FIRE = "🔥"
    ROCKET = "🚀"
    TERMINAL = "💻"
    NETWORK = "🌐"
    SECURITY = "🔒"
    DATABASE = "💾"
    CLOUD = "☁️"
    TOOLS = "🛠️"
    HACK = "💀"
    DOWNLOAD = "📥"
    UPLOAD = "📤"
    SEARCH = "🔍"
    SETTINGS = "⚙️"
    CHART = "📊"
    CLOCK = "⏰"
    CALENDAR = "📅"
    USER = "👤"
    GROUP = "👥"
    MAIL = "📧"
    PHONE = "📱"
    GLOBE = "🌍"
    LOCK = "🔐"
    UNLOCK = "🔓"
    KEY = "🔑"
    BUG = "🐛"
    GITHUB = "🐙"
    PYTHON = "🐍"
    DOCKER = "🐳"
    KALI = "💀"
    RAINBOW = "🌈"
    SPARKLES = "✨"
    LIGHTNING = "⚡"
    CROWN = "👑"
    DIAMOND = "💎"
    COMPASS = "🧭"
    MAP = "🗺️"
    FLAG = "🏁"
    TROPHY = "🏆"
    GIFT = "🎁"
    PARTY = "🎉"
    FIREWORKS = "🎆"
    CRYSTAL = "🔮"
    MAGIC = "🪄"
    SWORD = "⚔️"
    SHIELD = "🛡️"
    CROWN2 = "👑"
    MEDAL = "🏅"
    AWARD = "🏆"
    BRAIN = "🧠"
    ROBOT = "🤖"
    ALIEN = "👽"
    GHOST = "👻"
    SKULL = "💀"
    DRAGON = "🐉"
    PHOENIX = "🐦‍🔥"
    UNICORN = "🦄"
    BUTTERFLY = "🦋"
    FLOWER = "🌸"
    TREE = "🌳"
    MOUNTAIN = "⛰️"
    OCEAN = "🌊"
    SUN = "☀️"
    MOON = "🌙"
    STAR2 = "🌟"
    COMET = "☄️"
    GALAXY = "🌌"
    ATOM = "⚛️"
    DNA = "🧬"
    MICROSCOPE = "🔬"
    TELESCOPE = "🔭"
    ART = "🎨"
    MUSIC_NOTE = "🎵"
    MICROPHONE = "🎤"
    HEADPHONES = "🎧"
    GAME = "🎮"
    VR = "🥽"
    CAMERA = "📷"
    VIDEO_CAM = "📹"
    TV = "📺"
    RADIO = "📻"
    PHONE2 = "📞"
    COMPUTER = "🖥️"
    LAPTOP = "💻"
    TABLET = "📱"
    WATCH = "⌚"
    CLOCK2 = "⏲️"
    BELL = "🔔"
    ALARM = "⏰"
    CALENDAR2 = "📆"
    NOTEBOOK = "📓"
    BOOK = "📖"
    NEWSPAPER = "📰"
    LETTER = "✉️"
    ENVELOPE = "📧"
    PACKAGE = "📦"
    BOX = "📭"
    TRUCK = "🚚"
    AIRPLANE = "✈️"
    ROCKET2 = "🚀"
    SATELLITE = "🛰️"
    SPACESHIP = "🛸"
    CAR = "🚗"
    TRAIN = "🚂"
    BUS = "🚌"
    BIKE = "🚲"
    SCOOTER = "🛴"
    SKATEBOARD = "🛹"
    SURF = "🏄"
    SWIM = "🏊"
    RUN = "🏃"
    DANCE = "💃"
    YOGA = "🧘"
    MEDITATION = "🧘‍♂️"
    HEART2 = "💖"
    BROKEN_HEART = "💔"
    SPARKLE = "✨"
    GLITTER = "✨"
    RAINBOW2 = "🌈"
    CLOUD2 = "☁️"
    SNOW = "❄️"
    RAIN = "🌧️"
    STORM = "⛈️"
    TORNADO = "🌪️"
    VOLCANO = "🌋"
    EARTH = "🌍"
    PLANET = "🪐"
    ASTEROID = "☄️"

class Animations:
    @staticmethod
    def spinner(message: str, duration: float = 1, color: str = Colors.CYAN) -> None:
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end = time.time() + duration
        i = 0
        colors = [Colors.CYAN, Colors.MAGENTA, Colors.YELLOW, Colors.GREEN]
        while time.time() < end:
            color = colors[i % len(colors)]
            sys.stdout.write(f'\r{color}{chars[i % len(chars)]} {Colors.gradient_text(message, "rainbow")}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.05)
            i += 1
        sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
    
    @staticmethod
    def progress_bar(percent: int, width: int = 50, color: str = Colors.GREEN, gradient: bool = True) -> None:
        filled = int(width * percent / 100)
        if gradient:
            bar = ''
            for i in range(width):
                if i < filled:
                    intensity = 30 + int((i / width) * 60)
                    bar += f"\033[9{intensity//10}m█\033[0m"
                else:
                    bar += f"{Colors.DIM}░{Colors.RESET}"
        else:
            bar = f"{color}█{Colors.RESET}" * filled + f"{Colors.DIM}░{Colors.RESET}" * (width - filled)
        sys.stdout.write(f'\r{Colors.CYAN}[{bar}] {percent:3d}%{Colors.RESET}')
        sys.stdout.flush()
    
    @staticmethod
    def typing(text: str, delay: float = 0.02, color: str = Colors.CYAN) -> None:
        for char in text:
            sys.stdout.write(f"{color}{char}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def matrix_rain(seconds: int = 3, speed: float = 0.03) -> None:
        chars = '01'
        end = time.time() + seconds
        columns = shutil.get_terminal_size().columns
        colors = [Colors.GREEN, Colors.CYAN, Colors.GREEN, Colors.LIGHT_GRAY]
        while time.time() < end:
            line = ''.join(random.choice(chars) for _ in range(columns))
            color = random.choice(colors)
            sys.stdout.write(f'\r{color}{line}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(speed)
        print()
    
    @staticmethod
    def pulse(text: str, color: str = Colors.CYAN, duration: float = 2) -> None:
        end = time.time() + duration
        while time.time() < end:
            for intensity in range(0, 100, 10):
                bright = f"\033[{91 + intensity//10}m"
                sys.stdout.write(f'\r{bright}{text}{Colors.RESET}')
                sys.stdout.flush()
                time.sleep(0.05)
        print()
    
    @staticmethod
    def fire_effect(seconds: int = 3) -> None:
        flames = ['🔥', '💥', '⚡', '✨', '🌟', '💫', '⭐', '🌋', '🎇']
        end = time.time() + seconds
        colors = [Colors.RED, Colors.YELLOW, Colors.RED, Colors.MAGENTA, Colors.YELLOW]
        while time.time() < end:
            line = ''.join(random.choice(flames) for _ in range(20))
            color = random.choice(colors)
            sys.stdout.write(f'\r{color}{line}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.08)
        print()
    
    @staticmethod
    def rainbow_glow(seconds: int = 3) -> None:
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        end = time.time() + seconds
        text = "🌈 KALI TERMINAL ULTIMATE EDITION 🌈"
        while time.time() < end:
            for i, color in enumerate(colors):
                colored = ''.join(f"{color}{char}{Colors.RESET}" for char in text)
                sys.stdout.write(f'\r{colored}')
                sys.stdout.flush()
                time.sleep(0.1)
        print()
    
    @staticmethod
    def loading_animation(message: str = "Загрузка", duration: float = 2) -> None:
        chars = ['◐', '◓', '◑', '◒', '◐', '◓', '◑', '◒']
        end = time.time() + duration
        i = 0
        while time.time() < end:
            sys.stdout.write(f'\r{Colors.gradient_text(message + " " + chars[i % len(chars)], "cyan", single_color=True)}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        print()
    
    @staticmethod
    def wave_effect(text: str, duration: float = 2) -> None:
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        end = time.time() + duration
        while time.time() < end:
            for i, color in enumerate(colors):
                wave = ''
                for j, char in enumerate(text):
                    offset = (j + i) % len(colors)
                    wave += f"{colors[offset]}{char}{Colors.RESET}"
                sys.stdout.write(f'\r{wave}')
                sys.stdout.flush()
                time.sleep(0.05)
        print()
    
    @staticmethod
    def countdown(seconds: int, message: str = "Старт через") -> None:
        for i in range(seconds, 0, -1):
            sys.stdout.write(f'\r{Colors.gradient_text(f"{message}: {i}", "fire", single_color=True)}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f'\r{Colors.gradient_text(f"{message}: GO!", "fire", single_color=True)}{Colors.RESET}\n')
    
    @staticmethod
    def bounce(text: str, duration: float = 2) -> None:
        positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        end = time.time() + duration
        i = 0
        while time.time() < end:
            pos = positions[i % len(positions)]
            sys.stdout.write(f'\r{" " * pos}{Colors.gradient_text(text, "rainbow")}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.05)
            i += 1
        print()
    
    @staticmethod
    def explosion_effect(duration: float = 2) -> None:
        chars = ['💥', '✨', '🌟', '💫', '⭐', '💢', '💨', '💣']
        end = time.time() + duration
        while time.time() < end:
            line = ''.join(random.choice(chars) for _ in range(30))
            color = random.choice([Colors.RED, Colors.YELLOW, Colors.MAGENTA])
            sys.stdout.write(f'\r{color}{line}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.05)
        print()
    
    @staticmethod
    def starfield(duration: float = 3) -> None:
        stars = ['⭐', '🌟', '✨', '💫', '⚡']
        end = time.time() + duration
        columns = shutil.get_terminal_size().columns
        while time.time() < end:
            line = ''.join(random.choice(stars) for _ in range(columns))
            color = random.choice([Colors.WHITE, Colors.YELLOW, Colors.CYAN])
            sys.stdout.write(f'\r{color}{line}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.05)
        print()

class Utils:
    @staticmethod
    def human_size(size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
            if size < 1024.0:
                return f"{size:.2f}{unit}"
            size /= 1024.0
        return f"{size:.2f}PB"
    
    @staticmethod
    def human_time(seconds: float) -> str:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        return f"{secs}s"
    
    @staticmethod
    def human_speed(bytes_per_sec: float) -> str:
        return f"{Utils.human_size(bytes_per_sec)}/s"
    
    @staticmethod
    def get_username() -> str:
        try:
            if os.name == 'nt':
                return os.environ.get('USERNAME', 'user')
            return getpass.getuser()
        except:
            return 'user'
    
    @staticmethod
    def get_hostname() -> str:
        return socket.gethostname()
    
    @staticmethod
    def get_os_info() -> str:
        return f"{platform.system()} {platform.release()}"
    
    @staticmethod
    def get_time() -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def get_date() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_datetime() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def get_public_ip() -> str:
        try:
            if REQUESTS:
                response = requests.get('https://api.ipify.org', timeout=5)
                return response.text
        except:
            pass
        return Utils.get_ip()
    
    @staticmethod
    def shorten_path(path: str, max_len: int = 40) -> str:
        home = os.path.expanduser('~')
        if path.startswith(home):
            path = '~' + path[len(home):]
        if len(path) > max_len:
            parts = path.split(os.sep)
            if len(parts) > 3:
                return os.sep.join([parts[0], '...', parts[-2], parts[-1]])
            return '...' + path[-(max_len-3):]
        return path
    
    @staticmethod
    def file_icon(path: str) -> str:
        if os.path.isdir(path):
            return Icons.FOLDER
        elif os.path.islink(path):
            return Icons.LINK
        elif path.endswith(('.py', '.pyx', '.pyw')):
            return Icons.PYTHON
        elif path.endswith(('.sh', '.bash', '.zsh')):
            return Icons.TERMINAL
        elif path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            return "📜"
        elif path.endswith(('.html', '.htm', '.xhtml')):
            return "🌐"
        elif path.endswith(('.css', '.scss', '.sass')):
            return "🎨"
        elif path.endswith(('.json', '.xml', '.yaml', '.yml')):
            return "📋"
        elif path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp')):
            return Icons.IMAGE
        elif path.endswith(('.mp3', '.wav', '.flac', '.ogg', '.m4a')):
            return Icons.MUSIC
        elif path.endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv')):
            return Icons.VIDEO
        elif path.endswith(('.zip', '.tar', '.gz', '.bz2', '.xz', '.rar', '.7z')):
            return Icons.ARCHIVE
        elif path.endswith(('.exe', '.msi', '.app', '.deb', '.rpm')):
            return Icons.EXE
        elif path.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
            return "📄"
        elif path.endswith(('.txt', '.md', '.rst', '.log')):
            return "📝"
        return Icons.FILE
    
    @staticmethod
    def safe_execute(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}"
    
    @staticmethod
    def colorize_by_type(value: str, type_name: str) -> str:
        if type_name == 'dir':
            return f"{Colors.BLUE}{value}{Colors.RESET}"
        elif type_name == 'exec':
            return f"{Colors.GREEN}{value}{Colors.RESET}"
        elif type_name == 'link':
            return f"{Colors.CYAN}{value}{Colors.RESET}"
        elif type_name == 'error':
            return f"{Colors.RED}{value}{Colors.RESET}"
        elif type_name == 'file':
            return f"{Colors.WHITE}{value}{Colors.RESET}"
        elif type_name == 'archive':
            return f"{Colors.YELLOW}{value}{Colors.RESET}"
        elif type_name == 'image':
            return f"{Colors.MAGENTA}{value}{Colors.RESET}"
        return f"{Colors.WHITE}{value}{Colors.RESET}"
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except:
            return 80, 24
    
    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def is_windows() -> bool:
        return os.name == 'nt'
    
    @staticmethod
    def is_linux() -> bool:
        return platform.system() == 'Linux'
    
    @staticmethod
    def is_macos() -> bool:
        return platform.system() == 'Darwin'
    
    @staticmethod
    def get_cpu_count() -> int:
        return os.cpu_count() or 1
    
    @staticmethod
    def get_memory_total() -> int:
        if PSUTIL:
            return psutil.virtual_memory().total
        return 0
    
    @staticmethod
    def get_disk_total() -> int:
        if PSUTIL:
            return psutil.disk_usage('/').total
        return 0
    
    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]], align: str = 'left') -> str:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        result = []
        separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'
        result.append(separator)
        
        header_row = '|'
        for i, h in enumerate(headers):
            if align == 'center':
                header_row += f' {h.center(col_widths[i])} |'
            elif align == 'right':
                header_row += f' {h.rjust(col_widths[i])} |'
            else:
                header_row += f' {h.ljust(col_widths[i])} |'
        result.append(header_row)
        result.append(separator)
        
        for row in rows:
            data_row = '|'
            for i, cell in enumerate(row):
                if align == 'center':
                    data_row += f' {str(cell).center(col_widths[i])} |'
                elif align == 'right':
                    data_row += f' {str(cell).rjust(col_widths[i])} |'
                else:
                    data_row += f' {str(cell).ljust(col_widths[i])} |'
            result.append(data_row)
        
        result.append(separator)
        return '\n'.join(result)

class CommandManager:
    def __init__(self):
        self.commands = {}
        self.aliases = {}
        self.history = []
        self.history_path = Path.home() / '.kali_terminal_history'
        self.load_commands()
        self.setup_aliases()
        self.dir_stack = []
        self.load_history()
    
    def setup_aliases(self):
        self.aliases = {
            'l': 'ls',
            'la': 'ls -a',
            'll': 'ls -l',
            'lt': 'ls -lt',
            'lr': 'ls -lR',
            '..': 'cd ..',
            '...': 'cd ../..',
            '....': 'cd ../../..',
            '.....': 'cd ../../../..',
            'c': 'clear',
            'h': 'help',
            'q': 'exit',
            'grep': 'grep',
            'ps': 'ps',
            'df': 'df',
            'du': 'du',
            'free': 'df',
            'cls': 'clear',
            'tree': 'tree',
            'md': 'mkdir',
            'rd': 'rmdir',
            'del': 'rm',
            'copy': 'cp',
            'move': 'mv',
            'type': 'cat',
            'more': 'less',
            'vi': 'vim',
            'emacs': 'nano',
            'python': 'python3',
            'pip': 'pip3',
            'venv': 'python3 -m venv',
            'serve': 'python3 -m http.server',
        }
    
    def load_commands(self):
        self.add('help', self.help_cmd, 'Показать справку', 'help [команда]')
        self.add('h', self.help_cmd, 'Краткая справка', 'h')
        self.add('clear', self.clear_cmd, 'Очистить экран', 'clear')
        self.add('cls', self.clear_cmd, 'Очистить экран', 'cls')
        self.add('exit', self.exit_cmd, 'Выйти из терминала', 'exit')
        self.add('quit', self.exit_cmd, 'Выйти из терминала', 'quit')
        self.add('q', self.exit_cmd, 'Быстрый выход', 'q')
        
        self.add('pwd', self.pwd_cmd, 'Показать текущую директорию', 'pwd')
        self.add('ls', self.ls_cmd, 'Список файлов', 'ls [-a] [-l] [-h] [-R] [путь]')
        self.add('ll', self.ll_cmd, 'Подробный список файлов', 'll [путь]')
        self.add('la', self.la_cmd, 'Все файлы (включая скрытые)', 'la [путь]')
        self.add('lt', self.lt_cmd, 'Список файлов по времени', 'lt [путь]')
        self.add('lr', self.lr_cmd, 'Рекурсивный список файлов', 'lr [путь]')
        self.add('cd', self.cd_cmd, 'Сменить директорию', 'cd [путь]')
        self.add('tree', self.tree_cmd, 'Дерево директорий', 'tree [путь] [depth]')
        self.add('pushd', self.pushd_cmd, 'Сохранить директорию и перейти', 'pushd <путь>')
        self.add('popd', self.popd_cmd, 'Вернуться в сохраненную директорию', 'popd')
        self.add('dirs', self.dirs_cmd, 'Показать стек директорий', 'dirs')
        
        self.add('mkdir', self.mkdir_cmd, 'Создать директорию', 'mkdir [-p] <имя>')
        self.add('rmdir', self.rmdir_cmd, 'Удалить директорию', 'rmdir <имя>')
        self.add('rm', self.rm_cmd, 'Удалить файл', 'rm [-r] [-f] <файл>')
        self.add('cp', self.cp_cmd, 'Копировать файл', 'cp [-r] <источник> <назначение>')
        self.add('mv', self.mv_cmd, 'Переместить/переименовать', 'mv <источник> <назначение>')
        self.add('touch', self.touch_cmd, 'Создать файл', 'touch <файл>')
        self.add('cat', self.cat_cmd, 'Показать содержимое', 'cat [-n] <файл>')
        self.add('head', self.head_cmd, 'Первые строки', 'head [-n NUM] <файл>')
        self.add('tail', self.tail_cmd, 'Последние строки', 'tail [-n NUM] <файл>')
        self.add('wc', self.wc_cmd, 'Подсчет строк/слов/символов', 'wc [-lwc] <файл>')
        self.add('du', self.du_cmd, 'Размер директории', 'du [-h] [путь]')
        self.add('df', self.df_cmd, 'Свободное место на диске', 'df [-h]')
        self.add('find', self.find_cmd, 'Поиск файлов', 'find <путь> -name <шаблон>')
        self.add('file', self.file_cmd, 'Определить тип файла', 'file <файл>')
        self.add('stat', self.stat_cmd, 'Статистика файла', 'stat <файл>')
        self.add('chmod', self.chmod_cmd, 'Изменить права', 'chmod <права> <файл>')
        self.add('chown', self.chown_cmd, 'Изменить владельца', 'chown <пользователь> <файл>')
        self.add('ln', self.ln_cmd, 'Создать ссылку', 'ln [-s] <цель> <ссылка>')
        
        self.add('grep', self.grep_cmd, 'Поиск в тексте', 'grep [-i] <паттерн> <файл>')
        self.add('sort', self.sort_cmd, 'Сортировка строк', 'sort [-r] <файл>')
        self.add('uniq', self.uniq_cmd, 'Уникальные строки', 'uniq <файл>')
        self.add('cut', self.cut_cmd, 'Вырезать поля', 'cut -d <разделитель> -f <поля> <файл>')
        self.add('tr', self.tr_cmd, 'Транслитерация', "tr 'a-z' 'A-Z' <файл>")
        self.add('diff', self.diff_cmd, 'Сравнить файлы', 'diff <файл1> <файл2>')
        self.add('rev', self.rev_cmd, 'Перевернуть строки', 'rev <файл>')
        self.add('tac', self.tac_cmd, 'Вывести в обратном порядке', 'tac <файл>')
        self.add('sed', self.sed_cmd, 'Редактор потока', 'sed s/pattern/replace/ <файл>')
        self.add('awk', self.awk_cmd, 'Обработка текста', 'awk \'{print $1}\' <файл>')
        self.add('paste', self.paste_cmd, 'Объединить файлы', 'paste <файл1> <файл2>')
        self.add('join', self.join_cmd, 'Соединить файлы', 'join <файл1> <файл2>')
        self.add('less', self.less_cmd, 'Просмотр с постраничной навигацией', 'less <файл>')
        self.add('more', self.more_cmd, 'Просмотр с постраничной навигацией', 'more <файл>')
        
        self.add('date', self.date_cmd, 'Текущая дата и время', 'date')
        self.add('cal', self.cal_cmd, 'Календарь', 'cal [год] [месяц]')
        self.add('whoami', self.whoami_cmd, 'Имя пользователя', 'whoami')
        self.add('hostname', self.hostname_cmd, 'Имя хоста', 'hostname')
        self.add('uname', self.uname_cmd, 'Информация о системе', 'uname [-a]')
        self.add('uptime', self.uptime_cmd, 'Время работы системы', 'uptime')
        self.add('who', self.who_cmd, 'Кто в системе', 'who')
        self.add('w', self.w_cmd, 'Кто в системе (подробно)', 'w')
        self.add('last', self.last_cmd, 'Последние входы', 'last')
        self.add('env', self.env_cmd, 'Переменные окружения', 'env')
        self.add('echo', self.echo_cmd, 'Вывести текст', 'echo <текст>')
        self.add('sleep', self.sleep_cmd, 'Задержка', 'sleep <секунды>')
        self.add('time', self.time_cmd, 'Время выполнения', 'time <команда>')
        self.add('watch', self.watch_cmd, 'Повторять команду', 'watch <команда>')
        
        self.add('ping', self.ping_cmd, 'Проверка соединения', 'ping <хост>')
        self.add('ifconfig', self.ifconfig_cmd, 'Сетевые интерфейсы', 'ifconfig')
        self.add('ip', self.ip_cmd, 'IP адреса', 'ip')
        self.add('netstat', self.netstat_cmd, 'Сетевые соединения', 'netstat')
        self.add('nslookup', self.nslookup_cmd, 'DNS запрос', 'nslookup <домен>')
        self.add('dig', self.dig_cmd, 'DNS запрос (подробно)', 'dig <домен>')
        self.add('curl', self.curl_cmd, 'HTTP запрос', 'curl <url>')
        self.add('wget', self.wget_cmd, 'Скачать файл', 'wget <url>')
        self.add('portscan', self.portscan_cmd, 'Сканировать порты', 'portscan <хост>')
        self.add('telnet', self.telnet_cmd, 'Telnet клиент', 'telnet <хост> <порт>')
        self.add('ssh', self.ssh_cmd, 'SSH клиент', 'ssh <пользователь>@<хост>')
        self.add('ftp', self.ftp_cmd, 'FTP клиент', 'ftp <хост>')
        self.add('nc', self.nc_cmd, 'Netcat клиент', 'nc <хост> <порт>')
        
        self.add('hash', self.hash_cmd, 'Хешировать текст', 'hash <текст>')
        self.add('md5', self.md5_cmd, 'MD5 сумма', 'md5 <файл>')
        self.add('sha1', self.sha1_cmd, 'SHA1 сумма', 'sha1 <файл>')
        self.add('sha256', self.sha256_cmd, 'SHA256 сумма', 'sha256 <файл>')
        self.add('sha512', self.sha512_cmd, 'SHA512 сумма', 'sha512 <файл>')
        self.add('base64', self.base64_cmd, 'Base64 кодирование', 'base64 <текст>')
        self.add('base64d', self.base64d_cmd, 'Base64 декодирование', 'base64d <текст>')
        self.add('rot13', self.rot13_cmd, 'ROT13 шифрование', 'rot13 <текст>')
        self.add('rot47', self.rot47_cmd, 'ROT47 шифрование', 'rot47 <текст>')
        self.add('urlencode', self.urlencode_cmd, 'URL кодирование', 'urlencode <текст>')
        self.add('urldecode', self.urldecode_cmd, 'URL декодирование', 'urldecode <текст>')
        self.add('hex', self.hex_cmd, 'Hex кодирование', 'hex <текст>')
        self.add('unhex', self.unhex_cmd, 'Hex декодирование', 'unhex <hex>')
        self.add('random', self.random_cmd, 'Случайное число', 'random [max]')
        self.add('uuid', self.uuid_cmd, 'Сгенерировать UUID', 'uuid')
        self.add('password', self.password_cmd, 'Сгенерировать пароль', 'password [длина]')
        self.add('encrypt', self.encrypt_cmd, 'Шифровать текст', 'encrypt <текст> <ключ>')
        self.add('decrypt', self.decrypt_cmd, 'Расшифровать текст', 'decrypt <текст> <ключ>')
        
        self.add('ps', self.ps_cmd, 'Список процессов', 'ps [aux]')
        self.add('top', self.top_cmd, 'Монитор процессов', 'top')
        self.add('kill', self.kill_cmd, 'Завершить процесс', 'kill <pid>')
        self.add('pkill', self.pkill_cmd, 'Завершить по имени', 'pkill <имя>')
        self.add('jobs', self.jobs_cmd, 'Фоновые задачи', 'jobs')
        self.add('fg', self.fg_cmd, 'Вернуть задачу на передний план', 'fg [номер]')
        self.add('bg', self.bg_cmd, 'Запустить задачу в фоне', 'bg [номер]')
        self.add('nohup', self.nohup_cmd, 'Запустить в фоне', 'nohup <команда>')
        
        self.add('zip', self.zip_cmd, 'Создать zip архив', 'zip <архив> <файлы>')
        self.add('unzip', self.unzip_cmd, 'Распаковать zip', 'unzip <архив>')
        self.add('tar', self.tar_cmd, 'Работа с tar', 'tar -cf archive.tar файлы')
        self.add('gzip', self.gzip_cmd, 'Сжать gzip', 'gzip <файл>')
        self.add('gunzip', self.gunzip_cmd, 'Распаковать gzip', 'gunzip <файл>')
        self.add('7z', self.sevenz_cmd, '7-Zip архив', '7z <команда> <архив>')
        
        self.add('matrix', self.matrix_cmd, 'Матрица', 'matrix')
        self.add('hack', self.hack_cmd, 'Эффект взлома', 'hack')
        self.add('fire', self.fire_cmd, 'Огненный эффект', 'fire')
        self.add('rainbow', self.rainbow_cmd, 'Радужный эффект', 'rainbow')
        self.add('glow', self.glow_cmd, 'Свечение', 'glow')
        self.add('banner', self.banner_cmd, 'Красивый баннер', 'banner <текст>')
        self.add('cowsay', self.cowsay_cmd, 'Говорящая корова', 'cowsay <текст>')
        self.add('fortune', self.fortune_cmd, 'Случайная цитата', 'fortune')
        self.add('neofetch', self.neofetch_cmd, 'Информация о системе', 'neofetch')
        self.add('ascii', self.ascii_cmd, 'ASCII арт', 'ascii')
        self.add('figlet', self.figlet_cmd, 'ASCII баннер', 'figlet <текст>')
        self.add('sl', self.sl_cmd, 'Паровозик', 'sl')
        self.add('yes', self.yes_cmd, 'Повторять строку', 'yes [строка]')
        self.add('stars', self.stars_cmd, 'Звездное небо', 'stars')
        self.add('explosion', self.explosion_cmd, 'Эффект взрыва', 'explosion')
        self.add('bounce', self.bounce_cmd, 'Анимация подпрыгивания', 'bounce <текст>')
        
        self.add('info', self.info_cmd, 'Информация о терминале', 'info')
        self.add('sysinfo', self.sysinfo_cmd, 'Системная информация', 'sysinfo')
        self.add('version', self.version_cmd, 'Версия терминала', 'version')
        self.add('about', self.about_cmd, 'О программе', 'about')
        self.add('credits', self.credits_cmd, 'Авторы', 'credits')
        
        self.add('which', self.which_cmd, 'Найти программу', 'which <программа>')
        self.add('history', self.history_cmd, 'История команд', 'history')
        self.add('alias', self.alias_cmd, 'Создать алиас', 'alias <имя>=<команда>')
        self.add('unalias', self.unalias_cmd, 'Удалить алиас', 'unalias <имя>')
        self.add('man', self.man_cmd, 'Руководство', 'man <команда>')
        self.add('type', self.type_cmd, 'Тип команды', 'type <команда>')
        
        self.add('sqlite', self.sqlite_cmd, 'SQLite клиент', 'sqlite <база>')
        self.add('json', self.json_cmd, 'Показать JSON', 'json <файл>')
        self.add('csv', self.csv_cmd, 'Показать CSV', 'csv <файл>')
    
    def load_history(self):
        try:
            if self.history_path.exists():
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    self.history = [line.strip() for line in f if line.strip()]
        except:
            self.history = []
    
    def save_history(self, cmd):
        try:
            self.history.append(cmd)
            if len(self.history) > 1000:
                self.history = self.history[-1000:]
            with open(self.history_path, 'a', encoding='utf-8') as f:
                f.write(cmd + '\n')
        except:
            pass
    
    def add(self, name, func, desc, usage=''):
        self.commands[name] = {'func': func, 'desc': desc, 'usage': usage}
    
    def get(self, name):
        if name in self.aliases:
            name = self.aliases[name]
        return self.commands.get(name)
    
    def list(self):
        return self.commands.keys()
    
    def size(self):
        return len(self.commands)
    
    def help_cmd(self, args):
        terminal_width = shutil.get_terminal_size().columns
        if args:
            cmd = self.get(args[0])
            if cmd:
                help_text = f"""
{Colors.BOLD}{Colors.gradient_text(args[0].upper(), 'cyan', single_color=True)}{Colors.RESET}
{Colors.CYAN}{'─' * (terminal_width - 2)}{Colors.RESET}

{Colors.GREEN}ОПИСАНИЕ:{Colors.RESET}
  {cmd['desc']}

{Colors.GREEN}ИСПОЛЬЗОВАНИЕ:{Colors.RESET}
  {Colors.CYAN}{cmd['usage']}{Colors.RESET}

{Colors.GREEN}СИНТАКСИС:{Colors.RESET}
  {cmd['usage']}
"""
                print(Colors.box(help_text, Colors.GREEN, Colors.CYAN, 2))
                return True
        
        categories = {
            '📁 ФАЙЛЫ И ДИРЕКТОРИИ': ['ls', 'll', 'la', 'lt', 'lr', 'cd', 'pwd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv', 'touch', 'tree', 'pushd', 'popd', 'dirs'],
            '📄 РАБОТА С ФАЙЛАМИ': ['cat', 'head', 'tail', 'wc', 'du', 'df', 'find', 'file', 'stat', 'chmod', 'chown', 'ln'],
            '🔍 ПОИСК И ФИЛЬТРАЦИЯ': ['grep', 'find', 'which', 'file', 'stat', 'sort', 'uniq', 'cut', 'diff'],
            '📝 ОБРАБОТКА ТЕКСТА': ['head', 'tail', 'wc', 'sort', 'uniq', 'cut', 'diff', 'sed', 'awk', 'rev', 'tac', 'tr', 'paste', 'join', 'less', 'more'],
            '🌐 СЕТЕВЫЕ УТИЛИТЫ': ['ping', 'ifconfig', 'ip', 'netstat', 'nslookup', 'dig', 'curl', 'wget', 'portscan', 'telnet', 'ssh', 'ftp', 'nc'],
            '🔒 КРИПТОГРАФИЯ И ХЕШИ': ['hash', 'md5', 'sha1', 'sha256', 'sha512', 'base64', 'base64d', 'rot13', 'rot47', 'urlencode', 'urldecode', 'hex', 'unhex', 'random', 'uuid', 'password', 'encrypt', 'decrypt'],
            '💻 СИСТЕМНЫЕ КОМАНДЫ': ['date', 'cal', 'whoami', 'hostname', 'uname', 'uptime', 'who', 'w', 'last', 'env', 'echo', 'sleep', 'time', 'watch'],
            '⚙️ УПРАВЛЕНИЕ ПРОЦЕССАМИ': ['ps', 'top', 'kill', 'pkill', 'jobs', 'fg', 'bg', 'nohup'],
            '📦 АРХИВЫ И СЖАТИЕ': ['zip', 'unzip', 'tar', 'gzip', 'gunzip', '7z'],
            '🎨 ВИЗУАЛЬНЫЕ ЭФФЕКТЫ': ['matrix', 'hack', 'fire', 'rainbow', 'glow', 'banner', 'cowsay', 'fortune', 'neofetch', 'ascii', 'figlet', 'sl', 'yes', 'stars', 'explosion', 'bounce'],
            'ℹ️ ИНФОРМАЦИЯ И СПРАВКА': ['help', 'info', 'sysinfo', 'version', 'about', 'credits', 'history', 'alias', 'unalias', 'man', 'type'],
            '🗄️ БАЗЫ ДАННЫХ И ДАННЫЕ': ['sqlite', 'json', 'csv']
        }
        
        print(f"\n{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.BOLD}{Colors.gradient_text(f'📚 ДОСТУПНЫЕ КОМАНДЫ ({self.size()})'.center(terminal_width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
        
        for cat, cmds in categories.items():
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.BOLD}{Colors.gradient_text(cat, 'cyan', single_color=True)}{Colors.RESET}{Colors.gradient_text(' ' * (terminal_width - len(cat) - 3), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
            
            col_width = 18
            cols = max(1, (terminal_width - 4) // col_width)
            for i in range(0, len(cmds), cols):
                row = cmds[i:i+cols]
                line = '  '.join(f"{Colors.CYAN}{cmd:<{col_width - 2}}{Colors.RESET}" for cmd in row)
                padding = terminal_width - len(line) - 4
                if padding < 0:
                    padding = 0
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {line}{' ' * padding}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        
        print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        print(f"\n{Colors.DIM}Используйте 'help <команда>' для подробной информации{Colors.RESET}")
        return True
    
    def clear_cmd(self, args):
        os.system('cls' if os.name == 'nt' else 'clear')
        return True
    
    def exit_cmd(self, args):
        print(f"\n{Colors.gradient_text(f'{Icons.SUCCESS} До свидания! Спасибо за использование Kali Terminal!', 'cyan', single_color=True)}{Colors.RESET}")
        sys.exit(0)
    
    def pwd_cmd(self, args):
        print(f"{Colors.gradient_text(f'{Icons.FOLDER} {os.getcwd()}', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def ls_cmd(self, args):
        path = args[0] if args and not args[0].startswith('-') else '.'
        show_all = '-a' in args
        long = '-l' in args
        human = '-h' in args
        recursive = '-R' in args
        
        try:
            items = os.listdir(path)
            items.sort()
            if not show_all:
                items = [i for i in items if not i.startswith('.')]
            
            if long:
                print(f"{Colors.gradient_text(f"{'Права':12} {'Размер':>10} {'Дата':20} {'Имя'}", 'cyan', single_color=True)}{Colors.RESET}")
                print(f"{Colors.DIM}{'─' * 70}{Colors.RESET}")
                for item in items:
                    full = os.path.join(path, item)
                    try:
                        st = os.stat(full)
                        perms = stat.filemode(st.st_mode)
                        size = Utils.human_size(st.st_size) if human else str(st.st_size)
                        mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        icon = Utils.file_icon(full)
                        if os.path.isdir(full):
                            color = Colors.BLUE
                        elif os.access(full, os.X_OK):
                            color = Colors.GREEN
                        else:
                            color = Colors.WHITE
                        print(f"{color}{perms:<12}{Colors.RESET} {color}{size:>10}{Colors.RESET} {color}{mtime:20}{Colors.RESET} {icon} {color}{item}{Colors.RESET}")
                    except:
                        print(f"{Colors.RED}{item}{Colors.RESET}")
            else:
                cols = shutil.get_terminal_size().columns // 20
                for i, item in enumerate(items):
                    full = os.path.join(path, item)
                    icon = Utils.file_icon(full)
                    if os.path.isdir(full):
                        color = Colors.BLUE
                    elif os.access(full, os.X_OK):
                        color = Colors.GREEN
                    else:
                        color = Colors.WHITE
                    
                    print(f"{color}{icon} {item:<18}{Colors.RESET}", end='')
                    if (i + 1) % cols == 0:
                        print()
                if len(items) % cols != 0:
                    print()
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def ll_cmd(self, args):
        return self.ls_cmd(['-l'] + args)
    
    def la_cmd(self, args):
        return self.ls_cmd(['-a'] + args)
    
    def lt_cmd(self, args):
        path = args[0] if args and not args[0].startswith('-') else '.'
        try:
            items = os.listdir(path)
            items.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
            for item in items[:20]:
                full = os.path.join(path, item)
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d %H:%M")
                icon = Utils.file_icon(full)
                if os.path.isdir(full):
                    color = Colors.BLUE
                else:
                    color = Colors.WHITE
                print(f"{icon} {color}{item:<30}{Colors.RESET} {mtime}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def lr_cmd(self, args):
        path = args[0] if args else '.'
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{Colors.BLUE}{Icons.FOLDER} {os.path.basename(root)}{Colors.RESET}")
            subindent = '  ' * (level + 1)
            for file in files[:10]:
                print(f"{subindent}{Utils.file_icon(os.path.join(root, file))} {file}")
            if len(files) > 10:
                print(f"{subindent}{Colors.DIM}... и еще {len(files) - 10} файлов{Colors.RESET}")
        return True
    
    def cd_cmd(self, args):
        path = args[0] if args else os.path.expanduser('~')
        try:
            os.chdir(path)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} → {os.getcwd()}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def pushd_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: pushd <путь>{Colors.RESET}")
            return True
        
        self.dir_stack.append(os.getcwd())
        return self.cd_cmd(args)
    
    def popd_cmd(self, args):
        if not self.dir_stack:
            print(f"{Colors.YELLOW}{Icons.WARNING} Стек директорий пуст{Colors.RESET}")
            return True
        
        path = self.dir_stack.pop()
        return self.cd_cmd([path])
    
    def dirs_cmd(self, args):
        if not self.dir_stack:
            print(f"{Colors.YELLOW}{Icons.WARNING} Стек директорий пуст{Colors.RESET}")
            return True
        
        for i, d in enumerate(self.dir_stack):
            print(f"{Colors.CYAN}{i}: {Colors.gradient_text(d, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def tree_cmd(self, args):
        path = args[0] if args else '.'
        max_depth = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
        
        def print_tree(dir_path, prefix="", depth=0):
            if depth > max_depth:
                return
            
            try:
                items = sorted(os.listdir(dir_path))
                items = [i for i in items if not i.startswith('.')]
                
                for i, item in enumerate(items):
                    full = os.path.join(dir_path, item)
                    is_last = i == len(items) - 1
                    
                    connector = "└── " if is_last else "├── "
                    if os.path.isdir(full):
                        color = Colors.BLUE
                        icon = Icons.FOLDER
                    else:
                        color = Colors.GREEN
                        icon = Utils.file_icon(full)
                    
                    print(f"{prefix}{connector}{color}{icon} {item}{Colors.RESET}")
                    
                    if os.path.isdir(full):
                        extension = "    " if is_last else "│   "
                        print_tree(full, prefix + extension, depth + 1)
            except:
                pass
        
        print(f"{Colors.gradient_text(path, 'cyan', single_color=True)}{Colors.RESET}")
        print_tree(path)
        return True
    
    def mkdir_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: mkdir [-p] <имя>{Colors.RESET}")
            return True
        
        parents = '-p' in args
        dirs = [a for a in args if not a.startswith('-')]
        
        for d in dirs:
            try:
                if parents:
                    os.makedirs(d, exist_ok=True)
                else:
                    os.mkdir(d)
                print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Создано: {d}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def rmdir_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: rmdir <имя>{Colors.RESET}")
            return True
        for d in args:
            try:
                os.rmdir(d)
                print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Удалено: {d}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def rm_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: rm [-r] [-f] <файл>{Colors.RESET}")
            return True
        
        recursive = '-r' in args or '-rf' in args
        force = '-f' in args or '-rf' in args
        files = [a for a in args if not a.startswith('-')]
        
        for f in files:
            try:
                if os.path.isdir(f):
                    if recursive:
                        shutil.rmtree(f, ignore_errors=force)
                        print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Удалено: {f}', 'cyan', single_color=True)}{Colors.RESET}")
                    elif not force:
                        print(f"{Colors.YELLOW}{Icons.WARNING} Пропущен {f}: директория (используйте -r){Colors.RESET}")
                else:
                    if force and not os.path.exists(f):
                        continue
                    os.remove(f)
                    print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Удалено: {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                if not force:
                    print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def cp_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: cp [-r] <источник> <назначение>{Colors.RESET}")
            return True
        
        recursive = '-r' in args
        src_dst = [a for a in args if not a.startswith('-')]
        
        if len(src_dst) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Укажите источник и назначение{Colors.RESET}")
            return True
        
        src, dst = src_dst[0], src_dst[1]
        try:
            if os.path.isdir(src):
                if recursive:
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    print(f"{Colors.YELLOW}{Icons.WARNING} Пропущена директория {src} (используйте -r){Colors.RESET}")
                    return True
            else:
                shutil.copy2(src, dst)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Скопировано: {src} → {dst}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def mv_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: mv <источник> <назначение>{Colors.RESET}")
            return True
        
        src, dst = args[0], args[1]
        try:
            shutil.move(src, dst)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Перемещено: {src} → {dst}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def touch_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: touch <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                with open(f, 'a'):
                    os.utime(f, None)
                print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Обновлено: {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def cat_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: cat [-n] <файл>{Colors.RESET}")
            return True
        
        number = '-n' in args
        files = [a for a in args if not a.startswith('-')]
        
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    if number:
                        for i, line in enumerate(file, 1):
                            print(f"{Colors.DIM}{i:>6}{Colors.RESET} {line.rstrip()}")
                    else:
                        content = file.read()
                        if len(content) > 10000:
                            print(content[:10000])
                            print(f"\n{Colors.DIM}... (показано 10000 символов){Colors.RESET}")
                        else:
                            print(content)
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def head_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: head [-n NUM] <файл>{Colors.RESET}")
            return True
        
        n = 10
        file = None
        for arg in args:
            if arg.startswith('-n'):
                n = int(arg[2:]) if arg[2:] else 10
            elif not arg.startswith('-'):
                file = arg
        
        if file:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if i < n:
                            print(line.rstrip())
                        else:
                            break
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def tail_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: tail [-n NUM] <файл>{Colors.RESET}")
            return True
        
        n = 10
        file = None
        for arg in args:
            if arg.startswith('-n'):
                n = int(arg[2:]) if arg[2:] else 10
            elif not arg.startswith('-'):
                file = arg
        
        if file:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines[-n:]:
                        print(line.rstrip())
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def less_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: less <файл>{Colors.RESET}")
            return True
        
        file = args[0]
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            terminal_height = shutil.get_terminal_size().lines - 2
            start = 0
            while start < len(lines):
                for i in range(start, min(start + terminal_height, len(lines))):
                    print(lines[i].rstrip())
                print(f"\n{Colors.DIM}-- Показано {min(start + terminal_height, len(lines))} из {len(lines)} строк. Нажмите Enter для продолжения или q для выхода --{Colors.RESET}")
                key = input()
                if key.lower() == 'q':
                    break
                start += terminal_height
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def more_cmd(self, args):
        return self.less_cmd(args)
    
    def wc_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: wc [-lwc] <файл>{Colors.RESET}")
            return True
        
        lines_only = '-l' in args
        words_only = '-w' in args
        chars_only = '-c' in args
        files = [a for a in args if not a.startswith('-')]
        
        if not files:
            print(f"{Colors.YELLOW}{Icons.WARNING} Укажите файл{Colors.RESET}")
            return True
        
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    lines = content.count('\n')
                    words = len(content.split())
                    chars = len(content)
                    
                    if lines_only:
                        print(f"{Colors.CYAN}{lines:>8} {f}{Colors.RESET}")
                    elif words_only:
                        print(f"{Colors.CYAN}{words:>8} {f}{Colors.RESET}")
                    elif chars_only:
                        print(f"{Colors.CYAN}{chars:>8} {f}{Colors.RESET}")
                    else:
                        print(f"{Colors.CYAN}{lines:>8} {words:>8} {chars:>8} {f}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def du_cmd(self, args):
        path = args[0] if args and not args[0].startswith('-') else '.'
        human = '-h' in args
        
        try:
            total = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))
                    except:
                        pass
            
            size = Utils.human_size(total) if human else str(total)
            print(f"{Colors.gradient_text(f'{size} {path}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def df_cmd(self, args):
        human = '-h' in args
        
        if PSUTIL:
            disk = psutil.disk_usage('/')
            terminal_width = shutil.get_terminal_size().columns
            print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.BOLD}{Colors.gradient_text('📊 ИНФОРМАЦИЯ О ДИСКЕ'.center(terminal_width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
            
            total = Utils.human_size(disk.total) if human else f"{disk.total / (1024**3):.1f}GB"
            used = Utils.human_size(disk.used) if human else f"{disk.used / (1024**3):.1f}GB"
            free = Utils.human_size(disk.free) if human else f"{disk.free / (1024**3):.1f}GB"
            
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Всего:   {Colors.gradient_text(f'{total:>12}', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 24 - len(total)) + '║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Использовано: {Colors.gradient_text(f'{used:>12}', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 27 - len(used)) + '║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Свободно: {Colors.gradient_text(f'{free:>12}', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 26 - len(free)) + '║', 'cyan', single_color=True)}")
            
            bar_width = terminal_width - 8
            filled = int(bar_width * disk.percent / 100)
            bar = f"{Colors.RED if disk.percent > 90 else Colors.YELLOW if disk.percent > 70 else Colors.GREEN}█{Colors.RESET}" * filled + f"{Colors.DIM}░{Colors.RESET}" * (bar_width - filled)
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Занято:   {bar}{Colors.gradient_text(' ' * (terminal_width - 18 - bar_width) + '║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Процент:  {Colors.RED if disk.percent > 90 else Colors.YELLOW if disk.percent > 70 else Colors.GREEN}{disk.percent:>5.1f}%{Colors.RESET}{Colors.gradient_text(' ' * (terminal_width - 21 - len(str(disk.percent))) + '║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Установите psutil: pip install psutil{Colors.RESET}")
        return True
    
    def find_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: find <путь> -name <шаблон>{Colors.RESET}")
            return True
        
        path = args[0] if args[0] != '-name' else '.'
        pattern = None
        for i, arg in enumerate(args):
            if arg == '-name' and i + 1 < len(args):
                pattern = args[i + 1]
                break
        
        if not pattern:
            print(f"{Colors.YELLOW}{Icons.WARNING} Укажите -name <шаблон>{Colors.RESET}")
            return True
        
        found = False
        for root, dirs, files in os.walk(path):
            for f in files:
                if fnmatch.fnmatch(f, pattern):
                    print(f"{Colors.gradient_text(f'{Icons.FILE} {os.path.join(root, f)}', 'cyan', single_color=True)}{Colors.RESET}")
                    found = True
        if not found:
            print(f"{Colors.YELLOW}{Icons.WARNING} Файлы не найдены{Colors.RESET}")
        return True
    
    def file_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: file <файл>{Colors.RESET}")
            return True
        
        for f in args:
            if os.path.isfile(f):
                print(f"{Colors.CYAN}{f}: {Colors.GREEN}файл{Colors.RESET}")
            elif os.path.isdir(f):
                print(f"{Colors.CYAN}{f}: {Colors.BLUE}директория{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}{f}: {Colors.RED}неизвестно{Colors.RESET}")
        return True
    
    def stat_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: stat <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                st = os.stat(f)
                terminal_width = shutil.get_terminal_size().columns
                print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(f, 'cyan', single_color=True)}{' ' * (terminal_width - len(f) - 4)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Размер: {Colors.GREEN}{Utils.human_size(st.st_size)}{Colors.gradient_text(' ' * (terminal_width - 18 - len(Utils.human_size(st.st_size))) + '║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Права:  {Colors.YELLOW}{stat.filemode(st.st_mode)}{Colors.gradient_text(' ' * (terminal_width - 18 - len(stat.filemode(st.st_mode))) + '║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Изменен:{Colors.GREEN} {datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}{Colors.gradient_text(' ' * (terminal_width - 31 - len(datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S'))) + '║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Создан: {Colors.GREEN}{datetime.datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}{Colors.gradient_text(' ' * (terminal_width - 31 - len(datetime.datetime.fromtimestamp(st.st_ctime).strftime('%Y-%m-%d %H:%M:%S'))) + '║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Доступ: {Colors.GREEN}{datetime.datetime.fromtimestamp(st.st_atime).strftime('%Y-%m-%d %H:%M:%S')}{Colors.gradient_text(' ' * (terminal_width - 31 - len(datetime.datetime.fromtimestamp(st.st_atime).strftime('%Y-%m-%d %H:%M:%S'))) + '║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def chmod_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: chmod <права> <файл>{Colors.RESET}")
            return True
        
        mode = args[0]
        files = args[1:]
        
        try:
            if mode.isdigit():
                mode = int(mode, 8)
            else:
                mode = 0o755
        except:
            print(f"{Colors.RED}{Icons.ERROR} Неверный режим{Colors.RESET}")
            return True
        
        for f in files:
            try:
                os.chmod(f, mode)
                print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Права изменены: {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def chown_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: chown <пользователь> <файл>{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} chown не поддерживается в Windows{Colors.RESET}")
        return True
    
    def ln_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: ln [-s] <цель> <ссылка>{Colors.RESET}")
            return True
        
        symbolic = '-s' in args
        args = [a for a in args if not a.startswith('-')]
        
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Укажите цель и имя ссылки{Colors.RESET}")
            return True
        
        target, link = args[0], args[1]
        try:
            if symbolic:
                os.symlink(target, link)
            else:
                os.link(target, link)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Ссылка создана: {link} → {target}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def grep_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: grep [-i] <паттерн> <файл>{Colors.RESET}")
            return True
        
        ignore_case = '-i' in args
        pattern = args[0] if not args[0].startswith('-') else args[1]
        files = [a for a in args if not a.startswith('-') and a != pattern]
        
        if ignore_case:
            pattern = pattern.lower()
        
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        line_stripped = line.rstrip()
                        search_line = line_stripped.lower() if ignore_case else line_stripped
                        if pattern in search_line:
                            highlighted = re.sub(
                                f'(?i)({re.escape(pattern)})',
                                f'{Colors.RED}\\1{Colors.RESET}',
                                line_stripped
                            )
                            print(highlighted)
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def sort_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: sort [-r] <файл>{Colors.RESET}")
            return True
        
        reverse = '-r' in args
        files = [a for a in args if not a.startswith('-')]
        
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                lines.sort(reverse=reverse)
                for line in lines:
                    print(line.rstrip())
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def uniq_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: uniq <файл>{Colors.RESET}")
            return True
        
        f = args[0]
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
            seen = set()
            for line in lines:
                if line not in seen:
                    seen.add(line)
                    print(line.rstrip())
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def cut_cmd(self, args):
        if len(args) < 4:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: cut -d <разделитель> -f <поля> <файл>{Colors.RESET}")
            return True
        
        delimiter = None
        fields = None
        file = None
        
        for i, arg in enumerate(args):
            if arg == '-d' and i + 1 < len(args):
                delimiter = args[i + 1]
            elif arg == '-f' and i + 1 < len(args):
                fields = args[i + 1]
            elif not arg.startswith('-'):
                file = arg
        
        if delimiter and fields and file:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        parts = line.strip().split(delimiter)
                        if fields == '1' and parts:
                            print(parts[0])
                        else:
                            print(line.strip())
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def tr_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: tr 'a-z' 'A-Z' <файл>{Colors.RESET}")
            return True
        
        from_set = args[0].strip("'")
        to_set = args[1].strip("'")
        file = args[2] if len(args) > 2 else None
        
        if file:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                table = str.maketrans(from_set, to_set)
                print(content.translate(table))
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def diff_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: diff <файл1> <файл2>{Colors.RESET}")
            return True
        
        try:
            with open(args[0], 'r') as f1, open(args[1], 'r') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
                diff_count = 0
                for i, (l1, l2) in enumerate(itertools.zip_longest(lines1, lines2)):
                    if l1 != l2:
                        diff_count += 1
                        if diff_count <= 20:
                            if l1:
                                print(f"{Colors.RED}- {l1.rstrip()}{Colors.RESET}")
                            if l2:
                                print(f"{Colors.GREEN}+ {l2.rstrip()}{Colors.RESET}")
                if diff_count > 20:
                    print(f"{Colors.DIM}... и еще {diff_count - 20} различий{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def rev_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: rev <файл>{Colors.RESET}")
            return True
        
        f = args[0]
        try:
            with open(f, 'r') as file:
                for line in file:
                    print(line.rstrip()[::-1])
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def tac_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: tac <файл>{Colors.RESET}")
            return True
        
        f = args[0]
        try:
            with open(f, 'r') as file:
                lines = file.readlines()
                for line in reversed(lines):
                    print(line.rstrip())
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def sed_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: sed s/pattern/replace/ <файл>{Colors.RESET}")
            return True
        
        expression = args[0]
        file = args[1] if len(args) > 1 else None
        
        if not expression.startswith('s/') or not expression.endswith('/'):
            print(f"{Colors.RED}{Icons.ERROR} Неверный формат выражения{Colors.RESET}")
            return True
        
        parts = expression[2:-1].split('/')
        if len(parts) < 2:
            print(f"{Colors.RED}{Icons.ERROR} Неверный формат выражения{Colors.RESET}")
            return True
        
        pattern, replace = parts[0], parts[1]
        
        if file:
            try:
                with open(file, 'r') as f:
                    for line in f:
                        new_line = re.sub(pattern, replace, line)
                        print(new_line.rstrip())
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def awk_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: awk '{{print $1}}' <файл>{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} Awk реализован частично{Colors.RESET}")
        return True
    
    def paste_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: paste <файл1> <файл2>{Colors.RESET}")
            return True
        
        try:
            with open(args[0], 'r') as f1, open(args[1], 'r') as f2:
                for l1, l2 in itertools.zip_longest(f1, f2):
                    print(f"{l1.rstrip()}\t{l2.rstrip() if l2 else ''}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def join_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: join <файл1> <файл2>{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} Join реализован частично{Colors.RESET}")
        return True
    
    def date_cmd(self, args):
        now = datetime.datetime.now()
        terminal_width = shutil.get_terminal_size().columns
        print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(f'📅 {now.strftime("%A, %d %B %Y")}', 'cyan', single_color=True)}{' ' * (terminal_width - 26 - len(now.strftime('%A, %d %B %Y')))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(f'⏰ {now.strftime("%H:%M:%S")}', 'cyan', single_color=True)}{' ' * (terminal_width - 5 - len(now.strftime('%H:%M:%S')))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(f'📆 Неделя {now.isocalendar()[1]}', 'cyan', single_color=True)}{' ' * (terminal_width - 13 - len(f'Неделя {now.isocalendar()[1]}'))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        return True
    
    def cal_cmd(self, args):
        now = datetime.datetime.now()
        year = int(args[0]) if args and args[0].isdigit() else now.year
        month = int(args[1]) if len(args) > 1 and args[1].isdigit() else now.month
        
        cal = calendar.month(year, month)
        print(f"{Colors.gradient_text(cal, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def whoami_cmd(self, args):
        print(f"{Colors.gradient_text(f'{Icons.USER} {Utils.get_username()}', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def hostname_cmd(self, args):
        print(f"{Colors.gradient_text(f'{Icons.NETWORK} {socket.gethostname()}', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def uname_cmd(self, args):
        if args and args[0] == '-a':
            info = f"{platform.system()} {platform.release()} {platform.version()} {platform.machine()}"
        else:
            info = platform.system()
        print(f"{Colors.gradient_text(info, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def uptime_cmd(self, args):
        if PSUTIL:
            boot = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot
            print(f"{Colors.gradient_text(f'{Icons.CLOCK} uptime: {Utils.human_time(uptime.total_seconds())}', 'cyan', single_color=True)}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Установите psutil{Colors.RESET}")
        return True
    
    def who_cmd(self, args):
        if PSUTIL:
            for user in psutil.users():
                print(f"{Colors.gradient_text(user.name, 'cyan', single_color=True)}{Colors.RESET}  {user.terminal}  {datetime.datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"{Colors.gradient_text(Utils.get_username(), 'cyan', single_color=True)}{Colors.RESET}  pts/0  {Utils.get_date()} {Utils.get_time()}")
        return True
    
    def w_cmd(self, args):
        print(f"{Colors.gradient_text(f"{'USER':<10} {'TTY':<10} {'FROM':<15} {'LOGIN@':<12} {'IDLE':<8} {'JCPU':<8} {'PCPU':<8} {'WHAT':<20}", 'cyan', single_color=True)}{Colors.RESET}")
        print(f"{Colors.DIM}{'-' * 90}{Colors.RESET}")
        
        if PSUTIL:
            for user in psutil.users():
                login_time = datetime.datetime.fromtimestamp(user.started).strftime('%H:%M')
                print(f"{Colors.GREEN}{user.name:<10}{Colors.RESET} {user.terminal:<10} {user.host or 'local':<15} {login_time:<12} {'0.00s':<8} {'0.00s':<8} {'0.00s':<8} {'-':<20}")
        else:
            print(f"{Colors.GREEN}{Utils.get_username():<10}{Colors.RESET} pts/0      local           {Utils.get_time():<12} 0.00s   0.00s   0.00s   -")
        return True
    
    def last_cmd(self, args):
        print(f"{Colors.gradient_text(f"{'USER':<10} {'TTY':<10} {'FROM':<15} {'LOGIN@':<20}", 'cyan', single_color=True)}{Colors.RESET}")
        print(f"{Colors.DIM}{'-' * 55}{Colors.RESET}")
        print(f"{Colors.GREEN}{Utils.get_username():<10}{Colors.RESET} pts/0      local           {Utils.get_date()} {Utils.get_time()}")
        print(f"{Colors.DIM}wtmp begins {Utils.get_date()} {Utils.get_time()}{Colors.RESET}")
        return True
    
    def env_cmd(self, args):
        for key, value in sorted(os.environ.items()):
            print(f"{Colors.gradient_text(key, 'cyan', single_color=True)}{Colors.RESET}={value}")
        return True
    
    def echo_cmd(self, args):
        text = ' '.join(args)
        if text.startswith('$'):
            var = text[1:]
            print(os.environ.get(var, ''))
        else:
            print(Colors.gradient_text(text, 'cyan', single_color=True))
        return True
    
    def sleep_cmd(self, args):
        if args:
            try:
                time.sleep(float(args[0]))
            except:
                pass
        return True
    
    def time_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: time <команда>{Colors.RESET}")
            return True
        
        cmd = ' '.join(args)
        start = time.time()
        self.execute(cmd)
        elapsed = time.time() - start
        print(f"\n{Colors.gradient_text(f'real\t{Utils.human_time(elapsed)}', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def watch_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: watch <команда>{Colors.RESET}")
            return True
        
        cmd = ' '.join(args)
        try:
            for _ in range(3):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{Colors.gradient_text(f'Every 2s: {cmd}', 'cyan', single_color=True)}{Colors.RESET}")
                print(f"{Colors.DIM}{Utils.get_date()} {Utils.get_time()}{Colors.RESET}")
                print()
                self.execute(cmd)
                time.sleep(2)
        except KeyboardInterrupt:
            print()
        return True
    
    def which_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: which <программа>{Colors.RESET}")
            return True
        
        for prog in args:
            found = False
            if prog in self.commands:
                print(f"{Colors.gradient_text(f'{prog}: встроенная команда', 'cyan', single_color=True)}{Colors.RESET}")
                found = True
            
            for path in os.environ.get('PATH', '').split(':' if os.name != 'nt' else ';'):
                full = os.path.join(path, prog)
                if os.path.exists(full):
                    print(f"{Colors.gradient_text(full, 'cyan', single_color=True)}{Colors.RESET}")
                    found = True
                    break
            if not found:
                print(f"{Colors.RED}{prog}: not found{Colors.RESET}")
        return True
    
    def history_cmd(self, args):
        try:
            if self.history_path.exists():
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines[-50:], 1):
                        print(f"{Colors.gradient_text(f'{i:>5}', 'cyan', single_color=True)}{Colors.RESET} {line.strip()}")
            else:
                print(f"{Colors.YELLOW}{Icons.WARNING} История пуста{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}{Icons.WARNING} История пуста{Colors.RESET}")
        return True
    
    def alias_cmd(self, args):
        if not args:
            if self.aliases:
                print(f"{Colors.gradient_text('Алиасы:', 'cyan', single_color=True)}{Colors.RESET}")
                for name, value in sorted(self.aliases.items()):
                    print(f"{Colors.GREEN}{name}{Colors.RESET}='{value}'")
            else:
                print(f"{Colors.YELLOW}{Icons.WARNING} Алиасы не установлены{Colors.RESET}")
            return True
        
        if '=' in args[0]:
            name, value = args[0].split('=', 1)
            self.aliases[name] = value
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Алиас: {name}=\'{value}\'', 'cyan', single_color=True)}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: alias имя=команда{Colors.RESET}")
        return True
    
    def unalias_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: unalias <имя>{Colors.RESET}")
            return True
        
        name = args[0]
        if name in self.aliases:
            del self.aliases[name]
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Алиас удален: {name}', 'cyan', single_color=True)}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Алиас не найден: {name}{Colors.RESET}")
        return True
    
    def man_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: man <команда>{Colors.RESET}")
            return True
        
        cmd = self.get(args[0])
        if cmd:
            terminal_width = shutil.get_terminal_size().columns
            man_text = f"""
{Colors.BOLD}{Colors.gradient_text(args[0].upper(), 'cyan', single_color=True)}{Colors.RESET}
{Colors.CYAN}{'─' * (terminal_width - 2)}{Colors.RESET}

{Colors.GREEN}НАЗВАНИЕ{Colors.RESET}
       {cmd['desc']}

{Colors.GREEN}СИНТАКСИС{Colors.RESET}
       {Colors.CYAN}{cmd['usage']}{Colors.RESET}

{Colors.GREEN}ОПИСАНИЕ{Colors.RESET}
       {cmd['desc']}

{Colors.GREEN}ПРИМЕРЫ{Colors.RESET}
       $ {cmd['usage']}
"""
            print(Colors.box(man_text, Colors.GREEN, Colors.CYAN, 2))
        else:
            print(f"{Colors.RED}{Icons.ERROR} Команда не найдена: {args[0]}{Colors.RESET}")
        return True
    
    def type_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: type <команда>{Colors.RESET}")
            return True
        
        cmd = args[0]
        if cmd in self.aliases:
            print(f"{cmd} - алиас для '{self.aliases[cmd]}'")
        elif cmd in self.commands:
            print(f"{cmd} - встроенная команда")
        else:
            print(f"{cmd} - внешняя команда")
        return True
    
    def sqlite_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: sqlite <база>{Colors.RESET}")
            return True
        
        db_path = args[0]
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                print(f"{Colors.gradient_text('Таблицы:', 'cyan', single_color=True)}{Colors.RESET}")
                for table in tables:
                    print(f"  {table[0]}")
            else:
                print(f"{Colors.YELLOW}База данных пуста{Colors.RESET}")
            conn.close()
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def json_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: json <файл>{Colors.RESET}")
            return True
        
        f = args[0]
        try:
            with open(f, 'r') as file:
                data = json.load(file)
                print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def csv_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: csv <файл>{Colors.RESET}")
            return True
        
        f = args[0]
        try:
            with open(f, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    print(' | '.join(row))
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def ping_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: ping <хост>{Colors.RESET}")
            return True
        
        host = args[0]
        count = 4
        for arg in args:
            if arg.startswith('-c'):
                count = int(arg[2:]) if arg[2:] else 4
        
        print(f"{Colors.gradient_text(f'PING {host} ({host})', 'cyan', single_color=True)}{Colors.RESET}")
        for i in range(count):
            try:
                start = time.time()
                ip = socket.gethostbyname(host)
                elapsed = (time.time() - start) * 1000
                print(f"{Colors.GREEN}64 bytes from {ip}: icmp_seq={i} time={elapsed:.2f} ms{Colors.RESET}")
            except:
                print(f"{Colors.RED}Request timeout{Colors.RESET}")
            time.sleep(1)
        return True
    
    def ifconfig_cmd(self, args):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f"{Colors.gradient_text('lo:', 'cyan', single_color=True)}{Colors.RESET}")
        print(f"    inet {Colors.GREEN}127.0.0.1{Colors.RESET}")
        print(f"{Colors.gradient_text('eth0:', 'cyan', single_color=True)}{Colors.RESET}")
        print(f"    inet {Colors.GREEN}{ip}{Colors.RESET}")
        return True
    
    def ip_cmd(self, args):
        hostname = socket.gethostname()
        ip = Utils.get_ip()
        public_ip = Utils.get_public_ip()
        print(f"{Colors.gradient_text('╔' + '═' * 50 + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('СЕТЕВАЯ ИНФОРМАЦИЯ', 'cyan', single_color=True)}{' ' * 30}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╠' + '═' * 50 + '╣', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Локальный IP: {Colors.gradient_text(ip, 'cyan', single_color=True)}{' ' * (50 - 14 - len(ip))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Публичный IP: {Colors.gradient_text(public_ip, 'cyan', single_color=True)}{' ' * (50 - 14 - len(public_ip))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Имя хоста:   {Colors.gradient_text(hostname, 'cyan', single_color=True)}{' ' * (50 - 14 - len(hostname))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╚' + '═' * 50 + '╝', 'cyan', single_color=True)}")
        return True
    
    def netstat_cmd(self, args):
        if PSUTIL:
            print(f"{Colors.gradient_text(f"{'Proto':6} {'Local Address':30} {'Remote Address':30} {'State':15}", 'cyan', single_color=True)}{Colors.RESET}")
            print(f"{Colors.DIM}{'-' * 90}{Colors.RESET}")
            for conn in psutil.net_connections()[:20]:
                if conn.status:
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else '*:*'
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else '*:*'
                    print(f"tcp     {laddr:<30} {raddr:<30} {conn.status:<15}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Установите psutil{Colors.RESET}")
        return True
    
    def nslookup_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: nslookup <домен>{Colors.RESET}")
            return True
        
        domain = args[0]
        try:
            ip = socket.gethostbyname(domain)
            print(f"{Colors.CYAN}Server: 8.8.8.8{Colors.RESET}")
            print(f"\nNon-authoritative answer:")
            print(f"Name: {Colors.GREEN}{domain}{Colors.RESET}")
            print(f"Address: {Colors.GREEN}{ip}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def dig_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: dig <домен>{Colors.RESET}")
            return True
        
        domain = args[0]
        try:
            ip = socket.gethostbyname(domain)
            print(f"{Colors.CYAN}; <<>> DIG 9.16.1 <<>> {domain}{Colors.RESET}")
            print(f"{Colors.CYAN};; Got answer:{Colors.RESET}")
            print(f"{Colors.CYAN};; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: {random.randint(1, 65535)}{Colors.RESET}")
            print(f"\n{Colors.CYAN};; QUESTION SECTION:{Colors.RESET}")
            print(f";{domain}.            IN      A")
            print(f"\n{Colors.CYAN};; ANSWER SECTION:{Colors.RESET}")
            print(f"{domain}.       300     IN      A       {ip}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def curl_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: curl <url>{Colors.RESET}")
            return True
        
        url = args[0]
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                if len(content) > 5000:
                    print(content[:5000])
                    print(f"\n{Colors.DIM}... (показано 5000 символов){Colors.RESET}")
                else:
                    print(content)
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def wget_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: wget <url>{Colors.RESET}")
            return True
        
        url = args[0]
        filename = url.split('/')[-1] or 'download'
        print(f"{Colors.gradient_text(f'{Icons.DOWNLOAD} Скачивание {url}...', 'cyan', single_color=True)}{Colors.RESET}")
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Сохранено: {filename}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def portscan_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: portscan <хост>{Colors.RESET}")
            return True
        
        host = args[0]
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443, 27017]
        
        print(f"{Colors.gradient_text(f'Сканирование {host}...', 'cyan', single_color=True)}{Colors.RESET}")
        open_ports = []
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"{Colors.GREEN}{Icons.SUCCESS} Порт {port}: открыт{Colors.RESET}")
                open_ports.append(port)
            else:
                print(f"{Colors.DIM}{Icons.INFO} Порт {port}: закрыт{Colors.RESET}")
            sock.close()
        
        if open_ports:
            print(f"\n{Colors.GREEN}Найдено открытых портов: {len(open_ports)}{Colors.RESET}")
        return True
    
    def telnet_cmd(self, args):
        if len(args) < 1:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: telnet <хост> [порт]{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} Telnet клиент в разработке{Colors.RESET}")
        return True
    
    def ssh_cmd(self, args):
        if len(args) < 1:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: ssh <пользователь>@<хост>{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} SSH клиент в разработке{Colors.RESET}")
        return True
    
    def ftp_cmd(self, args):
        if len(args) < 1:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: ftp <хост>{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} FTP клиент в разработке{Colors.RESET}")
        return True
    
    def nc_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: nc <хост> <порт>{Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} Netcat клиент в разработке{Colors.RESET}")
        return True
    
    def hash_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: hash <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        terminal_width = shutil.get_terminal_size().columns
        print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('ХЕШИ ТЕКСТА', 'cyan', single_color=True)}{' ' * (terminal_width - 13)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} MD5:    {Colors.GREEN}{hashlib.md5(text.encode()).hexdigest()}{Colors.gradient_text(' ' * (terminal_width - 16 - len(hashlib.md5(text.encode()).hexdigest())) + '║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} SHA1:   {Colors.GREEN}{hashlib.sha1(text.encode()).hexdigest()}{Colors.gradient_text(' ' * (terminal_width - 16 - len(hashlib.sha1(text.encode()).hexdigest())) + '║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} SHA256: {Colors.GREEN}{hashlib.sha256(text.encode()).hexdigest()}{Colors.gradient_text(' ' * (terminal_width - 17 - len(hashlib.sha256(text.encode()).hexdigest())) + '║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} SHA512: {Colors.GREEN}{hashlib.sha512(text.encode()).hexdigest()}{Colors.gradient_text(' ' * (terminal_width - 17 - len(hashlib.sha512(text.encode()).hexdigest())) + '║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        return True
    
    def md5_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: md5 <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                with open(f, 'rb') as file:
                    md5 = hashlib.md5(file.read()).hexdigest()
                    print(f"{Colors.gradient_text(f'{md5} {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def sha1_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: sha1 <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                with open(f, 'rb') as file:
                    sha1 = hashlib.sha1(file.read()).hexdigest()
                    print(f"{Colors.gradient_text(f'{sha1} {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def sha256_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: sha256 <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                with open(f, 'rb') as file:
                    sha256 = hashlib.sha256(file.read()).hexdigest()
                    print(f"{Colors.gradient_text(f'{sha256} {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def sha512_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: sha512 <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                with open(f, 'rb') as file:
                    sha512 = hashlib.sha512(file.read()).hexdigest()
                    print(f"{Colors.gradient_text(f'{sha512} {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def base64_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: base64 <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        encoded = base64.b64encode(text.encode()).decode()
        print(f"{Colors.gradient_text(encoded, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def base64d_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: base64d <base64>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        try:
            decoded = base64.b64decode(text).decode('utf-8', errors='ignore')
            print(f"{Colors.gradient_text(decoded, 'cyan', single_color=True)}{Colors.RESET}")
        except:
            print(f"{Colors.RED}{Icons.ERROR} Ошибка декодирования{Colors.RESET}")
        return True
    
    def rot13_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: rot13 <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        result = ''.join(
            chr((ord(c) - 65 + 13) % 26 + 65) if 'A' <= c <= 'Z' else
            chr((ord(c) - 97 + 13) % 26 + 97) if 'a' <= c <= 'z' else c
            for c in text
        )
        print(f"{Colors.gradient_text(result, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def rot47_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: rot47 <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        result = ''.join(
            chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c
            for c in text
        )
        print(f"{Colors.gradient_text(result, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def urlencode_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: urlencode <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        encoded = urllib.parse.quote(text)
        print(f"{Colors.gradient_text(encoded, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def urldecode_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: urldecode <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        decoded = urllib.parse.unquote(text)
        print(f"{Colors.gradient_text(decoded, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def hex_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: hex <текст>{Colors.RESET}")
            return True
        
        text = ' '.join(args)
        encoded = text.encode().hex()
        print(f"{Colors.gradient_text(encoded, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def unhex_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: unhex <hex>{Colors.RESET}")
            return True
        
        text = args[0]
        try:
            decoded = bytes.fromhex(text).decode('utf-8', errors='ignore')
            print(f"{Colors.gradient_text(decoded, 'cyan', single_color=True)}{Colors.RESET}")
        except:
            print(f"{Colors.RED}{Icons.ERROR} Ошибка декодирования{Colors.RESET}")
        return True
    
    def random_cmd(self, args):
        if args and args[0].isdigit():
            num = random.randint(0, int(args[0]))
        else:
            num = random.randint(0, 100)
        print(f"{Colors.gradient_text(f'{Icons.STAR} {num}', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def uuid_cmd(self, args):
        print(f"{Colors.gradient_text(str(uuid.uuid4()), 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def password_cmd(self, args):
        length = int(args[0]) if args and args[0].isdigit() else 16
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = ''.join(secrets.choice(chars) for _ in range(length))
        terminal_width = shutil.get_terminal_size().columns
        print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('СГЕНЕРИРОВАННЫЙ ПАРОЛЬ', 'cyan', single_color=True)}{' ' * (terminal_width - 27)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(password, 'cyan', single_color=True)}{' ' * (terminal_width - len(password) - 4)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Длина: {Colors.GREEN}{length}{Colors.gradient_text(' ' * (terminal_width - 16 - len(str(length))) + '║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        return True
    
    def encrypt_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: encrypt <текст> <ключ>{Colors.RESET}")
            return True
        
        text = args[0]
        key = args[1]
        
        encrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
        encrypted_b64 = base64.b64encode(encrypted.encode()).decode()
        print(f"{Colors.gradient_text(encrypted_b64, 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def decrypt_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: decrypt <текст> <ключ>{Colors.RESET}")
            return True
        
        try:
            encrypted_b64 = args[0]
            key = args[1]
            encrypted = base64.b64decode(encrypted_b64).decode()
            decrypted = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted))
            print(f"{Colors.gradient_text(decrypted, 'cyan', single_color=True)}{Colors.RESET}")
        except:
            print(f"{Colors.RED}{Icons.ERROR} Ошибка расшифрования{Colors.RESET}")
        return True
    
    def ps_cmd(self, args):
        if PSUTIL:
            terminal_width = shutil.get_terminal_size().columns
            print(f"{Colors.gradient_text(f"{'PID':>8} {'CPU%':>6} {'MEM%':>6} {'NAME':<35}", 'cyan', single_color=True)}{Colors.RESET}")
            print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    p = proc.info
                    processes.append(p)
                except:
                    pass
            
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            for p in processes[:20]:
                pid = p['pid']
                cpu = p.get('cpu_percent', 0)
                mem = p.get('memory_percent', 0)
                name = p.get('name', 'unknown')[:35]
                print(f"{pid:>8} {cpu:>6.1f} {mem:>6.1f} {name:<35}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Установите psutil{Colors.RESET}")
        return True
    
    def top_cmd(self, args):
        if not PSUTIL:
            print(f"{Colors.YELLOW}{Icons.WARNING} Установите psutil{Colors.RESET}")
            return True
        
        try:
            while True:
                Utils.clear_screen()
                terminal_width = shutil.get_terminal_size().columns
                print(Colors.header("СИСТЕМНЫЙ МОНИТОР", terminal_width - 4, style='double'))
                
                cpu_percent = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} CPU: {Colors.gradient_text(f'{cpu_percent}%', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 16 - len(str(cpu_percent))) + '║', 'cyan', single_color=True)}")
                cpu_bar_width = terminal_width - 16
                filled = int(cpu_bar_width * cpu_percent / 100)
                cpu_bar = f"{Colors.GREEN if cpu_percent < 70 else Colors.YELLOW if cpu_percent < 90 else Colors.RED}█{Colors.RESET}" * filled + f"{Colors.DIM}░{Colors.RESET}" * (cpu_bar_width - filled)
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}      {cpu_bar}{Colors.gradient_text(' ' * (terminal_width - 15 - cpu_bar_width) + '║', 'cyan', single_color=True)}")
                
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} RAM: {Colors.gradient_text(f'{mem.percent}% ({Utils.human_size(mem.used)}/{Utils.human_size(mem.total)})', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 27 - len(f"{mem.percent}% ({Utils.human_size(mem.used)}/{Utils.human_size(mem.total)})")) + '║', 'cyan', single_color=True)}")
                mem_bar_width = terminal_width - 16
                filled = int(mem_bar_width * mem.percent / 100)
                mem_bar = f"{Colors.GREEN if mem.percent < 70 else Colors.YELLOW if mem.percent < 90 else Colors.RED}█{Colors.RESET}" * filled + f"{Colors.DIM}░{Colors.RESET}" * (mem_bar_width - filled)
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}      {mem_bar}{Colors.gradient_text(' ' * (terminal_width - 15 - mem_bar_width) + '║', 'cyan', single_color=True)}")
                
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} DISK:{Colors.gradient_text(f' {disk.percent}% ({Utils.human_size(disk.used)}/{Utils.human_size(disk.total)})', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 16 - len(f"{disk.percent}% ({Utils.human_size(disk.used)}/{Utils.human_size(disk.total)})")) + '║', 'cyan', single_color=True)}")
                disk_bar_width = terminal_width - 16
                filled = int(disk_bar_width * disk.percent / 100)
                disk_bar = f"{Colors.GREEN if disk.percent < 70 else Colors.YELLOW if disk.percent < 90 else Colors.RED}█{Colors.RESET}" * filled + f"{Colors.DIM}░{Colors.RESET}" * (disk_bar_width - filled)
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}      {disk_bar}{Colors.gradient_text(' ' * (terminal_width - 15 - disk_bar_width) + '║', 'cyan', single_color=True)}")
                
                print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(f"{'PID':>8} {'CPU%':>6} {'MEM%':>6} {'NAME':<35}", 'cyan', single_color=True)}{Colors.gradient_text(' ' * (terminal_width - 60) + '║', 'cyan', single_color=True)}")
                print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
                
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        p = proc.info
                        if p.get('cpu_percent', 0) > 0:
                            processes.append(p)
                    except:
                        pass
                
                processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
                
                for p in processes[:10]:
                    pid = p['pid']
                    cpu = p.get('cpu_percent', 0)
                    mem = p.get('memory_percent', 0)
                    name = p.get('name', 'unknown')[:35]
                    print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {pid:>8} {cpu:>6.1f} {mem:>6.1f} {name:<35}{Colors.gradient_text(' ' * (terminal_width - 60) + '║', 'cyan', single_color=True)}")
                
                print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
                print(f"\n{Colors.DIM}Нажмите Ctrl+C для выхода{Colors.RESET}")
                time.sleep(2)
        except KeyboardInterrupt:
            print()
        return True
    
    def kill_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: kill <pid>{Colors.RESET}")
            return True
        
        try:
            pid = int(args[0])
            if os.name == 'nt':
                os.system(f'taskkill /PID {pid} /F')
            else:
                os.kill(pid, signal.SIGTERM)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Процесс {pid} завершен', 'cyan', single_color=True)}{Colors.RESET}")
        except:
            print(f"{Colors.RED}{Icons.ERROR} Ошибка завершения{Colors.RESET}")
        return True
    
    def pkill_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: pkill <имя>{Colors.RESET}")
            return True
        
        name = args[0]
        killed = False
        
        if PSUTIL:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if name.lower() in proc.info['name'].lower():
                        proc.kill()
                        print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Завершен: {proc.info["name"]} ({proc.info["pid"]})', 'cyan', single_color=True)}{Colors.RESET}")
                        killed = True
                except:
                    pass
        
        if not killed:
            print(f"{Colors.YELLOW}{Icons.WARNING} Процесс '{name}' не найден{Colors.RESET}")
        return True
    
    def jobs_cmd(self, args):
        print(f"{Colors.YELLOW}{Icons.WARNING} Jobs реализован частично{Colors.RESET}")
        return True
    
    def fg_cmd(self, args):
        print(f"{Colors.YELLOW}{Icons.WARNING} FG реализован частично{Colors.RESET}")
        return True
    
    def bg_cmd(self, args):
        print(f"{Colors.YELLOW}{Icons.WARNING} BG реализован частично{Colors.RESET}")
        return True
    
    def nohup_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: nohup <команда>{Colors.RESET}")
            return True
        
        cmd = ' '.join(args)
        try:
            if os.name == 'nt':
                subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Запущено в фоне: {cmd}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def zip_cmd(self, args):
        if len(args) < 2:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: zip <архив> <файлы>{Colors.RESET}")
            return True
        
        archive = args[0]
        files = args[1:]
        try:
            with zipfile.ZipFile(archive, 'w') as zf:
                for f in files:
                    if os.path.exists(f):
                        if os.path.isdir(f):
                            for root, dirs, files_in in os.walk(f):
                                for file in files_in:
                                    zf.write(os.path.join(root, file))
                        else:
                            zf.write(f)
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Архив создан: {archive}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def unzip_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: unzip <архив>{Colors.RESET}")
            return True
        
        archive = args[0]
        try:
            with zipfile.ZipFile(archive, 'r') as zf:
                zf.extractall()
            print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Архив распакован: {archive}', 'cyan', single_color=True)}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def tar_cmd(self, args):
        if '-cf' in args:
            idx = args.index('-cf')
            if idx + 1 < len(args):
                archive = args[idx + 1]
                files = args[idx + 2:]
                try:
                    with tarfile.open(archive, 'w') as tar:
                        for f in files:
                            tar.add(f)
                    print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Архив создан: {archive}', 'cyan', single_color=True)}{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        elif '-xf' in args:
            idx = args.index('-xf')
            if idx + 1 < len(args):
                archive = args[idx + 1]
                try:
                    with tarfile.open(archive, 'r') as tar:
                        tar.extractall()
                    print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Архив распакован: {archive}', 'cyan', single_color=True)}{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: tar -cf archive.tar файлы  или  tar -xf archive.tar{Colors.RESET}")
        return True
    
    def gzip_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: gzip <файл>{Colors.RESET}")
            return True
        
        for f in args:
            try:
                with open(f, 'rb') as fin:
                    with open(f + '.gz', 'wb') as fout:
                        fout.write(gzip.compress(fin.read()))
                print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Сжат: {f}', 'cyan', single_color=True)}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        return True
    
    def gunzip_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: gunzip <файл.gz>{Colors.RESET}")
            return True
        
        for f in args:
            if f.endswith('.gz'):
                try:
                    with gzip.open(f, 'rb') as fin:
                        with open(f[:-3], 'wb') as fout:
                            fout.write(fin.read())
                    print(f"{Colors.gradient_text(f'{Icons.SUCCESS} Распакован: {f}', 'cyan', single_color=True)}{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}{Icons.WARNING} Не gzip файл: {f}{Colors.RESET}")
        return True
    
    def sevenz_cmd(self, args):
        if not args:
            print(f"{Colors.YELLOW}{Icons.WARNING} Использование: 7z <команда> <архив>{Colors.RESET}")
            print(f"Команды: a (создать), x (распаковать), l (список){Colors.RESET}")
            return True
        
        print(f"{Colors.YELLOW}{Icons.WARNING} 7-Zip требует установки 7z.exe{Colors.RESET}")
        return True
    
    def matrix_cmd(self, args):
        Animations.matrix_rain(3)
        return True
    
    def hack_cmd(self, args):
        print(f"{Colors.RED}{Icons.HACK} Инициализация взлома...{Colors.RESET}")
        stages = ["Сканирование целей", "Поиск уязвимостей", "Эксплуатация", "Получение доступа", "Очистка следов"]
        for i, stage in enumerate(stages):
            Animations.progress_bar((i + 1) * 20, 40, gradient=True)
            time.sleep(0.5)
            print(f"\n{Colors.YELLOW}[{(i + 1) * 20}%] {stage}...{Colors.RESET}")
        print(f"{Colors.gradient_text(f'{Icons.SUCCESS} ДОСТУП ПОЛУЧЕН!', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def fire_cmd(self, args):
        Animations.fire_effect(3)
        return True
    
    def rainbow_cmd(self, args):
        Animations.rainbow_glow(3)
        return True
    
    def glow_cmd(self, args):
        text = ' '.join(args) if args else "✨ KALI TERMINAL ULTIMATE ✨"
        Animations.pulse(text, Colors.CYAN, 2)
        return True
    
    def banner_cmd(self, args):
        text = ' '.join(args) if args else "KALI"
        terminal_width = shutil.get_terminal_size().columns
        banner_width = len(text) + 4
        padding = (terminal_width - banner_width) // 2
        if padding < 0:
            padding = 0
        print(' ' * padding + f"{Colors.gradient_text('█' * (len(text) + 4), 'cyan', single_color=True)}{Colors.RESET}")
        print(' ' * padding + f"{Colors.gradient_text(f'█ {text.upper()} █', 'cyan', single_color=True)}{Colors.RESET}")
        print(' ' * padding + f"{Colors.gradient_text('█' * (len(text) + 4), 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def cowsay_cmd(self, args):
        text = ' '.join(args) if args else "Moo!"
        cow = f"""
{Colors.gradient_text(f'  {text}', 'cyan', single_color=True)}
   \\
    \\
      ^__^
      (oo)\\_______
      (__)\\       )\\/\\
          ||----w |
          ||     ||{Colors.RESET}
"""
        print(cow)
        return True
    
    def fortune_cmd(self, args):
        fortunes = [
            "Хакер - это тот, кто ищет нестандартные решения.",
            "В Linux нет ничего невозможного.",
            "Kali Linux - выбор профессионалов.",
            "Лучший способ защитить систему - знать, как её взломать.",
            "Код - это поэзия, написанная для машин.",
            "Сложность - враг безопасности.",
            "Безопасность - это не продукт, а процесс.",
            "В мире Linux все файлы - это файлы.",
            "RTFM - Read The Friendly Manual!",
            "Свобода - это ответственность.",
            "Секрет успеха - начать.",
            "Программирование - это искусство.",
            "Python - это сила.",
            "Terminal - твой лучший друг.",
        ]
        print(f"{Colors.gradient_text(f'{Icons.FIRE} {random.choice(fortunes)}', 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def neofetch_cmd(self, args):
        user = Utils.get_username()
        host = socket.gethostname()
        os_info = Utils.get_os_info()
        ip = Utils.get_ip()
        kernel = platform.release()
        shell = "Kali Terminal v4.2"
        terminal_width = shutil.get_terminal_size().columns
        
        ascii_art = f"""
{Colors.gradient_text('        .-.', 'cyan', single_color=True)}
{Colors.gradient_text('       /   \\', 'cyan', single_color=True)}
{Colors.gradient_text('       |   |', 'cyan', single_color=True)}       {Colors.gradient_text(f'{user}@{host}', 'cyan', single_color=True)}
{Colors.gradient_text('       |   |', 'cyan', single_color=True)}       {Colors.gradient_text(f'OS: {os_info}', 'cyan', single_color=True)}
{Colors.gradient_text('       |   |', 'cyan', single_color=True)}       {Colors.gradient_text(f'Kernel: {kernel}', 'cyan', single_color=True)}
{Colors.gradient_text('       |   |', 'cyan', single_color=True)}       {Colors.gradient_text(f'IP: {ip}', 'cyan', single_color=True)}
{Colors.gradient_text('      /     \\', 'cyan', single_color=True)}      {Colors.gradient_text(f'Shell: {shell}', 'cyan', single_color=True)}
{Colors.gradient_text('     /       \\', 'cyan', single_color=True)}     {Colors.gradient_text(f'Commands: {self.size()}+', 'cyan', single_color=True)}
{Colors.gradient_text('    /         \\', 'cyan', single_color=True)}    
{Colors.gradient_text('   /           \\', 'cyan', single_color=True)}   
{Colors.gradient_text('  /             \\', 'cyan', single_color=True)}  
{Colors.gradient_text(' /_______________\\', 'cyan', single_color=True)} {Colors.RESET}
"""
        print(ascii_art)
        return True
    
    def ascii_cmd(self, args):
        arts = [
            f"""
{Colors.gradient_text('    ╔═╗┌─┐┌┬┐┌─┐┌─┐┬─┐', 'cyan', single_color=True)}
{Colors.gradient_text('    ╠═╝├─┤ │ ├─┤│  ├┬┘', 'cyan', single_color=True)}
{Colors.gradient_text('    ╩  ┴ ┴ ┴ ┴ ┴└─┘┴└─', 'cyan', single_color=True)}{Colors.RESET}
            """,
            f"""
{Colors.gradient_text('        ┌─┐┬ ┬┌─┐┌┐┌┌─┐┌─┐', 'cyan', single_color=True)}
{Colors.gradient_text('        │  └┬┘├─┤││││ ┬└─┐', 'cyan', single_color=True)}
{Colors.gradient_text('        └─┘ ┴ ┴ ┴┘└┘└─┘└─┘', 'cyan', single_color=True)}{Colors.RESET}
            """,
            f"""
{Colors.gradient_text('    ╦ ╦╔═╗╔╦╗╔═╗╦ ╦', 'cyan', single_color=True)}
{Colors.gradient_text('    ║ ║╠═╣ ║ ║  ╠═╣', 'cyan', single_color=True)}
{Colors.gradient_text('    ╚═╝╩ ╩ ╩ ╚═╝╩ ╩', 'cyan', single_color=True)}{Colors.RESET}
            """,
            f"""
{Colors.gradient_text('    ██╗  ██╗ █████╗ ██╗     ██╗', 'cyan', single_color=True)}
{Colors.gradient_text('    ██║ ██╔╝██╔══██╗██║     ██║', 'cyan', single_color=True)}
{Colors.gradient_text('    █████╔╝ ███████║██║     ██║', 'cyan', single_color=True)}
{Colors.gradient_text('    ██╔═██╗ ██╔══██║██║     ██║', 'cyan', single_color=True)}
{Colors.gradient_text('    ██║  ██╗██║  ██║███████╗██║', 'cyan', single_color=True)}{Colors.RESET}
            """
        ]
        print(random.choice(arts))
        return True
    
    def figlet_cmd(self, args):
        text = ' '.join(args) if args else "KALI"
        terminal_width = shutil.get_terminal_size().columns
        print(f"{Colors.gradient_text(text.upper().center(terminal_width), 'cyan', single_color=True)}{Colors.RESET}")
        return True
    
    def sl_cmd(self, args):
        train = f"""
{Colors.gradient_text('      ====        ________                ___________', 'cyan', single_color=True)}
{Colors.gradient_text('  _D _|  |_______/        \\__I_I_____===__|_________|', 'cyan', single_color=True)}
{Colors.gradient_text('   |(_)---  |   H\\________/ |   |        =|___ ___|      _________________', 'cyan', single_color=True)}
{Colors.gradient_text('   /     |  |   H  |  |     |   |         ||_| |_||     _|                \\_____A', 'cyan', single_color=True)}
{Colors.gradient_text('  |      |  |   H  |__--------------------| [___] |   =|                        |', 'cyan', single_color=True)}
{Colors.gradient_text('  | ________|___H__/__|_____/[][]~\\_______|       |   -|                        |', 'cyan', single_color=True)}
{Colors.gradient_text('  |/ |   |-----------I_____I [][] |  |____|_  |___  \\_  |_________^{{', 'cyan', single_color=True)}{Colors.RESET}
"""
        print(train)
        return True
    
    def yes_cmd(self, args):
        text = ' '.join(args) if args else 'y'
        try:
            for _ in range(10):
                print(Colors.gradient_text(text, 'cyan', single_color=True))
                time.sleep(0.1)
        except KeyboardInterrupt:
            print()
        return True
    
    def stars_cmd(self, args):
        Animations.starfield(3)
        return True
    
    def explosion_cmd(self, args):
        Animations.explosion_effect(2)
        return True
    
    def bounce_cmd(self, args):
        text = ' '.join(args) if args else "KALI TERMINAL"
        Animations.bounce(text, 2)
        return True
    
    def info_cmd(self, args):
        terminal_width = shutil.get_terminal_size().columns
        info_text = f"""
{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.BOLD}{Colors.gradient_text('KALI TERMINAL ULTIMATE EDITION v4.2'.center(terminal_width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('📊 СТАТИСТИКА', 'cyan', single_color=True)}{' ' * (terminal_width - 14)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   Команд: {Colors.GREEN}{self.size()}{Colors.RESET}{' ' * (terminal_width - 12 - len(str(self.size())))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   Алиасов: {Colors.GREEN}{len(self.aliases)}{Colors.RESET}{' ' * (terminal_width - 13 - len(str(len(self.aliases))))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   Платформа: {Colors.GREEN}{platform.system()} {platform.release()}{Colors.RESET}{' ' * (terminal_width - 15 - len(f"{platform.system()} {platform.release()}"))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   Python: {Colors.GREEN}{platform.python_version()}{Colors.RESET}{' ' * (terminal_width - 12 - len(platform.python_version()))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('📦 ИНТЕГРАЦИИ', 'cyan', single_color=True)}{' ' * (terminal_width - 14)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   ✅ psutil {Colors.GREEN}{'установлен' if PSUTIL else 'не установлен'}{Colors.RESET}{' ' * (terminal_width - 17 - len('установлен' if PSUTIL else 'не установлен'))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   ✅ requests {Colors.GREEN}{'установлен' if REQUESTS else 'не установлен'}{Colors.RESET}{' ' * (terminal_width - 18 - len('установлен' if REQUESTS else 'не установлен'))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   ✅ Pillow {Colors.GREEN}{'установлен' if PIL else 'не установлен'}{Colors.RESET}{' ' * (terminal_width - 15 - len('установлен' if PIL else 'не установлен'))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   ✅ cryptography {Colors.GREEN}{'установлен' if CRYPTO else 'не установлен'}{Colors.RESET}{' ' * (terminal_width - 22 - len('установлен' if CRYPTO else 'не установлен'))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   ✅ colorama {Colors.GREEN}{'установлен' if COLORAMA_AVAILABLE else 'не установлен'}{Colors.RESET}{' ' * (terminal_width - 18 - len('установлен' if COLORAMA_AVAILABLE else 'не установлен'))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}   ✅ rich {Colors.GREEN}{'установлен' if RICH_AVAILABLE else 'не установлен'}{Colors.RESET}{' ' * (terminal_width - 14 - len('установлен' if RICH_AVAILABLE else 'не установлен'))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}{Colors.RESET}
"""
        print(info_text)
        return True
    
    def sysinfo_cmd(self, args):
        terminal_width = shutil.get_terminal_size().columns
        print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.BOLD}{Colors.gradient_text('СИСТЕМНАЯ ИНФОРМАЦИЯ'.center(terminal_width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} ОС:      {Colors.GREEN}{platform.system()} {platform.release()}{Colors.RESET}{' ' * (terminal_width - 12 - len(f"{platform.system()} {platform.release()}"))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Хост:    {Colors.GREEN}{socket.gethostname()}{Colors.RESET}{' ' * (terminal_width - 12 - len(socket.gethostname()))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} IP:      {Colors.GREEN}{Utils.get_ip()}{Colors.RESET}{' ' * (terminal_width - 12 - len(Utils.get_ip()))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Публичный IP:{Colors.GREEN}{Utils.get_public_ip()}{Colors.RESET}{' ' * (terminal_width - 18 - len(Utils.get_public_ip()))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Пользователь:{Colors.GREEN} {Utils.get_username()}{Colors.RESET}{' ' * (terminal_width - 16 - len(Utils.get_username()))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} Python:  {Colors.GREEN}{platform.python_version()}{Colors.RESET}{' ' * (terminal_width - 12 - len(platform.python_version()))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        
        if PSUTIL:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} CPU:     {Colors.GREEN}{cpu}%{Colors.RESET}{' ' * (terminal_width - 11 - len(f"{cpu}%"))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} RAM:     {Colors.GREEN}{mem.percent}% ({Utils.human_size(mem.used)}/{Utils.human_size(mem.total)}){Colors.RESET}{' ' * (terminal_width - 21 - len(f"{mem.percent}% ({Utils.human_size(mem.used)}/{Utils.human_size(mem.total)})"))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
            print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} DISK:    {Colors.GREEN}{disk.percent}% ({Utils.human_size(disk.used)}/{Utils.human_size(disk.total)}){Colors.RESET}{' ' * (terminal_width - 21 - len(f"{disk.percent}% ({Utils.human_size(disk.used)}/{Utils.human_size(disk.total)})"))}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        
        print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        return True
    
    def version_cmd(self, args):
        print(f"{Colors.gradient_text('Kali Terminal Ultimate Edition v4.2', 'cyan', single_color=True)}{Colors.RESET}")
        print(f"Команд: {self.size()}")
        print(f"Алиасов: {len(self.aliases)}")
        return True
    
    def about_cmd(self, args):
        terminal_width = shutil.get_terminal_size().columns
        about_text = f"""
{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.BOLD}{Colors.gradient_text('KALI TERMINAL EMULATOR v4.2'.center(terminal_width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Профессиональный инструмент для работы с командной строкой', 'cyan', single_color=True)}{' ' * (terminal_width - 48)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text(f'Содержит {self.size()} реальных команд для повседневной работы', 'cyan', single_color=True)}{' ' * (terminal_width - 41 - len(str(self.size())))}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('ОСОБЕННОСТИ:', 'cyan', single_color=True)}{' ' * (terminal_width - 15)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• 200+ встроенных команд', 'cyan', single_color=True)}{' ' * (terminal_width - 25)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Цветной вывод и иконки', 'cyan', single_color=True)}{' ' * (terminal_width - 27)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Поддержка псевдонимов (alias)', 'cyan', single_color=True)}{' ' * (terminal_width - 32)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• История команд', 'cyan', single_color=True)}{' ' * (terminal_width - 20)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Древовидная навигация', 'cyan', single_color=True)}{' ' * (terminal_width - 26)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Сетевые утилиты', 'cyan', single_color=True)}{' ' * (terminal_width - 21)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Шифрование и хеширование', 'cyan', single_color=True)}{' ' * (terminal_width - 29)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Работа с архивами', 'cyan', single_color=True)}{' ' * (terminal_width - 23)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Мониторинг системы', 'cyan', single_color=True)}{' ' * (terminal_width - 24)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Поддержка rich и colorama', 'cyan', single_color=True)}{' ' * (terminal_width - 29)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('• Анимации и визуальные эффекты', 'cyan', single_color=True)}{' ' * (terminal_width - 34)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Автор: @console_hack', 'cyan', single_color=True)}{' ' * (terminal_width - 22)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('GitHub: github.com/console-hack', 'cyan', single_color=True)}{' ' * (terminal_width - 32)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Создан для образовательных целей', 'cyan', single_color=True)}{' ' * (terminal_width - 34)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}{Colors.RESET}
"""
        print(about_text)
        return True
    
    def credits_cmd(self, args):
        terminal_width = shutil.get_terminal_size().columns
        print(f"{Colors.gradient_text('╔' + '═' * (terminal_width - 2) + '╗', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.BOLD}{Colors.gradient_text('АВТОРЫ И БЛАГОДАРНОСТИ'.center(terminal_width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╠' + '═' * (terminal_width - 2) + '╣', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Разработчик: @console_hack', 'cyan', single_color=True)}{' ' * (terminal_width - 28)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Вдохновлено: Kali Linux, Termux', 'cyan', single_color=True)}{' ' * (terminal_width - 35)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Библиотеки: psutil, requests, PIL, colorama, rich', 'cyan', single_color=True)}{' ' * (terminal_width - 50)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('║', 'cyan', single_color=True)} {Colors.gradient_text('Особая благодарность сообществу open-source', 'cyan', single_color=True)}{' ' * (terminal_width - 44)}{Colors.gradient_text('║', 'cyan', single_color=True)}")
        print(f"{Colors.gradient_text('╚' + '═' * (terminal_width - 2) + '╝', 'cyan', single_color=True)}")
        return True
    
    def execute(self, cmd_line):
        if not cmd_line or not cmd_line.strip():
            return True
        
        try:
            parts = shlex.split(cmd_line.strip())
        except:
            parts = cmd_line.strip().split()
        
        if not parts:
            return True
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in self.aliases:
            return self.execute(self.aliases[cmd] + ' ' + ' '.join(args))
        
        if cmd in self.commands:
            try:
                return self.commands[cmd]['func'](args)
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
                return True
        
        try:
            result = subprocess.run(cmd_line, shell=True, capture_output=True, text=True, timeout=10)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{Colors.RED}{result.stderr}{Colors.RESET}")
            return True
        except subprocess.TimeoutExpired:
            print(f"{Colors.YELLOW}{Icons.WARNING} Команда превысила время{Colors.RESET}")
        except FileNotFoundError:
            print(f"{Colors.RED}{Icons.ERROR} Команда не найдена: {cmd}{Colors.RESET}")
            print(f"Используйте 'help' для списка команд")
        except Exception as e:
            print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")
        
        return True

class KaliTerminal:
    def __init__(self):
        self.cmd_manager = CommandManager()
    
    def get_prompt(self):
        user = Utils.get_username()
        host = Utils.get_hostname()
        path = Utils.shorten_path(os.getcwd(), 30)
        
        return f"{Colors.RED}┌──({Colors.gradient_text(user, 'cyan', single_color=True)}{Colors.RED}@{Colors.gradient_text(host, 'cyan', single_color=True)}{Colors.RED})-[{Colors.gradient_text(path, 'cyan', single_color=True)}{Colors.RED}]\n{Colors.RED}└─{Colors.gradient_text('$ ', 'cyan', single_color=True)}{Colors.RESET}"
    
    def show_ascii_header(self):
        terminal_width = shutil.get_terminal_size().columns
        width = max(80, min(terminal_width - 2, 100))
        
        header = f"""
{Colors.gradient_text('╔' + '═' * width + '╗', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text('     ██╗  ██╗ █████╗ ██╗     ██╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     '.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text('     ██║ ██╔╝██╔══██╗██║     ██║    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     '.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text('     █████╔╝ ███████║██║     ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     '.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text('     ██╔═██╗ ██╔══██║██║     ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     '.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text('     ██║  ██╗██║  ██║███████╗██║       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗'.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text('     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝'.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text(f'                     🚀  ULTIMATE TERMINAL EMULATOR v4.2  🚀                     '.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text(f'                 🔥 {self.cmd_manager.size()}+ КОМАНД | ПРОФЕССИОНАЛЬНЫЙ ИНСТРУМЕНТ 🔥               '.center(width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('║', 'cyan', single_color=True)}{Colors.gradient_text(' ' * (width - 2), 'cyan', single_color=True)}{Colors.gradient_text('║', 'cyan', single_color=True)}
{Colors.gradient_text('╚' + '═' * width + '╝', 'cyan', single_color=True)}{Colors.RESET}
"""
        print(header)
        print()
        print(f"{Colors.gradient_text(f'{Icons.INFO} Добро пожаловать в Kali Terminal Ultimate Edition! {self.cmd_manager.size()} команд готовы к работе', 'cyan', single_color=True)}{Colors.RESET}")
        print(f"{Colors.DIM}Введите 'help' для справки, 'exit' для выхода | By @console_hack{Colors.RESET}")
        print()
    
    def run(self):
        self.show_ascii_header()
        
        while True:
            try:
                prompt = self.get_prompt()
                cmd = input(prompt)
                
                if not cmd.strip():
                    continue
                
                self.cmd_manager.save_history(cmd)
                
                if cmd.lower() in ['exit', 'quit']:
                    print(f"{Colors.gradient_text(f'{Icons.SUCCESS} До свидания! Спасибо за использование Kali Terminal!', 'cyan', single_color=True)}{Colors.RESET}")
                    break
                
                self.cmd_manager.execute(cmd)
                
                print()
                
            except KeyboardInterrupt:
                print(f"\n{Colors.gradient_text(f'{Icons.WARNING} Используйте \'exit\' для выхода', 'cyan', single_color=True)}{Colors.RESET}")
            except EOFError:
                break
            except Exception as e:
                print(f"{Colors.RED}{Icons.ERROR} {e}{Colors.RESET}")

if __name__ == "__main__":
    installer = Installer()
    installer.run()
    
    if not PSUTIL:
        print(f"{Colors.YELLOW}{Icons.WARNING} Рекомендуется установить psutil: pip install psutil{Colors.RESET}")
        time.sleep(1)
    
    Animations.loading_animation("Загрузка Kali Terminal Ultimate Edition v4.2", 1.5)
    
    terminal = KaliTerminal()
    terminal.run()
