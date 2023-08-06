import argparse
import validators
import yaml

class ArgParseException(Exception):
    def __init__(self, string, type):
        super(ArgParseException, self).__init__(f"Argument {string} could not be cast to {type}")

def str2bool(string):
    string = string.lower()
    if string in ["true", "1", "yes"]:
        return True

    if string in ["false", "0", "no"]:
        return False

    raise ArgParseException(string, "boolean")

def url(string):
    if not validators.url(string):
        raise ArgParseException(string, "url")
    return string

def get_args():
    parser = argparse.ArgumentParser()

    try:
        with open("./config/config.yaml", "r") as f:
            conf = yaml.safe_load(f)
    except:
        conf = {}

    def add_argument(argname, type, default=-1):
        conf_argname = argname[2:] if argname.startswith("--") else argname

        if default != -1:
            new_default = type(conf[conf_argname]) if conf_argname in conf else default
            parser.add_argument(argname, type=type, default=new_default)
        else:
            parser.add_argument(argname, type=type)

    add_argument("--verbose", type=str2bool, default=True)
    add_argument("--configfile", type=str, default="config.yaml")
    add_argument("--layout", type=str, default="./config/defaultlayout.md")
    add_argument("--pdfdirname", type=str, default="pdfs")
    add_argument("--postdirname", type=str, default="_posts")
    add_argument("--archive", type=str, default="arxiv")

    parser.add_argument("paperurl", type=url)
    parser.add_argument("categories", type=str, nargs="+")

    return parser.parse_args()
