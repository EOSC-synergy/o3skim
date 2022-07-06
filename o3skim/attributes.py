"""Methods and for attributes standardization following cf conventions.
See https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9/cf-conventions.html#attribute-appendix
"""
import pandas as pd
import os
import sys

__all__ = [
    "attributes",
    "global_attributes",
    "coordinate_attributes",
    "variables_attributes",
]


o3skim_dir = os.path.dirname(sys.modules["o3skim"].__file__)
attrs_file = "/".join([o3skim_dir, "data/cf_attributes.csv"])
attributes = pd.read_csv(attrs_file, index_col=0)


"""Documented on CF document as 'Use: G' attributes on Appendix A
:return: Dataframe with global attributes
"""
mask = attributes.Use.str.contains("G")
global_attributes = attributes[mask]


"""Documented on CF document as 'Use: C' attributes on Appendix A
:return: Dataframe with attributes for variables containing coordinate data
"""
mask = attributes.Use.str.contains("C")
coordinate_attributes = attributes[mask]


"""Documented on CF document as 'Use: D' attributes on Appendix A
:return: Dataframe with attributes for data variables
"""
mask = attributes.Use.str.contains("D")
variables_attributes = attributes[mask]
