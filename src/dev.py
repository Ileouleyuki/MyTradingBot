import logging

from lib.logger import SQLiteHandler

logger = logging.getLogger('someLoggerNameLikeDebugOrWhatever')


def main():

    logger = logging.getLogger('WEBAPP')
    logger.setLevel(logging.DEBUG)

    # sqlite handler
    sh = SQLiteHandler(db="test.db")
    sh.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(sh)

    # test
    logging.info('Start')
    logging.info('End')
    logging.warning('Some warning')
    logging.error('Alarma!')
    logging.debug('Debug')
    # test
    logger.info('Start')
    logger.info('End')
    logger.warning('Some warning')
    logger.error('Alarma!')
    logger.debug('Debug')

    raise Exception("toto")

    """
    # Create a logging object (after configuring logging)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(SQLiteHandler('debugLog.sqlite'))
    # test
    logger.debug('Test 1')
    logger.warning('Some warning')
    logger.error('Alarma!')
    logger.info('Start')
    logger.info('End')
    logger.warning('Some warning')
    logger.error('Alarma!')
    logger.debug('Debug')
    """


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
