import os

def get_ffmpeg_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(base_dir, 'bin', 'ffmpeg.exe')
    return ffmpeg_path

def get_ffmpeg_path():
    cwd = os.getcwd()  # mendapatkan direktori kerja saat ini
    ffmpeg_path = os.path.join(cwd, 'bin', 'ffmpeg.exe')
    return ffmpeg_path

from pathlib import Path

def get_ffmpeg_path():
    base_dir = Path(__file__).resolve().parent  # Dapatkan direktori tempat skrip berada
    ffmpeg_path = base_dir / 'bin' / 'ffmpeg.exe'
    return ffmpeg_path

import sys
import os

def get_ffmpeg_path():
    base_dir = os.path.dirname(sys.argv[0])  # Mendapatkan path dari argumen pertama
    ffmpeg_path = os.path.join(base_dir, 'bin', 'ffmpeg.exe')
    return ffmpeg_path

import os

def get_ffmpeg_path():
    base_dir = os.environ.get('FFMPEG_HOME', os.getcwd())  # Mendapatkan nilai variabel lingkungan, fallback ke cwd jika tidak ada
    ffmpeg_path = os.path.join(base_dir, 'bin', 'ffmpeg.exe')
    return ffmpeg_path

print("FFmpeg path:", get_ffmpeg_path())
print("Exists?", os.path.exists(get_ffmpeg_path()))

