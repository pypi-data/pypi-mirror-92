# -*- coding: utf-8 -*-
"""
Raster and spatial interpolation functions.
"""
import os
import pandas as pd
import numpy as np
try:
    from rasterio import open as ras_open
    from rasterio import transform
except:
    print('Install rasterio for raster functions')
from gistools.util import convert_crs


def save_geotiff(df, data_col, crs, x_col='x', y_col='y', time_col=None, nfiles='many', grid_res=None, export_path='geotiff.tif', ):
    """
    Function to convert a dataframe of x, y, and data to a GeoTiff. If the DataFrame has a time_col, then these instances can be saved as multiple bands in the GeoTiff or as multiple GeoTiffs.

    df: DataFrame
        DataFrame with at least an x_col, y_col, and data_col. The combo of x_col and y_col must be unique without a corresponding time_col.
    x_col: str
        The x column name.
    y_col: str
        The y column name.
    data_col:str
        The data column name.
    crs: str or int
        The projection info for the data (either a proj4 str or epsg int).
    time_col: str or None
        The time column if one exists.
    nfiles:str
        If time_col is passed, how many files should be created? 'one' will make a single GeoTiff with many bands and 'many' will make many GeoTiffs.
    export_path: str
        The save path.
    grid_res:int
        The grid resolution of the output raster. The default None will output the the resolution based on the point spacing of a regular grid.

    Returns
    -------
    None
    """

    ### create the xy coordinates
    if time_col is None:
        xy1 = df[[x_col, y_col]]
    else:
        time = df[time_col].sort_values().unique()
        xy1 = df.loc[df[time_col] == time[0], [x_col, y_col]]
    if any(xy1.duplicated()):
        raise ValueError('x and y coordinates are not unique!')

    ### Determine grid res
    if grid_res is None:
        res_df1 = (xy1.loc[0] - xy1).abs()
        res_df2 = res_df1.replace(0, np.nan).min()
        x_res = res_df2[x_col]
        y_res = res_df2[y_col]
    elif isinstance(grid_res, int):
        x_res = y_res = grid_res
    else:
        raise ValueError('grid_res must either be None or an integer.')

    ### Make the affline transformation for Rasterio
    trans2 = transform.from_origin(xy1[x_col].min() - x_res/2, xy1[y_col].max() + y_res/2, x_res, y_res)

    ### Make the rasters
    if time_col is None:
        z = df.set_index([y_col, x_col])[data_col].unstack().values[::-1]
        new_dataset = ras_open(export_path, 'w', driver='GTiff', height=len(xy1[y_col].unique()), width=len(xy1[x_col].unique()), count=1, dtype=df[data_col].dtype, crs=convert_crs(crs, pass_str=True), transform=trans2)
        new_dataset.write(z, 1)
        new_dataset.close()
    else:
        if nfiles == 'one':
            new_dataset = ras_open(export_path, 'w', driver='GTiff', height=len(xy1[y_col].unique()), width=len(xy1[x_col].unique()), count=len(time), dtype=df[data_col].dtype, crs=convert_crs(crs), transform=trans2)
            for i in range(1, len(time)+1):
                z = df.loc[df[time_col] == time[i - 1]].set_index([y_col, x_col])[data_col].unstack().values[::-1]
                new_dataset.write(z, i)
            new_dataset.close()
        elif nfiles == 'many':
            file1 = os.path.splitext(export_path)[0]
            for i in time:
                str_date = pd.to_datetime(i).strftime('%Y-%m-%d_%H')
                file2 = file1 + '_' + str_date + '.tif'
                z = df.loc[df[time_col] == i].set_index([y_col, x_col])[data_col].unstack().values[::-1]
                new_dataset = ras_open(file2, 'w', driver='GTiff', height=len(xy1[y_col].unique()), width=len(xy1[x_col].unique()), count=1, dtype=df[data_col].dtype, crs=convert_crs(crs), transform=trans2)
                new_dataset.write(z, 1)
                new_dataset.close()
