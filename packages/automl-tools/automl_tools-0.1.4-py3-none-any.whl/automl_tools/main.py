import pandas as pd
from sklearn.model_selection import StratifiedKFold, KFold

from automl_tools.functions.imputation import get_dataset_missing_processing, get_dataset_binding_processing
from automl_tools.functions.logger import seed_everything, get_stage, get_logger
from automl_tools.functions.modeling import run_model
from automl_tools.functions.optimization import get_dataset_parameter_baseline
from automl_tools.functions.prepare import get_dataset_remove_low_information, get_dataset_remove_correlation
from automl_tools.functions.processing import get_dataset_info, get_dataset_resume_table, get_dataset_statistical, get_dataset_outlier, get_dataset_outlier_processing
from automl_tools.functions.selection import get_dataset_feature_selection
from automl_tools.functions.utils import reduce_memory, display_importance, display_roc_curve, display_precision_recall, ks_report, display_confusion_matrix, get_seed

logger = get_logger()


def automl_run(train=pd.DataFrame,
               test=pd.DataFrame,
               id_col=None,
               target_col="target",
               imp_num="knn",
               imp_cat="knn",
               processing=None,
               mutual_information=False,
               correlation_drop=False,
               model_feature_selection=None,
               model_run="LR",
               augmentation=False,
               Stratified=True,
               cv=5):
    """
    :type train: DataFrame
    :type test: DataFrame
    :type id_col: String -> Default: None
    :type target_col: String
    :type imp_num: String ["gaussian", "arbitrary", "median", "mean", "random", "knn"] -> Default: "knn"
    :type imp_cat: String ["frequent", "constant", "rare", "knn"] -> Default: "knn"
    :type processing: String : ["woe", "binding" ]-> Default: False
    :type mutual_information: Boolean : [True, False]-> Default: False
    :type correlation_drop: Boolean : [True, False]-> Default: False
    :type model_feature_selection: List :
        paramter:
            binary:
                  LR  : LogisticRegression
                  RF  : RandomForestClassifier
                  SVM : SVC
                  LS  : LASSO
                  RD  : RIDGE
                  NET : Elasticnet
                  DT  : DecisionTreeClassifier
                  ET  : ExtraTreesClassifier
                  GB  : GradientBoostingClassifier
                  AB  : AdaBoostClassifier
                  XGB  : XGBClassifier
                  LGB  : LGBMClassifier
                  CTB  : CatBoostClassifier
                  NGB  : NGBClassifier
        Default: ["LR", "RF", "LGB"]

    :type model_run: String :
        paramter:
            binary:
                  LR  : LogisticRegression
                  RF  : RandomForestClassifier
                  SVM : SVC
                  LS  : LASSO
                  RD  : RIDGE
                  NET : Elasticnet
                  DT  : DecisionTreeClassifier
                  ET  : ExtraTreesClassifier
                  GB  : GradientBoostingClassifier
                  AB  : AdaBoostClassifier
                  XGB  : XGBClassifier
                  LGB  : LGBMClassifier
                  CTB  : CatBoostClassifier
                  NGB  : NGBClassifier
        Default: ["RF"]
    :type augmentation: Boolean : [True, False]-> Default: False
    :type Stratified: Boolean : [True, False]-> Default: True
    :type cv: Integer : Default: 5
    """

    if model_feature_selection is None:
        model_feature_selection = ["LR", "RF", "LGB"]
    assert type(model_feature_selection) == list
    if 0 < len(model_feature_selection) <= 3:
        print(f"Model selection variables default: {model_feature_selection}")
    else:
        print(f"model_feature_selection required min 1 parameter and max 3")

    seed_everything()

    train = reduce_memory(train)
    test = reduce_memory(test)
    get_stage(0)
    get_stage(1)
    logger.info('Load processing')
    get_dataset_info(train, test, target_col)

    get_stage(2)
    _train, _test, _id_train, _id_test, _target = get_dataset_statistical(train, test, id_col, target_col)
    get_stage(3)
    get_dataset_resume_table(train, test)

    get_stage(4)
    get_stage(5)
    get_dataset_outlier(_train, _test)

    get_stage(6)
    _train, _test = get_dataset_outlier_processing(_train, _test)
    get_dataset_outlier(_train, _test)

    get_stage(7)
    logger.info('Load imputation')
    _train, _test = get_dataset_missing_processing(_train, _test, _target, imp_num=imp_num, imp_cat=imp_cat)
    get_dataset_resume_table(_train, _test)

    if processing:
        get_stage(9)
        _train, _test = get_dataset_binding_processing(_train, _test, _target, processing)
        get_dataset_outlier(_train, _test)

    logger.info('Load prepare data')
    if mutual_information:
        get_stage(10)
        _train, _test = get_dataset_remove_low_information(_train, _test)

    if correlation_drop:
        _train, _test = get_dataset_remove_correlation(_train, _test, _target, threshold=0.70)

    get_stage(11)
    get_stage(12)
    logger.info('Load feature selection')
    feature_name = get_dataset_feature_selection(_train, _target, model_names=model_feature_selection)

    get_stage(13)
    get_stage(14)
    logger.info('Load feature optimization')
    best_parameter_tuning = get_dataset_parameter_baseline(_train, _target, feature_name, model_run)

    get_stage(15)
    logger.info('Load cross-validation')
    if Stratified:
        folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=get_seed())
    else:
        folds = KFold(n_splits=cv, shuffle=True, random_state=get_seed())

    logger.info('Load run model')
    model_dict = run_model(_train, _test, _target, _id_train, _id_test, folds, augmentation,
                           feature_name, model_run, best_parameter_tuning)

    logger.info('generate report')
    display_importance(feature_importance_=model_dict.get("feature_importance_"),
                       model_name=model_run)

    display_roc_curve(y_=_target,
                      oof_preds_=model_dict.get("oof_preds"),
                      folds_idx_=model_dict.get("folds_idx"),
                      model_name=model_run)
    display_precision_recall(y_=_target,
                             oof_preds_=model_dict.get("oof_preds"),
                             folds_idx_=model_dict.get("folds_idx"),
                             model_name=model_run)

    display_confusion_matrix(y_=_target,
                             oof_preds_=model_dict.get("oof_preds"),
                             labels=model_dict.get("name_class"),
                             threshold=None,
                             normalize=False,
                             model_name=model_run)

    display_confusion_matrix(y_=_target,
                             oof_preds_=model_dict.get("oof_preds"),
                             labels=model_dict.get("name_class"),
                             threshold=model_dict.get("cutoff_optimal")[0],
                             normalize=False,
                             model_name=model_run)

    display_confusion_matrix(y_=_target,
                             oof_preds_=model_dict.get("oof_preds"),
                             labels=model_dict.get("name_class"),
                             threshold=model_dict.get("cutoff_optimal")[0],
                             normalize=True,
                             model_name=model_run)

    model_dict.get("oof_train_preds").to_csv("trained.csv", index=False)
    model_dict.get("oof_test_preds").to_csv("submission.csv", index=False)

    _ks_report = ks_report(data=model_dict.get("oof_train_preds"),
                           target="target",
                           prob="prediction")
    _ks_report.to_csv("ks_report.csv", index=False)
