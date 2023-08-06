#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:10:31 2021

@author: mike
"""
from datetime import datetime, date
from typing import List, Optional, Union
from pydantic import BaseModel, Field
import orjson
from enum import Enum


########################################
### Helper functions


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


#########################################
### Models


class Period(str, Enum):
    seconds = 'S'
    hours = 'H'
    days = 'D'
    weeks = 'W'
    months = 'M'
    years = 'Y'


class Units(str, Enum):
    liters = 'l'
    cubic_meters = 'm3'


class LimitBoundary(str, Enum):
    min = 'min'
    max = 'max'


class AggregationStat(str, Enum):
    min = 'min'
    max = 'max'
    median = 'median'
    mean = 'mean'


class Limit(BaseModel):
    """

    """
    value: Union[int, float]
    period: Period
    units: Units
    limit_boundary: LimitBoundary
    aggregation_stat: Optional[AggregationStat]


class ConditionType(str, Enum):
    abstraction_limit = 'abstraction limit'


class Condition(BaseModel):
    """

    """
    condition_type: ConditionType
    limit: Optional[List[Limit]]
    text: Optional[str]


class GeometryType(str, Enum):
    point = 'Point'
    line = 'Line'
    polygon = 'Polygon'


class Geometry(BaseModel):
    """
    Geojson-like geometry model.
    """
    type: GeometryType
    coordinates: List[float]


class ActivityType(str, Enum):
    consumptive_take_water = 'consumptive take water'
    non_consumptive_take_water = 'non-consumptive take water'
    divert_water = 'divert water'
    dam_water = 'dam water'
    use_water = 'use water'
    discharge_water = 'discharge water'


class Station(BaseModel):
    """
    Contains the station data of a dataset.
    """
    station_id: str = Field(..., description='station uuid based on the geometry')
    ref: str = Field(..., description='station reference ID given by owner')
    name: Optional[str]
    osm_id: Optional[int]
    geometry: Geometry
    altitude: Optional[float]
    stream_depletion_ratio: Optional[float]
    # properties: Dict = Field(None, description='Any additional station specific properties.')

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class HydroFeature(str, Enum):
    surface_water = 'surface water'
    groundwater = 'groundwater'


class Activity(BaseModel):
    """

    """
    activity_type: ActivityType
    hydro_feature: HydroFeature
    primary_purpose: Optional[str]
    station: List[Station]
    condition: List[Condition]


class Status(str, Enum):
    expired = 'Expired'
    surrendered = 'Surrendered'
    active = 'Active'
    archived = 'Archived'
    lapsed = 'Lapsed'
    superseded = 'Superseded'
    cancelled = 'Cancelled'
    expired_124 = 'Expired - S.124 Protection'


class PermitType(str, Enum):
    water_permit = 'water permit'


class Permit(BaseModel):
    """

    """
    permit_id: str
    status: Status
    status_changed_date: Optional[date]
    commencement_date: date
    expiry_date: date
    effective_end_date: Optional[date]
    excercised: bool
    permitting_authority: str
    permit_type: PermitType
    activity: Activity
    modified_date: datetime = Field(..., description='The modification date of the last edit.')

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


# class PermitList(BaseModel):
#     """

#     """
#     permit_list: List[Permit]

#     class Config:
#         json_loads = orjson.loads
#         json_dumps = orjson_dumps



# data2 = [d for d in data1['features'] if d['geometry'] is not None]

# data3 = [d for d in data2 if d['properties']['CalcAverageVolume_litres_sec'] is not None]



# class S3ObjectKey(BaseModel):
#     """
#     S3 object key and associated metadata.
#     """
#     key: str
#     bucket: str
#     content_length: int
#     etag: str
#     run_date: datetime

# class StationBase(BaseModel):
#     """
#     Contains the base station data.
#     """
#     station_id: str = Field(..., description='station uuid based on the geometry')
#     ref: str = None
#     name: str = None
#     osm_id: int = None
#     # virtual_station: bool
#     lon: float
#     lat: float
#     altitude: float
#     properties: Dict = Field(None, description='Any additional station specific properties.')


# class Station(BaseModel):
#     """
#     Contains the station data of a dataset.
#     """
#     dataset_id: str = Field(..., description='The unique dataset uuid.')
#     station_id: str = Field(..., description='station uuid based on the geometry')
#     ref: str = None
#     name: str = None
#     osm_id: int = None
#     virtual_station: bool
#     geometry: Geometry
#     altitude: float
#     stats: Stats
#     results_object_key: List[S3ObjectKey]
#     properties: Dict = Field(None, description='Any additional station specific properties.')
#     modified_date: datetime = Field(..., description='The modification date of the last edit.')
