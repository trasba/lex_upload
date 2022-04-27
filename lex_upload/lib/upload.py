'''
module handling the upload of a file to lexoffice
'''
import os
import logging
import logging.handlers
import time
import requests

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

def lex_upload(filepath, api_key):
    '''
    function handling the upload of a file to lexoffice
    input: filepath, api_key
    output: response.status_code (int 202, 401 ...)
    '''
    filename=os.path.basename(filepath)
    logger.info(f'uploading file: {filename}')
    url = "https://api.lexoffice.io/v1/files"
    payload={'type': 'voucher'}
    files=[('file',('file.pdf',open(filepath,'rb'),'application/octet-stream'))]
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    # if file is accepted move to 202 folder
    if response.status_code == 202:
        logger.info('file upload accepted')
        print('file upload accepted')
    else:
        logger.error(f'response status code: {str(response.status_code)}')
        print('response status code', response.status_code)
    return response.status_code

if __name__ == '__main__':
    # log_setup()
    # print(lex_upload("upload/test.pdf", config['api_key']))
    pass
