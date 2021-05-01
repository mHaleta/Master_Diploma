from sqlalchemy import create_engine
from Covid19.utils.insert_countries import append_Country, append_Country_Worldometer

engine = create_engine('oracle://"MHaleta":trankvilisator@localhost:1521/xe', max_identifier_length=128)

append_Country(engine, 'BO', 'BOL')    # Bolivia
append_Country(engine, 'BR', 'BRA')    # Brazil
append_Country(engine, 'PE', 'PER')    # Peru
append_Country(engine, 'CL', 'CHL')    # Chile
append_Country(engine, 'CO', 'COL')    # Colombia
append_Country(engine, 'AR', 'ARG')    # Argentina
append_Country(engine, 'EC', 'ECU')    # Ecuador
append_Country(engine, 'VE', 'VEN')    # Venezuela
append_Country(engine, 'GF', 'GUF')    # French Guiana
append_Country(engine, 'PY', 'PRY')    # Paraguay
append_Country(engine, 'UY', 'URY')    # Uruguay
append_Country(engine, 'SR', 'SUR')    # Suriname
append_Country(engine, 'GY', 'GUY')    # Guyana

append_Country(engine, 'AU', 'AUS')    # Australia
append_Country(engine, 'NZ', 'NZL')    # New Zealand
append_Country(engine, 'PF', 'PYF')    # French Polynesia
append_Country(engine, 'FJ', 'FJI')    # Fiji
append_Country(engine, 'NC', 'NCL')    # New Caledonia
append_Country(engine, 'PG', 'PNG')    # Papua New Guinea

append_Country_Worldometer(engine, 'COG')    # Congo
append_Country_Worldometer(engine, 'SSD')    # South Sudan
append_Country_Worldometer(engine, 'FLK')    # Falkland Islands
append_Country_Worldometer(engine, 'SPM')    # Saint Pierre and Miquelon
append_Country_Worldometer(engine, 'SXM')    # Sint Maarten
append_Country_Worldometer(engine, 'BES')    # Bonaire

engine.dispose()