from hermeskit.exceptions import LengthMismatched
from hermeskit.exceptions import InvalidProbabilityValueRange
from hermeskit.exceptions import InvalidMulticlassLabel
from hermeskit.exceptions import InvalidOneClassLabel
from hermeskit.exceptions import DiscreteException
from hermeskit.exceptions import IterableException
from hermeskit.exceptions import SameSizeException
from hermeskit.exceptions import NanValueException
from hermeskit.exceptions import InvalidParameter

import numpy as np
import pandas as pd
from IPython.core.display import display, HTML
import yaml
from pathlib import Path

# -----------------------------------------------
import sklearn 
from sklearn.metrics import roc_curve



config_file = Path(__file__).parent / "config.yaml"
config = yaml.load(config_file.open(mode='r'),Loader=yaml.FullLoader)

THRESHOLD_MONTHLY_GINI = config['THRESHOLD_MONTHLY_GINI']


def _check_iterable(y):
    if type(y) not in [list, np.ndarray, pd.Series, pd.DataFrame, tuple]:
        raise IterableException()

    
def _check_ndarray_type(x):
    if type(x) is not np.ndarray:
        raise ValueError()


def _check_dataframe_type(x):
    if type(x) is not pd.DataFrame:
        raise ValueError()

    
def _check_same_length(y_true, y_pred):
    _check_iterable(y_true)
    _check_iterable(y_pred)
    if len(y_true) != len(y_pred):
        raise LengthMismatched()

        
def _check_discrete_number(_list):
    _check_iterable(_list)
    if any(type(i) != np.int for i in _list):
        if any(i % 1 != 0 for i in _list):
            raise DiscreteException()

        
def _check_binary_label(_list):
    _check_iterable(_list)
    _check_discrete_number(_list)
    unique_label = np.unique(_list)
    if len(unique_label) > 2:
        raise InvalidMulticlassLabel()
    elif len(unique_label) < 2:
        raise InvalidOneClassLabel()
    else:
        if (unique_label[0] != 0) or (unique_label[1] != 1):
            raise InvalidBinaryLabel()

        
def _check_probability_range(_list):
    _check_iterable(_list)
    if (np.max(_list) > 1) or (np.min(_list) < 0):
        raise InvalidProbabilityValueRange()

        
def _visualize(_obj, title=None, visualize=True, highlight=True, **kwargs):
    if visualize:
        if title is not None:
            display(HTML(f'<h2><b>{title}</b></h2>'))
        if type(_obj) in [pd.DataFrame, pd.Series]:
            if type(_obj) == pd.Series:
                _obj = _obj.to_frame()
            _visualize_dataframe(_obj)
        else:
            print(_obj)

        
def _visualize_dataframe(df):
    if len(df) <= 20:
        display(df.style.applymap(_highlight_invalid_metric))
    else:
        print('[WARNING]: Highlight this dataframe is not allowed due to too long')
        display(df)
        

def _highlight_invalid_metric(val):
    result = ''
    if (type(val) == float) and (val < THRESHOLD_MONTHLY_GINI):
        result = 'color: red'
    elif (type(val) == float) and (val >= THRESHOLD_MONTHLY_GINI):
        result = 'background-color: lightgreen' 
    else:
        result = 'color: black'
    return result


def _report(y_true, y_pred, user_id=None, disbursement_date=None, quarterly_gini=False, **kwargs):
    _check_same_length(y_true, y_pred)
    _check_binary_label(y_true)    
    _check_probability_range(y_pred)
    df = pd.DataFrame({
        'y_true': y_true,
        'y_pred': y_pred,
    })
    
    if user_id is not None:
        _check_iterable(user_id)
        _check_same_length(y_true, user_id)
        user_id = user_id
        df.insert(0, 'user_id', user_id)
        
    global_gini = calculate_gini_score(df['y_true'], df['y_pred'])
    meta_report = {
        'input': df,
        'gini': {
            'global': global_gini,
        }
    }
    
    if disbursement_date is not None:
        _check_iterable(disbursement_date)
        _check_same_length(y_true, disbursement_date)
        disbursement_date = pd.to_datetime(disbursement_date, format='%Y-%m-%d')
        df.insert(1, 'disbursement_date', disbursement_date)
        df['month'] = df['disbursement_date'].apply(lambda x: x.strftime('%Y-%m'))
        monthly_report = df.groupby('month')[['y_true', 'y_pred']].apply(lambda x: calculate_gini_score(x['y_true'], x['y_pred'])).to_frame(name='gini_score')
        meta_report['gini']['month'] = monthly_report
        if quarterly_gini:
            df['quarter'] = df['disbursement_date'].apply(lambda x: x.strftime(f'%Y-Q{x.quarter}'))
            quarterly_report = df.groupby('quarter')[['y_true', 'y_pred']].apply(lambda x: calculate_gini_score(x['y_true'], x['y_pred'])).to_frame(name='gini_score')
            meta_report['gini']['quarter'] = quarterly_report
            
    _visualize(df, 'Input', **kwargs)
    _visualize(global_gini, 'Global Gini', **kwargs)
    if disbursement_date is not None: 
        _visualize(monthly_report, 'Monthly Gini Report', **kwargs)
        if quarterly_gini:
            _visualize(quarterly_report, 'Quarterly Gini Report', **kwargs)
    return meta_report


def _convert_dataframe2ndarray(df):
    _check_iterable(df)
    if type(df) == pd.DataFrame:
        return df.values
    elif type(df) == np.ndarray:
        return df
    else:
        return np.array(df)


def calculate_gini_score(_y_true, _y_pred):
    fpr, tpr, thresholds = roc_curve(_y_true, _y_pred)
    roc_auc = sklearn.metrics.auc(fpr, tpr)
    gini = (2 * roc_auc) - 1
    return gini
        
    
def calculate_psi(expected, actual, buckettype='quantiles', buckets=10, axis=0, columns=None, to_excel=False, allow_na=True, fillna=10e-6):
    '''Calculate the PSI (population stability index) across all variables
    Args:
       expected: numpy matrix of original values
       actual: numpy matrix of new values, same size as expected
       buckettype: type of strategy for creating buckets, bins splits into even splits, quantiles splits into quantile buckets
       buckets: number of quantiles to use in bucketing variables
       axis: axis by which variables are defined, 0 for vertical, 1 for horizontal
    Returns:
       psi_values: ndarray of psi values for each variable
    Author:
       Matthew Burke
       github.com/mwburke
       worksofchart.com
    '''

    def psi(expected_array, actual_array, buckets):
        
        '''Calculate the PSI for a single variable
        Args:
           expected_array: numpy array of original values
           actual_array: numpy array of new values, same size as expected
           buckets: number of percentile ranges to bucket the values into
        Returns:
           psi_value: calculated PSI value
        '''

        def scale_range (input_, min_, max_):
            input_ += -(np.min(input_))
            input_ /= np.max(input_) / (max_ - min_)
            input_ += min_
            return input_


        breakpoints = np.arange(0, buckets + 1) / (buckets) * 100

        if buckettype == 'bins':
            breakpoints = scale_range(breakpoints, np.min(expected_array), np.max(expected_array))
            if len(breakpoints) == 2:
                breakpoints = breakpoints.tolist()
                breakpoints.insert(0,-np.inf)
                breakpoints.append(np.inf)
                breakpoints = np.array(breakpoints)
            else:
                breakpoints[0] = -np.inf
                breakpoints[-1] = np.inf
           
        elif buckettype == 'quantiles':
            breakpoints = np.sort(np.array(list(set(np.stack([np.percentile(expected_array, b) for b in breakpoints])))))
            if len(breakpoints) == 2:
                breakpoints = breakpoints.tolist()
                breakpoints.insert(0,-np.inf)
                breakpoints.append(np.inf)
                breakpoints = np.array(breakpoints)
            else:
                breakpoints[0] = -np.inf
                breakpoints[-1] = np.inf
        expected_array = pd.Series(expected_array.tolist(), dtype=object).fillna(-np.inf).tolist()
        actual_array = pd.Series(actual_array.tolist(), dtype=object).fillna(-np.inf).tolist()

        expected_percents = np.histogram(expected_array, breakpoints)[0] / len(expected_array)
        actual_percents = np.histogram(actual_array, breakpoints)[0] / len(actual_array)
        def sub_psi(e_perc, a_perc):
            '''Calculate the actual PSI value from comparing the values.
               Update the actual value to a very small number if equal to zero
            '''
            if a_perc == 0:
                a_perc = 0.0001
            if e_perc == 0:
                e_perc = 0.0001

            value = (e_perc - a_perc) * np.log(e_perc / a_perc)
            return(value)

        psi_value = sum(sub_psi(expected_percents[i], actual_percents[i]) for i in range(0, len(expected_percents)))

        return(psi_value)
    
    # Check input data types, can be dataframe or ndarray, after this all will be ndarray
    expected = _convert_dataframe2ndarray(expected)
    actual = _convert_dataframe2ndarray(actual)
    # Check input data size, must be same size
    if expected.shape != actual.shape:
        raise SameSizeException()
    # Check input data numerical type, must not include Nan values
    if np.any(np.isnan(expected)):
        if allow_na is False:
            raise NanValueException()
        expected[np.isnan(expected)] = fillna
    if np.any(np.isnan(actual)):
        if allow_na is False:
            raise NanValueException()
        actual[np.isnan(actual)] = fillna
    # Check columns and axis
    if columns is not None:
        _check_iterable(columns)
        if expected.shape[1] != len(columns):
            raise SameSizeException()
        if axis == 0:
            raise InvalidParameter('To use columns param set axis=1')
        
    if len(expected.shape) == 1:
        psi_values = np.empty(len(expected.shape))
    else:
        psi_values = np.empty(expected.shape[axis])

    for i in range(0, len(psi_values)):
        if len(psi_values) == 1:
            psi_values = psi(expected, actual, buckets)
        elif axis == 1:
            psi_values[i] = psi(expected[:,i], actual[:,i], buckets)
        elif axis == 0:
            psi_values[i] = psi(expected[i,:], actual[i,:], buckets)
            
    result = {}
    if columns is not None:
        result['feature'] = columns
    result['psi'] = psi_values
    result = pd.DataFrame(result)
    if to_excel:
        result.to_excel('psi_values.xlsx')
    return result
    

def credit_scoring_report(y_true, y_pred, user_id=None, disbursement_date=None, quarterly_gini=False, **kwargs):
    return _report(y_true, y_pred, user_id, disbursement_date, quarterly_gini, **kwargs)