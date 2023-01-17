import logging

# 출력 포맷 정하기
logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s ', level=logging.DEBUG)
logging.debug('debug text')
logging.info('information text')
logging.warning('warning text')

logger = logging.getLogger('hello_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(ch)
logger.debug('debug text')