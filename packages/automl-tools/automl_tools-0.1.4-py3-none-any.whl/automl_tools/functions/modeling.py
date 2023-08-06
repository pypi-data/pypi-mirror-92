import gc

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from automl_tools.functions.selection import search_model
from automl_tools.functions.utils import target_count_class, find_optimal_cutoff


def augment(x, y, t=2):
    xs, xn = [], []
    for i in range(t):
        mask = y > 0
        x1 = x[mask].copy()
        ids = np.arange(x1.shape[0])
        for c in range(x1.shape[1]):
            np.random.shuffle(ids)
            x1[:, c] = x1[ids][:, c]
        xs.append(x1)

    for i in range(t // 2):
        mask = y == 0
        x1 = x[mask].copy()
        ids = np.arange(x1.shape[0])
        for c in range(x1.shape[1]):
            np.random.shuffle(ids)
            x1[:, c] = x1[ids][:, c]
        xn.append(x1)

    xs = np.vstack(xs)
    xn = np.vstack(xn)
    ys = np.ones(xs.shape[0])
    yn = np.zeros(xn.shape[0])
    x = np.vstack([x, xs, xn])
    y = np.concatenate([y, ys, yn])
    return x, y


def run_model(train_df, test_df, target, id_train, id_test, folds_,
              augmentation, feature_name, model_name, best_parameter_tuning):
    oof_preds = np.zeros(train_df.shape[0])
    sub_preds = np.zeros(test_df.shape[0])
    feature_importance_df = pd.DataFrame()

    rs_dict = dict()
    feats = [col for col in train_df.columns if col in feature_name]
    model_type, _num_class, _name_class = target_count_class(target)
    _clf = search_model(model_name, model_type, _num_class)

    for n_fold, (trn_idx, val_idx) in enumerate(folds_.split(train_df, target)):
        trn_x, trn_y = train_df[feats].iloc[trn_idx], target.iloc[trn_idx]
        val_x, val_y = train_df[feats].iloc[val_idx], target.iloc[val_idx]

        if augmentation:
            trn_x, trn_y = augment(trn_x.values, trn_y.values)
            trn_x = pd.DataFrame(trn_x)

        clf = _clf.set_params(**best_parameter_tuning)

        clf.fit(trn_x, trn_y)

        oof_preds[val_idx] = clf.predict_proba(val_x)[:, 1]
        sub_preds += clf.predict_proba(test_df[feats])[:, 1] / folds_.n_splits

        fold_importance_df = pd.DataFrame()
        fold_importance_df["feature"] = feats
        if model_name == "SVM":
            fold_importance_df["importance"] = clf.coef0
        elif model_name == "LR":
            fold_importance_df["importance"] = clf.coef_[0]
        elif model_name == "NGB":
            fold_importance_df["importance"] = clf.feature_importances_[0]
        else:
            fold_importance_df["importance"] = clf.feature_importances_
        fold_importance_df["fold"] = n_fold + 1
        feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)

        print(f'Fold {n_fold + 1:2d} auc : {roc_auc_score(val_y, oof_preds[val_idx]):.6f}')
        print(f'Fold {n_fold + 1:2d} cutoff : {find_optimal_cutoff(val_y, oof_preds[val_idx])}')

        del clf, trn_x, trn_y, val_x, val_y
        gc.collect()

    print('full auc score {:.6f}'.format(roc_auc_score(target, oof_preds)))
    print("full cutoff optimal: {0}".format(find_optimal_cutoff(target, oof_preds)))

    test_df['target'] = sub_preds

    df_oof_train_preds = pd.DataFrame({'id_code': id_train, 'target': target, 'prediction': oof_preds})
    df_oof_test_preds = pd.DataFrame({'id_code': id_test, 'prediction': sub_preds})
    folds_idx = [(trn_idx, val_idx) for trn_idx, val_idx in folds_.split(train_df, target)]

    rs_dict["oof_preds"] = oof_preds
    rs_dict["oof_train_preds"] = df_oof_train_preds
    rs_dict["oof_test_preds"] = df_oof_test_preds
    rs_dict["feature_importance_"] = feature_importance_df
    rs_dict["score"] = roc_auc_score(target, oof_preds)
    rs_dict["model_type"] = model_type
    rs_dict["num_class"] = _num_class
    rs_dict["name_class"] = _name_class
    rs_dict["full_auc_score"] = round(roc_auc_score(target, oof_preds), 4)
    rs_dict["cutoff_optimal"] = find_optimal_cutoff(target, oof_preds)
    rs_dict["folds_idx"] = folds_idx

    return rs_dict
