import distutils.util
import os
import json
from typing import Union

import yaml

import argparse


def convert(input_file: str, output_file: str, extra_params: Union[dict, None] = None):
    if extra_params is None:
        extra_params = dict()

    with open(input_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    base_path = os.path.abspath(os.path.dirname(input_file))
    params = dict()
    for key, value in config.items():
        if type(value) is dict:
            if "file" in value:
                with open(base_path + '/' + value['file'], encoding="utf-8") as f:
                    data = str(f.read())
                params[key] = {"value": data}
        else:
            params[key] = {"value": value}

    for key, value in extra_params.items():
        try:
            params[key] = {"value": int(value)}
        except ValueError:
            try:
                params[key] = {"value": bool(distutils.util.strtobool(value))}
            except ValueError:
                params[key] = {"value": value}
    paramsFile = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": params
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(paramsFile, f, indent=2)
    print(f"parameter file written to {output_file}")
