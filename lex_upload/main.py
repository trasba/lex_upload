'''
package to upload files to lexoffice api
config.json holds settings (api_key and folders)
upload folder is watched for new files,
on new_file the file is checked to be a valid pdf file,
the fie is uploaded and according to the return_code the file is moved to a folder
    202 = accepted
    4xx = some kind of failure
    corrupted = not a valid pdf
'''
import logging
import logging.handlers
import time
import os
import json
import re
import signal
import sys
# from pathlib import Path
from .lib import lex_upload, pdf_check, filewatcher

# logging when called as module
logger = logging.getLogger(__name__)

# main_dir = os.path.dirname(os.path.realpath(__file__))
home_dir = os.path.expanduser('~')
CONF_DIR = '.trasba/lex_upload'
CONF_FILENAME = 'config.json'
conf_path = os.path.join(home_dir, CONF_DIR, CONF_FILENAME)
log_path = os.path.join(home_dir, CONF_DIR, 'log')

if not os.path.exists(conf_path):
    print(f'ERROR {conf_path} does not exist. Please create the config file!')
conf_file = open(conf_path, encoding='utf8')
config = json.load(conf_file)
conf_file.close()

def init():
    ''' initialize module, create folders if not existing'''
    for folder in ["202", "4xx", "corrupt"]:
        if not os.path.exists(config[folder]):
            os.makedirs(config[folder])

def signal_handler(_sig, _frame):
    '''signal handler to catch user CTRL-C input and exit system '''
    print('You pressed Ctrl+C!')
    logger.info('user pressed Ctrl+C!')
    sys.exit(0)

def log_setup():
    '''setup logger'''
    log_handler = logging.handlers.WatchedFileHandler(log_path)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(funcName)s %(levelname)-8s [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    # logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def helper_dup(dest_filepath):
    ''' helper to handle duplicates and logging '''
    res = dup_handling(dest_filepath)
    if res != dest_filepath:
        logger.info(f'file already existant, changing filename to: {os.path.basename(res)}')
    return res

def dup_handling(in_path):
    '''
    input: in_path (path to file)
    if a file with given path already exists it will return a path with suffix '#_[00-99]'
    incrementing the number until it finds a "free" path
    *****
    return: modified path
    '''
    if os.path.exists(in_path):
        res = dup_handling(inc_suffix(in_path))
    else:
        res = in_path
    return res

def inc_suffix(in_str):
    '''
    input: in_str
    will search for the string '#_[00-99].' in in_str and increment the number by 1
    if the string is not found '#_00 will be added before the file extension
    *****
    return: modified string
    '''
    reg_ex = re.search('#_[0-9][0-9]', in_str)
    if reg_ex:
        # pos = start position of # string
        # pos = reg_ex.start(0)
        # get number of # string
        reg_num = int(reg_ex.group(0)[2:4])
        reg_num += 1
        reg_replace = '#_' + str(reg_num).zfill(2)
        return in_str.replace(reg_ex.group(0), reg_replace)
    else:
        _filename, file_extension = os.path.splitext(in_str)
        if file_extension == '':
            return in_str + '#_00'
        else:
            return in_str.replace(file_extension, '#_00' + file_extension)

def helper_upload(filepath):
    ''' helper function for callback from filewatcher, handles returned files,
        checks if its valid pdf than uploads them and handles the possible return codes'''
    # check if pdf valid
    pdf_res = pdf_check(filepath)
    if pdf_res == 0:
        # upload file
        lex_result = lex_upload(filepath, config["api_key"])
        # move file to folder according to status_code
        if lex_result == 202:
            logger.info('moving file to 202 folder')
            dest_filepath = helper_dup(config["202"] + os.path.basename(filepath))
            os.rename(filepath, dest_filepath)
        else:
            logger.info('moving file to 4xx folder')
            dest_filepath = helper_dup(config["4xx"] + os.path.basename(filepath))
            os.rename(filepath, dest_filepath)
    else:
        logger.info('moving file to corrupt folder')
        dest_filepath = helper_dup(config["corrupt"] + os.path.basename(filepath))
        os.rename(filepath, dest_filepath)

if __name__ == '__main__':
    logger = logging.getLogger()
    log_setup()
    init()
    signal.signal(signal.SIGINT, signal_handler)
    try:
        filewatcher(config["upload"], helper_upload)
    except BaseException as er:
        logger.error(str(er))
