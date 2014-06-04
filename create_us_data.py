##
## Create U.S. food security and indicators file for analysis
## Since this is meant to be simple data for practicing visualizations,
## completely ignoring margins of error.
##

import pandas as pd
from decimal import Decimal

def household_snap_rate(row):
    return round(
        Decimal(row['households_snap']) / Decimal(row['households_total']) * 100
        ,2)

#food security numbers from CPS Food Security Supplement (3 year estimates)
fs = pd.read_csv('data/usda_cps_food_security.csv')

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

#merge into one dataframe, the split up by US and states, and save
us = pd.concat([snap,dp],axis=1)
us = us.reset_index()
us['fips'] = us['fips'].map(lambda x: x[-2:])
states = us[us['fips'] <> 'US']
us = us[us['fips'] == 'US']
#states = us.iloc[us.index.get_level_values('geoid') <> '0100000US']
#us = us.iloc[us.index.get_level_values('geoid') == '0100000US']
states.to_csv('data/us_state_indicators.csv')
us.to_csv('data/us_indicators.csv')
