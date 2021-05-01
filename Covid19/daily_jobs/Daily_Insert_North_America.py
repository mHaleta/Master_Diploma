from sqlalchemy import create_engine
from Covid19.utils.insert_countries import append_Country

engine = create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe', max_identifier_length=128)

append_Country(engine, 'US', 'USA')   # United States
append_Country(engine, 'MX', 'MEX')   # Mexico
append_Country(engine, 'CA', 'CAN')   # Canada
append_Country(engine, 'PA', 'PAN')   # Panama
append_Country(engine, 'DO', 'DOM')   # Dominican Republic
append_Country(engine, 'GT', 'GTM')   # Guatemala
append_Country(engine, 'HN', 'HND')   # Honduras
append_Country(engine, 'SV', 'SLV')   # El Salvador
append_Country(engine, 'CR', 'CRI')   # Costa Rica
append_Country(engine, 'HT', 'HTI')   # Haiti
append_Country(engine, 'NI', 'NIC')   # Nicaragua
append_Country(engine, 'CU', 'CUB')   # Cuba
append_Country(engine, 'JM', 'JAM')   # Jamaica
append_Country(engine, 'MQ', 'MTQ')   # Martinique
append_Country(engine, 'KY', 'CYM')   # Cayman Islands
append_Country(engine, 'GP', 'GLP')   # Guadeloupe
append_Country(engine, 'BM', 'BMU')   # Bermuda
append_Country(engine, 'TT', 'TTO')   # Trinidad and Tobago
append_Country(engine, 'BS', 'BHS')   # Bahamas
append_Country(engine, 'AW', 'ABW')   # Aruba
append_Country(engine, 'BB', 'BRB')   # Barbados
append_Country(engine, 'AG', 'ATG')   # Antigua and Barbuda
append_Country(engine, 'TC', 'TCA')   # Turks and Caicos Islands
append_Country(engine, 'MF', 'MAF')   # Saint Martin (French part)
append_Country(engine, 'BZ', 'BLZ')   # Belize
append_Country(engine, 'VC', 'VCT')   # Saint Vincent and the Grenadines
append_Country(engine, 'CW', 'CUW')   # Curaçao
append_Country(engine, 'GD', 'GRD')   # Grenada
append_Country(engine, 'LC', 'LCA')   # Saint Lucia
append_Country(engine, 'DM', 'DMA')   # Dominica
append_Country(engine, 'KN', 'KNA')   # Saint Kitts and Nevis
append_Country(engine, 'GL', 'GRL')   # Greenland
append_Country(engine, 'MS', 'MSR')   # Montserrat
append_Country(engine, 'VG', 'VGB')   # Virgin Islands, British
append_Country(engine, 'BL', 'BLM')   # Saint Barthélemy
append_Country(engine, 'AI', 'AIA')   # Anguilla

engine.dispose()