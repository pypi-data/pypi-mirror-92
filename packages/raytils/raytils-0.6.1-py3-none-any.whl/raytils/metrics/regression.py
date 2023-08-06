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
from io import StringIO


class RegressionReport:
    """Generate regression report for two arrays similar to sklearn classification report

    Examples:
        To run a report, plot and get specific metrics

        >>> report = RegressionReport(np.array([0.5, 1.0]), np.array([1.0, 0.5]))  # generate report for two arrays
        >>> fig = report.plot()  # plot using plotly express
        >>> report.print()  # print(report)
        Regression Report:
                 explained_variance_score:               -3.000
                                max_error:                0.500
                      mean_absolute_error:                0.500
           mean_absolute_percentage_error:                0.750
                      mean_gamma_deviance:                0.500
                    mean_poisson_deviance:                0.347
                       mean_squared_error:                0.250
                   mean_squared_log_error:                0.083
            mean_squared_percentage_error:                0.625
                    mean_tweedie_deviance:                0.250
                    median_absolute_error:                0.500
                                min_error:                0.500
                                 r2_score:               -3.000
                  relative_absolute_error:                2.000
                   relative_squared_error:                4.000
                  residual_sum_of_squares:                0.500
                   root_mean_square_error:                0.500
        root_mean_square_percentage_error:                0.391
        Percentiles:
                                        5:               -0.450
                                       25:               -0.250
                                       50:                0.000
                                       75:                0.250
                                       95:                0.450
        >>> r2 = report["r2_score"]  # get specific metric
        -3.000
    """
    def __init__(self, y_true, y_pred):
        prefix = "metric_"  # all metric functions should have this prefix to be in the report
        self._y_true, self._y_pred = self._check_arrays(y_true, y_pred)
        self._computed_metrics = {}
        for class_attribute in [x for x in dir(self) if prefix in x]:
            metric_name, metric_value = class_attribute.replace(prefix, ""), float("NaN")
            try:
                metric_value = getattr(self, class_attribute)()
            except Exception:
                pass
            self._computed_metrics[metric_name] = metric_value

    @staticmethod
    def _check_arrays(y_true, y_pred):
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        return y_true, y_pred

    def __str__(self):
        report_str = []
        fmt_string = "{:>" + str(max([len(x) for x in self._computed_metrics.keys()])) + "s}: {: >20.3f}"

        report_str.append('Regression Report:')
        error_metrics = []

        for metric_name, metric_value in self._computed_metrics.items():
            report_str.append(fmt_string.format(metric_name, metric_value))
            if metric_value == float("NaN"):
                error_metrics.append(metric_name)

        report_str.append('\nPercentiles:')
        percentile = [5, 25, 50, 75, 95]
        percentile_value = np.percentile(self._y_true - self._y_pred, percentile)
        for p, pv in zip(percentile, percentile_value):
            report_str.append(fmt_string.format(str(p), pv))
        if len(error_metrics):
            report_str.append("\nCould not compute: {}".format(len(error_metrics), ", ".join(error_metrics)))
        return '\n'.join(report_str)

    def __repr__(self):
        return self.__str__()

    def print(self):
        print(self)

    def __getitem__(self, item):
        return self._computed_metrics[item]

    def plot(self, target_name=None, show=True):
        labels = ["y (Truth)", "ŷ (Prediction)"]
        title = "Ground Truth vs Predictions"
        yaxis_title = ""
        if target_name:
            target_name = target_name + (" " * (not target_name.endswith(" ")))
            labels = [target_name + x for x in labels]
            title = target_name + title
            yaxis_title = target_name
        labels = ["Time Index"] + labels
        df = pd.DataFrame(dict(zip(labels, [np.arange(len(self._y_true)), self._y_true, self._y_pred])))
        fig = px.line(df, x=labels[0], y=labels[1:], title=title)
        fig.update_layout(yaxis_title=yaxis_title)
        if show:
            fig.show()
        return fig

    def metric_residual_sum_of_squares(self):
        rss = np.sum(np.square(self._y_true - self._y_pred))
        return rss

    def metric_mean_squared_error(self):
        mse = mean_squared_error(self._y_true, self._y_pred)
        return mse

    def metric_mean_squared_percentage_error(self):
        mspe = np.mean(np.divide(np.square(self._y_true - self._y_pred), np.square(self._y_true)))
        return mspe

    def metric_root_mean_square_error(self):
        rmse = mean_squared_error(self._y_true, self._y_pred, squared=False)
        return rmse

    def metric_root_mean_square_percentage_error(self):
        rmspe = np.square(np.mean(np.divide(np.square(self._y_true - self._y_pred), np.square(self._y_true))))
        return rmspe

    def metric_mean_absolute_error(self):
        mae = mean_absolute_error(self._y_true, self._y_pred)
        return mae

    def metric_mean_absolute_percentage_error(self):
        mape = np.mean(np.abs(np.divide((self._y_true - self._y_pred), self._y_true)))
        return mape

    def metric_relative_squared_error(self):
        rse = np.divide(np.sum(np.square(self._y_true - self._y_pred)),
                        np.sum(np.square(self._y_true - np.mean(self._y_true))))
        return rse

    def metric_relative_absolute_error(self):
        rae = np.divide(np.sum(np.abs(self._y_true - self._y_pred)),
                        np.sum(np.abs(self._y_true - np.mean(self._y_true))))
        return rae

    def metric_r2_score(self):
        # Coefficient of determination
        r2 = r2_score(self._y_true, self._y_pred)
        return r2

    def metric_explained_variance_score(self):
        return explained_variance_score(self._y_true, self._y_pred)

    def metric_max_error(self):
        return max_error(self._y_true, self._y_pred)

    def metric_min_error(self):
        return np.min(np.abs(self._y_true - self._y_pred))

    def metric_mean_squared_log_error(self):
        return mean_squared_log_error(self._y_true, self._y_pred)

    def metric_median_absolute_error(self):
        return median_absolute_error(self._y_true, self._y_pred)

    def metric_mean_poisson_deviance(self):
        return mean_poisson_deviance(self._y_true, self._y_pred)

    def metric_mean_gamma_deviance(self):
        return mean_gamma_deviance(self._y_true, self._y_pred)

    def metric_mean_tweedie_deviance(self):
        return mean_tweedie_deviance(self._y_true, self._y_pred)
