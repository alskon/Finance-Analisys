class Analysis:
    def __init__(self, sfp_variables, sc_variables):
        self.sfp_variables = sfp_variables
        self.sc_variables = sc_variables
        self.current_assets = self.calculate_sfp_assets()
        self.current_liabilities = self.calculate_sfp_liabilities()
        self.net_income = self.calculate_net_income()
        self.gross_profit = self.calculate_gross_profit()

        self.current_ratio = self.calculate_current_ratio()
        self.quick_ratio = self.calculate_quick_ratio()
        self.cash_ratio = self.calculate_cash_ratio()
        self.debt_ratio = self.calculate_debt_ratio()
        self.gross_margin_ratio = self.calculate_gross_margin_ratio()
        self.roa_ratio = self.calculate_roa_ratio()

    def calculate_gross_profit(self):
        return self.sc_variables['a'] - self.sc_variables['b']

    def calculate_sfp_assets(self):
        return self.sfp_variables['a'] + self.sfp_variables['b'] + self.sfp_variables['c'] + \
                         self.sfp_variables['d'] + self.sfp_variables['e'] + self.sfp_variables['f'] + \
                         self.sfp_variables['g'] + self.sfp_variables['h'] + self.sfp_variables['i']

    def calculate_sfp_liabilities(self):
        return self.sfp_variables['k'] + self.sfp_variables['l'] + self.sfp_variables['m'] + \
                              self.sfp_variables['n'] + self.sfp_variables['o'] + self.sfp_variables['p'] + \
                              self.sfp_variables['q'] + self.sfp_variables['r']

    def calculate_net_income(self):
        return self.sc_variables['a'] + self.sc_variables['c'] - self.sc_variables['b'] - self.sc_variables['d'] - \
               self.sc_variables['e'] - self.sc_variables['f'] - self.sc_variables['g']

    def calculate_current_ratio(self):
        return self.current_assets / self.current_liabilities

    def calculate_quick_ratio(self):
        liquid_assets = self.current_assets - self.sfp_variables['a'] - self.sfp_variables['b'] - \
                        self.sfp_variables['e'] - self.sfp_variables['f'] - self.sfp_variables['g']
        return liquid_assets - self.current_liabilities

    def calculate_cash_ratio(self):
        return self.sfp_variables['i']/self.current_liabilities

    def calculate_debt_ratio(self):
        return self.current_liabilities / self.current_assets

    def calculate_gross_margin_ratio(self):
        return (self.sc_variables['a'] - self.sc_variables['b']) / self.sc_variables['a']

    def calculate_roa_ratio(self):
        return self.net_income / self.current_assets

    def calculate(self):
        ratios = {'assets': self.current_assets, 'liabilities': self.current_liabilities,
                  'gross profit': self.gross_profit,
                  'net income': self.net_income,
                  'current ratio': self.current_ratio, 'quick ratio': self.quick_ratio,
                  'cash ratio': self.cash_ratio, 'debt ratio': self.debt_ratio,
                  'gross margin ratio': self.gross_margin_ratio, 'return on assets ratio': self.roa_ratio
                  }
        ratios = {k: round(v, 2) for k, v in ratios.items()}

        return ratios
