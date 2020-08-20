"""This module creates the sources objects"""
import yaml


def load(yaml_file):
    with open(yaml_file, "r") as ymlfile:
        return yaml.load(ymlfile)
