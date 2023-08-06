#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:43:15 2021

@author: mike
"""
import numpy as np
import pandas as pd
import requests
import orjson
import copy
from gistools import data_io
from nzpermits.data_models import Permit, Station
from nzpermits.utils import assign_station_id, create_geometry

##########################################
### Functions for processing IRIS data

## Environemnt Southland


def process_es_permits(stream_depletion_csv):
    """

    """
    ### Parameters
    base_url = 'https://maps.es.govt.nz/server/rest/services/Public/Consents/MapServer/'

    layer_id = 22

    ### Extract raw data
    data1 = data_io.query_esri_mapserver(base_url, layer_id)

    ### Load in the stream depletion csv
    sd_df = pd.read_csv(stream_depletion_csv)
    sd_df['ref'] = sd_df['ref'].str.strip()
    sd_df = sd_df[['ref', 'sd_ratio']].drop_duplicates('ref')
    sd_df = sd_df[sd_df['sd_ratio'] > 0].copy()

    ### Process data
    run_date = pd.Timestamp.now(tz='utc').round('s').tz_localize(None)

    data2 = {}
    bad_data = []

    for d in data1['features']:

        ## Make sure the minium amount of data exists, else continue to next
        if d['geometry'] is None:
            bad_data.extend([d])
            continue
        prop = d['properties']
        if (not isinstance(prop['AbstractionSiteNo'], str)) or (not isinstance(prop['CurrentStatus'], str)) or (not isinstance(prop['CommencementDate'], int)) or (not isinstance(prop['ExpiryDate'], int)) or (not isinstance(prop['ActivitySubType'], str)) or (not isinstance(prop['IRISID'], str)):
            bad_data.extend([d])
            continue

        permit_id = prop['IRISID']

        ## Create updated geometry
        geo1 = create_geometry(d['geometry']['coordinates'])
        stn_id = assign_station_id(geo1)

        ## get stream depletion ratio
        ref = prop['AbstractionSiteNo'].strip()

        sd_ratio1 = sd_df[sd_df['ref'] == ref]

        if sd_ratio1.empty:
            sd_ratio = None
        else:
            sd_ratio = float(sd_ratio1.iloc[0]['sd_ratio'])

        ## Assign station data
        if permit_id in data2:
            old_permit = data2[permit_id]
            station = old_permit['activity']['station']
            check1 = [s for s in station if ref == s['ref']]
            if len(check1) > 0:
                continue
            else:
                new_station = orjson.loads(Station(**{'station_id': stn_id, 'ref': ref, 'geometry': geo1, 'stream_depletion_ratio': sd_ratio}).json(exclude_none=True))
                station.extend([new_station])
                data2[permit_id]['activity'].update({'station': station})

            continue
        else:
            station = [{'station_id': stn_id, 'ref': ref, 'geometry': geo1, 'stream_depletion_ratio': sd_ratio}]

        ## Calc liters/sec
        l_s = prop['MaxAuthVolume_litres_sec']

        if not isinstance(l_s, (int, float)):
            if isinstance(prop['CalcAverageVolume_litres_sec'], (int, float)):
                l_s = prop['CalcAverageVolume_litres_sec']
            else:
                if isinstance(prop['Volume_m3_day'], (int, float)):
                    l_s = prop['Volume_m3_day']/24/60/60*1000
                else:
                    if isinstance(prop['Volume_m3_day'], (int, float)):
                        l_s = prop['MaximumVolume_m3_day']/24/60/60*1000
                    else:
                        bad_data.extend([d])
                        continue

        l_s = round(l_s)

        ## Process activity and hydro_feature
        act0 = prop['ActivitySubType'].lower().split('water ')
        act1 = act0[1].split(' ')

        if act1[0] == 'take':
            cons1 = act1[1]
            if cons1 == '(consumptive)':
                act2 = 'consumptive take water'
            else:
                'non-consumptive take water'
        else:
            act2 = act1[0]

        hydro_feature = act0[0] + 'water'

        ## Assign conditions
        condition = [{'condition_type': 'abstraction limit', 'limit': [{'value': l_s, 'period': 'S', 'units': 'l', 'limit_boundary': 'max'}]}]

        ## Assign the Activity
        activity = {'activity_type': act2, 'hydro_feature': hydro_feature, 'primary_purpose': prop['PrimaryIndustry'], 'station': station, 'condition': condition}

        ## Assign base permit data
        permit = {'permit_id': permit_id,
                  'permitting_authority': 'Environment Southland',
                  'permit_type': 'water permit',
                  'activity': activity,
                  'modified_date': run_date}

        ## Assign status
        status = prop['CurrentStatus']
        if (status == 'Current') or (status == 'Current (Database)'):
            status = 'Active'

        permit.update({'status': status})

        ## Assign dates
        if isinstance(prop['CommencementDate'], int):
            permit.update({'commencement_date': pd.Timestamp(prop['CommencementDate'], unit='ms').ceil('D')})
        if isinstance(prop['CurrentStatusFromDate'], int):
            permit.update({'status_changed_date': pd.Timestamp(prop['CurrentStatusFromDate'], unit='ms').ceil('D')})
        if isinstance(prop['ExpiryDate'], int):
            permit.update({'expiry_date': pd.Timestamp(prop['ExpiryDate'], unit='ms').ceil('D')})
        if isinstance(prop['AuthEffectiveEndDate'], int):
            permit.update({'effective_end_date': pd.Timestamp(prop['AuthEffectiveEndDate'], unit='ms').ceil('D')})

        ## Assign excercised
        if isinstance(prop['AuthorisationExercised'], str):
            excer = prop['AuthorisationExercised'].lower().strip()
            if excer == 'no':
                permit.update({'excercised': False})
            else:
                permit.update({'excercised': True})
        else:
            permit.update({'excercised': True})

        ### Make the permit object
        permit1 = Permit(**permit)
        permit2 = orjson.loads(permit1.json(exclude_none=True))

        data2[permit_id] = permit2

    data3 = list(data2.values())

    return data3
