import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_ffmpeg_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(base_dir, 'bin', 'ffmpeg.exe')
    logging.info(f"FFmpeg path: {ffmpeg_path}")
    return ffmpeg_path

def check_ffmpeg():
    ffmpeg_path = get_ffmpeg_path()

    if not os.path.exists(ffmpeg_path):
        logging.error(f"FFmpeg not found at {ffmpeg_path}")
        return False

    try:
        result = subprocess.run([ffmpeg_path, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logging.info(f"FFmpeg is available: {result.stdout}")
            return True
        else:
            logging.error(f"FFmpeg error: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Error running FFmpeg: {e}")
        return False

# Call the check_ffmpeg function to verify FFmpeg
check_ffmpeg()
