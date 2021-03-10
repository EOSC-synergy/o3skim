"""This module offers some utils for code management. For example
utils to change easily from directory or create netCDF files.

Although this module is not expected to be used out of the o3skim
package, some functions might be convenient when using the python 
shell.
"""
import logging
import yaml
import io

logger = logging.getLogger('o3skim.utils')


def load(yaml_file):
    """Loads the .yaml file and returns a python dictionary with all
    the yaml keys and values. Note a yaml file can have key:values 
    sotored inside values, therefore the returned dictionary might 
    have dictionaries stored inside values. 

    :param yaml_file: Path pointing to the yaml configuration file.
    :type yaml_file: str

    :return: Dictionary with the yaml structure key:value.
    :rtype: dict
    """
    with open(yaml_file, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
        logging.debug("Configuration data: %s", config)
        return config


def save(yaml_file, metadata):
    """Saves the metadata dict on the current folder with yaml 
    format. 

    :param yaml_file: Name for the output yaml file.
    :type yaml_file: str

    :param metadata: Dict with the data to save into.
    :type metadata: dict
    """
    with open(yaml_file, 'w') as ymlfile:
        yaml.dump(metadata, ymlfile, allow_unicode=True)


def mergedicts(d1, d2, if_conflict=lambda _, d: d):
    """Merges dict d2 in dict d2 recursively. If two keys exist in 
    both dicts, the value in d1 is superseded by the value in d2.

    :param d1: Dict to be recursively completed by d2.
    :type d1: dict

    :param d2: Dict to be recursively merged in d1.
    :type d2: dict

    :param if_conflict: Action to perform when key from d1 exists in d1.
        Fun(d1,d2) which returns the value to store in d1.
        Default action is to replace d1 key value by d2 key value.
    :type if_conflict: function, optional
    """
    for key in d2:
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                mergedicts(d1[key], d2[key], if_conflict)
            elif d1[key] == d2[key]:
                pass  # same leaf value
            else:
                d1[key] = if_conflict(d1[key], d2[key])
        else:
            d1[key] = d2[key]


def chunkio(headid, str_iter):
    """Chunks an iterable of strings. The text passed by str_iter is
    evaluated element by element (normally line by line). The elements
    are grouped/chunked by every element (line) which contains a 
    "headid".

    :param headid: Line key word to separate chunks.
    :type headid: str

    :param str_iter: Iterable of strings to chunk.
    :type str_iter: iter

    :return: List of tuples with the header and chunk as StringIO.
    :rtype: [(str, :class:`io.StringIO`)]
    """
    heads = []
    chunks = []
    chunk = io.StringIO()
    for line in str_iter:
        if headid in line:
            heads.append(line)
            chunks.append(chunk)
            chunk.seek(0)   # rewind the stream
            chunk = io.StringIO()
        else:
            chunk.write(line)
    return zip(heads, chunks[1:-1])
