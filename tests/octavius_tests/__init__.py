# -*- coding: utf-8 -*-

def load_config():
    import ConfigParser, os

    here = os.path.abspath(os.path.dirname(__file__))
    config = ConfigParser.ConfigParser()
    config.read(here + "/test.ini")

    parsed = dict()
    
    for section_name in config.sections():
        if not section_name in parsed.keys():
            parsed[section_name] = dict()
            
        for item in config.items(section_name): 
            parsed[section_name][item[0]] = item[1]

    return parsed

if __name__ == "__main__":
    print load_config()