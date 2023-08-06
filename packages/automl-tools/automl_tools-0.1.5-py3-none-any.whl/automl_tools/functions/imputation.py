import numpy as np
import pandas as pd
from category_encoders.cat_boost import CatBoostEncoder
from optbinning import BinningProcess, MulticlassOptimalBinning
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

from automl_tools.functions.utils import target_count_class, get_seed


def optimize_impute_knn(df, variable, target):
    rmse = lambda y, yhat: np.sqrt(mean_squared_error(y, yhat))

    errors_list = list()
    for k in range(1, 20, 2):
        imputer = KNNImputer(n_neighbors=k)
        imputed = imputer.fit_transform(df[variable].values.reshape(-1, 1))
        df_imputed = pd.DataFrame(imputed, columns=[variable])

        X = df_imputed
        y = target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=get_seed())
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        error = rmse(y_test, preds)
        errors_list.append({'K': k, 'RMSE': error})
    optimal_k = min(errors_list, key=lambda x: x['RMSE'])
    return optimal_k["K"], errors_list


def impute_na(df_train, df_test, target,
              _type_numerical="gaussian",
              _type_categorical="knn"):
    def encoder_data(df):
        var_ord_enc = OrdinalEncoder()
        _var = df[col]
        _var_not_null = _var[_var.notnull()]
        _reshaped_vals = _var_not_null.values.reshape(-1, 1)
        _encoded_vals = var_ord_enc.fit_transform(_reshaped_vals)
        df.loc[_var.notnull(), col] = np.squeeze(_encoded_vals)
        return df, var_ord_enc

    for col in df_train.columns:
        if df_train[col].isnull().sum() > 0:
            if is_numeric_dtype(df_train[col]):

                if _type_numerical == "gaussian":
                    train_new_value = df_train[col].mean() + 3 * df_train[col].std()
                    test_new_value = df_test[col].mean() + 3 * df_test[col].std()
                    df_train[f'{col}_imputed'] = df_train[col].fillna(train_new_value)
                    df_test[f'{col}_imputed'] = df_test[col].fillna(test_new_value)

                elif _type_numerical == "arbitrary":
                    train_new_value = -999
                    test_new_value = -999
                    df_train[f'{col}_imputed'] = df_train[col].fillna(train_new_value)
                    df_test[f'{col}_imputed'] = df_test[col].fillna(test_new_value)

                elif _type_numerical == "median":
                    train_new_value = df_train[col].median()
                    test_new_value = df_test[col].median()
                    df_train[f'{col}_imputed'] = df_train[col].fillna(train_new_value)
                    df_test[f'{col}_imputed'] = df_test[col].fillna(test_new_value)

                elif _type_numerical == "mean":
                    train_new_value = df_train[col].mean()
                    test_new_value = df_test[col].mean()
                    df_train[f'{col}_imputed'] = df_train[col].fillna(train_new_value)
                    df_test[f'{col}_imputed'] = df_test[col].fillna(test_new_value)

                elif _type_numerical == "random":
                    train_random_sample = df_train[col].dropna().sample(df_train[col].isnull().sum(), random_state=2021)
                    test_random_sample = df_test[col].dropna().sample(df_test[col].isnull().sum(), random_state=2021)
                    df_train[f'{col}_imputed'] = np.where(df_train[col].isnull(), train_random_sample, df_train[col])
                    df_test[f'{col}_imputed'] = np.where(df_test[col].isnull(), test_random_sample, df_test[col])

                elif _type_numerical == "knn":
                    optimal_k, _ = optimize_impute_knn(df_train, col, target)
                    train_new_value = df_train[col]
                    test_new_value = df_test[col]
                    imputer = KNNImputer(n_neighbors=optimal_k)
                    train_imputed = imputer.fit_transform(train_new_value.values.reshape(-1, 1))
                    test_imputed = imputer.fit_transform(test_new_value.values.reshape(-1, 1))

                    df_train[f'{col}_imputed'] = pd.DataFrame(train_imputed)
                    df_test[f'{col}_imputed'] = pd.DataFrame(test_imputed)


            elif is_string_dtype(df_train[col]):

                if _type_categorical == "frequent":
                    train_new_value = df_train[col].mode()
                    test_new_value = df_test[col].mode()
                    df_train[f'{col}_imputed'] = df_train[col].fillna(train_new_value)
                    df_test[f'{col}_imputed'] = df_test[col].fillna(test_new_value)

                elif _type_categorical == "constant":
                    train_new_value = "missing"
                    test_new_value = "missing"
                    df_train[f'{col}_imputed'] = df_train[col].fillna(train_new_value)
                    df_test[f'{col}_imputed'] = df_test[col].fillna(test_new_value)

                elif _type_categorical == "rare":
                    _df_train = pd.DataFrame()
                    _df_train[col] = df_train[col]
                    total_houses = len(_df_train)
                    temp_df = pd.Series(_df_train[col].value_counts() / total_houses)
                    grouping_dict = {
                        k: ('rare' if k not in temp_df[temp_df >= 0.05].index else k)
                        for k in temp_df.index
                    }
                    df_train[f'{col}_imputed'] = df_train[col].map(grouping_dict)
                    df_test[f'{col}_imputed'] = df_test[col].map(grouping_dict)

                elif _type_categorical == "knn":
                    _df_train, _df_test = pd.DataFrame(), pd.DataFrame()
                    _df_train[col] = df_train[col]
                    _df_test[col] = df_test[col]

                    _df_train, var_ord_enc = encoder_data(_df_train)
                    _df_test, _ = encoder_data(_df_test)

                    optimal_k, _ = optimize_impute_knn(_df_train, col, target)
                    train_new_value = _df_train[col].copy()
                    test_new_value = _df_test[col].copy()
                    imputer = KNNImputer(n_neighbors=optimal_k)
                    train_imputed = imputer.fit_transform(train_new_value.values.reshape(-1, 1))
                    # train_inverse_imputed = var_ord_enc.inverse_transform(train_imputed)
                    test_imputed = imputer.fit_transform(test_new_value.values.reshape(-1, 1))
                    # test_inverse_imputed = var_ord_enc.inverse_transform(test_imputed)

                    df_train[f'{col}_imputed'] = pd.DataFrame(train_imputed)
                    df_test[f'{col}_imputed'] = pd.DataFrame(test_imputed)

    return df_train, df_test


def get_dataset_missing_processing(train, test, target, imp_num, imp_cat):
    train, test = impute_na(df_train=train, df_test=test,
                            target=target,
                            _type_numerical=imp_num,
                            _type_categorical=imp_cat)
    drop_all_columns = [str(col).split("_")[0] for col in train.columns.tolist() if str(col).endswith("_imputed")]

    cat_cols = [col for col in train.select_dtypes(include=['object']).columns]

    cbe_encoder = CatBoostEncoder()
    for col in cat_cols:
        train[col] = cbe_encoder.fit_transform(train[col], target)
        test[col] = cbe_encoder.transform(test[col])

    train.drop(drop_all_columns, axis=1, inplace=True)
    test.drop(drop_all_columns, axis=1, inplace=True)
    return train, test


def get_dataset_binding_processing(train, test, target, processing):
    model_type, _, _ = target_count_class(target)
    if processing == "binding":
        metric = "indices"
    else:
        metric = "woe"

    if str(model_type) == "binary":
        num_cols = [col for col in train.select_dtypes(include=['number']).columns]
        cat_cols = [col for col in train.select_dtypes(include=['object']).columns]
        all_var = num_cols + cat_cols
        X = train[all_var]
        y = target
        binning_process = BinningProcess(variable_names=all_var,
                                         categorical_variables=cat_cols)
        binning_process.fit(X, y)
        var_list = list(binning_process.get_support(names=True))
        for col in var_list:
            optb = binning_process.get_binned_variable(col)
            train_transform_indices = optb.transform(train[col].values, metric=metric)
            test_transform_indices = optb.transform(test[col].values, metric=metric)
            train[f'{col}_bin'] = train_transform_indices
            test[f'{col}_bin'] = test_transform_indices
            del train[col]
            del test[col]

    elif str(model_type) == "multi_class":
        y = target
        for col in train.columns:
            optb = MulticlassOptimalBinning(name=col, solver="mip")
            optb.fit(train[col], y)
            train_transform_indices = optb.transform(train[col].values, metric=metric)
            test_transform_indices = optb.transform(test[col].values, metric=metric)
            train[f'{col}_bin'] = train_transform_indices
            test[f'{col}_bin'] = test_transform_indices
            del train[col]
            del test[col]

    return train, test
