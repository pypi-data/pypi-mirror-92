import logging
import pathlib
import sys


logger = logging.getLogger('pukpuk')
formatter = {
    logging.DEBUG: logging.Formatter('%(name)s %(levelname)s [%(asctime)s] %(message)s'),
    logging.INFO: logging.Formatter('[%(asctime)s] %(message)s')
}
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def init(loglevel, directory):
    handler.setLevel(loglevel)
    logger.setLevel(loglevel)
    handler.setFormatter(formatter[loglevel])
    logger.addHandler(logging.FileHandler(filename=pathlib.Path(directory, 'pukpuk.log')))
