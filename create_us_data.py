##
## Create U.S. food security and indicators file for analysis
## Since this is meant to be simple data for practicing visualizations,
## completely ignoring margins of error.
## Years represent 3-year estimates (e.g., 2011 represents 2009-2011)
##

import pandas as pd, numpy as np
from decimal import Decimal

def get_fips(x):
    if x[-2:] <> 'US':
        return x[-2:]
    else:
        return '00'

def household_snap_rate(row):
    return round(
        Decimal(row['households_snap']) / Decimal(row['households_total']) * 100
        ,2)

#food security numbers from CPS Food Security Supplement (3 year estimates)
fs = pd.read_csv(
    'data/usda_cps_food_security.csv',
    dtype={'fips':np.object}
)

fs.set_index(['fips','year'],inplace=True)

#household SNAP totals from 3-year ACS estimates
acscols = ['GEO.id','HC01_EST_VC01','HC02_EST_VC01']
snap_2008 = pd.read_csv('data/ACS_08_3YR_S2201_with_ann.csv', usecols=acscols)
snap_2008['year'] = 2008
snap_2009 = pd.read_csv('data/ACS_09_3YR_S2201_with_ann.csv', usecols=acscols)
snap_2009['year'] = 2009
snap_2010 = pd.read_csv('data/ACS_10_3YR_S2201_with_ann.csv', usecols=acscols)
snap_2010['year'] = 2010
snap_2011 = pd.read_csv('data/ACS_11_3YR_S2201_with_ann.csv', usecols=acscols)
snap_2011['year'] = 2011
snap_2012 = pd.read_csv('data/ACS_12_3YR_S2201_with_ann.csv', usecols=acscols)
snap_2012['year'] = 2012
snap = pd.concat([snap_2008, snap_2009, snap_2010, snap_2011, snap_2012])
snap.columns = ['fips', 'households_total', 'households_snap', 'year']
snap = snap[snap.fips != 'Id']
snap['household_snap_rate'] = snap.apply(lambda row: household_snap_rate(row), axis=1)
snap.set_index(['fips','year'],inplace=True)

#selected economic profiles from 3-year ACS estimates
dpcols = ['fips', 'unemployment_rate', 'poverty_rate', 'year']
dp_2008 = pd.read_csv('data/ACS_08_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC01_EST_VC10', 'HC01_EST_VC103'])
dp_2008['year'] = 2008
dp_2008.columns = dpcols
dp_2009 = pd.read_csv('data/ACS_09_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC01_EST_VC10', 'HC01_EST_VC111'])
dp_2009['year'] = 2009
dp_2009.columns = dpcols
dp_2010 = pd.read_csv('data/ACS_10_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC03_VC13', 'HC03_VC156'])
dp_2010['year'] = 2010
dp_2010.columns = dpcols
dp_2011 = pd.read_csv('data/ACS_11_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC03_VC13', 'HC03_VC156'])
dp_2011['year'] = 2011
dp_2011.columns = dpcols
dp_2012 = pd.read_csv('data/ACS_12_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC03_VC13', 'HC03_VC156'])
dp_2012['year'] = 2012
dp_2012.columns = dpcols
dp = pd.concat([dp_2008, dp_2009, dp_2010, dp_2011, dp_2012])
dp = dp[dp.fips != 'Id']
dp.set_index(['fips','year'],inplace=True)

#merge into one dataframe, the split up by US and states
#(setting & resetting the multi-index = more convenient concat/subset syntax)
us = pd.concat([snap,dp],axis=1)
us = us.reset_index()
us['fips'] = us['fips'].apply(lambda x: get_fips(x))
us.set_index(['fips','year'],inplace=True)
us = pd.concat([us, fs], axis=1)
us = us.reset_index()
states = us[us['fips'] <> '00']
us = us[us['fips'] == '00']

#save US and state files (selected columns)
collist = [
    'state_name', 'year', 'food_insecure_percent',
    'food_insecure_low_percent', 'household_snap_rate',
    'unemployment_rate', 'poverty_rate', 'state_abbr', 'fips'
]
states.to_csv('data/us_state_indicators.csv', cols=collist, index=False)
us.to_csv('data/us_indicators.csv', cols=collist, index=False)
