from accessify import private

class CountriesDiscrepancies:
    def __init__(self):
        self.df_new = None
        self.df_old = None
        self.discrepancies = None
    
    def find_discrepancies(self, engine, countries=None):
        from numpy import sort, datetime64
        from pandas import read_sql, DataFrame
        from Covid19.utils.dbqueries import DBQueries
        
        if countries is None:
            codes = DBQueries().select_countries_with_discrepancies(engine)
        elif countries == '*':
            query = DBQueries().select_table(engine, "Covid19_data", True, ['ISO3_Code'], order=["ISO3_Code"])
            codes = read_sql(query, engine).ISO3_Code.values.reshape(-1)
        else:
            codes = sort(countries)
        
        if len(codes) != 0:
            query = DBQueries().select_table(engine, "Worldometer", condition=("Code","in",codes), order=['Code'])
            links = read_sql(query, engine).Link.values.reshape(-1)
            
            query = DBQueries().select_table(engine, "Covid19_data", condition={'and':[("ISO3_Code","in",codes),("Date",">=","22.01.2020")]}, order=["ISO3_Code", "Date"])
            self.df_old = read_sql(query, engine)
            
            dtype = self.df_old.dtypes.to_dict()
            dtype.pop('table_id')
            self.df_new = self.get_new_values(codes, links).astype(dtype)
            for iso3 in codes:
                min_date_new = datetime64(self.df_new[self.df_new.ISO3_Code == iso3].Date.values.min(), 'D')
                if min_date_new == datetime64('2020-02-15', 'D') if iso3 != 'CHN' else datetime64('2020-01-22', 'D'):
                    min_date_old = datetime64(self.df_old[(self.df_old.ISO3_Code == iso3)&((self.df_old.Date >= '2020-02-15')|(self.df_old[self.df_old.ISO3_Code == 'CHN'].Date >= '2020-01-22'))].Date.values.min(), 'D')
                
                    self.df_new.loc[(self.df_new.ISO3_Code == iso3)&(self.df_new.Date == min_date_new), ['New_Cases', 'New_Deaths']] = self.df_old.loc[(self.df_old.ISO3_Code == iso3)&(self.df_old.Date == min_date_old), ['New_Cases', 'New_Deaths']].values
            
            self.df_new = self.df_new.merge(self.df_old[["table_id", "ISO3_Code", "Date"]], how="inner", on=["ISO3_Code","Date"]).iloc[:,[6,0,1,2,3,4,5]]
            
            cols = ['Total_Cases', 'New_Cases', 'Total_Deaths', 'New_Deaths']
            self.discrepancies = self.df_new.iloc[(self.df_new[cols].values != self.df_old[(self.df_old.ISO3_Code.isin(self.df_new.ISO3_Code.unique()))&((self.df_old.Date >= '2020-02-15')|(self.df_old[self.df_old.ISO3_Code == 'CHN'].Date >= '2020-01-22'))][cols].values).any(axis=1)]
        else:
            cols = ['table_id', 'ISO3_Code', 'Date', 'Total_Cases', 'New_Cases', 'Total_Deaths', 'New_Deaths']
            self.discrepancies = DataFrame(data=[], columns=cols)
        
        return self.discrepancies
    
    @private
    def get_new_values(self, codes, links):
        from numpy import datetime64, timedelta64, array, concatenate
        from datetime import datetime, timedelta, timezone
        from pandas import DataFrame, concat
        from Covid19.utils.miscellaneous import get_totals_from_worldometer
        
        dt = datetime.now(tz=timezone(timedelta(hours=-1))).strftime('%Y-%m-%d')
        
        df_new = []
        for iso3, link in zip(codes, links):
            cases, deaths = get_totals_from_worldometer(link)
            dates = array(list(map(lambda x: datetime64(dt, 'D')-timedelta64(x,'D'), range(len(cases)-1,-1,-1))))
            icode = array(len(cases)*[iso3])
            new_c = concatenate(([cases[0]], cases[1:]-cases[:-1]))
            new_d = concatenate(([deaths[0]], deaths[1:]-deaths[:-1]))
            
            data = array([icode, dates, cases, new_c, deaths, new_d]).T
            
            df = DataFrame(data=data, columns=['ISO3_Code', 'Date', 'Total_Cases', 'New_Cases', 'Total_Deaths', 'New_Deaths'])
            
            df_new.append(df)
            
        df_new = concat(df_new, axis=0, ignore_index=True)
        
        return df_new
    
    def update(self, engine, df):
        from Covid19.utils.dbqueries import DBQueries
        
        cols = ['Total_Cases', 'New_Cases', 'Total_Deaths', 'New_Deaths']
        for table_id in df.table_id.values:
            cases, new_cases, deaths, new_deaths = df[df.table_id == table_id][cols].values[0]
            vd = {"Total_Cases":int(cases), "New_Cases":int(new_cases), "Total_Deaths":int(deaths), "New_Deaths":int(new_deaths)}
            condition = ("table_id","=",int(table_id))
            query = DBQueries().update_table(engine, "Covid19_data", vd, condition)
            engine.execute(query)