import inspect
import os
from logbook import Logger,TimedRotatingFileHandler
this_file=inspect.getfile(inspect.currentframe())
path=os.path.abspath(os.path.dirname(this_file))
tpath=path+os.sep+"logs"

logger=Logger("xinhua news")
def register_handlers():
    try:
        sys_handler = TimedRotatingFileHandler(tpath + os.sep + 'sys_logs.txt', \
                                               level="DEBUG", date_format='%Y-%m-%d', backup_count=30)
        sys_handler.push_application()

        info_handler = TimedRotatingFileHandler(tpath + os.sep + 'info_logs.txt', \
                                                level="INFO", date_format='%Y-%m-%d', backup_count=30)
        info_handler.push_application()
        error_handler = TimedRotatingFileHandler(tpath + os.sep + 'error_logs.txt', \
                                                 level="ERROR", date_format='%Y-%m-%d', backup_count=30)
        error_handler.push_application()

    except:
        write_err("handers注册失败，请检查！")
        print("handers注册失败，请检查！")
        exit(0)
def write_info(text):
    if text:
        logger.info(text)





def write_sys(text):
    if text:
        logger.debug(text)


def write_err(text):
    if text:
        logger.error(text)
register_handlers()