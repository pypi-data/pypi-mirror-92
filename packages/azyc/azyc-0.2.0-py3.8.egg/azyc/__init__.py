import argparse
from .convert import convert


def run_azyc():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", default="deployment-params.yml")
    p.add_argument("--output", "-o", default="template-parameters.json")
    p.add_argument("--param", action='append',
                   type=lambda kv: kv.split("="), dest='extra')
    args = p.parse_args()
    extra_params = dict(args.extra) if args.extra != None else dict()
    convert(args.input, args.output, extra_params)
