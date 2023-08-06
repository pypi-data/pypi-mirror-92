from cicd.archetype import IArchetype
from cicd.util import python_util

class Pip(IArchetype):
    def __init__(self, application_name):
        self.application_name = application_name
    def build(self):
        python_util.run_tests()
        python_util.build()
    def publish(self, lifecycle: str):
        build_version = python_util.get_version()
        build_name = python_util.get_name()
        python_util.publish(build_name, build_version)
