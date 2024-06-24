# import datetime
# from loguru import logger
# import os
#
#
# class LoggerConfig:
#     def __init__(self, folder="./log/", prefix="polaris-", rotation="10 MB", encoding="utf-8", backtrace=True,
#                  diagnose=True, append=False):
#         self.folder = folder
#         self.prefix = prefix
#         self.rotation = rotation
#         self.encoding = encoding
#         self.backtrace = backtrace
#         self.diagnose = diagnose
#         self.append = append
#         self.format = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> '
#                        '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> '
#                        '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>')
#
#         if not os.path.exists(self.folder):
#             os.makedirs(self.folder)
#
#     def get_logfile_name(self, suffix):
#         if self.append:
#             # 续写日志文件名加上当前日期
#             date = datetime.datetime.now().strftime("%Y-%m-%d")
#             return f"{self.folder}{self.prefix}{suffix}_{date}.log"
#         else:
#             timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             return f"{self.folder}{self.prefix}{suffix}_{timestamp}.log"
#
#     def configure_logging(self):
#         # 设置 debug 级别的日志
#         debug_logfile = self.get_logfile_name("debug")
#         logger.add(debug_logfile, level="DEBUG", backtrace=self.backtrace, diagnose=self.diagnose, format=self.format,colorize=True,
#                    rotation=self.rotation, encoding=self.encoding,
#                    filter=lambda record: record["level"].no >= logger.level("DEBUG").no)
#
#         # 设置 info 级别的日志
#         info_logfile = self.get_logfile_name("info")
#         logger.add(info_logfile, level="INFO", backtrace=self.backtrace, diagnose=self.diagnose, format=self.format,colorize=True,
#                    rotation=self.rotation, encoding=self.encoding,
#                    filter=lambda record: record["level"].no >= logger.level("INFO").no)
#
#
# if __name__ == "__main__":
#     # 创建LoggerConfig实例并配置日志
#     logger_config = LoggerConfig(append=True)  # 设置append为True以续写日志
#     logger_config.configure_logging()
#
#     # 输出不同级别的日志消息
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")

import datetime
import os
import sys

from loguru import logger


class LoggerConfig:
    _instance = None  # 单例模式的关键字

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self, folder="./log/", prefix="polaris-", rotation="10 MB", encoding="utf-8", backtrace=True,
                 diagnose=True, append=False):
        if not hasattr(self, 'initialized'):  # 防止多次初始化
            self.folder = folder
            self.prefix = prefix
            self.rotation = rotation
            self.encoding = encoding
            self.backtrace = backtrace
            self.diagnose = diagnose
            self.append = append
            self.format = ('<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> '
                           '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> '
                           '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>')

            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

            self.initialized = True

    def get_logfile_name(self, suffix):
        if self.append:
            # 续写日志文件名加上当前日期
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            return f"{self.folder}{self.prefix}{suffix}_{date}.log"
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            return f"{self.folder}{self.prefix}{suffix}_{timestamp}.log"

    def configure_logging(self):
        # 设置 debug 级别的日志
        debug_logfile = self.get_logfile_name("debug")
        logger.add(debug_logfile, level="DEBUG", backtrace=self.backtrace, diagnose=self.diagnose, format=self.format,
                   colorize=True,
                   rotation=self.rotation, encoding=self.encoding,
                   filter=lambda record: record["level"].no >= logger.level("DEBUG").no)

        # 设置 info 级别的日志
        info_logfile = self.get_logfile_name("info")
        logger.add(info_logfile, level="INFO", backtrace=self.backtrace, diagnose=self.diagnose, format=self.format,
                   colorize=True,
                   rotation=self.rotation, encoding=self.encoding,
                   filter=lambda record: record["level"].no >= logger.level("INFO").no)


# 应用启动时创建LoggerConfig单例
# logger.remove(0)
# logger.add(sys.stderr, level="DEBUG")
# # logger.add(sys.stderr, level="INFO")
# # 应用日志配置
# logger_config = LoggerConfig(append=0)  # 设置append为1以续写日志
# logger_config.configure_logging()
