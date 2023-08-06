import os,sys
from dotenv.main import dotenv_values


def load_configs(path):
    configs = []
    try:
        if os.path.isfile(path):
            return [dotenv_values(dotenv_path=path)]
        configFiles = os.listdir(path)
        for file in configFiles:
            file_path = ('{}/{}'.format(path,file))
            configs.append(dotenv_values(dotenv_path=file_path))
    except FileNotFoundError:
        print('Invalid path: {}'.format(path))
        sys.exit(0)

    return configs

def get_variables(config):
    return {**get_environment_variables(config), **get_secret_variables(config)}
    
def get_environment_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('ENV_'), config.keys()))
    variables = {}
    for key in env_keys:
        variables[key.replace('ENV_','')] = config[key]
    return variables


def get_secret_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('SECRET_'), config.keys()))
    variables = {}
    for key in env_keys:
        variables[key.replace('SECRET_','')] = config[key]
    return variables
