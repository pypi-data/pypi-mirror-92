import cicd.archetype.util as archetype_util
from cicd import parser
from cicd.util import file_util

CONFIG_FILE_PATH = '.cicd_config.yml'

def main():
    args = parser.parseArgs()
    config = build_config(args)
    validate_config(config)
    archetypes = archetype_util.get_archetypes()
    if config['archetype'] in archetypes:
        archetype_instance = archetype_util.get_archetype(config['archetype'], config['application_name'])
        if args.which == 'deps':
            archetype_instance.deps()
        if args.which == 'build':
            archetype_instance.build()
        elif args.which == 'publish':
            archetype_instance.publish(args.lifecycle)
        elif args.which == 'deploy':
            archetype_instance.deploy(args.resource, args.lifecycle)
        elif args.which == 'undeploy':
            archetype_instance.undeploy(args.resource, args.lifecycle)
        elif args.which == 'smoke_test':
            archetype_instance.smoke_test(args.lifecycle)

def build_config(args):
    config = read_config()
    if args.archetype != None:
        config['archetype'] = args.archetype
    if args.name != None:
        config['application_name'] = args.name
    return config

def validate_config(config):
    if not 'application_name' in config:
        raise Exception('Application name must be provided through cli arguement or .cicd_config.yml file')

def read_config():
    if file_util.isFile(CONFIG_FILE_PATH):
        return file_util.readYamlFile(CONFIG_FILE_PATH)
    return {
        'archetype': 'dropwizard',
    }
