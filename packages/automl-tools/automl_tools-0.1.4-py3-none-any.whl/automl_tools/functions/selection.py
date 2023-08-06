import pandas as pd
import psutil
from catboost import CatBoostClassifier, CatBoostRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from ngboost import NGBClassifier, NGBRegressor
from ngboost.distns import Bernoulli
from ngboost.distns import Normal
from ngboost.distns import k_categorical
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.ensemble import ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import SGDClassifier, SGDRegressor, LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBClassifier, XGBRegressor

from automl_tools.functions.utils import target_count_class, get_tabulate


def search_model(model_name, model_type, _num_class):
    global models
    n_jobs = psutil.cpu_count(logical=False) if psutil.cpu_count(logical=False) > 0 else None
    max_depth = 6
    num_leaves = 2 ^ max_depth - 1
    if model_type in ("binary", "multi_class"):
        XGB = XGBClassifier(objective="binary:logistic", eval_metric="error",
                            use_label_encoder=False, max_depth=max_depth,
                            n_estimators=100, learning_rate=0.05)
        LGB = LGBMClassifier(objective="binary", metric="logloss", num_class=_num_class,
                             max_depth=max_depth, num_leaves=num_leaves,
                             n_estimators=100, learning_rate=0.05)
        CTB = CatBoostClassifier(loss_function="Logloss", eval_metric="AUC", verbose=0,
                                 allow_writing_files=False,
                                 max_depth=max_depth, leaf_estimation_method='Newton',
                                 thread_count=n_jobs, learning_rate=0.05)
        NGB = NGBClassifier(Dist=Bernoulli, verbose=False)

        if model_name == "XGB":
            if model_type == "multi_class":
                _objective = "multi:softprob"
                _metric = 'merror'
                XGB.set_params(objective=_objective, eval_metric=_metric)
        elif model_name == "LGB":
            if model_type == "multi_class":
                _objective = "multiclass"
                _metric = 'multi_logloss'
                LGB.set_params(objective=_objective, metric=_metric)
        elif model_name == "CTB":
            if model_type == "multi_class":
                _objective = "MultiClass"
                _metric = 'AUC'
                CTB.set_params(objective=_objective, eval_metric=_metric)
        elif model_name == "NGB":
            if model_type == "multi_class":
                _objective = k_categorical(_num_class)
                NGB.set_params(Dist=_objective)

        models = dict(
            LR=LogisticRegression(),
            RF=RandomForestClassifier(max_depth=max_depth, n_estimators=100),
            SVM=SVC(probability=True),
            LS=SGDClassifier(loss="log", penalty="l1"),
            RD=SGDClassifier(loss="log", penalty="l2"),
            NET=SGDClassifier(loss="log", penalty="elasticnet"),
            DT=DecisionTreeClassifier(max_depth=max_depth),
            ET=ExtraTreesClassifier(max_depth=max_depth, n_estimators=100),
            GB=GradientBoostingClassifier(max_depth=max_depth, n_estimators=100),
            AB=AdaBoostClassifier(n_estimators=100),
            XGB=XGB,
            LGB=LGB,
            CTB=CTB,
            NGB=NGB
        )

    if model_type == "regression":
        XGB = XGBRegressor(objective="reg:squarederror", use_label_encoder=False, max_depth=max_depth,
                           num_leaves=num_leaves, n_estimators=100, learning_rate=0.05)
        LGB = LGBMRegressor(objective="regression", max_depth=max_depth, num_leaves=num_leaves,
                            n_estimators=100, learning_rate=0.05)
        CTB = CatBoostRegressor(loss_function="RMSE", max_depth=max_depth,
                                leaf_estimation_method='Newton', learning_rate=0.05)
        NGB = NGBRegressor(Dist=Normal, verbose=False)
        models = dict(
            LR=LinearRegression(),
            RF=RandomForestRegressor(max_depth=max_depth, n_estimators=100),
            SVM=SVR(kernel='rbf'),
            LS=SGDRegressor(loss="log", penalty="l1"),
            RD=SGDRegressor(loss="log", penalty="l2"),
            NET=SGDRegressor(loss="log", penalty="elasticnet"),
            DT=DecisionTreeRegressor(max_depth=max_depth),
            ET=ExtraTreesRegressor(max_depth=max_depth, n_estimators=100),
            GB=GradientBoostingRegressor(max_depth=max_depth, n_estimators=100),
            AB=AdaBoostRegressor(n_estimators=100),
            XGB=XGB,
            LGB=LGB,
            CTB=CTB,
            NGB=NGB
        )

    clf = models[model_name]
    return clf


def model_selection_support(train, target, model_names, model_type, _num_class):
    x_train, x_val, y_train, y_val = train_test_split(train, target, test_size=0.20, random_state=2021)

    feat_labels = train.columns.tolist()
    global model_based, clf
    selection_list = list()
    feature_name = list()

    for model_name in model_names:

        if model_type in ("binary", "multi_class"):
            clf = search_model(model_name, model_type, _num_class)
            model_based = SelectFromModel(clf, threshold='median')
        if model_type == "regression":
            clf = search_model(model_name, model_type, _num_class)
            model_based = SelectFromModel(clf, threshold='median')

        if model_name in "NGB":
            model_based.fit(x_train, y_train)
        else:
            model_based.fit_transform(x_train, y_train)

        feature_name += [feat_labels[col] for col in model_based.get_support(indices=True)]

        selection_dict = dict()
        for col in train.columns:
            if str(col) in feature_name:
                selection_dict[col] = "YES"
            else:
                selection_dict[col] = "NO"
        selection_dict["model_name"] = model_name
        selection_list.append(selection_dict)

    feature_name = list(set(feature_name))
    feature_count = len(feature_name)
    return selection_list, feature_name, feature_count


def get_dataset_feature_selection(train, target, model_names):
    model_type, _num_class, _ = target_count_class(target)
    selection_list, feature_name, feature_count = model_selection_support(train, target, model_names, model_type, _num_class)
    df = pd.DataFrame(selection_list)
    df2 = df.set_index("model_name")

    get_tabulate(df2)

    print(f"Number feature selection: {feature_count}")
    return feature_name
