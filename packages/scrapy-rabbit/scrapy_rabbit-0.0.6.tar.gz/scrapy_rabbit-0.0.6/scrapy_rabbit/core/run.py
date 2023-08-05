# -*- coding: utf-8 -*-
import sys
import os
from importlib import import_module
import datetime
import logging
import time

import inspect
from scrapy_rabbit.Lib.loadspider import SpiderLoader

sys.path.append(os.path.abspath('.'))

try:
    sys.path.append(os.path.abspath('../..'))
    import settings
except ModuleNotFoundError:
    sys.path.append(os.path.abspath('..'))
    import settings

config = dict()

save_log_file = getattr(settings, 'SAVE_LOG', False)
if save_log_file:
    logging.basicConfig(level=getattr(logging, getattr(settings, 'LOG_LEVEL', 'DEBUG')),
                        format='pid:%(process)d %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=getattr(settings, 'LOG_FILE', f'{time.strftime("%Y-%m-%d", time.localtime())}.log'),
                        # filename=getattr(settings, 'LOG_FILE', f'{time.strftime("%Y-%m-%d", time.localtime())}.log'),
                        # filename=getattr(logging, getattr(settings, 'LOG_FILE', '')),
                        # filemode='a'
                        )
else:
    logging.basicConfig(level=getattr(logging, getattr(settings, 'LOG_LEVEL', 'DEBUG')),
                        format='pid:%(process)d %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        # filename=getattr(logging, getattr(settings, 'LOG_FILE', '')),
                        # filemode='a'
                        )


def run(cmd) -> None:
    """手动启动方法"""

    if isinstance(cmd, str):
        cmd = cmd.split(' ')
    while '' in cmd:
        cmd.remove('')
    base_path = 'spiders.'
    if len(cmd) != 4:
        logging.error("命令行格式错误")
        raise
    try:
        path = base_path + cmd[0]
        root_path = cmd[0]
        spider_name = cmd[1]
        way = cmd[2]
        async_num = int(cmd[3])
        queue_name = cmd[0] + '/' + spider_name
    except Exception:
        logging.error("命令行格式错误")
        raise

    start_time = datetime.datetime.now()
    logging.info(f"爬虫启动时间：{start_time}")

    sl = SpiderLoader(type("settings", (object,), dict(getlist=lambda x: [path], getbool=lambda x: False)))
    spider_module = sl.load(spider_name)
    sp = spider_module(path=path, queue_name=queue_name, way=way, async_num=async_num)

    # frame = __import__(spider_name)
    # print(spider_module)
    # print(frame)
    #
    # classes = ''
    # clsmembers = inspect.getmembers(spider_module, inspect.isclass)
    # for (name, _) in clsmembers:
    #     print(name, _)
    #     if 'Spider' in name:
    #         classes = name
    # print(classes)
    get_settings = getattr(spider_module, 'custom_settings', None)

    # a = {
    #     'a': 123,
    #     'b': 3231,
    #     'asd': 321,
    #     'c': 4325
    # }
    #
    # print(sorted(a.items(), key=lambda item: item[1]))

    if get_settings:
        try:
            item_pipelines = list(get_settings['ITEM_PIPELINES'].keys())
            if '.' in item_pipelines[0]:
                pipline_name = item_pipelines[0].split('.')[-1]
            else:
                pipline_name = item_pipelines[0]
        except KeyError:
            pipline_name = "%sPipeline" % root_path
    else:
        pipline_name = "%sPipeline" % root_path

    pipeline = import_module("pipelines")
    pipelineObj = getattr(pipeline, pipline_name, getattr(pipeline, 'Pipeline'))()

    pipelineObj.open_spider(sp)
    setattr(sp, "pipelineObj", pipelineObj)
    sp.main()
    pipelineObj.close_spider(sp)
    end_time = datetime.datetime.now()

    logging.info(f"爬虫启动时间：{start_time}")
    logging.info(f"爬虫结束时间：{end_time}")
    logging.info(f"爬虫运行时长：{end_time - start_time}")
    logging.info(f"Item数量：{pipelineObj.count}")
