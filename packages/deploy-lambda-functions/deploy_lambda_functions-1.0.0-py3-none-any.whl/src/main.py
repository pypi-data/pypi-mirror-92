import sys, argparse
from configManager import load_configs,get_variables
from LambdaFunction import LambdaFunction
from File import File



def deploy(configs):
    for config in configs:
        code_file = File(config["ZIP_DIR"])
        function = LambdaFunction(config["FUNCTION_NAME"])
        variables = get_variables(config)

        function.deploy(code_file.get_bytes())
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
    configs = load_configs(args.config)
    deploy(configs)
