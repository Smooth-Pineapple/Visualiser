#sudo pip install Flask-Colorpicker
#sudo pip install flask_bootstrap
#sudo pip install flask

import sys
sys.path.append("..")

import socket 
import os
import shutil
import flask
import re
import time
import threading

from flask import Flask, request, render_template, send_file, send_from_directory, redirect
from flask_bootstrap import Bootstrap
from flask_colorpicker import colorpicker
from subprocess import check_output

from serv_logging.serv_logging import Logging
from file_management.file_management import FileManagement
from webapp.translations.main import translations as translations_main
from webapp.translations._404 import translations as translations_404
from webapp.translations.shutdown import translations as translations_shutdown
from webapp.translations.download_fail import translations as translations_download_fail
from webapp.translations.config_fail import translations as translations_config_fail

app = Flask(__name__)
my_path = os.path.dirname(os.path.abspath(__file__))

Bootstrap(app)

colorpicker(app, local=['static/js/spectrum.js', 'static/css/spectrum.css'])

log_path = str(my_path) + '/../log/visualiser_server.log'
config_path = str(my_path) + '/../config/config.txt'

ip = 'None'
colour_key = 'colour'
pattern_key = 'pattern_type'

def get_ip():
    ip = "None"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception as e:
        logger.write(Logging.ERR, "Error when getting IP: " + str(e)) 
    finally:
        s.close()
    return ip

def extract_config_data(config_data):
    config_error = False

    if colour_key not in config_data:
        config_data[colour_key] = 'rgba(18,237,159,1)'
        logger.write(Logging.WAR, "Colour config not present, setting to default") 
        config_error = True
    elif not config_data[colour_key]:
        config_data[colour_key] = 'rgba(0,0,0,0)'

    if pattern_key not in config_data or not config_data[pattern_key]:
        config_data[pattern_key] = '1'
        logger.write(Logging.WAR, "Pattern key not present, setting to default") 
        config_error = True

    rgb_regex = '^rgb\\(\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*\\)$'
    rgba_regex = '^rgba\\(\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*(0|[1-9]\\d?|1\\d\\d?|2[0-4]\\d|25[0-5])%?\\s*,\\s*((0.[1-9])|[01])\\s*\\)$'
  
    if not re.match(rgb_regex, config_data[colour_key]):
        if not re.match(rgba_regex, config_data[colour_key]):
            config_data[colour_key] = 'rgba(18,237,159,1)'
            logger.write(Logging.WAR, "Colour config does not match RBG or RGBA, setting to default") 
            config_error = True

    if is_pattern_config(config_data[pattern_key]) is False:
        config_data[pattern_key] = '1'
        logger.write(Logging.WAR, "Pattern key not valid, setting to default")
        config_error = True

    if config_error is True:
        FileManagement.write_json(config_path, config_data, log_path)

    return config_data

def is_pattern_config(pattern_config):
    try:
        pattern_config_int = int(pattern_config)
        if pattern_config_int < 1 or pattern_config_int > 3:
            raise ValueError 

        return True
    except ValueError:
        logger.write(Logging.ERR, "Invalid pattern config: " + pattern_config)
        return False

def shutdown_thread(delay):
    time.sleep(delay)
    logger.write(Logging.INF, "Shutdown delay passed")
    os.system('sudo shutdown -h now')

@app.route('/')
def index():
    logger.write(Logging.DEB, "Base page") 
    config_data = extract_config_data(FileManagement.read_json(config_path, log_path))
    
    if 'lang' not in config_data or not config_data['lang']:
        config_data['lang'] = 'en'
        FileManagement.update_json(config_path, config_data, log_path)

    return render_template('/main.html', colour_key=colour_key, pattern_key=pattern_key, config_data=config_data, translations=translations_main, lang=config_data['lang'])

@app.route('/en', methods = ['GET', 'POST'])
def english():
    logger.write(Logging.DEB, "Setting language to English") 
    config_data = {'lang': 'en'}
    FileManagement.update_json(config_path, config_data, log_path)

    return redirect('/')

@app.route('/it', methods = ['GET', 'POST'])
def italian():
    logger.write(Logging.DEB, "Setting language to Italian") 
    config_data = {'lang': 'it'}
    FileManagement.update_json(config_path, config_data, log_path)

    return redirect('/')

@app.route('/config-mod', methods = ['GET', 'POST'])
def submit():
    logger.write(Logging.INF, "Applying config") 
    if 'apply' in request.form:
        try:
            colour = request.form.get('colour-picker')
            pattern_type = request.form.getlist('pattern-options')
            if pattern_type is not None and len(pattern_type) > 0:
                pattern_type = pattern_type[0]
    
            logger.write(Logging.DEB, "Config change: " + colour + ", " + pattern_type) 
            config_data = {colour_key: colour, pattern_key: pattern_type, 'ip': ip}

            FileManagement.update_json(config_path, config_data, log_path)
        except Exception as e: 
            logger.write(Logging.ERR, "Error when saving config change: " + str(e)) 
            config_data = extract_config_data(FileManagement.read_json(config_path, log_path))
            return render_template('/sub_page.html', translations=translations_config_fail, lang=config_data['lang']), 500
    
    elif 'cancel' in request.form:
        logger.write(Logging.DEB, "Cancel clicked, so reseting page") 

    return redirect('/')

@app.route('/shutdown', methods = ['GET', 'POST'])
def shutdown():
    logger.write(Logging.INF, "Attempting shutdown") 
    config_data = extract_config_data(FileManagement.read_json(config_path, log_path))
    try:
        shutdown_T = threading.Thread(target=shutdown_thread, args=(3,))
        shutdown_T.start()
    except Exception as e:
        logger.write(Logging.ERR, "Failed to shutdown: " + str(e)) 

    return render_template('/sub_page.html', translations=translations_shutdown, lang=config_data['lang'], img_path='Hippie.gif')

@app.route('/dwn-log',  methods = ['GET', 'POST'])
def download_logs():
    logger.write(Logging.INF, "Downloading logs") 
    config_data = extract_config_data(FileManagement.read_json(config_path, log_path))
    log_zip_dir = str(my_path) + '/../'
    try:
        shutil.make_archive(base_dir='log', root_dir=log_zip_dir, format='zip', base_name=log_zip_dir + 'Visualiser_Logs')

        return send_file(log_zip_dir + 'Visualiser_Logs.zip', as_attachment=True)
    except Exception as e: 
        logger.write(Logging.ERR, "Error when downloading logs: " + str(e)) 
        return render_template('/sub_page.html', translations=translations_download_fail, lang=config_data['lang'], img_path='Huel.gif'), 500

@app.route('/view-server-log')
def view_server_log():
    logger.write(Logging.DEB, "View server logs") 
    config_data = extract_config_data(FileManagement.read_json(config_path, log_path))

    return render_template('/view_logs.html', log=logger.read(), translations=translations_main, lang=config_data['lang'])
        
@app.route('/test-sub-page')
def test_sub_page():
    lang = 'en'

    page = request.args.get('page')
    if request.args.get('lang') == 'en' or request.args.get('lang') == 'it':
        lang = request.args.get('lang')

    logger.write(Logging.DEB, "Test sub page: " + page) 

    translations = None
    img_path = None 

    if page == "dfail":
        translations = translations_download_fail
        img_path = 'Huel.gif'
    elif page == "sdown":
        translations = translations_shutdown
        img_path = 'Hippie.gif'
    elif page == "cfail":
        translations = translations_config_fail
    else:
        translations = translations_404
        img_path = 'SexyPriest.gif'

    return render_template('/sub_page.html', translations=translations, lang=lang, img_path=img_path, debug=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/ico'), 'cowboy.ico')

@app.errorhandler(404)
def not_found(e):
    logger.write(Logging.ERR, str(e) + ": " + request.base_url) 
    config_data = extract_config_data(FileManagement.read_json(config_path, log_path))
    
    return render_template('/sub_page.html', translations=translations_404, lang=config_data['lang'], img_path='SexyPriest.gif')

if __name__ == '__main__':
    logger = Logging.getInstance(Logging.DEB)
    logger.open(log_path)
    
    ip = None
    cmd_arg = sys.argv 
    logger.write(Logging.DEB, "Sys arg: " + str(cmd_arg)) 
    if len(cmd_arg) > 1: 
        if sys.argv[1] is not None:
            ip_regex = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'   
            if re.match(ip_regex, sys.argv[1]):
                ip = sys.argv[1]
                logger.write(Logging.INF, "IP address passed from rc.local: " + ip) 
            
    if ip is None:
        for attempt in range(10):
            try: 
                ip = get_ip()
                logger.write(Logging.INF, "IP address found socket: " + ip) 
            except Exception as e: 
                logger.write(Logging.ERR, "Unable to get Hostname and IP: " + str(e)) 

            time.sleep(1)
    
    FileManagement.update_json(config_path, {'ip': ip}, log_path)
    app.run(debug=True, host='0.0.0.0')