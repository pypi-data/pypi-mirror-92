import sys, argparse
from .configManager import load_config,get_variables
from .LambdaFunction import LambdaFunction
from .Zip import Zip



def deploy(config):
    code_zip = Zip(name=config["FUNCTION_NAME"],path=config["CODE_DIR"]).get_bytes()
    function = LambdaFunction(config["FUNCTION_NAME"])
    variables = get_variables(config)
    function.deploy(code_zip)
    function.update_env_variables(variables)
    version = function.publish_version(config["VERSION"])["Version"]
    function.update_alias(alias="stable",description=config["VERSION"],version=version)
        

def parse_args():
    parser = argparse.ArgumentParser(description='Deploy lambda function')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='config directory or file',
        required=True
    )
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)
    deploy(config)