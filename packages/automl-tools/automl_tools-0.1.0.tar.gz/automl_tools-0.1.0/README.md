# Automl_tools: automl binary classification

[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


Automl_tools is a Python library that implements Gradient Boosting
## Installation

```sh
pip install automl-tools
```

## Usage

Probabilistic binary example on the Boston housing dataset:

```python
import pandas as pd
from automl_tools.main import automl_run

train = pd.read_csv("https://raw.githubusercontent.com/jonaqp/automl_tools/main/automl_tools/examples/train.csv?token=AAN2ZBGCYYR7PATAMC6NIKDABSDCQ", sep=";")
test = pd.read_csv("https://raw.githubusercontent.com/jonaqp/automl_tools/main/automl_tools/examples/test.csv?token=AAN2ZBBD63PDQLGJNUWVHOLABSC4O", sep=";")

automl_run(train=train,
           test=test,
           target_col="Survived",
           imp_num="knn",
           imp_cat="knn",
           processing="binding",
           mutual_information=False,
           correlation_drop=False,
           model_feature_selection=None,
           model_run="LR",
           augmentation=True,
           Stratified=True)

```


## License

[Apache License 2.0](https://github.com/stanfordmlgroup/ngboost/blob/master/LICENSE).


## New features v2.1
 * multiclass
 * regression

## Reference
Jonathan Quiza binary automl.

