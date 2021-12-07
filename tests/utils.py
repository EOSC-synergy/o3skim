"""Tests utils module"""
import itertools


def all_perm(*args):
    """Returns all arguments permutations in 1 list"""
    radios = range(1, len(args) + 1)
    perm = lambda r: itertools.permutations(args, r)
    return [list(y) for r in radios for y in perm(r)]
