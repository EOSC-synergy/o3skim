"""This module offers some utils for code management."""
import logging
import io
from o3skim import attributes

logger = logging.getLogger("o3skim.utils")


def cf_clean(dataset):
    """Removes those existing attributes which are not in the CF specifications.
    :param dataset: Xarray dataset following CF conventions
    """
    # Clean global attributes
    cfds_attrs = set(attributes.global_attributes().index)
    dataset.attrs = {k: v for k, v in dataset.attrs.items() if k in cfds_attrs}
    # Clean coordinate attributes
    cfds_attrs = set(attributes.coordinate_attributes().index)
    for var in dataset.coords:
        var = dataset[var]
        var.attrs = {k: v for k, v in var.attrs.items() if k in cfds_attrs}
    # Clean data variables attributes
    cfds_attrs = set(attributes.variables_attributes().index)
    for var in dataset.data_vars:
        var = dataset[var]
        var.attrs = {k: v for k, v in var.attrs.items() if k in cfds_attrs}


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
            chunk.seek(0)  # rewind the stream
            chunk = io.StringIO()
        else:
            chunk.write(line)
    return zip(heads, chunks[1:-1])
