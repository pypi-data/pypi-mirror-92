# -*- coding: utf-8 -*-
"""
Functions to delineate catchments.
"""
import numpy as np
import pandas as pd
from gistools.vector import kd_nearest, convert_lines_to_points
from gistools.util import load_geo_data
from shapely.geometry import box

#####################################################
#### MFE REC streams network


def find_upstream(nzreach, rec_streams, segment_id_col='nzsegment', from_node_col='FROM_NODE', to_node_col='TO_NODE'):
    """
    Function to estimate all of the reaches (and nodes) upstream of specific reaches.

    Parameters
    ----------
    nzreach : list, ndarray, Series of int
        The NZ reach IDs
    rec_streams_shp : str path or GeoDataFrame
        str path to the REC streams shapefile or the equivelant GeoDataFrame.
    segment_id_col : str
        The column name of the line segment id.
    from_node_col : str
        The from node column
    to_node_col : str
        The to node column

    Returns
    -------
    DataFrame
    """
    if not isinstance(nzreach, (list, np.ndarray, pd.Series)):
        raise TypeError('nzreach must be a list, ndarray or Series.')

    ### Load data
    rec = load_geo_data(rec_streams).drop('geometry', axis=1).copy()

    ### Run through all nzreaches
    reaches_lst = []
    for i in nzreach:
        reach1 = rec[rec[segment_id_col] == i].copy()
        up1 = rec[rec[to_node_col].isin(reach1[from_node_col])]
        while not up1.empty:
            reach1 = pd.concat([reach1, up1])
            up1 = rec[rec[to_node_col].isin(up1[from_node_col])]
        reach1.loc[:, 'start'] = i
        reaches_lst.append(reach1)

    reaches = pd.concat(reaches_lst)
    reaches.set_index('start', inplace=True)

    return reaches


###############################################
### Catch delineation using the REC


def extract_catch(reaches, rec_catch, segment_id_col='nzsegment'):
    """
    Function to extract the catchment polygons from the rec catchments layer. Appends to reaches layer.

    Parameters
    ----------
    reaches : DataFrame
        The output DataFrame from the find_upstream function.
    rec_catch_shp : str path, dict, or GeoDataFrame
        str path to the REC catchment shapefile or a GeoDataFrame.
    segment_id_col : str
        The column name of the line segment id.

    Returns
    -------
    GeoDataFrame
    """
    sites = reaches[segment_id_col].unique().astype('int32')
    catch0 = load_geo_data(rec_catch)

    catch1 = catch0[catch0[segment_id_col].isin(sites)].copy()
    catch2 = catch1.dissolve(segment_id_col).reset_index()[[segment_id_col, 'geometry']]

    ### Combine with original sites
    catch3 = catch2.merge(reaches.reset_index(), on=segment_id_col)
    catch3.crs = catch0.crs

    return catch3


def agg_catch(rec_catch):
    """
    Simple function to aggregate rec catchments.

    Parameters
    ----------
    rec_catch : GeoDataFrame
        The output from extract_catch

    Returns
    -------
    GeoDataFrame
    """
    rec_shed = rec_catch[['start', 'geometry']].dissolve('start')
    rec_shed.index = rec_shed.index.astype('int32')
    rec_shed['area'] = rec_shed.area
    rec_shed.crs = rec_catch.crs
    return rec_shed.reset_index()


def catch_delineate(sites, rec_streams, rec_catch, segment_id_col='nzsegment', from_node_col='FROM_NODE', to_node_col='TO_NODE', ignore_order=1, stream_order_col='StreamOrde', max_distance=np.inf, site_delineate='all', returns='catch'):
    """
    Catchment delineation using the REC streams and catchments.

    Parameters
    ----------
    sites : str path or GeoDataFrame
        Points shapfile of the sites along the streams or the equivelant GeoDataFrame.
    rec_streams : str path or GeoDataFrame
        str path to the REC streams shapefile, the equivelant GeoDataFrame, or a dict of parameters to read in an mssql table using the rd_sql function.
    rec_catch : str path or GeoDataFrame
        str path to the REC catchment shapefile, the equivelant GeoDataFrame, or a dict of parameters to read in an mssql table using the rd_sql function.
    segment_id_col : str
        The column name of the line segment id.
    from_node_col : str
        The from node column
    to_node_col : str
        The to node column
    ignore_order : int
        Ignore the stream orders in the search up to this int.
    stream_order_col : str
        The stream order column.
    max_distance : non-negative float, optional
        Return only neighbors within this distance. This is used to prune tree searches, so if you are doing a series of nearest-neighbor queries, it may help to supply the distance to the nearest neighbor of the most recent point. It's best to define a reasonable distance for the search.
    site_delineate : 'all' or 'between'
        Whether the catchments should be dileated all the way to the top or only in between the sites.
    returns : 'catch' or 'all'
        Return only the catchment polygons or the catchments, reaches, and sites

    Returns
    -------
    GeoDataFrame
        Polygons
    """

    ### Parameters


    ### Modifications {segment_id_col: {NZTNODE/NZFNODE: node # to change}}
    # mods = {13053151: {segment_id_col: 13055874}, 13048353: {'NZTNODE': 13048851}, 13048498: {'NZTNODE': 13048851}, 13048490: {'ORDER': 3}}

    ### Load data
    rec_catch = load_geo_data(rec_catch)
    rec_streams = load_geo_data(rec_streams)
    pts = load_geo_data(sites)
    pts['geometry'] = pts.geometry.simplify(1)

    ### make mods
    # for i in mods:
    #     rec_streams.loc[rec_streams['segment_id_col'] == i, list(mods[i].keys())] = list(mods[i].values())

    ### Find closest REC segment to points
    if max_distance == np.inf:
        buffer_dis = 100000
    else:
        buffer_dis = max_distance

    pts_extent = box(*pts.unary_union.buffer(buffer_dis).bounds)

    s_order = list(range(1, ignore_order + 1))
    rec_streams2 = rec_streams[~rec_streams[stream_order_col].isin(s_order)]

    rec_pts2 = convert_lines_to_points(rec_streams2, segment_id_col, pts_extent)

    # rec_pts1 = rec_streams2[rec_streams2.intersects(pts_extent)].set_index(segment_id_col).copy()
    # coords = rec_pts1.geometry.apply(lambda x: list(x.coords)).explode()
    # geo1 = coords.apply(lambda x: Point(x))
    #
    # rec_pts2 = gpd.GeoDataFrame(coords, geometry=geo1, crs=rec_pts1.crs).reset_index()

    pts_seg = kd_nearest(pts, rec_pts2, segment_id_col, max_distance=max_distance)
    pts_seg = pts_seg[pts_seg[segment_id_col].notnull()].copy()
    nzreach = pts_seg[segment_id_col].copy().unique()

    ### Find all upstream reaches
    reaches = find_upstream(nzreach, rec_streams=rec_streams, segment_id_col=segment_id_col, from_node_col=from_node_col, to_node_col=to_node_col)

    ### Clip reaches to in-between sites if required
    if site_delineate == 'between':
        reaches1 = reaches.reset_index().copy()
        reaches2 = reaches1.loc[reaches1[segment_id_col].isin(reaches1.start.unique()), ['start', segment_id_col]]
        reaches2 = reaches2[reaches2.start != reaches2[segment_id_col]]

        grp1 = reaches2.groupby('start')

        for index, r in grp1:
#            print(index, r)
            r2 = reaches1[reaches1.start.isin(r[segment_id_col])][segment_id_col].unique()
            reaches1 = reaches1[~((reaches1.start == index) & (reaches1[segment_id_col].isin(r2)))]

        reaches = reaches1.set_index('start').copy()

    ### Extract associated catchments
    rec_catch2 = extract_catch(reaches, rec_catch=rec_catch, segment_id_col=segment_id_col)

    ### Aggregate individual catchments
    rec_shed = agg_catch(rec_catch2)
    rec_shed.columns = [segment_id_col, 'geometry', 'area']
    rec_shed1 = rec_shed.merge(pts_seg.drop('geometry', axis=1), on=segment_id_col)

    ### Return
    if returns == 'catch':
        return rec_shed1
    else:
        return rec_shed1, reaches, pts_seg
