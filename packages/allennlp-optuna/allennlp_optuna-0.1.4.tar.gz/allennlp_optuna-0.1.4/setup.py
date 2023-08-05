# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allennlp_optuna', 'allennlp_optuna.commands']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=1.0.0,<2.0.0', 'optuna>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'allennlp-optuna',
    'version': '0.1.4',
    'description': 'AllenNLP integration for hyperparameter optimization',
    'long_description': '# AllenNLP subcommand for hyperparameter optimization\n\n`allennlp-optuna` is [AllenNLP](https://github.com/allenai/allennlp) plugin for\nhyperparameter optimization using [Optuna](https://github.com/optuna/optuna).\n\n\n#### Supported environments\n\nMachine \\ Device | Single GPU             | Multi GPUs\n---------------- | ---------------------- | ---------------\nSingle Node      | :white_check_mark:     | Partial\nMulti Nodes      | :white_check_mark:     | Partial\n\nAllenNLP provides a way of distributed training (https://medium.com/ai2-blog/c4d7c17eb6d6).\nUnfortunately, `allennlp-optuna` doesn\'t fully support this feature.\nWith multiple GPUs, you can run hyperparameter optimization.\nBut you cannot enable a pruning feature.\n(For more detail, please see [himkt/allennlp-optuna#20](https://github.com/himkt/allennlp-optuna/issues/20)\nand [optuna/optuna#1990](https://github.com/optuna/optuna/issues/1990))\n\nAlternatively, `allennlp-optuna` supports distributed optimization with multiple machines.\nPlease read the [tutorial](https://allennlp-optuna.readthedocs.io/en/latest/tutorial/hyperparameter_optimization_at_scale.html) about\ndistributed optimization in `allennlp-optuna`.\nYou can also learn about a mechanism of Optuna in the [paper](https://arxiv.org/pdf/1907.10902.pdf)\nor [documentation](https://optuna.readthedocs.io/en/stable/).\n\n\n#### Documentation\n\nYou can read the documentation on [readthedocs](https://allennlp-optuna.readthedocs.io/).\n\n\n## 1. Installation\n\n```sh\npip install allennlp_optuna\n\n# Create .allennlp_plugins at the top of your repository or $HOME/.allennlp/plugins\n# For more information, please see https://github.com/allenai/allennlp#plugins\necho \'allennlp_optuna\' >> .allennlp_plugins\n```\n\n\n## 2. Optimization\n\n\n### 2.1. AllenNLP config\n\nModel configuration written in Jsonnet.\n\nYou have to replace values of hyperparameters with jsonnet function `std.extVar`.\nRemember casting external variables to desired types by `std.parseInt`, `std.parseJson`.\n\n```jsonnet\nlocal lr = 0.1;  // before\n↓↓↓\nlocal lr = std.parseJson(std.extVar(\'lr\'));  // after\n```\n\nFor more information, please refer to [AllenNLP Guide](https://guide.allennlp.org/hyperparameter-optimization).\n\n\n### 2.2. Define hyperparameter search speaces\n\nYou can define search space in Json.\n\nEach hyperparameter config must have `type` and `keyword`.\nYou can see what parameters are available for each hyperparameter in\n[Optuna API reference](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial).\n\n```json\n[\n  {\n    "type": "int",\n    "attributes": {\n      "name": "embedding_dim",\n      "low": 64,\n      "high": 128\n    }\n  },\n  {\n    "type": "int",\n    "attributes": {\n      "name": "max_filter_size",\n      "low": 2,\n      "high": 5\n    }\n  },\n  {\n    "type": "int",\n    "attributes": {\n      "name": "num_filters",\n      "low": 64,\n      "high": 256\n    }\n  },\n  {\n    "type": "int",\n    "attributes": {\n      "name": "output_dim",\n      "low": 64,\n      "high": 256\n    }\n  },\n  {\n    "type": "float",\n    "attributes": {\n      "name": "dropout",\n      "low": 0.0,\n      "high": 0.5\n    }\n  },\n  {\n    "type": "float",\n    "attributes": {\n      "name": "lr",\n      "low": 5e-3,\n      "high": 5e-1,\n      "log": true\n    }\n  }\n]\n```\n\nParameters for `suggest_#{type}` are available for config of `type=#{type}`. (e.g. when `type=float`,\nyou can see the available parameters in [suggest\\_float](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.suggest_float)\n\nPlease see the [example](./config/hparams.json) in detail.\n\n\n### 2.3. Optimize hyperparameters by allennlp cli\n\n\n```shell\nallennlp tune \\\n    config/imdb_optuna.jsonnet \\\n    config/hparams.json \\\n    --serialization-dir result/hpo \\\n    --study-name test\n```\n\n\n### 2.4. [Optional] Specify Optuna configurations\n\nYou can choose a pruner/sample implemented in Optuna.\nTo specify a pruner/sampler, create a JSON config file\n\nThe example of [optuna.json](./config/optuna.json) looks like:\n\n```json\n{\n  "pruner": {\n    "type": "HyperbandPruner",\n    "attributes": {\n      "min_resource": 1,\n      "reduction_factor": 5\n    }\n  },\n  "sampler": {\n    "type": "TPESampler",\n    "attributes": {\n      "n_startup_trials": 5\n    }\n  }\n}\n```\n\nAnd add a epoch callback to your configuration.\n(https://guide.allennlp.org/hyperparameter-optimization#6)\n\n```\n  epoch_callbacks: [\n    {\n      type: \'optuna_pruner\',\n    }\n  ],\n```\n\n- [`config/imdb_optuna.jsonnet`](./config/imdb_optuna.jsonnet) is a simple configuration for allennlp-optuna\n- [`config/imdb_optuna_with_pruning.jsonnet`](./config/imdb_optuna_with_pruning.jsonnet) is a configuration using Optuna pruner (and TPEsampler)\n\n```sh\n$ diff config/imdb_optuna.jsonnet config/imdb_optuna_with_pruning.jsonnet\n32d31\n<   datasets_for_vocab_creation: [\'train\'],\n58a58,62\n>     epoch_callbacks: [\n>       {\n>         type: \'optuna_pruner\',\n>       }\n>     ],\n```\n\nThen, you can use a pruning callback by running following:\n\n```shell\nallennlp tune \\\n    config/imdb_optuna_with_pruning.jsonnet \\\n    config/hparams.json \\\n    --optuna-param-path config/optuna.json \\\n    --serialization-dir result/hpo_with_optuna_config \\\n    --study-name test_with_pruning\n```\n\n\n\n## 3. Get best hyperparameters\n\n```shell\nallennlp best-params \\\n    --study-name test\n```\n\n\n## 4. Retrain a model with optimized hyperparameters\n\n```shell\nallennlp retrain \\\n    config/imdb_optuna.jsonnet \\\n    --serialization-dir retrain_result \\\n    --study-name test\n```\n\n\n## 5. Hyperparameter optimization at scale!\n\nyou can run optimizations in parallel.\nYou can easily run distributed optimization by adding an option\n`--skip-if-exists` to `allennlp tune` command.\n\n```\nallennlp tune \\\n    config/imdb_optuna.jsonnet \\\n    config/hparams.json \\\n    --optuna-param-path config/optuna.json \\\n    --serialization-dir result \\\n    --study-name test \\\n    --skip-if-exists\n```\n\nallennlp-optuna uses SQLite as a default storage for storing results.\nYou can easily run distributed optimization **over machines**\nby using MySQL or PostgreSQL as a storage.\n\nFor example, if you want to use MySQL as a storage,\nthe command should be like following:\n\n```\nallennlp tune \\\n    config/imdb_optuna.jsonnet \\\n    config/hparams.json \\\n    --optuna-param-path config/optuna.json \\\n    --serialization-dir result \\\n    --study-name test \\\n    --storage mysql://<user_name>:<passwd>@<db_host>/<db_name> \\\n    --skip-if-exists\n```\n\nYou can run the above command on each machine to\nrun multi-node distributed optimization.\n\nIf you want to know about a mechanism of Optuna distributed optimization,\nplease see the official documentation: https://optuna.readthedocs.io/en/latest/tutorial/10_key_features/004_distributed.html\n\n\n#### Reference\n\n- Cookpad Techlife (in Japanese): https://techlife.cookpad.com/entry/2020/11/06/110000\n  - `allennlp-optuna` is used for optimizing hyperparameter of NER model\n',
    'author': 'himkt',
    'author_email': 'himkt@klis.tsukuba.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
