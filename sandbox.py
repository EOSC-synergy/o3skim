#!/usr/bin/env python3
"""Creates sandbox data inside 'data' forder"""
import o3mocks
import xarray as xr

files_convention = "CF-1.8"
files_prefix = "toz"
data_folder = "data"
dataset_name = f"{data_folder}/{files_prefix}.{files_convention}.nc"

if files_convention == "CF-1.8":
    o3mocks.cf_18.toz_dataset(dataset_name)
else:
    raise NotImplementedError("Unknown CF Conventions")


ds = xr.open_dataset(dataset_name)
dates, datasets = zip(*ds.groupby("time"))
paths = [f"{dataset_name[:-3]}_{t}.nc" for t in dates]
xr.save_mfdataset(datasets, paths)
