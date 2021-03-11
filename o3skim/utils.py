"""This module offers some utils for code management."""
import logging
import io

logger = logging.getLogger('o3skim.utils')


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
