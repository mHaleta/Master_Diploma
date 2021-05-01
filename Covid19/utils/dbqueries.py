from accessify import private

class DBQueries:
    
    @private
    def build_simple_filter(self, t_name, condition):
        filtr = []
        
        if type(condition) == dict:
            clause, condition = list(condition.items())[0]
        elif type(condition) == tuple:
            condition = [condition]
        
        for cond in condition:
            if type(cond) == dict:
                filtr.append(self.build_simple_filter(t_name, cond))
            else:
                col, op, value = cond
                col = getattr(t_name.c, col)
                if op == '=':
                    filtr.append(col == value)
                elif op == '!=':
                    filtr.append(col != value)
                elif op == '>':
                    filtr.append(col > value)
                elif op == '<':
                    filtr.append(col < value)
                elif op == '>=':
                    filtr.append(col >= value)
                elif op == '<=':
                    filtr.append(col <= value)
                elif op == 'in':
                    filtr.append(col.in_(value))
                elif op == 'not in':
                    filtr.append(~col.in_(value))
                elif op == 'like':
                    filtr.append(col.like(value))
                elif op == 'not like':
                    filtr.append(~col.like(value))
                elif op == 'between':
                    filtr.append(col.between(*value))
                elif op == 'not between':
                    filtr.append(~col.between(*value))
        
        try:
            if clause == 'and':
                from sqlalchemy.sql.expression import and_
                filtr = and_(*filtr)
            elif clause == 'or':
                from sqlalchemy.sql.expression import or_
                filtr = or_(*filtr)
        except Exception:
            filtr = filtr[0]
        
        return filtr
    
    def select_table(self, engine, table, dist=False, columns=None, condition=None, order=None):
        from sqlalchemy import Table, MetaData, select
        
        t_name = Table(table, MetaData(), autoload=True, autoload_with=engine)
        
        if columns is None:
            s = select([t_name])
        else:
            columns = list(map(lambda x: getattr(t_name.c, x), columns))
            s = select(columns)
        
        if dist:
            s = s.distinct()
        if condition is not None:
            filtr = self.build_simple_filter(t_name, condition)
            s = s.where(filtr)
        if order is not None:
            order = list(map(lambda x: getattr(t_name.c, x) if type(x) != dict else getattr(t_name.c, x['desc']).desc(), order))
            s = s.order_by(*order)
        
        return s
    
    def select_countries_with_discrepancies(self, engine):
        from pandas import read_sql
        
        query = """
            select distinct "ISO3_Code"
            from (
                select
                    "ISO3_Code",
                    "New_Cases",
                    "Total_Cases" - lag("Total_Cases", 1) over (partition by "ISO3_Code" order by "ISO3_Code", "Date") as "New_Cases_lag",
                    "New_Deaths",
                    "Total_Deaths" - lag("Total_Deaths", 1) over (partition by "ISO3_Code" order by "ISO3_Code", "Date") as "New_Deaths_lag"
                from "Covid19_data"
            ) t
            where
                "New_Cases" != "New_Cases_lag"
                or "New_Deaths" != "New_Deaths_lag"
            order by 1
        """
        codes = read_sql(query, engine).values.reshape(-1)
        
        return codes
    
    def insert_table(self, engine, table, values_dict):
        from sqlalchemy import Table, MetaData
        
        t_name = Table(table, MetaData(), autoload=True, autoload_with=engine)
        
        i = t_name.insert().values(values_dict)
        
        return i
    
    def update_table(self, engine, table, values_dict, condition=None):
        from sqlalchemy import Table, MetaData
        
        t_name = Table(table, MetaData(), autoload=True, autoload_with=engine)
        
        u = t_name.update()
        if condition is not None:
            filtr = self.build_simple_filter(t_name, condition)
            u = u.where(filtr)
        u = u.values(values_dict)
        
        return u
    
    def delete_table(self, engine, table, condition=None):
        from sqlalchemy import Table, MetaData
        
        t_name = Table(table, MetaData(), autoload=True, autoload_with=engine)
        
        d = t_name.delete()
        if condition is not None:
            filtr = self.build_simple_filter(t_name, condition)
            d = d.where(filtr)
        
        return d