from collections import OrderedDict

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import LabelEncoder

from automl_tools.functions.utils import target_count_class, iqr_outliers, zr_score_outlier, winsorization_outliers, get_tabulate, generate_id


def get_dataset_info(train, test, target):
    t = [{"Train Row": train.shape[0],
          'Train Column': train.shape[1],
          'Test Row': test.shape[0],
          'Test Column': test.shape[1],
          'Test/Train ratio': f"{test.shape[0] / float(train.shape[0]):.2f}"
          }]
    get_tabulate(t, True)

    model_type, count_class, _ = target_count_class(train[target])

    if model_type in ("binary", "multi_class"):
        print(f"Model type: {model_type}")
        t = list()
        count = OrderedDict(train[target].value_counts().to_dict())
        for key, value in count.items():
            t_dict = {"target": key, "#_rows": value, "%_perc": f'{value / train.shape[0]:.2f}'}
            t.append(t_dict)
        get_tabulate(t)
    else:
        print(f"Model type: {model_type}")
    return True


def get_dataset_statistical(train, test, id_col, target_col):
    train[target_col] = LabelEncoder().fit_transform(train[target_col])
    total_rows = train.shape[0]

    id_columns = []
    uniques_columns = []
    date_columns = []
    missing_columns = []
    numeric_binary_columns = []
    numeric_continuous_columns = []
    numeric_discrete_columns = []
    category_binary_columns = []
    category_nominal_columns = []

    if id_col is None:
        train = generate_id(train)
        test = generate_id(test)
        id_col = "NEW_ID"
    else:
        if not int(train[id_col].value_counts().shape[0]) == int(total_rows):
            raise ValueError(f'the column {id_col} is not unique value')

    id_columns.append(id_col)

    for col in train.columns:
        if train[col].dtype == 'datetime64[ns]':
            date_columns.append(col)

    for col in train.select_dtypes('number').columns:
        if train[col].value_counts().shape[0] == 2:
            numeric_binary_columns.append(col)
        elif 2 < train[col].value_counts().shape[0] <= 50:
            numeric_continuous_columns.append(col)
        elif int(train[col].value_counts().shape[0]) == int(total_rows):
            uniques_columns.append(col)
        else:
            numeric_discrete_columns.append(col)

    for col in train.select_dtypes('category').columns:
        if train[col].value_counts().shape[0] == 2:
            category_binary_columns.append(col)
        else:
            category_nominal_columns.append(col)

    for col in list(train):
        if (len(train[col].value_counts()) == 1) | (train[col].isnull().sum() / len(train) >= 0.90):
            missing_columns.append(col)

    t = [{"ID features": len(id_columns),
          'date features': len(date_columns),
          'missing features': len(missing_columns),
          'numeric Binary features': len(numeric_binary_columns),
          'numeric continuous features': len(numeric_continuous_columns),
          'numeric discrete features': len(numeric_discrete_columns),
          'categorical Binary features': len(category_binary_columns),
          'categorical Nominal features': len(category_nominal_columns)
          }]
    get_tabulate(t, True)

    _id_train = train[id_columns[0]]
    _target = train[target_col]
    drop_all_columns = missing_columns + id_columns + date_columns + [target_col] + uniques_columns

    train.drop(drop_all_columns, axis=1, inplace=True)
    _id_test = test[id_columns[0]]
    test = test[train.columns]
    return train, test, _id_train, _id_test, _target


def get_dataset_resume_table(train, test):
    train_total_values = train.shape[0]
    test_total_values = test.shape[0]

    t = list()

    for col in train.columns:
        train_dtype = train[col].dtypes
        train_unique_list = list(train[col].unique())
        train_total_uniques = len(train[col].unique())
        train_total_missing = train[col].isnull().sum()
        train_perc_missing = np.round((100 * train[col].isnull().sum() / train_total_values), 2)
        train_entropy = round(stats.entropy(train[col].value_counts(normalize=True), base=2), 2)

        if {col}.issubset(test.columns):
            test_dtype = test[col].dtypes
            test_unique_list = list(test[col].unique())
            test_total_uniques = len(test[col].unique())
            test_total_missing = test[col].isnull().sum()
            test_perc_missing = np.round((100 * test[col].isnull().sum() / test_total_values), 2)
            test_entropy = round(stats.entropy(test[col].value_counts(normalize=True), base=2), 2)
            train_with_test_unique = len(train_unique_list) - len(set(train_unique_list).intersection(test_unique_list))
            test_with_train_unique = len(test_unique_list) - len(set(test_unique_list).intersection(train_unique_list))
        else:
            test_dtype = np.nan
            test_total_uniques = np.nan
            test_total_missing = np.nan
            test_perc_missing = np.nan
            test_entropy = np.nan
            train_with_test_unique = np.nan
            test_with_train_unique = np.nan

        t_dict = dict(
            Name=col,
            train_dtype=train_dtype, train_uniques=train_total_uniques, train_missing=train_total_missing,
            train_perc_missing=train_perc_missing, train_entropy=train_entropy,
            test_dtype=test_dtype, test_uniques=test_total_uniques, test_missing=test_total_missing,
            test_perc_missing=test_perc_missing, test_entropy=test_entropy,
            train_with_test_unique=train_with_test_unique, test_with_train_unique=test_with_train_unique)
        t.append(t_dict)

    get_tabulate(t)


def get_dataset_outlier(train, test):
    train_total_values = train.shape[0]
    test_total_values = test.shape[0]

    t = list()
    for col in train.select_dtypes('number').columns:
        train_dtype = train[col].dtypes
        train_zr_score_outlier = zr_score_outlier(train[col])
        train_winsorization_outliers = winsorization_outliers(train[col])

        if {col}.issubset(test.columns):
            test_dtype = test[col].dtypes
            test_zr_score_outlier = zr_score_outlier(test[col])
            test_winsorization_outliers = winsorization_outliers(test[col])
        else:
            test_dtype = np.nan
            test_zr_score_outlier = np.nan
            test_winsorization_outliers = np.nan

        t_dict = dict(
            Name=col,
            train_dtype=train_dtype, train_total_values=train_total_values,
            train_zrscore=train_zr_score_outlier, train_winsorizercscore=train_winsorization_outliers,
            test_dtype=test_dtype, test_total_values=test_total_values,
            test_zrscore=test_zr_score_outlier, test_winsorizercscore=test_winsorization_outliers)
        t.append(t_dict)
    get_tabulate(t)
    return True


def get_dataset_outlier_processing(train, test):
    pd.options.mode.chained_assignment = None

    for col in train.select_dtypes('number').columns:
        is_out = iqr_outliers(train[col])
        if is_out == "yes":
            first_quartile, third_quartile = np.percentile(train[col], [25, 75])
            first_percentile, ninetynine_percentile = np.percentile(train[col], [1, 99])
            iqr = third_quartile - first_quartile
            lower_bound = first_quartile - (1.5 * iqr)
            upper_bound = third_quartile + (1.5 * iqr)
            train[col].loc[train[col] > upper_bound] = ninetynine_percentile
            test[col].loc[test[col] > upper_bound] = ninetynine_percentile
            train[col].loc[train[col] < lower_bound] = first_percentile
            test[col].loc[test[col] < lower_bound] = first_percentile

    return train, test
