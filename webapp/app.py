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

from serv_logging.serv_logging import Logging
from file_management.file_management import FileManagement
from file_management.data_extraction import DataExtraction

from webapp.flask_colorpicker import colorpicker

app = Flask(__name__)

Bootstrap(app)

colorpicker(app, local=['static/js/spectrum.min.js', 'static/css/spectrum.min.css'])

my_path = os.path.dirname(os.path.abspath(__file__))
log_path = str(my_path) + '/../log/visualiser_server.log'
config_path = str(my_path) + '/../config/config.txt'
translations_dir_path = str(my_path) + '/translations/'

ip = 'None'
colour_key = 'colour'
pattern_key = 'pattern_type'
language_set = set()

def get_ip():
    ip = "None"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception as e:
        logger.write(Logging.ERR, "Error when getting IP: " + str(e)) 
    finally:
        s.close()
    return ip

def shutdown_thread(delay):
    time.sleep(delay)
    logger.write(Logging.INF, "Shutdown delay passed")
    os.system('sudo shutdown -h now')

@app.route('/')
def index():
    logger.write(Logging.DEB, "Base page") 
    config_data = DataExtraction.fix_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, config_path, log_path)
    
    if 'lang' not in config_data or not config_data['lang']:
        config_data['lang'] = 'en'
        FileManagement.update_json(config_path, config_data, log_path)

    translation_json = {}
    if config_data['lang'] in language_set:
        translation_json = FileManagement.read_json(translations_dir_path + config_data['lang'] + '.json' , log_path)

    return render_template('/main.html', colour_key=colour_key, pattern_key=pattern_key, config_data=config_data, translations=translation_json, language_set=language_set, lang=config_data['lang'])

@app.route('/set_lang', methods = ['GET', 'POST'])
def set_lang():
    lang = 'en'
    if request.args.get('lang'):
        lang = request.args.get('lang')

    logger.write(Logging.DEB, "Setting language to: " + lang) 
    config_data = {'lang': lang}
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
            config_data = DataExtraction.fix_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, config_path, log_path)

            translation_json = {}
            if config_data['lang'] in language_set:
                translation_json = FileManagement.read_json(translations_dir_path + config_data['lang'] + '.json' , log_path)

            translations_config_fail = {
                'TITLE': "",
                'MESSAGE': ""
            }

            if 'TITLE_CONFIG_FAIL' in translation_json:
                translations_config_fail['TITLE'] = translation_json['TITLE_CONFIG_FAIL']

            if 'MESSAGE_CONFIG_FAIL' in translation_json:
                translations_config_fail['MESSAGE'] = translation_json['MESSAGE_CONFIG_FAIL']

            return render_template('/sub_page.html', translations=translations_config_fail, lang=config_data['lang'], have_home=True), 500
    
    elif 'cancel' in request.form:
        logger.write(Logging.DEB, "Cancel clicked, so reseting page") 

    return redirect('/')

@app.route('/shutdown', methods = ['GET', 'POST'])
def shutdown():
    logger.write(Logging.INF, "Attempting shutdown") 
    config_data = DataExtraction.fix_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, config_path, log_path)
    try:
        shutdown_T = threading.Thread(target=shutdown_thread, args=(3,))
        shutdown_T.start()
    except Exception as e:
        logger.write(Logging.ERR, "Failed to shutdown: " + str(e)) 

    translation_json = {}
    if config_data['lang'] in language_set:
        translation_json = FileManagement.read_json(translations_dir_path + config_data['lang'] + '.json' , log_path)
    
    translations_shutdown = {
        'TITLE': "",
        'MESSAGE': ""
    }

    if 'TITLE_SHUTDOWN' in translation_json:
        translations_shutdown['TITLE'] = translation_json['TITLE_SHUTDOWN']

    if 'MESSAGE_SHUTDOWN' in translation_json:
        translations_shutdown['MESSAGE'] = translation_json['MESSAGE_SHUTDOWN']

    return render_template('/sub_page.html', translations=translations_shutdown, lang=config_data['lang'], img_path='hippie.gif')

@app.route('/dwn-log',  methods = ['GET', 'POST'])
def download_logs():
    logger.write(Logging.INF, "Downloading logs") 
    log_zip_dir = str(my_path) + '/../'
    try:
        shutil.make_archive(base_dir='log', root_dir=log_zip_dir, format='zip', base_name=log_zip_dir + 'Visualiser_Logs')

        return send_file(log_zip_dir + 'Visualiser_Logs.zip', as_attachment=True)
    except Exception as e: 
        logger.write(Logging.ERR, "Error when downloading logs: " + str(e)) 

        config_data = DataExtraction.fix_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, config_path, log_path)

        translation_json = {}
        if config_data['lang'] in language_set:
            translation_json = FileManagement.read_json(translations_dir_path + config_data['lang'] + '.json' , log_path)

        translations_download_fail = {
            'TITLE': "",
            'MESSAGE': ""
        }

        if 'TITLE_DOWNLOAD_FAIL' in translation_json:
            translations_download_fail['TITLE'] = translation_json['TITLE_DOWNLOAD_FAIL']

        if 'MESSAGE_DOWNLOAD_FAIL' in translation_json:
            translations_download_fail['MESSAGE'] = translation_json['MESSAGE_DOWNLOAD_FAIL']

        return render_template('/sub_page.html', translations=translations_download_fail, lang=config_data['lang'], img_path='huel.gif', have_home=True), 500

@app.route('/view-server-log')
def view_server_log():
    logger.write(Logging.DEB, "View server logs") 

    config_data = DataExtraction.fix_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, config_path, log_path)

    translation_json = {}
    if config_data['lang'] in language_set:
        translation_json = FileManagement.read_json(translations_dir_path + config_data['lang'] + '.json' , log_path)

    return render_template('/view_logs.html', log=logger.read(), translations=translation_json, lang=config_data['lang'])
        
@app.route('/test-sub-page')
def test_sub_page():
    page = request.args.get('page')
    
    lang = 'en'
    if request.args.get('lang'):
        lang = request.args.get('lang')
    
    logger.write(Logging.DEB, "Test sub page: " + page) 

    translation_json = {}
    if lang in language_set:
        translation_json = FileManagement.read_json(translations_dir_path + lang + '.json' , log_path)

    translation_sub = {
        'TITLE': "",
        'MESSAGE': ""
    }
    img_path = None 

    if page == "dfail":
        if 'TITLE_DOWNLOAD_FAIL' in translation_json:
            translation_sub['TITLE'] = translation_json['TITLE_DOWNLOAD_FAIL']
        if 'MESSAGE_DOWNLOAD_FAIL' in translation_json:
            translation_sub['MESSAGE'] = translation_json['MESSAGE_DOWNLOAD_FAIL']

        img_path = 'huel.gif'
    elif page == "sdown":
        if 'TITLE_SHUTDOWN' in translation_json:
            translation_sub['TITLE'] = translation_json['TITLE_SHUTDOWN']
        if 'MESSAGE_SHUTDOWN' in translation_json:
            translation_sub['MESSAGE'] = translation_json['MESSAGE_SHUTDOWN']

        img_path = 'hippie.gif'
    elif page == "cfail":
        if 'TITLE_CONFIG_FAIL' in translation_json:
            translation_sub['TITLE'] = translation_json['TITLE_CONFIG_FAIL']
        if 'MESSAGE_CONFIG_FAIL' in translation_json:
            translation_sub['MESSAGE'] = translation_json['MESSAGE_CONFIG_FAIL']
    else:
        if 'TITLE_404' in translation_json:
            translation_sub['TITLE'] = translation_json['TITLE_404']
        if 'MESSAGE_404' in translation_json:
            translation_sub['MESSAGE'] = translation_json['MESSAGE_404']

        img_path = 'sexy_priest.gif'

    return render_template('/sub_page.html', translations=translation_sub, lang=lang, img_path=img_path, debug=True, have_home=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/ico'), 'cowboy.ico')

@app.errorhandler(404)
def not_found(e):
    logger.write(Logging.ERR, str(e) + ": " + request.base_url) 

    config_data = DataExtraction.fix_config_data(FileManagement.read_json(config_path, log_path), colour_key, pattern_key, config_path, log_path)
    
    translation_json = {}
    if config_data['lang'] in language_set:
        translation_json = FileManagement.read_json(translations_dir_path + config_data['lang'] + '.json' , log_path)

    translations_404 = {
        'TITLE': "",
        'MESSAGE': ""
    }

    if 'TITLE_404' in translation_json:
        translations_404['TITLE'] = translation_json['TITLE_404']

    if 'MESSAGE_404' in translation_json:
        translations_404['MESSAGE'] = translation_json['MESSAGE_404']

    return render_template('/sub_page.html', translations=translations_404, lang=config_data['lang'], img_path='sexy_priest.gif', have_home=True)

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
            

    for file in os.listdir(translations_dir_path):
        if file.endswith('.json'):
            language_set.add(os.path.splitext(file)[0])

    if ip is None:
        for attempt in range(10):
            try: 
                ip = get_ip()
                if ip is not None:
                    logger.write(Logging.INF, "IP address found socket: " + ip) 

                    FileManagement.update_json(config_path, {'ip': ip}, log_path)
                    app.run(debug=True, host='0.0.0.0')

                    break
                
            except Exception as e: 
                logger.write(Logging.ERR, "Unable to get Hostname and IP: " + str(e)) 

            time.sleep(1)

        if ip is None:
            FileManagement.update_json(config_path, {'ip': ''}, log_path)
