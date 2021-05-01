from sqlalchemy import create_engine
from Covid19.utils.insert_countries import append_Country

engine = create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe', max_identifier_length=128)

append_Country(engine, 'IN', 'IND')   # India
append_Country(engine, 'IR', 'IRN')   # Iran
append_Country(engine, 'PK', 'PAK')   # Pakistan
append_Country(engine, 'SA', 'SAU')   # Saudi Arabia
append_Country(engine, 'TR', 'TUR')   # Turkey
append_Country(engine, 'BD', 'BGD')   # Bangladesh
append_Country(engine, 'QA', 'QAT')   # Qatar
append_Country(engine, 'CN', 'CHN')   # China
append_Country(engine, 'IQ', 'IRQ')   # Iraq
append_Country(engine, 'ID', 'IDN')   # Indonesia
append_Country(engine, 'KZ', 'KAZ')   # Kazakhstan
append_Country(engine, 'OM', 'OMN')   # Oman
append_Country(engine, 'PH', 'PHL')   # Philippines
append_Country(engine, 'KW', 'KWT')   # Kuwait
append_Country(engine, 'AE', 'ARE')   # United Arab Emirates
append_Country(engine, 'SG', 'SGP')   # Singapore
append_Country(engine, 'IL', 'ISR')   # Israel
append_Country(engine, 'AF', 'AFG')   # Afghanistan
append_Country(engine, 'BH', 'BHR')   # Bahrain
append_Country(engine, 'AM', 'ARM')   # Armenia
append_Country(engine, 'AZ', 'AZE')   # Azerbaijan
append_Country(engine, 'JP', 'JPN')   # Japan
append_Country(engine, 'NP', 'NPL')   # Nepal
append_Country(engine, 'KR', 'KOR')   # South Korea
append_Country(engine, 'UZ', 'UZB')   # Uzbekistan
append_Country(engine, 'KG', 'KGZ')   # Kyrgyzstan
append_Country(engine, 'MY', 'MYS')   # Malaysia
append_Country(engine, 'TJ', 'TJK')   # Tajikistan
append_Country(engine, 'PS', 'PSE')   # Palestine
append_Country(engine, 'TH', 'THA')   # Thailand
append_Country(engine, 'MV', 'MDV')   # Maldives
append_Country(engine, 'LK', 'LKA')   # Sri Lanka
append_Country(engine, 'LB', 'LBN')   # Lebanon
append_Country(engine, 'HK', 'HKG')   # Hong Kong
append_Country(engine, 'YE', 'YEM')   # Yemen
append_Country(engine, 'JO', 'JOR')   # Jordan
append_Country(engine, 'CY', 'CYP')   # Cyprus
append_Country(engine, 'GE', 'GEO')   # Georgia
append_Country(engine, 'TW', 'TWN')   # Taiwan
append_Country(engine, 'SY', 'SYR')   # Syria
append_Country(engine, 'VN', 'VNM')   # Viet Nam
append_Country(engine, 'MM', 'MMR')   # Myanmar
append_Country(engine, 'MN', 'MNG')   # Mongolia
append_Country(engine, 'KH', 'KHM')   # Cambodia
append_Country(engine, 'BN', 'BRN')   # Brunei
append_Country(engine, 'BT', 'BTN')   # Bhutan
append_Country(engine, 'MO', 'MAC')   # Macao
append_Country(engine, 'TL', 'TLS')   # Timor-Leste
append_Country(engine, 'LA', 'LAO')   # Laos

engine.dispose()