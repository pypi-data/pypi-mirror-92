# -*- coding: utf-8 -*-

from hagworm.frame.gunicorn import DEFAULT_WORKER_STR, SIMPLE_LOG_CONFIG

from setting import ConfigDynamic

# 进程数
workers = ConfigDynamic.ProcessNum

# 工人类
worker_class = DEFAULT_WORKER_STR

# 日志配置
logconfig_dict = SIMPLE_LOG_CONFIG
