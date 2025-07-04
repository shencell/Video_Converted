import time
import os
import sys
from flask import Flask, request, render_template, url_for
from .converter import convert_video, check_nvenc_available

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
CONVERTED_FOLDER = os.path.join(BASE_DIR, 'converted')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

SUPPORTED_FORMATS = [
    'mp4', 'mkv', 'avi', 'mov', 'webm', 'flv', 'ts', 'm2ts', '3gp', 'ogg', 'rm', 'vob',
    'wmv', 'mpeg', 'mpg', 'ogv', 'swf', 'mjpeg', 'mxf', 'mts', 'm4v', 'm2v', 'hevc',
    'f4v', 'asf', 'wtv', 'amv'
]

@app.context_processor
def inject_time():
    return {
        'time': int(time.time()),
        'converted_folder_path': os.path.abspath(CONVERTED_FOLDER)
    }

@app.route('/')
def index():
    return render_template('index.html', message=None, output_file=None)

def select_best_codec(output_format):
    format_preferred_codecs = {
        'mp4': ['hevc', 'h264'],
        'mkv': ['hevc', 'h264'],
        'mov': ['hevc', 'h264'],
        'ogv': ['theora'],
        'ogg': ['theora'],
        'flv': ['h264'],
        'f4v': ['h264'],
        'asf': ['h264'],
        'wmv': ['h264'],
        'ts': ['hevc'],
        'mpg': ['mpeg']
    }
    preferred_codecs = format_preferred_codecs.get(output_format, ['h264'])

    nvenc_h264 = check_nvenc_available('h264_nvenc')
    nvenc_hevc = check_nvenc_available('hevc_nvenc')

    for codec in preferred_codecs:
        if codec == 'h264' and nvenc_h264:
            return 'h264'
        if codec == 'hevc' and nvenc_hevc:
            return 'hevc'
        if codec in ['theora', 'mpeg']:
            return codec
    return preferred_codecs[0]

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if not file:
        return render_template('index.html', message="No file uploaded", output_file=None)

    filename = file.filename
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in SUPPORTED_FORMATS:
        return render_template('index.html', message=f"Unsupported input file format: {ext}", output_file=None)

    bitrate = request.form.get('bitrate')
    resolution = request.form.get('resolution')
    output_format = request.form.get('output_format')
    fps = request.form.get('fps')

    if output_format not in SUPPORTED_FORMATS:
        return render_template('index.html', message=f"Unsupported output format: {output_format}", output_file=None)

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # Automatically select the best codec
    actual_codec = select_best_codec(output_format)

    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_{bitrate}_{actual_codec}_{resolution}_{fps}.{output_format}"
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    try:
        convert_video(input_path, output_path, actual_codec, resolution, bitrate, fps)
        os.remove(input_path)
        return render_template('index.html',
            message="Conversion complete! Check the 'converted' folder where you installed the app.",
            output_file=None)
    except Exception as e:
        if os.path.exists(input_path):
            os.remove(input_path)
        return render_template('index.html',
            message=f"Error during conversion: {str(e)}",
            output_file=None)

# Add configurable host/port
HOST = '127.0.0.1'
PORT = 5000

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)