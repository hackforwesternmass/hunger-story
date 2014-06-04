##
## Create U.S. food security and indicators file for analysis
##

import pandas as pd

#food security numbers from CPS Food Security Supplement (3 year estimates)
fs = pd.read_csv('data/usda_cps_food_security.csv')

#household SNAP totals from 3-year ACS estimates
snap_2008 = pd.read_csv('data/ACS_08_3YR_S2201_with_ann.csv', usecols=['GEO.id','HC01_EST_VC01','HC02_EST_VC01'])
snap_2008['year'] = 2008
snap_2009 = pd.read_csv('data/ACS_09_3YR_S2201_with_ann.csv', usecols=['GEO.id','HC01_EST_VC01','HC02_EST_VC01'])
snap_2009['year'] = 2009
snap_2010 = pd.read_csv('data/ACS_10_3YR_S2201_with_ann.csv', usecols=['GEO.id','HC01_EST_VC01','HC02_EST_VC01'])
snap_2010['year'] = 2010
snap_2011 = pd.read_csv('data/ACS_11_3YR_S2201_with_ann.csv', usecols=['GEO.id','HC01_EST_VC01','HC02_EST_VC01'])
snap_2011['year'] = 2011
snap_2012 = pd.read_csv('data/ACS_12_3YR_S2201_with_ann.csv', usecols=['GEO.id','HC01_EST_VC01','HC02_EST_VC01'])
snap_2012['year'] = 2012
snap = pd.concat([snap_2008, snap_2009, snap_2010, snap_2011, snap_2012])
snap.columns = ['geoid', 'households_total', 'households_snap', 'year']
snap = snap[snap.geoid != 'Id']

#selected economic profiles from 3-year ACS estimates
dp_2008 = pd.read_csv('data/ACS_08_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC01_EST_VC10', 'HC01_EST_VC103'])
dp_2008['year'] = 2008
dp_2008.columns = ['geoid', 'unemployment_rate', 'poverty_rate', 'year']
dp_2009 = pd.read_csv('data/ACS_09_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC01_EST_VC10', 'HC01_EST_VC111'])
dp_2009['year'] = 2009
dp_2009.columns = ['geoid', 'unemployment_rate', 'poverty_rate', 'year']
dp_2010 = pd.read_csv('data/ACS_10_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC03_VC13', 'HC03_VC156'])
dp_2010['year'] = 2010
dp_2010.columns = ['geoid', 'unemployment_rate', 'poverty_rate', 'year']
dp_2011 = pd.read_csv('data/ACS_11_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC03_VC13', 'HC03_VC156'])
dp_2011['year'] = 2011
dp_2011.columns = ['geoid', 'unemployment_rate', 'poverty_rate', 'year']
dp_2012 = pd.read_csv('data/ACS_12_3YR_DP03_with_ann.csv', usecols=['GEO.id', 'HC03_VC13', 'HC03_VC156'])
dp_2012['year'] = 2012
dp_2012.columns = ['geoid', 'unemployment_rate', 'poverty_rate', 'year']
dp = pd.concat([dp_2008, dp_2009, dp_2010, dp_2011, dp_2012])
dp = dp[dp.geoid != 'Id']

#merge everything together


