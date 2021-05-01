from accessify import private

class Preprocessing:
    def get_days_beta_batches(self, df, interval=1):
        from dateutil.relativedelta import relativedelta
        
        df = df.copy()
        
        current_date = df.Date.min()
        max_date = df.Date.max()
        batches = {'days':[], 'beta':[], 'dates':[]}
        while current_date + relativedelta(months=interval) < max_date:
            next_date = current_date + relativedelta(months=interval)
            
            cases = df[(df.Date >= current_date)&(df.Date <= next_date)].Total_Cases.values.reshape(-1)
            
            beta = (cases[1:]-cases[:-1])/cases[:-1]
            days = df[(df.Date >= current_date)&(df.Date <= next_date)].Day_count.values.reshape(-1)[1:]
            dates = df[(df.Date >= current_date)&(df.Date <= next_date)].Date.values.astype('datetime64[D]').reshape(-1)[1:]
            
            batches['days'].append(days)
            batches['beta'].append(beta)
            batches['dates'].append(dates)
            
            current_date = next_date
        
        return batches


class CoronavirusModelling:
    def __init__(self, strategy, with_outliers=True, p_deg=None):
        self.strategy = strategy
        self.with_outliers = with_outliers
        if strategy == 'polynomial':
            self.p_deg = p_deg
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.filtr = None
        self.coef = None
        self.fitter = None
        self.score = None
        self.str_fitter = None
    
    @private
    def linear(self, X, y):
        from sklearn.linear_model import LinearRegression
        from sympy import Poly, Symbol
        from numpy import array, round as round_
        from Covid19.utils.miscellaneous import round_to_significant_digits
        
        lr = LinearRegression()
        lr.fit(X.reshape(-1,1), y)
        
        b = lr.coef_[0]
        a = lr.intercept_
        
        self.coef = array([a,b])
        coeffs = array([a,b])
        for i in range(len(coeffs)):
            if round_(coeffs[i], 3) == 0:
                coeffs[i] = round_to_significant_digits(coeffs[i], 1)
            else:
                coeffs[i] = round_(coeffs[i], 3)
        
        f = lambda t: a + b*t
        R2 = lr.score(X.reshape(-1,1), y)
        f_str = str(Poly(coeffs, Symbol('t')).expr).replace('*','')
        
        f_str = r'$\beta = ' + f_str + f', \quad R^2 = {round_(R2,2)}' + '$'
        
        return f, R2, f_str
    
    @private
    def exponential(self, X, y):
        from sklearn.linear_model import LinearRegression
        from numpy import array, exp, log, round as round_
        from sympy import Symbol, Mul, Pow
        from Covid19.utils.miscellaneous import round_to_significant_digits
        
        lr = LinearRegression()
        lr.fit(X.reshape(-1,1), log(y))
        
        a = exp(lr.intercept_)
        b = lr.coef_[0]
        
        self.coef = array([a, b])
        coeffs = array([a, b])
        for i in range(len(coeffs)):
            if round_(coeffs[i], 3) == 0:
                coeffs[i] = round_to_significant_digits(coeffs[i], 1)
            else:
                coeffs[i] = round_(coeffs[i], 3)
        
        f = lambda t: a*exp(b*t)
        R2 = lr.score(X.reshape(-1,1), log(y))
        f_str = str(Mul(coeffs[0], Pow(Symbol('e'), Mul(coeffs[1], Symbol('t')))))
        
        f_str = f_str.replace('**', '^').replace('*','').replace('(','{').replace(')', '}')
        f_str = r'$\beta = ' + f_str + f', \quad R^2 = {round_(R2,2)}' + '$'
        
        return f, R2, f_str
    
    @private
    def polynomial(self, X, y, deg=None):
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import LinearRegression
        from numpy import arange, sum as sum_, vstack, power, round as round_, flip
        from sympy import Poly, Symbol
        from Covid19.utils.miscellaneous import round_to_significant_digits
        
        if deg is None:
            deg = self.p_deg

        pf = PolynomialFeatures(deg)
        pf.fit(X.reshape(-1,1), y)

        X_t = pf.transform(X.reshape(-1,1))

        lr = LinearRegression(fit_intercept=False)
        lr.fit(X_t, y)
        
        self.coef = lr.coef_.copy()
        coeffs = lr.coef_.copy()
        for i in range(len(coeffs)):
            if round_(coeffs[i], 3) == 0:
                coeffs[i] = round_to_significant_digits(coeffs[i], 1)
            else:
                coeffs[i] = round_(coeffs[i], 3)

        f = lambda t: sum_(power(vstack(t), arange(deg+1)) @ vstack(lr.coef_), axis=1)
        R2 = round_(lr.score(X_t, y), 2)
        f_str = str(Poly(flip(coeffs), Symbol('t')).expr)
        
        f_str = f_str.replace('**','^').replace('*','')
        f_str = r'$\beta = ' + f_str + f', \quad R^2 = {round_(R2,2)}' + '$'

        return f, R2, f_str
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        
        if not self.with_outliers:
            from Covid19.utils.miscellaneous import outliers_filter
            from numpy import where
            
            self.filtr = outliers_filter(y)
            X = X[where(~self.filtr)]
            y = y[where(~self.filtr)]
        
        if self.strategy != 'auto':
            method = getattr(self, self.strategy)
            self.fitter, self.score, self.str_fitter = method(X, y)
        else:
            from numpy import argmax
            
            f1, sc1, fs1 = self.linear(X, y)
            f2, sc2, fs2 = self.exponential(X, y)
            f3, sc3, fs3 = self.polynomial(X, y, 2)
            f4, sc4, fs4 = self.polynomial(X, y, 3)
            f5, sc5, fs5 = self.polynomial(X, y, 4)
            
            i = argmax([sc1, sc2, sc3, sc4, sc5])
            
            if [sc1, sc2, sc3, sc4, sc5][i] < 0.6:
                raise Exception("the best R^2 score is less than 0.6")
            
            self.fitter = [f1, f2, f3, f4, f5][i]
            self.score = [sc1, sc2, sc3, sc4, sc5][i]
            self.str_fitter = [fs1, fs2, fs3, fs4, fs5][i]
            self.strategy = (['linear', 'exponential']+3*['polynomial'])[i]
            self.p_deg = [1,None,2,3,4][i]
            
    
    def predict(self, X):
        self.X_test = X
        self.y_test = self.fitter(X)
        
        return self.y_test


class Plotter:
    
    def single_figure_plot(self, X, y, suptitle=None, title=None, dates=None,
                           showfliers=True, fitter=None, str_fitter=None):
        import matplotlib.pyplot as plt
        
        X = X.copy()
        y = y.copy()
        
        plt.figure(figsize=(8,6))
        
        if suptitle is not None:
            plt.suptitle(suptitle, fontsize=16)
            
        plt.xlabel('Day', fontsize=12)
        plt.ylabel('Beta', fontsize=12)
        
        if not showfliers:
            from Covid19.utils.miscellaneous import outliers_filter
            from numpy import where
            
            filtr = outliers_filter(y)
            X = X[where(~filtr)]
            y = y[where(~filtr)]
            
            if dates is not None:
                dates = dates.copy()
                dates = dates[where(~filtr)]
        
        if title is not None and dates is None:
            plt.title(title, fontsize=14)
        elif title is not None and dates is not None:
            min_date = dates[0]
            max_date = dates[-1]
            title += f'\n{min_date} — {max_date}'
            
            plt.title(title, fontsize=14)
        elif title is None and dates is not None:
            min_date = dates[0]
            max_date = dates[-1]
            title = f'{min_date} — {max_date}'
            
            plt.title(title, fontsize=14)
        
        plt.scatter(X, y)
        
        if fitter is not None:
            from numpy import linspace
            
            min_v = min(X)
            max_v = max(X)
            
            t = linspace(min_v, max_v, 1000, endpoint=True)
            if str_fitter is None:
                plt.plot(t, fitter(t), c='red')
            else:
                plt.plot(t, fitter(t), c='red', label=str_fitter)
                plt.legend(fontsize=11)
        
        plt.grid(True)
        plt.show()
    
    def single_gridspec_plot(self, X, y, grid, suptitle=None, title=None, dates=None,
                             showfliers=None, fitter=None, str_fitter=None):
        import matplotlib.pyplot as plt
        from matplotlib import gridspec
        
        X = X.copy()
        y = y.copy()
        
        if title is None:
            title = len(X)*[title]
        if dates is None:
            dates = len(X)*[dates]
        else:
            dates = dates.copy()
        if showfliers is None:
            showfliers = len(X)*[True]
        if fitter is None:
            fitter = len(X)*[fitter]
        if str_fitter is None:
            str_fitter = len(X)*[str_fitter]
        
        fig = plt.figure(figsize=(16,6*grid[0]+1))
        if suptitle is not None:
            fig.suptitle(suptitle, fontsize=16)
            fig.subplots_adjust(top=(0.98*6*grid[0]-1)/(6*grid[0]))
        
        gs = gridspec.GridSpec(*grid, figure=fig, hspace=0.28, wspace=0.2)
        for i in range(len(X)):
            ax = fig.add_subplot(gs[i//grid[1],i%grid[1]])
            
            ax.set_xlabel('Day', fontsize=12)
            if i%grid[1] == 0:
                ax.set_ylabel('Beta', fontsize=12)
            
            if not showfliers[i]:
                from Covid19.utils.miscellaneous import outliers_filter
                from numpy import where
                
                filtr = outliers_filter(y[i])
                X[i] = X[i][where(~filtr)]
                y[i] = y[i][where(~filtr)]
                dates[i] = dates[i][where(~filtr)]
            
            if title[i] is not None and dates[i] is None:
                ax.set_title(title[i], fontsize=14)
            elif title[i] is not None and dates[i] is not None:
                min_date = dates[i][0]
                max_date = dates[i][-1]
                title[i] += f'\n{min_date} — {max_date}'
                
                ax.set_title(title[i], fontsize=14)
            elif title[i] is None and dates[i] is not None:
                min_date = dates[i][0]
                max_date = dates[i][-1]
                title[i] = f'{min_date} — {max_date}'
                
                ax.set_title(title[i], fontsize=14)
            
            ax.scatter(X[i], y[i], s=10)
            
            if fitter[i] is not None:
                from numpy import linspace
            
                min_v = min(X[i])
                max_v = max(X[i])
                
                t = linspace(min_v, max_v, 1000, endpoint=True)
                if str_fitter[i] is None:
                    ax.plot(t, fitter[i](t), c='red')
                else:
                    ax.plot(t, fitter[i](t), c='red', label=str_fitter[i])
                    ax.legend(fontsize=11)
            
            ax.grid(True)
        plt.show()
            
            
            
            
            
            
            
            
            
            
            
    