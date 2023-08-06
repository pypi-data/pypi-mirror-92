import numpy as np
from prettytable import PrettyTable
from scipy import stats


def get_dataset_remove_low_information(train, test):
    # remove quasi constant
    t = PrettyTable()
    t.field_names = ['Quasi Variable']
    quasi_cols_remove = list()
    for col in train.columns:
        if train[col].std() == 0:
            quasi_cols_remove.append(col)

    t = PrettyTable()
    t.field_names = ['Column Quasi']
    if len(quasi_cols_remove) > 0:
        for col in quasi_cols_remove:
            t.add_row([col])
    else:
        t.add_row(["NOT VARIABLES QUASI"])
    print(t)

    # remove duplicate columns
    groups = train.columns.to_series().groupby(train.dtypes).groups
    duplicate_cols_remove = list()
    for t, v in groups.items():
        cs = train[v].columns
        vs = train[v]
        lcs = len(cs)
        for i in range(lcs):
            ia = vs.iloc[:, i].values
            for j in range(i + 1, lcs):
                ja = vs.iloc[:, j].values
                if np.array_equal(ia, ja):
                    duplicate_cols_remove.append(cs[i])
                    break

    t = PrettyTable()
    t.field_names = ['Column Duplicates']
    if len(duplicate_cols_remove) > 0:
        for col in duplicate_cols_remove:
            t.add_row([col])
    else:
        t.add_row(["NOT VARIABLES DUPLICATES"])
    print(t)

    # drop sparse columns
    flist = [x for x in train.columns]
    sparse_cols_remove = list()
    for col in flist:
        if len(np.unique(train[col])) < 2:
            sparse_cols_remove.append(col)

    t = PrettyTable()
    t.field_names = ['Column Sparse']
    if len(sparse_cols_remove) > 0:
        for col in sparse_cols_remove:
            t.add_row([col])
    else:
        t.add_row(["NOT VARIABLES SPARSE"])
    print(t)

    drop_all_columns = quasi_cols_remove + duplicate_cols_remove + sparse_cols_remove

    train.drop(drop_all_columns, axis=1, inplace=True)
    test.drop(drop_all_columns, axis=1, inplace=True)
    return train, test


def get_dataset_remove_correlation(train, test, target, threshold=0.95):
    drop_all_columns = list()

    for col in train.columns:
        value = stats.spearmanr(train[col].values, target.values)[0]
        if abs(value) > threshold:
            drop_all_columns.append(col)

    t = PrettyTable()
    t.field_names = ['Column Correlations']
    if len(drop_all_columns) > 0:
        for col in drop_all_columns:
            t.add_row([col])
    else:
        t.add_row(["NOT VARIABLES CORRELATIONS"])
    print(t)

    train.drop(drop_all_columns, axis=1, inplace=True)
    test.drop(drop_all_columns, axis=1, inplace=True)
    return train, test
