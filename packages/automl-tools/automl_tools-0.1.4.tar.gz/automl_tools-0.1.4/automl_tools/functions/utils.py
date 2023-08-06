from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.core.display import display
from scipy import stats
from sklearn.metrics import roc_auc_score, roc_curve, average_precision_score, precision_recall_curve, confusion_matrix


def get_seed():
    return 2021


def get_tabulate(t, transpose=False):
    t = pd.DataFrame(t)
    if transpose:
        display(t.T)
    else:
        display(t)
    return True


def zr_score_outlier(df):
    out = list()
    med = np.median(df)
    ma = stats.median_absolute_deviation(df)
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
    out = list()
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
    out = list()
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    iqr = q3 - q1
    lower_tail = q1 - 1.5 * iqr
    upper_tail = q3 + 1.5 * iqr
    for i in df:
        if i > upper_tail or i < lower_tail:
            out.append(i)
    if len(out) > 0:
        has_out = "yes"
    else:
        has_out = "no"
    return has_out


def winsorization_outliers(df):
    out = list()
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


def reduce_memory(dataset, verbose=False):
    start_mem = dataset.memory_usage().sum() / 1024 ** 2
    int_columns = dataset.select_dtypes(include=[np.int8, np.int16, np.int32, np.int64]).columns.tolist()
    for col in int_columns:
        dataset[col] = pd.to_numeric(arg=dataset[col], downcast='integer')

    float_columns = dataset.select_dtypes(include=[np.float32, np.float64]).columns.tolist()
    for col in float_columns:
        dataset[col] = pd.to_numeric(arg=dataset[col], downcast='float')

    end_mem = dataset.memory_usage().sum() / 1024 ** 2
    dataset = clean_inf_nan(dataset)
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f} % reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return dataset


def generate_id(dataset):
    dataset.insert(0, 'NEW_ID', range(1, 1 + len(dataset)))
    return dataset


def find_optimal_cutoff(target, predicted):
    fpr, tpr, threshold = roc_curve(target, predicted)
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'tf': pd.Series(tpr - (1 - fpr), index=i), 'threshold': pd.Series(threshold, index=i)})
    roc_t = roc.iloc[(roc.tf - 0).abs().argsort()[:1]]
    return list(roc_t['threshold'])


def target_count_class(target):
    df = pd.DataFrame()
    df["target"] = target
    name_classes = list(sorted(df["target"].value_counts().to_dict().keys()))
    name_class = [f"class {cls}" for cls in name_classes]
    count_class = len(name_class)
    if count_class == 2:
        count_class = 1
        model_type = "binary"
    elif 2 < count_class <= 10:
        model_type = "multi_class"
    else:
        model_type = "regression"
    return model_type, count_class, name_class


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


def display_importance(feature_importance_, model_name):
    cols = feature_importance_[["feature", "importance"]].groupby("feature").mean() \
               .sort_values(by="importance", ascending=False)[:50].index
    best_features = feature_importance_.loc[feature_importance_.feature.isin(cols)]
    plt.figure(figsize=(8, 10))
    sns.barplot(x="importance", y="feature",
                data=best_features.sort_values(by="importance", ascending=False))
    plt.title(f'{model_name} Features (avg over folds)')
    plt.tight_layout()
    plt.savefig(f'{model_name}_importance.png')
    plt.show()


def ks_report(data=None, target=None, prob=None):
    data['target0'] = 1 - data[target]
    data['bucket'] = pd.qcut(data[prob], 10)
    grouped = data.groupby('bucket', as_index=False)
    ks_table = pd.DataFrame()
    ks_table['min_prob'] = grouped.min()[prob]
    ks_table['max_prob'] = grouped.max()[prob]
    ks_table['events'] = grouped.sum()[target]
    ks_table['nonevents'] = grouped.sum()['target0']
    ks_table = ks_table.sort_values(by="min_prob", ascending=False).reset_index(drop=True)
    ks_table['event_rate'] = (ks_table.events / data[target].sum()).apply('{0:.2%}'.format)
    ks_table['nonevent_rate'] = (ks_table.nonevents / data['target0'].sum()).apply('{0:.2%}'.format)
    ks_table['cum_event_rate'] = (ks_table.events / data[target].sum()).cumsum()
    ks_table['cum_nonevent_rate'] = (ks_table.nonevents / data['target0'].sum()).cumsum()
    ks_table['KS'] = np.round(ks_table['cum_event_rate'] - ks_table['cum_nonevent_rate'], 3) * 100

    # formatting
    ks_table['cum_event_rate'] = ks_table['cum_event_rate'].apply('{0:.2%}'.format)
    ks_table['cum_nonevent_rate'] = ks_table['cum_nonevent_rate'].apply('{0:.2%}'.format)
    ks_table.index = range(1, 11)
    ks_table.index.rename('Decile', inplace=True)

    # display KS
    from colorama import Fore
    print(Fore.RED + "KS is " + str(max(ks_table['KS'])) + "%" + " at decile " + str((ks_table.index[ks_table['KS'] == max(ks_table['KS'])][0])))
    return ks_table


def display_confusion_matrix(y_, oof_preds_, labels=None,
                             threshold=None, normalize=False, model_name=None):
    plt.figure(figsize=(6, 6))
    plt.rcParams["axes.grid"] = False
    color_bar = False
    if labels is None:
        labels = ["class 0", "class 1"]
    if threshold is None:
        threshold = 0.5
        name = "default"
    else:
        name = "optimal"

    y_pred_class = [1 if y > threshold else 0 for y in oof_preds_]

    cm = confusion_matrix(y_, y_pred_class, labels=[0, 1])

    title = 'Confusion matrix'
    matrix_name = "confusion_matrix"
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        title = 'Confusion matrix normalized'
        matrix_name = "confusion_matrix_normalized"

    plt.imshow(cm, cmap=plt.cm.gray_r)
    plt.title(title)
    if color_bar:
        plt.colorbar()

    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45, fontsize="18")
    plt.yticks(tick_marks, labels, fontsize="18")

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.

    for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black", fontsize=16)

    plt.ylabel('Target label', fontsize=18)
    plt.xlabel('Predicted label', fontsize=18)
    plt.tight_layout()
    plt.savefig(f'{model_name}_{matrix_name}_{name}.png')
    plt.show()
