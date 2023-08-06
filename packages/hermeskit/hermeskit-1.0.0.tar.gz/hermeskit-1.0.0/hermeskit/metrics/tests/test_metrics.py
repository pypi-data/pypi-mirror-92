import os
from pathlib import Path

import pytest

from hermeskit.metrics import credit_scoring_report
import pandas as pd
import numpy as np


def read_sample_data():
    sample_data = pd.read_pickle('sample_data')
    return sample_data


def prepare_dataset():
    sample_data = read_sample_data()
    y_true = sample_data['uid_label']
    y_pred = np.random.rand((len(y_true))) # Dummy label data
    disbursement_date = sample_data['uid_refer_time']
    user_id = sample_data['user_id']
    return sample_data, y_true, y_pred, user_id, disbursement_date


def test_runnable_report_metrics():
    sample_data, y_true, y_pred, user_id, disbursement_date = prepare_dataset()
    meta_report = credit_scoring_report(y_true, y_pred)
    assert list(meta_report.keys()) == ['input', 'gini']
    assert 'global' in meta_report['gini'].keys()
    
    
def test_report_metrics_with_user_id():
    sample_data, y_true, y_pred, user_id, disbursement_date = prepare_dataset()
    meta_report = credit_scoring_report(y_true, y_pred, user_id=user_id)
    assert list(meta_report.keys()) == ['input', 'gini']
    assert 'user_id' in meta_report['input'].columns
    assert 'global' in meta_report['gini'].keys()
    
    
def test_report_metrics_with_disbursement_date():
    sample_data, y_true, y_pred, user_id, disbursement_date = prepare_dataset()
    meta_report = credit_scoring_report(y_true, y_pred, disbursement_date=disbursement_date)
    assert list(meta_report.keys()) == ['input', 'gini']
    assert 'disbursement_date' in meta_report['input'].columns
    assert 'month' in meta_report['input'].columns
    assert 'global' in meta_report['gini'].keys()
    assert 'month' in meta_report['gini'].keys()
    
    
def test_report_metrics_with_user_id_and_disbursement_date():
    sample_data, y_true, y_pred, user_id, disbursement_date = prepare_dataset()
    meta_report = credit_scoring_report(y_true, y_pred, user_id=user_id, disbursement_date=disbursement_date)
    assert list(meta_report.keys()) == ['input', 'gini']
    assert 'user_id' in meta_report['input'].columns
    assert 'disbursement_date' in meta_report['input'].columns
    assert 'month' in meta_report['input'].columns
    assert 'global' in meta_report['gini'].keys()
    assert 'month' in meta_report['gini'].keys()
    
    
def test_report_metrics_with_user_id_and_disbursement_date_include_quarterly():
    sample_data, y_true, y_pred, user_id, disbursement_date = prepare_dataset()
    meta_report = credit_scoring_report(y_true, y_pred, user_id=user_id, disbursement_date=disbursement_date)
    assert list(meta_report.keys()) == ['input', 'gini']
    assert 'user_id' in meta_report['input'].columns
    assert 'disbursement_date' in meta_report['input'].columns
    assert 'month' in meta_report['input'].columns
    assert 'global' in meta_report['gini'].keys()
    assert 'month' in meta_report['gini'].keys()

    
if __name__ == '__main__':
    test_runnable_report_metrics()
    test_report_metrics_with_user_id()
    test_report_metrics_with_disbursement_date()
    test_report_metrics_with_user_id_and_disbursement_date()
    test_report_metrics_with_user_id_and_disbursement_date_include_quarterly()