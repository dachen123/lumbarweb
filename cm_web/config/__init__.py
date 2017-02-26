# -*- coding: utf-8 -*-
# author:  jianwen 
# company:  duoc
# date:      2016-01-09

import os
def load_config(test=False):
    """加载配置类"""

    mode = os.environ.get('CM_WEB_RUN_MODE')
    # if test is True:  #如果是unittest加载test配置
    #     if mode == 'PRODUCTION' or mode == 'TESTING':
    #         from .online_unittest import OnlineUnittestConfig
    #         return OnlineUnittestConfig
    #     else:
    #         from .unittesting import UnittestingConfig
    #         return UnittestingConfig
    try:
        if mode == 'TESTING' or test is True:
            from .test_config import Config
            return Config
        elif mode == 'PRODUCTION':
            from .production_config import Config
            return Config
    except ImportError, e:
        from .test_config import Config
        return Config

