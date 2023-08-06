# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_linter', 'data_linter.validators']

package_data = \
{'': ['*'], 'data_linter': ['schemas/*']}

install_requires = \
['boto3>=1.14.7,<2.0.0',
 'dataengineeringutils3>=1.0.1,<2.0.0',
 'frictionless==3.24.0',
 'iam_builder>=3.7.0,<4.0.0',
 'importlib-metadata>=1.7,<2.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0']

extras_require = \
{'ge': ['pandas==1.1.3', 'great-expectations==0.12.9', 'awswrangler==1.10.0']}

entry_points = \
{'console_scripts': ['data_linter = data_linter.command_line:main']}

setup_kwargs = {
    'name': 'data-linter',
    'version': '4.1.2',
    'description': 'data linter',
    'long_description': '# Data Linter\n\nA python package to to allow automatic validation of data as part of a Data Engineering pipeline. It is designed to automate the process of moving data from Land to Raw-History as described in the [ETL pipline guide](https://github.com/moj-analytical-services/etl-pipeline-example)\n\nThis package implements different validators using different packages:\n\n- `frictionless`: Uses Frictionless data to validate the data against our metadata schemas. More information can be found [here](https://github.com/frictionlessdata/frictionless-py/)\n- `great-expectations`: Uses the Great Expectations data to validate the data against our metadata schemas. More information can be found [here](https://github.com/frictionlessdata/frictionless-py/)\n\n\n## Installation\n\n```bash\npip install data_linter # frictionless only\n```\n\n```bash\npip install data_linter[ge] # To include packages required for teh great-expectations validator\n```\n\n## Usage\n\nThis package takes a `yaml` based config file written by the user (see example below), and validates data in the specified Land bucket against specified metadata. If the data conforms to the metadata, it is moved to the specified Raw bucket for the next step in the pipeline. Any failed checks are passed to a separate bucket for testing. The package also generates logs to allow you to explore issues in more detail.\n\nTo run the validation, at most simple you can use the following:\n\n```python\nfrom data_linter import run_validation\n\nconfig_path = "config.yaml"\n\nrun_validation(config_path)\n```\n\n## Example config file\n\n```yaml\nland-base-path: s3://land-bucket/my-folder/  # Where to get the data from\nfail-base-path: s3://fail-bucket/my-folder/  # Where to write the data if failed\npass-base-path: s3://pass-bucket/my-folder/  # Where to write the data if passed\nlog-base-path: s3://log-bucket/my-folder/  # Where to write logs\ncompress-data: true  # Compress data when moving elsewhere\nremove-tables-on-pass: true  # Delete the tables in land if validation passes\nall-must-pass: true  # Only move data if all tables have passed\nfail-unknown-files:\n    exceptions:\n        - additional_file.txt\n        - another_additional_file.txt\n\nvalidator-engine: frictionless # will default to this if unspecified\n\n# Tables to validate\ntables:\n    table1:\n        required: true  # Does the table have to exist\n        pattern: null  # Assumes file is called table1\n        metadata: meta_data/table1.json\n\n    table2:\n        required: true\n        pattern: ^table2\n        metadata: meta_data/table2.json\n        row-limit: 10000 # for big tables - only take the first x rows\n```\n\nYou can also run the validator as part of a python script, where you might want to dynamically generate your config:\n\n```python\nfrom data_linter.validation import run_validation\n\nbase_config = {\n    "land-base-path": "s3://my-bucket/land/",\n    "fail-base-path": "s3://my-bucket/fail/",\n    "pass-base-path": "s3://my-bucket/pass/",\n    "log-base-path": "s3://my-bucket/log/",\n    "compress-data": False,\n    "remove-tables-on-pass": False,\n    "all-must-pass": False,\n    "validator-engine": "great-expectations",\n    "validator-engine-params": {"default_result_fmt": "BASIC", "ignore_missing_cols": True},\n    "tables": {}\n}\n\ndef get_table_config(table_name):\n    d = {\n        "required": False,\n        "expect-header": True,\n        "metadata": f"metadata/{table_name}.json",\n        "pattern": r"^{}\\.jsonl$".format(table_name),\n        "headers-ignore-case": True,\n        "only-test-cols-in-metadata": True # Only currently supported by great-expectations validator\n    }\n    return d\n\nfor table in ["table1", "table2"]:\n    base_config["tables"][table_name] = get_table_config(table_name)\n\nrun_validation(base_config) # Then watch that log go...\n```\n\n## Validators\n\n### Frictionless\n\nKnown errors / gotchas:\n- Frictionless will drop cols in a jsonl files if keys are not present in the first row (would recommend using the `great-expectations` validator for jsonl as it uses pandas to read in the data). [Link to raised issue](https://github.com/frictionlessdata/frictionless-py/issues/490).\n\n\n### Great Expectations\n\nKnown errors / gotchas:\n- When setting the "default_result_fmt" to "COMPLETE" current default behavour of codebase. You may get errors due to the fact that the returned result from great expectations tries to serialise a `pd.NA` (as a value sample in you row that failed an expectation) when writing the result as a json blob. This can be avoided by setting the "default_result_fmt" to "BASIC" as seen in the Python example above. [Link to raised issue](https://github.com/great-expectations/great_expectations/issues/2029).\n\n\n#### Additional Parameters\n\n- `default_result_fmt`: This is passed to the GE validator, if unset default option is to set the value to `"COMPLETE"`. This value sets out how much information to be returned in the result from each "expectation". For more information [see here](https://docs.greatexpectations.io/en/v0.4.0/result_format.html). Also note the safest option is to set it to `"BASIC"` for reasons discussed in the gotcha section above.\n\n- `ignore_missing_cols`: Will not fail if columns don\'t exist in data but do in metadata (it ignores this).\n\n\n## Process Diagram\n\nHow logic works\n\n![](images/data_linter_process.png)\n\n## How to update\n\nWe have tests that run on the current state of the `poetry.lock` file (i.e. the current dependencies). We also run tests based on the most up to date dependencies allowed in `pyproject.toml`. This allows us to see if there will be any issues when updating dependences. These can be run locally in the `tests` folder.\n\nWhen updating this package, make sure to change the version number in `pyproject.toml` and describe the change in CHANGELOG.md.\n\nIf you have changed any dependencies in `pyproject.toml`, run `poetry update` to update `poetry.lock`.\n\nOnce you have created a release in GitHub, to publish the latest version to PyPI, run:\n\n```bash\npoetry build\npoetry publish -u <username>\n```\n\nHere, you should substitute <username> for your PyPI username. In order to publish to PyPI, you must be an owner of the project.',
    'author': 'Thomas Hirsch',
    'author_email': 'thomas.hirsch@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
