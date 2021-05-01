from sqlalchemy import create_engine
from Covid19.utils.insert_countries import append_Country

engine = create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe', max_identifier_length=128)

append_Country(engine, 'ES', 'ESP')   # Spain
append_Country(engine, 'DE', 'DEU')   # Germany
append_Country(engine, 'DK', 'DNK')   # Denmark
append_Country(engine, 'NO', 'NOR')   # Norway
append_Country(engine, 'UA', 'UKR')   # Ukraine
append_Country(engine, 'RU', 'RUS')   # Russia
append_Country(engine, 'BY', 'BLR')   # Belarus
append_Country(engine, 'PL', 'POL')   # Poland
append_Country(engine, 'HU', 'HUN')   # Hungary
append_Country(engine, 'CZ', 'CZE')   # Czechia
append_Country(engine, 'GB', 'GBR')   # United Kingdom
append_Country(engine, 'IT', 'ITA')   # Italy
append_Country(engine, 'FR', 'FRA')   # France
append_Country(engine, 'SE', 'SWE')   # Sweden
append_Country(engine, 'BE', 'BEL')   # Belgium
append_Country(engine, 'NL', 'NLD')   # Netherlands
append_Country(engine, 'PT', 'PRT')   # Portugal
append_Country(engine, 'CH', 'CHE')   # Switzerland
append_Country(engine, 'RO', 'ROU')   # Romania
append_Country(engine, 'IE', 'IRL')   # Ireland
append_Country(engine, 'AT', 'AUT')   # Austria
append_Country(engine, 'MD', 'MDA')   # Moldova
append_Country(engine, 'RS', 'SRB')   # Serbia
append_Country(engine, 'FI', 'FIN')   # Finland
append_Country(engine, 'MK', 'MKD')   # North Macedonia
append_Country(engine, 'BG', 'BGR')   # Bulgary
append_Country(engine, 'BA', 'BIH')   # Bosnia and Herzegovina
append_Country(engine, 'LU', 'LUX')   # Luxembourg
append_Country(engine, 'GR', 'GRC')   # Greece
append_Country(engine, 'HR', 'HRV')   # Croatia
append_Country(engine, 'AL', 'ALB')   # Albania
append_Country(engine, 'EE', 'EST')   # Estonia
append_Country(engine, 'IS', 'ISL')   # Iseland
append_Country(engine, 'LT', 'LTU')   # Lithuania
append_Country(engine, 'SK', 'SVK')   # Slovakia
append_Country(engine, 'SI', 'SVN')   # Slovenia
append_Country(engine, 'LV', 'LVA')   # Latvia
append_Country(engine, 'AD', 'AND')   # Andorra
append_Country(engine, 'SM', 'SMR')   # San Marino
append_Country(engine, 'MT', 'MLT')   # Malta
append_Country(engine, 'ME', 'MNE')   # Montenegro
append_Country(engine, 'FO', 'FRO')   # Faroe Islands
append_Country(engine, 'IM', 'IMN')   # Isle of Man
append_Country(engine, 'GI', 'GIB')   # Gibraltar
append_Country(engine, 'MC', 'MCO')   # Monaco
append_Country(engine, 'LI', 'LIE')   # Liechtestein
append_Country(engine, 'VA', 'VAT')   # Vatican


engine.dispose()