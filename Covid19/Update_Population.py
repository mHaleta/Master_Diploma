import numpy as np
import pandas as pd
import sqlalchemy as sa
from utils.miscellaneous import get_population_density
import pycountry_convert as pcc

df = pd.DataFrame(data=get_population_density(), columns=['Country', 'Area', 'Population'])

engine = sa.create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe',
                          max_identifier_length=128)

query = """
    select
        "ISO2_Code",
        "Country",
        "Common_Name"
    from
        "Countries"
"""
countries = pd.read_sql_query(query, engine)

engine.dispose()

df.loc[df.Country == 'Pitcairn Islands', 'Country'] = 'Pitcairn'
df.loc[df.Country == 'Eswatini (Swaziland)', 'Country'] = 'Eswatini'
df.loc[df.Country == 'Sint Maarten', 'Country'] = 'Sint Maarten (Dutch part)'
df.loc[df.Country == 'Vatican City', 'Country'] = 'Holy See (Vatican City State)'
df.loc[df.Country == 'Wallis & Futuna', 'Country'] = 'Wallis and Futuna'
df = df[df.Country != 'Antarctica']

codes = []
for country in df.Country.values:
    try:
        codes.append(pcc.country_name_to_country_alpha2(country, cn_name_format='default'))
    except Exception:
        codes.append(pd.NA)

df['ISO2_Code'] = codes

frame = countries.join(df.set_index('ISO2_Code').drop(columns=['Country']), on='ISO2_Code', how='left')

dtypes = {
    'ISO2_Code': sa.types.VARCHAR(2),
    'Population': sa.types.Numeric(10,0),
    'Density': sa.types.Numeric(8,2)
}

frame.drop(columns=['Country', 'Common_Name'], inplace=True)

frame = frame.groupby('ISO2_Code', as_index=False).agg({'Area':'sum','Population':'sum'})
frame.loc[frame.Area == 0, ['Area', 'Population']] = np.nan

frame['Density'] = np.round(frame['Population']/frame['Area'], 2)

frame.drop(columns=['Area'], inplace=True)

frame.to_sql('Population', engine, index=False, if_exists='replace', dtype=dtypes)

engine.dispose()