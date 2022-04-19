"""Methods and for attributes standardization following cf conventions.
See https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9/cf-conventions.html#attribute-appendix
"""
import pandas as pd
from functools import lru_cache

attributes = pd.read_csv("cf_attributes.csv", index_col=0)


@lru_cache
def global_attributes():
    """Documented on CF document as 'Use: G' attributes on Appendix A
    :return: Dataframe with global attributes
    """
    mask = attributes.Use.str.contains("G")
    return attributes[mask]


@lru_cache
def coordinate_attributes():
    """Documented on CF document as 'Use: C' attributes on Appendix A
    :return: Dataframe with attributes for variables containing coordinate data
    """
    mask = attributes.Use.str.contains("C")
    return attributes[mask]


@lru_cache
def variables_attributes():
    """Documented on CF document as 'Use: D' attributes on Appendix A
    :return: Dataframe with attributes for data variables
    """
    mask = attributes.Use.str.contains("D")
    return attributes[mask]
