# Create class for creating a regression report later (inspired by sklearn/classification_report)
import numpy as np
import pandas as pd
from sklearn.metrics import (
    explained_variance_score,
    max_error,
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    median_absolute_error,
    r2_score,
    mean_poisson_deviance,
    mean_gamma_deviance,
    mean_tweedie_deviance,
)
import plotly.express as px


class RegressionReport:
    """Usage: report = RegressionReport(y_true, y_pred)"""
    def __init__(self, y_true, y_pred, plot=False):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.results = {}

        if plot:
            self.fig = self.plot(self.y_true, self.y_pred, target_name=plot if isinstance(plot, str) else None)

        metrics = list(filter(lambda x: "metric_" in x, dir(self)))
        fmt_string = "{:>" + str(max([len(x) for x in metrics])) + "s}: {: >20.3f}"
        print('Regression Report :\n')
        error_metrics = []
        for metric in metrics:
            try:
                metric_value = getattr(self, metric)(self.y_true, self.y_pred)
                self.results[metric] = metric_value
                print(fmt_string.format(metric.replace("metric_", ""), metric_value))
            except Exception as e:
                error_metrics.append(metric)
        print('\nPercentiles:')
        percentile = [5, 25, 50, 75, 95]
        percentile_value = np.percentile(self.y_true - self.y_pred, percentile)
        for p, pv in zip(percentile, percentile_value):
            print(fmt_string.format(str(p), pv))
        if len(error_metrics):
            print("\nCould not compute {} metrics ({})".format(len(error_metrics), ", ".join(error_metrics)))

    @staticmethod
    def plot(y_true, y_pred, target_name=None, show=True):
        labels = ["y (Truth)", "ŷ (Prediction)"]
        title = "Ground Truth vs Predictions"
        yaxis_title = ""
        if target_name:
            target_name = target_name + (" " * (not target_name.endswith(" ")))
            labels = [target_name + x for x in labels]
            title = target_name + title
            yaxis_title = target_name
        labels = ["Time Index"] + labels
        df = pd.DataFrame(dict(zip(labels, [np.arange(len(y_true)), y_true, y_pred])))
        fig = px.line(df, x=labels[0], y=labels[1:], title=title)
        fig.update_layout(yaxis_title=yaxis_title)
        if show:
            fig.show()
        return fig

    @staticmethod
    def metric_residual_sum_of_squares(y_true, y_pred):
        rss = np.sum(np.square(y_true - y_pred))
        return rss

    @staticmethod
    def metric_mean_squared_error(y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        return mse

    @staticmethod
    def metric_mean_squared_percentage_error(y_true, y_pred):
        mspe = np.mean(np.divide(np.square(y_true - y_pred), np.square(y_true)))
        return mspe

    @staticmethod
    def metric_root_mean_square_error(y_true, y_pred):
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        return rmse

    @staticmethod
    def metric_root_mean_square_percentage_error(y_true, y_pred):
        rmspe = np.square(np.mean(np.divide(np.square(y_true - y_pred), np.square(y_true))))
        return rmspe

    @staticmethod
    def metric_mean_absolute_error(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        return mae

    @staticmethod
    def metric_mean_absolute_percentage_error(y_true, y_pred):
        mape = np.mean(np.abs(np.divide((y_true - y_pred), y_true)))
        return mape

    @staticmethod
    def metric_relative_squared_error(y_true, y_pred):
        rse = np.divide(np.sum(np.square(y_true - y_pred)),
                        np.sum(np.square(y_true - np.mean(y_true))))
        return rse

    @staticmethod
    def metric_relative_absolute_error(y_true, y_pred):
        rae = np.divide(np.sum(np.abs(y_true - y_pred)),
                        np.sum(np.abs(y_true - np.mean(y_true))))
        return rae

    @staticmethod
    def metric_r2_score(y_true, y_pred):
        # Coefficient of determination
        r2 = r2_score(y_true, y_pred)
        return r2

    @staticmethod
    def metric_explained_variance_score(y_true, y_pred):
        return explained_variance_score(y_true, y_pred)

    @staticmethod
    def metric_max_error(y_true, y_pred):
        return max_error(y_true, y_pred)

    @staticmethod
    def metric_min_error(y_true, y_pred):
        return np.min(np.abs(y_true - y_pred))

    @staticmethod
    def metric_mean_squared_log_error(y_true, y_pred):
        return mean_squared_log_error(y_true, y_pred)

    @staticmethod
    def metric_median_absolute_error(y_true, y_pred):
        return median_absolute_error(y_true, y_pred)

    @staticmethod
    def metric_mean_poisson_deviance(y_true, y_pred):
        return mean_poisson_deviance(y_true, y_pred)

    @staticmethod
    def metric_mean_gamma_deviance(y_true, y_pred):
        return mean_gamma_deviance(y_true, y_pred)

    @staticmethod
    def metric_mean_tweedie_deviance(y_true, y_pred):
        return mean_tweedie_deviance(y_true, y_pred)
