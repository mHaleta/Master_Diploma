import numpy as np
import pandas as pd
import sqlalchemy as sa
import pycountry as pc
import pycountry_convert as pcc

iso2, iso3, common_name, name, official_name, continent = [], [], [], [], [], []
for country in list(pc.countries):
    iso2.append([country.alpha_2])
    iso3.append([country.alpha_3])
    try:
        continent.append([pcc.convert_continent_code_to_continent_name(pcc.country_alpha2_to_continent_code(country.alpha_2))])
    except Exception:
        continent.append([pd.NA])
    try:
        common_name.append([country.common_name])
    except Exception:
        common_name.append([pd.NA])
    try:
        name.append([country.name])
    except Exception:
        name.append([pd.NA])
    try:
        official_name.append([country.official_name])
    except Exception:
        official_name.append([pd.NA])

df = pd.DataFrame(data=np.concatenate((iso2, iso3, continent, name, common_name, official_name), axis=1),
                  columns=['ISO2_Code', 'ISO3_Code', 'Continent', 'Country', 'Common_Name', 'Official_Name'])

engine = sa.create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe',
                          max_identifier_length=128)

dtypes = {
    "ISO2_Code": sa.types.VARCHAR(2),
    "ISO3_Code": sa.types.VARCHAR(3),
    "Continent": sa.types.VARCHAR(15),
    "Country": sa.types.NVARCHAR(80),
    "Common_Name": sa.types.NVARCHAR(80),
    "Official_Name": sa.types.NVARCHAR(80)
}

df.to_sql("Countries", engine, if_exists='replace', index=False, dtype=dtypes)

engine.dispose()