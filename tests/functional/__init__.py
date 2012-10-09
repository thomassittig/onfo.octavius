# -*- coding: utf-8 -*-

def load_config():
    import ConfigParser, os

    here = os.path.abspath(os.path.dirname(__file__))
    config = ConfigParser.ConfigParser()
    config.read(here + "/test.ini")

    configs = dict(main=dict())

    for item in config.items("main"):
        if not item[0] in configs.get("main").keys():
            configs.get("main")[item[0]] = item[1]

    return configs