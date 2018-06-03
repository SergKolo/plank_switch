# -*- coding: utf-8 -*-
import json,os
from collections import OrderedDict as od

conf_file = os.path.join(os.environ['HOME'],'.config/dde_dockswitch_config.json')

def read_config_file():
    global conf_file
    if not os.path.exists(conf_file):
        return od()
    with open(conf_file) as fd:
        try:
            return od(json.load(fd))
        except JSONDecodeError:
           # TODO: how to handle this
           pass

def write_config_file(conf):
    global conf_file
    with open(conf_file,"w") as fd:
        json.dump(conf,fd,indent=4,sort_keys=True)

def remove_config_file():
    global conf_file
    os.unlink(conf_file)
