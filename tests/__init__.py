"""Unit test package for torch_cd_example."""

import os
from o3skim import utils

data_dir = "./tests/data"


# Generation of mockup data
os.makedirs(data_dir, exist_ok=True)
with utils.cd(data_dir):
    from tests import mockup_data
