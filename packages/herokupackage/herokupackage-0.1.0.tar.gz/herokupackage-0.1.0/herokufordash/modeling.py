import warnings
import numpy as np
import pandas as pd
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_absolute_error


# from sklearn.metrics import r2_score


class modeling:
    warnings.filterwarnings("ignore")

    def __init__(self, data, storeid):
        self.data = data
        self.storeid = storeid
        self.storeweeklysales = self.data.loc[self.data.Store == self.storeid].set_index('Date').resample(
            'w').Sales.sum()
        self.average = np.full((8,), self.storeweeklysales[:-9].mean())
        self.mae = mean_absolute_error(self.storeweeklysales[-9:-1], self.average)
        self.WAPE = np.sum(abs(self.average - self.storeweeklysales[-9:-1])) / (
            self.data.set_index('Date').resample('w').Sales.sum()[-9:-1].sum())

    def predict(self):
        # storeweeklysales = self.data.loc[self.data.Store == self.storeid].set_index('Date').resample('w').Sales.sum()

        if len(self.storeweeklysales[(self.storeweeklysales == 0)].index) == 0:
            train, test = (self.storeweeklysales[:-9], self.storeweeklysales[-9:-1])
            arima_model = auto_arima(train, start_p=0, d=0, start_q=0,
                                     max_p=5, max_d=5, max_q=5, start_P=0,
                                     D=1, start_Q=0, max_P=5, max_D=5,
                                     max_Q=5, m=2, seasonal=True,
                                     error_action='warn', trace=False,
                                     supress_warnings=True, stepwise=False,
                                     random=True,
                                     random_state=20, n_fits=50)

            predictresult1 = arima_model.predict(n_periods=8)
            true_values = test.values
            mae = mean_absolute_error(true_values, predictresult1)
            WAPE = np.sum(abs(predictresult1 - true_values)) / (
                self.data.set_index('Date').resample('w').Sales.sum()[-9:-1].sum())

            # R2 = r2_score(true_values, predictresult1)
            return pd.DataFrame([mae, WAPE, self.mae, self.WAPE],
                                index=['MAE_AutoArima', 'WAPE_AutoArima', 'MAE_MeanMethod', 'WAPE_MeanMethod'],
                                columns=[self.storeid]).T
            # return pd.DataFrame([mae, R2])

        if len(self.storeweeklysales.loc[
               self.storeweeklysales[(self.storeweeklysales == 0)].index[-1]:].index) >= 2 and len(
                self.storeweeklysales.loc[
                self.storeweeklysales.loc[self.storeweeklysales[(self.storeweeklysales == 0)].index[-1]:].index[1]:][
                :-1]) >= 16:
            train_startdate = \
            self.storeweeklysales.loc[self.storeweeklysales[(self.storeweeklysales == 0)].index[-1]:].index[1]
            train_enddate = len(self.storeweeklysales.loc[train_startdate:]) - 9
            train = self.storeweeklysales.loc[train_startdate:][:train_enddate]
            # test = self.storeweeklysales.loc[train_startdate:][train_enddate:-1]
            test = self.storeweeklysales[-9:-1]

            arima_model = auto_arima(train, start_p=0, d=0,
                                     start_q=0,
                                     max_p=5, max_d=5, max_q=5, start_P=0,
                                     D=1, start_Q=0, max_P=5, max_D=5,
                                     max_Q=5, m=2, seasonal=True,
                                     error_action='warn', trace=False,
                                     supress_warnings=True, stepwise=False,
                                     random=True,
                                     random_state=20, n_fits=50)

            predictresult = arima_model.predict(n_periods=8)
            true_values = test.values
            mae_2 = mean_absolute_error(true_values, predictresult)
            WAPE_2 = np.sum(abs(predictresult - true_values)) / (
                self.data.set_index('Date').resample('w').Sales.sum()[-9:-1].sum())
            # R2_2 = r2_score(true_values, predictresult)
            return pd.DataFrame([mae_2, WAPE_2, self.mae, self.WAPE],
                                index=['MAE_AutoArima', 'WAPE_AutoArima', 'MAE_MeanMethod', 'WAPE_MeanMethod'],
                                columns=[self.storeid]).T
            # return pd.DataFrame([mae_2, R2_2])

        else:
            storeweeklysales_dropzero = self.storeweeklysales[self.storeweeklysales != 0]
            train, test = (storeweeklysales_dropzero[:-9], storeweeklysales_dropzero[-9:-1])
            arima_model = auto_arima(train, start_p=0, d=0, start_q=0,
                                     max_p=5, max_d=5, max_q=5, start_P=0,
                                     D=1, start_Q=0, max_P=5, max_D=5,
                                     max_Q=5, m=2, seasonal=True,
                                     error_action='warn', trace=False,
                                     supress_warnings=True, stepwise=False,
                                     random=True,
                                     random_state=20, n_fits=50)

            predictresult1 = arima_model.predict(n_periods=8)
            true_values = test.values
            mae = mean_absolute_error(true_values, predictresult1)
            WAPE = np.sum(abs(predictresult1 - true_values)) / (
                self.data.set_index('Date').resample('w').Sales.sum()[-9:-1].sum())
            # R2 = r2_score(true_values, predictresult1)
            return pd.DataFrame([mae, WAPE, self.mae, self.WAPE],
                                index=['MAE_AutoArima', 'WAPE_AutoArima', 'MAE_MeanMethod', 'WAPE_MeanMethod'],
                                columns=[self.storeid]).T
            # return pd.DataFrame([mae, R2])

    def forecast(self, start_date, end_date):
        # storeweeklysales = self.data.loc[self.data.Store == self.storeid].set_index('Date').resample('w').Sales.sum()
        # storeweeklysales = storeweeklysales[storeweeklysales!=0]
        forecastindex = pd.date_range(start_date, end_date, freq='W')
        if len(self.storeweeklysales[(self.storeweeklysales == 0)].index) == 0:
            train, test = (self.storeweeklysales[:-9], self.storeweeklysales[-9:-1])
            arima_model = auto_arima(self.storeweeklysales[:test.index[-1]], start_p=0, d=0, start_q=0,
                                     max_p=5, max_d=5, max_q=5, start_P=0,
                                     D=1, start_Q=0, max_P=5, max_D=5,
                                     max_Q=5, m=2, seasonal=True,
                                     error_action='warn', trace=False,
                                     supress_warnings=True, stepwise=False,
                                     random=True,
                                     random_state=20, n_fits=50)

            forecast, CI = arima_model.predict(n_periods=8, return_conf_int=True, alpha=0.05)
            forecastresult1 = pd.DataFrame([forecast, CI[:, 0], CI[:, 1]],
                                           index=['Forecast', 'lower CI', 'upper CI']).T.set_index(forecastindex)
            forecastresult1['Previous 8 Weeks'] = self.storeweeklysales[-9:-1].values
            return forecastresult1

        if len(self.storeweeklysales.loc[
               self.storeweeklysales[(self.storeweeklysales == 0)].index[-1]:].index) >= 2 and len(
                self.storeweeklysales.loc[
                self.storeweeklysales.loc[self.storeweeklysales[(self.storeweeklysales == 0)].index[-1]:].index[1]:][
                :-1]) >= 16:
            train_startdate = \
            self.storeweeklysales.loc[self.storeweeklysales[(self.storeweeklysales == 0)].index[-1]:].index[1]
            train_enddate = len(self.storeweeklysales.loc[train_startdate:]) - 9
            train = self.storeweeklysales.loc[train_startdate:][:train_enddate]
            # test = self.storeweeklysales.loc[train_startdate:][train_enddate:-1]
            test = self.storeweeklysales[-9:-1]

            arima_model = auto_arima(self.storeweeklysales.loc[train_startdate:test.index[-1]], start_p=0, d=0,
                                     start_q=0,
                                     max_p=5, max_d=5, max_q=5, start_P=0,
                                     D=1, start_Q=0, max_P=5, max_D=5,
                                     max_Q=5, m=2, seasonal=True,
                                     error_action='warn', trace=False,
                                     supress_warnings=True, stepwise=False,
                                     random=True,
                                     random_state=20, n_fits=50)

            forecast, CI = arima_model.predict(n_periods=8, return_conf_int=True, alpha=0.05)
            return pd.DataFrame([forecast, CI[:, 0], CI[:, 1], self.storeweeklysales[-9:-1].values],
                                index=['Forecast', 'lower CI', 'upper CI', 'Previous 8 Weeks']).T.set_index(
                forecastindex)


        else:
            storeweeklysales_dropzero = self.storeweeklysales[self.storeweeklysales != 0]
            train, test = (storeweeklysales_dropzero[:-9], storeweeklysales_dropzero[-9:-1])
            arima_model = auto_arima(storeweeklysales_dropzero[:test.index[-1]], start_p=0, d=0, start_q=0,
                                     max_p=5, max_d=5, max_q=5, start_P=0,
                                     D=1, start_Q=0, max_P=5, max_D=5,
                                     max_Q=5, m=2, seasonal=True,
                                     error_action='warn', trace=False,
                                     supress_warnings=True, stepwise=False,
                                     random=True,
                                     random_state=20, n_fits=50)

            forecast, CI = arima_model.predict(n_periods=8, return_conf_int=True, alpha=0.05)
            forecastresult1 = pd.DataFrame([forecast, CI[:, 0], CI[:, 1]],
                                           index=['Forecast', 'lower CI', 'upper CI']).T.set_index(forecastindex)

            forecastresult1['Previous 8 Weeks'] = self.storeweeklysales[-9:-1].values
            return forecastresult1



