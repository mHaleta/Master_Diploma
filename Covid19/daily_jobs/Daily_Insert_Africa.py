from sqlalchemy import create_engine
from Covid19.utils.insert_countries import append_Country

engine = create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe', max_identifier_length=128)

append_Country(engine, 'ZA', 'ZAF')   # South Africa
append_Country(engine, 'EG', 'EGY')   # Egypt
append_Country(engine, 'NG', 'NGA')   # Nigeria
append_Country(engine, 'GH', 'GHA')   # Ghana
append_Country(engine, 'DZ', 'DZA')   # Algeria
append_Country(engine, 'MA', 'MAR')   # Morocco
append_Country(engine, 'CM', 'CMR')   # Cameroon
append_Country(engine, 'CI', 'CIV')   # Côte d'Ivoire
append_Country(engine, 'SD', 'SDN')   # Sudan
append_Country(engine, 'KE', 'KEN')   # Kenya
append_Country(engine, 'CD', 'COD')   # Democratic Republic of the Congo
append_Country(engine, 'SN', 'SEN')   # Senegal
append_Country(engine, 'ET', 'ETH')   # Ethiopia
append_Country(engine, 'GN', 'GIN')   # Guinea
append_Country(engine, 'GA', 'GAB')   # Gabon
append_Country(engine, 'MR', 'MRT')   # Mauritania
append_Country(engine, 'DJ', 'DJI')   # Djibouti
append_Country(engine, 'CF', 'CAF')   # Central African Republic
append_Country(engine, 'MG', 'MDG')   # Madagascar
append_Country(engine, 'GQ', 'GNQ')   # Equatorial Guinea
append_Country(engine, 'SO', 'SOM')   # Somalia
append_Country(engine, 'YT', 'MYT')   # Mayotte
append_Country(engine, 'ML', 'MLI')   # Mali
append_Country(engine, 'MW', 'MWI')   # Malawi
append_Country(engine, 'ZM', 'ZMB')   # Zambia
append_Country(engine, 'GW', 'GNB')   # Guinea-Bissau
append_Country(engine, 'CV', 'CPV')   # Cabo Verde
append_Country(engine, 'SL', 'SLE')   # Sierra Leone
append_Country(engine, 'LY', 'LBY')   # Libya
append_Country(engine, 'BJ', 'BEN')   # Benin
append_Country(engine, 'SZ', 'SWZ')   # Eswatini
append_Country(engine, 'RW', 'RWA')   # Rwanda
append_Country(engine, 'TN', 'TUN')   # Tunisia
append_Country(engine, 'MZ', 'MOZ')   # Mozambique
append_Country(engine, 'NE', 'NER')   # Niger
append_Country(engine, 'BF', 'BFA')   # Burkina Faso
append_Country(engine, 'UG', 'UGA')   # Uganda
append_Country(engine, 'LR', 'LBR')   # Liberia
append_Country(engine, 'ZW', 'ZWE')   # Zimbabwe
append_Country(engine, 'TD', 'TCD')   # Chad
append_Country(engine, 'NA', 'NAM')   # Namibia
append_Country(engine, 'ST', 'STP')   # Sao Tome and Principe
append_Country(engine, 'TG', 'TGO')   # Togo
append_Country(engine, 'RE', 'REU')   # Réunion
append_Country(engine, 'TZ', 'TZA')   # Tanzania
append_Country(engine, 'AO', 'AGO')   # Angola
append_Country(engine, 'MU', 'MUS')   # Mauritius
append_Country(engine, 'KM', 'COM')   # Comoros
append_Country(engine, 'BW', 'BWA')   # Botswana
append_Country(engine, 'ER', 'ERI')   # Eritrea
append_Country(engine, 'BI', 'BDI')   # Burundi
append_Country(engine, 'LS', 'LSO')   # Lesotho
append_Country(engine, 'SC', 'SYC')   # Seychelles
append_Country(engine, 'GM', 'GMB')   # Gambia
append_Country(engine, 'EH', 'ESH')   # Western Sahara

engine.dispose()