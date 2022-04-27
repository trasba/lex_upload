'''
module to check wether a file is a valid pdf document
'''
import logging
import logging.handlers
import time
import os
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

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
    # logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def pdf_check(filepath):
    '''
    function to check wether a file is a valid pdf document
    input: filepath
    return: 0 == valid pdf, 1,2,3 => not a valid pdf
    '''
    try:
        _test = extract_text(filepath)
        logger.info(f'{os.path.basename(filepath)} pdf check successful')
        return 0

    except PDFSyntaxError as error:
        logger.error(f'{os.path.basename(filepath)} {str(error)}')
        return 1

    except FileNotFoundError as error:
        logger.error(f'{os.path.basename(filepath)} {str(error)}')
        return 2

    except BaseException as error:
        logger.error(f'{os.path.basename(filepath)} {str(error)}')
        return 3

if __name__ == "__main__":
    log_setup()
    print(pdf_check("test3.pdf"))
