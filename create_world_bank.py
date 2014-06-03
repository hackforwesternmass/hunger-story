##
## Reshape World Bank World Development Indicators for data analysis
##

import pandas as pd

#grab all indicators from 1990 and on
all = pd.read_excel('data/world_development_indicators_download.xlsx', 'Data', 
    usecols = [0,1,2,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,
        49,50,51,52,53,54,55,56,57])
all = all.rename(columns = {
    'Country Name':'country',
    'Country Code':'country_code',
    'Indicator Name':'indicator',
})

#create dataframe that's a subset of the indicators we want
indicator_list = [
    'Prevalence of undernourishment (% of population)',
    'Crop production index (2004-2006 = 100)',
    'Agricultural land (% of land area)',
    'Food production index (2004-2006 = 100)',
    'Food exports (% of merchandise exports)',
    'Food imports (% of merchandise imports)',
    'Land area (sq. km)',
    'Population (Total)',
    'Unemployment, female (% of female labor force) (modeled ILO estimate)',
    'Unemployment, male (% of male labor force) (modeled ILO estimate)',
    'Unemployment, total (% of total labor force) (modeled ILO estimate)',
    'GDP (constant 2005 US$)',
    'GDP per capita (constant 2005 US$)',
    'Adjusted net national income (constant 2005 US$)',
]
fs = all[all.indicator.isin(indicator_list)]

#remove country names that represent aggregates
#(see "Country" tab of the original indicators downloaded .xlsx for details)
agg_country_code_list = [
    'ARB', 'CSS', 'EAS', 'EAP', 'CEA', 'EMU', 'ECS', 'ECA', 'CEU', 'EUU',
    'HPC', 'HIC', 'NOC', 'OEC', 'LCN', 'LAC', 'CLA', 'LDC', 'LMY', 'LIC',
    'LMC', 'MEA', 'MNA', 'CME', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'SST',
    'SAS', 'CSA', 'SSF', 'SSA', 'CAA', 'UMC', 'WLD'
]
fs = fs[~fs.country_code.isin(agg_country_code_list)]

#reshape to put years in rows instead of columns
fs = pd.melt(fs, id_vars=['country', 'country_code', 'indicator'], var_name = 'year')

#reshape again to put indicators in columns instead of rows & save results
fs = pd.pivot_table(fs, values='value', index=['country', 'country_code', 'year'], columns = ['indicator'])
fs.to_csv('data/world_development_indicators.csv', cols=indicator_list)