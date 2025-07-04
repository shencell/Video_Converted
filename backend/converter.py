import os
import subprocess
import logging
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # ambil path dari run.exe
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    return resource_path(os.path.join('bin', 'ffmpeg.exe'))

def check_nvenc_available(encoder_name):
    ffmpeg_path = get_ffmpeg_path()
    try:
        result = subprocess.run(
            [ffmpeg_path, '-hide_banner', '-encoders'], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return encoder_name in result.stdout
    except Exception as e:
        logging.error(f"Error checking NVENC availability: {e}")
        return False

def convert_video(input_file, output_file, codec, resolution, bitrate, fps):
    codec_format_map = {
        'h264': ['mp4', 'mkv', 'mov', 'flv', 'f4v', 'asf', 'wmv'],
        'hevc': ['mp4', 'mkv', 'mov', 'ts', 'mts'],
        'theora': ['ogv', 'ogg'],
        'mpeg': ['mpg']
    }

    output_format = output_file.split('.')[-1]

    if output_format not in codec_format_map.get(codec, []):
        raise ValueError(f"The codec '{codec}' is not compatible with the output format '{output_format}'.")

    use_nvenc = False
    encoder = codec
    ffmpeg_path = get_ffmpeg_path()
    if codec == 'h264' and check_nvenc_available('h264_nvenc'):
        encoder = 'h264_nvenc'
        use_nvenc = True
    elif codec == 'hevc' and check_nvenc_available('hevc_nvenc'):
        encoder = 'hevc_nvenc'
        use_nvenc = True
        use_nvenc = True
    elif codec == 'mpeg':
        encoder = 'mpeg4'
    elif codec == 'theora':
        encoder = 'libtheora'

    # Add audio codec to combine audio and video
    audio_codec_map = {
        'mp4': 'aac',
        'mkv': 'aac',
        'mov': 'aac',
        'flv': 'aac',
        'f4v': 'aac',
        'asf': 'aac',
        'wmv': 'wmav2',
        '3gp': 'aac',
        'ts': 'aac',
        'mts': 'aac',
        'ogv': 'libvorbis',
        'ogg': 'libvorbis',
        'webm': 'libvorbis',
        'mpg': 'mp2'
    }
    audio_codec = audio_codec_map.get(output_format, 'aac')

    command = [
        ffmpeg_path,
        '-y',
        '-i', input_file,
        '-c:v', encoder,
        '-b:v', bitrate,
        '-s', resolution,
        '-r', str(fps),
        '-c:a', audio_codec,
        output_file
    ]

    try:
        # Windows-specific: Hide the terminal window
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        # Run FFmpeg with completely hidden console and no output
        subprocess.run(
            command,
            check=True,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        logging.info(f'Successfully converted {input_file} to {output_file} using {"NVENC" if use_nvenc else "CPU"} encoder and audio codec {audio_codec}.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error during conversion: {e}')
        raise