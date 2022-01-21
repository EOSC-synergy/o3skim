"""O3as package with utilities to handle ozone data skimming."""
import logging
from functools import reduce

from o3skim import operations

logger = logging.getLogger("o3skim")


def process(dataset, actions):
    """Function in charge of processing the list of o3skim operations
    to the ozone variables dataset. The available list of operations
    to perform are:

        :lon_mean: Longitudinal mean accross the dataset.
        :lat_mean: Latitudinal mean accross the dataset.

    Note that multiple operations can be concatenated. For example
    using the list ['lon_mean', 'lat_mean'] as actions parameter
    input would perform a longitudinal mean followed afterwards by
    a latitudinal mean before returning the result.

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`iris.Cube`

    :param actions: List of operation names to perform.
    :type actions: list

    :return: Dataset after processing listed operations.
    :rtype: :class:`iris.Cube`
    """
    logger.debug("Processing queue: %s", actions)
    return reduce(operations.run, actions, dataset)
