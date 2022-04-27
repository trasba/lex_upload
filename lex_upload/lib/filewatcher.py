'''
module to watch a folder for new files
'''
import os
import logging
import logging.handlers
import time

# logging when called as module
logger = logging.getLogger(__name__)

def log_setup():
    '''setup logger'''
    log_handler = logging.handlers.WatchedFileHandler('lex_upload.log')
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(funcName)s %(levelname)-8s [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def prt_filepath(filepath):
    ''' standard callback for filewatcher just printing the filepath '''
    print(filepath)

def filewatcher(path_to_watch = '', callback = prt_filepath):
    '''
    function to watch a folder for new files
    input: path_to_watch, callback
    if a file is found the callback function is called
    '''
    logger.info('starting filewatcher')
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    if path_to_watch == '':
        logger.info('path_to_watch is blank falling back to cwd')
        path_to_watch = cur_dir
    logger.info(f'watching folder {os.path.abspath(path_to_watch)} for new files')
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])

    while 1:
        time.sleep (1)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        #  removed = [f for f in before if not f in after]
        if added:
            for filename in added:
                if os.path.isfile(path_to_watch + filename):
                    logger.info(f'new file {os.path.abspath(path_to_watch + filename)}')
                    callback(os.path.abspath(path_to_watch + filename))
        before = after

if __name__ == '__main__':
    log_setup()
    print(filewatcher('upload/'))
