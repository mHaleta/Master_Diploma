def append_Country(engine, iso2, iso3):
    from json import loads
    from requests import get
    from datetime import datetime, timedelta, timezone
    from Covid19.utils.dbqueries import DBQueries
    
    coronatracker_api = 'http://api.coronatracker.com/v3/stats/worldometer/country'
    #thevirustracker_api = 'https://api.thevirustracker.com/free-api'
    
    try:
        country = loads(get(coronatracker_api, params={'countryCode':f'{iso2}'}).content)[0]
        #country = loads(get(thevirustracker_api, params={'countryTotal':f'{iso2}'}).content)
    except Exception:
        vd = {"Country_Code": iso3, "Error": "Проблема подключения к API"}
        query = DBQueries().insert_table(engine, "Errors", vd)
        engine.execute(query)
        return
    
    try:
        cases = country['totalConfirmed']
        new_cases = country['dailyConfirmed']
        deaths = country['totalDeaths']
        new_deaths = country['dailyDeaths']
        
        #cases = country['countrydata'][0]['total_cases']
        #new_cases = country['countrydata'][0]['total_new_cases_today']
        #deaths = country['countrydata'][0]['total_deaths']
        #new_deaths = country['countrydata'][0]['total_new_deaths_today']
    except Exception:
        vd = {"Country_Code": iso3, "Error": "API скорее всего возвращает null"}
        query = DBQueries().insert_table(engine, "Errors", vd)
        engine.execute(query)
        return
    
    dt = datetime.now(tz=timezone(timedelta(hours=-1))).strftime('%d.%m.%Y')
    
    try:
        vd = {"ISO3_Code":iso3, "Date":dt, "Total_Cases":cases, "New_Cases":new_cases, "Total_Deaths":deaths, "New_Deaths":new_deaths}
        query = DBQueries().insert_table(engine, "Covid19_data", vd)
        engine.execute(query)
    except Exception:
        try:
            condition = {'and': [("ISO3_Code", "=", iso3), ("Date", "=", dt)]}
            vd = {"Total_Cases":cases, "New_Cases":new_cases, "Total_Deaths":deaths, "New_Deaths":new_deaths}
            query = DBQueries().update_table(engine, "Covid19_data", vd, condition)
            engine.execute(query)
        except Exception as e:
            e = str(e).replace("'", "''")
            vd = {"Country_Code":iso3, "Error":e}
            query = DBQueries().insert_table(engine, "Errors", vd)
            engine.execute(query)
    
    return


def append_Country_Worldometer(engine, iso3):
    from pandas import read_sql
    from requests import Session
    from lxml.html import fromstring
    from datetime import datetime, timedelta, timezone
    from Covid19.utils.dbqueries import DBQueries
        
    query = DBQueries().select_table(engine, "Worldometer", False, ["Link"], ("Code", "=", iso3))
    
    try:
        link = read_sql(query, engine).values[0][0]
    except Exception:
        vd = {"Country_Code":iso3, "Error":"Error while reading from sql"}
        query = DBQueries().insert_table(engine, "Errors", vd)
        engine.execute(query)
        return
    
    try:
        session = Session()
        session.verify = False
        page = fromstring(session.get(link).text)
        
        today_cases = page.xpath('//*[@id="maincounter-wrap"]/div/span')[0].text.strip().replace(',','')
        today_deaths = page.xpath('//*[@id="maincounter-wrap"]/div/span')[1].text.strip().replace(',','')
    except Exception as e:
        e = str(e).replace("'", "''")
        vd = {"Country_Code":iso3, "Error":e}
        query = DBQueries().insert_table(engine, "Errors", vd)
        engine.execute(query)
        return
    
    try:
        dt = datetime.now(tz=timezone(-timedelta(hours=1))).strftime('%d.%m.%Y')
        dt_prev = (datetime.now(tz=timezone(-timedelta(hours=1)))-timedelta(days=1)).strftime('%d.%m.%Y')
    except Exception:
        vd = {"Country_Code":iso3, "Error":"Error when calculate dates"}
        query = DBQueries().insert_table(engine, "Errors", vd)
        engine.execute(query)
        return
    
    prev = DBQueries().select_table(engine, "Covid19_data", False, ["Total_Cases", "Total_Deaths"], {'and':[("ISO3_Code","=",iso3),("Date","=",dt_prev)]})
    prev_cases, prev_deaths = read_sql(prev, engine).values[0].reshape(-1)
    
    try:
        vd = {"ISO3_Code":iso3, "Date":dt, "Total_Cases":int(today_cases), "New_Cases":int(today_cases)-int(prev_cases), "Total_Deaths":int(today_deaths), "New_Deaths":int(today_deaths)-int(prev_deaths)}
        query = DBQueries().insert_table(engine, "Covid19_data", vd)
        engine.execute(query)
    except Exception:
        try:
            vd = {"Total_Cases":int(today_cases), "New_Cases":int(today_cases)-int(prev_cases), "Total_Deaths":int(today_deaths), "New_Deaths":int(today_deaths)-int(prev_deaths)}
            condition = {'and':[("ISO3_Code","=",iso3),("Date","=",dt)]}
            query = DBQueries().update_table(engine, "Covid19_data", vd, condition)
            engine.execute(query)
        except Exception as e:
            e = str(e).replace("'", "''")
            vd = {"Country_Code":iso3, "Error":e}
            query = DBQueries().insert_table(engine, "Errors", vd)
            engine.execute(query)
    
    return