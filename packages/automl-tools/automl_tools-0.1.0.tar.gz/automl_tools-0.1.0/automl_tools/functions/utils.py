import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.core.display import display
from sklearn.metrics import roc_auc_score, roc_curve, average_precision_score, precision_recall_curve


def get_tabulate(t, transpose=False):
    t = pd.DataFrame(t)
    if transpose:
        display(t.T)
    else:
        display(t)
    return True


def zr_score_outlier(df):
    out = []
    med = np.median(df)
    for i in df:
        try:
            z = (0.6745 * (i - med)) / (np.median(ma))
        except:
            z = 0
        if np.abs(z) > 3:
            out.append(i)
    if len(out) > 0:
        has_out = "yes"
    else:
        has_out = "no"
    return has_out


def z_score_outlier(df):
    out = []
    m = np.mean(df)
    sd = np.std(df)
    for i in df:
        z = (i - m) / sd
        if np.abs(z) > 3:
            out.append(i)
    if len(out) > 0:
        has_out = "yes"
    else:
        has_out = "no"
    return has_out


def iqr_outliers(df):
    out = []
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    iqr = q3 - q1
    Lower_tail = q1 - 1.5 * iqr
    Upper_tail = q3 + 1.5 * iqr
    for i in df:
        if i > Upper_tail or i < Lower_tail:
            out.append(i)
    if len(out) > 0:
        has_out = "yes"
    else:
        has_out = "no"
    return has_out


def winsorization_outliers(df):
    out = []
    q1 = np.percentile(df, 1)
    q3 = np.percentile(df, 99)
    for i in df:
        if i > q3 or i < q1:
            out.append(i)
    if len(out) > 0:
        has_out = "yes"
    else:
        has_out = "no"
    return has_out


def clean_inf_nan(df):
    return df.replace([np.inf, -np.inf], np.nan)


def reduce_memory(dataset, verbose=True):
    ds_tmp = dataset.copy()
    start_mem = ds_tmp.memory_usage().sum() / 1024 ** 2
    int_columns = ds_tmp.select_dtypes(include=[np.int8, np.int16, np.int32, np.int64]).columns.tolist()
    for col in int_columns:
        ds_tmp[col] = pd.to_numeric(arg=ds_tmp[col], downcast='integer')

    float_columns = ds_tmp.select_dtypes(include=[np.float32, np.float64]).columns.tolist()
    for col in float_columns:
        ds_tmp[col] = pd.to_numeric(arg=ds_tmp[col], downcast='float')

    end_mem = ds_tmp.memory_usage().sum() / 1024 ** 2
    ds_tmp = clean_inf_nan(ds_tmp)
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f} % reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    del dataset
    return ds_tmp


def find_optimal_cutoff(target, predicted):
    fpr, tpr, threshold = roc_curve(target, predicted)
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'tf': pd.Series(tpr - (1 - fpr), index=i), 'threshold': pd.Series(threshold, index=i)})
    roc_t = roc.iloc[(roc.tf - 0).abs().argsort()[:1]]
    return list(roc_t['threshold'])


def target_count_class(target):
    df = pd.DataFrame()
    df["target"] = target
    count_class = list(sorted(df["target"].value_counts().to_dict().keys()))
    count_class = len(count_class)
    if count_class == 2:
        count_class = 1
        model_type = "binary"
    elif 2 < count_class <= 10:
        model_type = "multi_class"
    else:
        model_type = "regression"
    return model_type, count_class


def display_roc_curve(y_, oof_preds_, folds_idx_, model_name):
    plt.figure(figsize=(6, 6))
    scores = []
    for n_fold, (_, val_idx) in enumerate(folds_idx_):
        fpr, tpr, thresholds = roc_curve(y_.iloc[val_idx], oof_preds_[val_idx])
        score = roc_auc_score(y_.iloc[val_idx], oof_preds_[val_idx])
        scores.append(score)
        plt.plot(fpr, tpr, lw=1, alpha=0.3, label='ROC fold %d (AUC = %0.4f)' % (n_fold + 1, score))

    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Luck', alpha=.8)
    fpr, tpr, thresholds = roc_curve(y_, oof_preds_)
    score = roc_auc_score(y_, oof_preds_)
    plt.plot(fpr, tpr, color='b', label=f'avg roc auc = {score:0.4f} $\pm$ {np.std(scores):0.4f})', lw=2, alpha=.8)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'{model_name.upper()} ROC CURVE')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(f'roc_curve_{model_name}.png')
    plt.show()


def display_precision_recall(y_, oof_preds_, folds_idx_, model_name):
    plt.figure(figsize=(6, 6))
    scores = []
    for n_fold, (_, val_idx) in enumerate(folds_idx_):
        fpr, tpr, thresholds = roc_curve(y_.iloc[val_idx], oof_preds_[val_idx])
        score = average_precision_score(y_.iloc[val_idx], oof_preds_[val_idx])
        scores.append(score)
        plt.plot(fpr, tpr, lw=1, alpha=0.3, label='AP fold %d (auc = %0.4f)' % (n_fold + 1, score))

    precision, recall, thresholds = precision_recall_curve(y_, oof_preds_)
    score = average_precision_score(y_, oof_preds_)
    plt.plot(precision, recall, color='b', lw=2, alpha=.8,
             label=f'avg roc (auc = {score:0.4f} $\pm$ {np.std(scores):0.4f})')

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(f'{model_name} Recall / Precision')
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(f'recall_precision_curve_{model_name}.png')
    plt.show()


def display_importances(feature_importance_df_, model_name):
    cols = feature_importance_df_[["feature", "importance"]].groupby("feature").mean() \
               .sort_values(by="importance", ascending=False)[:50].index
    best_features = feature_importance_df_.loc[feature_importance_df_.feature.isin(cols)]
    plt.figure(figsize=(8, 10))
    sns.barplot(x="importance", y="feature", data=best_features.sort_values(by="importance", ascending=False))
    plt.title(f'{model_name} Features (avg over folds)')
    plt.tight_layout()
    plt.savefig(f'{model_name}_importances.png')
    plt.show()


def ks_report(data=None, target=None, prob=None):
    data['target0'] = 1 - data[target]
    data['bucket'] = pd.qcut(data[prob], 10)
    grouped = data.groupby('bucket', as_index=False)
    kstable = pd.DataFrame()
    kstable['min_prob'] = grouped.min()[prob]
    kstable['max_prob'] = grouped.max()[prob]
    kstable['events'] = grouped.sum()[target]
    kstable['nonevents'] = grouped.sum()['target0']
    kstable = kstable.sort_values(by="min_prob", ascending=False).reset_index(drop=True)
    kstable['event_rate'] = (kstable.events / data[target].sum()).apply('{0:.2%}'.format)
    kstable['nonevent_rate'] = (kstable.nonevents / data['target0'].sum()).apply('{0:.2%}'.format)
    kstable['cum_eventrate'] = (kstable.events / data[target].sum()).cumsum()
    kstable['cum_noneventrate'] = (kstable.nonevents / data['target0'].sum()).cumsum()
    kstable['KS'] = np.round(kstable['cum_eventrate'] - kstable['cum_noneventrate'], 3) * 100

    # Formating
    kstable['cum_eventrate'] = kstable['cum_eventrate'].apply('{0:.2%}'.format)
    kstable['cum_noneventrate'] = kstable['cum_noneventrate'].apply('{0:.2%}'.format)
    kstable.index = range(1, 11)
    kstable.index.rename('Decile', inplace=True)

    # Display KS
    from colorama import Fore
    print(Fore.RED + "KS is " + str(max(kstable['KS'])) + "%" + " at decile " + str((kstable.index[kstable['KS'] == max(kstable['KS'])][0])))
    return kstable
