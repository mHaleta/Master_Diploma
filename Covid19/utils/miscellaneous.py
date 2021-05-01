def wikipedia_parse(country):
    from selenium import webdriver
    from numpy import datetime64
    
    driver = webdriver.Chrome()
    driver.get(f"https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data/{country}_medical_cases_chart")
    
    occurences = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div/div[2]/div/table/tbody/tr')
    
    buttons = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div/div[2]/div/table/tbody/tr[1]/th/div/p/span')
    for i in range(0, len(buttons)-2, 2):
        buttons[i].click()
    buttons[-1].click()
    
    date = []
    total_cases = []
    total_deaths = []
    for i in range(3, len(occurences)):
        d = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/div[2]/div/table/tbody/tr[{i}]/td[1]').text
        if d != u'\u22ee':
            date.append(datetime64(d, 'D'))
        else:
            continue
        c = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/div[2]/div/table/tbody/tr[{i}]/td[3]').text
        j = c.find('(')
        if j != -1:
            total_cases.append(int(c[:j].replace(',', '')))
        else:
            total_cases.append(int(c.replace(',', '')))
        dt = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/div[2]/div/table/tbody/tr[{i}]/td[4]').text
        if dt != '':
            j = dt.find('(')
            if j != -1:
                total_deaths.append(int(dt[:j].replace(',', '')))
            else:
                total_deaths.append(int(dt.replace(',', '')))
        else:
            total_deaths.append(0)
    
    driver.close()
    
    return date, total_cases, total_deaths


def get_population_density():
    from selenium import webdriver
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-images')
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_density")
    
    occurences = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr/td[@align="center"]')
    
    features = []
    for idx in range(len(occurences)):
        try:
            country = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/table[1]/tbody/tr[{idx+1}]/td[2]/i/a').text
        except Exception:
            try:
                country = driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/table[1]/tbody/tr[{idx+1}]/td[2]/a').text
            except Exception:
                continue
        area = float(driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/table[1]/tbody/tr[{idx+1}]/td[3]').text.replace(',', ''))
        population = int(driver.find_element_by_xpath(f'//*[@id="mw-content-text"]/div/table[1]/tbody/tr[{idx+1}]/td[5]').text.replace(',', ''))
        
        features.append([country, area, population])
    
    driver.close()
    
    return features


def get_totals_from_worldometer(link):
    from requests import get
    from numpy import where, array
    from lxml.html import fromstring

    page = get(f'{link}').text
    page_html = fromstring(page)

    today_total_cases = page_html.xpath('//*[@id="maincounter-wrap"]/div/span')[0].text.strip().replace(',','')

    start = page[page.find("text: 'Total Coronavirus Cases'"):].find('data')+ \
        page.find("text: 'Total Coronavirus Cases'")+7
    end = page[start:].find(']')+start
    cases = array(page[start:end].split(',')+[today_total_cases], dtype=int)
    cases = cases[where(cases != 0)[0]]

    if page.find("text: 'Total Coronavirus Deaths'") != -1:
        today_total_deaths = page_html.xpath('//*[@id="maincounter-wrap"]/div/span')[1].text.strip().replace(',','')
        start = page[page.find("text: 'Total Coronavirus Deaths'"):].find('data')+ \
            page.find("text: 'Total Coronavirus Deaths'")+7
        end = page[start:].find(']')+start
        deaths = array(page[start:end].split(',')+[today_total_deaths], dtype=int)
        deaths = deaths[len(deaths)-len(cases):]
    else:
        deaths = array(len(cases)*[0])

    return cases, deaths


def outliers_filter(x):
    from numpy import quantile
    
    Q1, Q3 = quantile(x, [0.25, 0.75])
    IQR = Q3 - Q1
    
    filtr = (x <= 0)|(x < Q1-1.5*IQR)|(x > Q3+1.5*IQR)
    
    return filtr


def datediff(date1, date2):
    res = {}
    res['years'] = date2.year - date2.year
    res['months'] = res['years']*12 + (date2.month - date1.month)
    res['days'] = (date2-date1).days
    try:
        res['hours'] = res['days']*24 + (date2.hour - date1.hour)
        res['minutes'] = res['hours']*60 + (date2.minute - date1.minute)
        res['seconds'] = res['minutes']*60 + (date2.second - date1.second)
    except Exception:
        pass
    
    return res


def round_to_significant_digits(x, sigdigits):
    from numpy import log10, round as round_, integer, isreal, sign, frexp, floor
    
    logBase10of2 = log10(2)
    
    if not (type(sigdigits) is int or isinstance(sigdigits, integer)):
        raise TypeError( "round_to_significant_digits: sigdigits must be an integer." )

    if sigdigits <= 0:
        raise ValueError( "round_to_significant_digits: sigdigits must be positive." )

    if not isreal(x):
        raise TypeError( "round_to_significant_digits: x must be real." )

    xsgn = sign(x)
    absx = xsgn * x
    mantissa, binaryExponent = frexp(absx)

    decimalExponent = logBase10of2 * binaryExponent
    omag = floor(decimalExponent)

    mantissa *= 10.0**(decimalExponent - omag)

    if mantissa < 1.0:
        mantissa *= 10.0
        omag -= 1.0

    return xsgn * round_(mantissa, decimals=sigdigits-1) * 10.0**omag


def restore_data_for_saved_model(engine, iso3, date_from, date_to):
    from Covid19.utils.dbqueries import DBQueries
    from pandas import read_sql
    
    cond = {'and':[("ISO3_Code","=",iso3),("Date", "between",[(date_from-1).item(), date_to.item()])]}
    query = DBQueries().select_table(engine, "Covid19_data_view", condition=cond, order=['Date'])
    df = read_sql(query, engine)
    
    cases = df.Total_Cases.values.reshape(-1)
    days = df.Day_count.values.reshape(-1)[1:]
    beta = (cases[1:]-cases[:-1])/cases[:-1]
    dates = df.Date.values.reshape(-1).astype('datetime64[D]')[1:]
    
    country = df.Country.unique()[0]
    
    return country, days, beta, dates


def make_function(coeffs, strategy):
    if strategy == 'linear':
        return lambda t: coeffs[0]+coeffs[1]*t
    elif strategy == 'exponential':
        from numpy import exp
        return lambda t: coeffs[0]*exp(coeffs[1]*t)
    elif strategy == 'polynomial':
        from numpy import sum as sum_, power, vstack, arange
        return lambda t: sum_(power(vstack(t), arange(len(coeffs))) @ vstack(coeffs), axis=1)
    