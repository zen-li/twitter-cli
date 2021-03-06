
from logger import getLogger
import requests
from urlparse import urlparse
from os.path import join, split, exists
from config import *

logger = getLogger(__name__)

def _download(url, output_dir, prefix, extension):
    try:
        paths = split(urlparse(url).path)
        filename = paths[-1]

        if '.' in filename:
            filename = '%s-%s' % (prefix, filename)
        else:
            filename = '%s-%s.%s' % (prefix, filename, extension)

        filepath = join(output_dir, filename)

        if exists(filepath):
            logger.info('Found existing file here, reusing it...')
            return filepath

        logger.info('Downloading %s' % url)
        response = requests.get(url, proxies=get_proxy())
        logger.info('Downloaded to %s' % filepath)

        with open(filepath, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        logger.exception(e)
        filepath = None

    return filepath

def download_video(url, output_dir, prefix='', extension='mp4'):
    return _download(url, output_dir, prefix, extension)

def download_photo(url, output_dir, prefix='', extension='jpg'):
    return _download(url, output_dir, prefix, extension)
