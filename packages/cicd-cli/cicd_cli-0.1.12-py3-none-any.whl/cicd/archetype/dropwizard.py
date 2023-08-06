#/usr/bin/python3
from cicd import config

from cicd.util import maven_util
from cicd.util import docker_util
from cicd.util import aws_util
from cicd.archetype import IArchetype
from cicd.util import terraform_util
from cicd.util import helm_util


class Dropwizard(IArchetype):

    def deps(self):
        maven_util.deps()
        aws_util.deps()
        terraform_util.deps()
        helm_util.deps()

    def build(self):
        maven_util.install()
        version = maven_util.get_version()
        docker_util.build(
            [],
            '.',
            [f"{self.application_name}:{version}", f"{self.application_name}:latest"],
            'Dockerfile'
        )

    def publish(self, lifecycle: str):
        version = maven_util.get_version()
        repository = aws_util.ensure_repository(self.application_name, lifecycle)

        aws_util.ecr_login(self.application_name, lifecycle)
        repository_uri = repository['repositoryUri']
        source_image = f"{self.application_name}:{version}"
        docker_util.tag(source_image, f"{repository_uri}:{version}")
        docker_util.tag(source_image, f"{repository_uri}:latest")

        docker_util.push([
            f"{repository_uri}:{version}",
            f"{repository_uri}:latest",
        ])

    def deploy(self, resource: str, lifecycle: str):
        version = maven_util.get_version()
        if 'application' == resource:
            if config.EKS_CLUSTER_NAME:
                aws_util.update_kubeconfig()
            helm_util.update_repo()
            helm_util.deploy(self.application_name, lifecycle, version, 'pago/dropwizard')
        else:
            terraform_util.init(self.application_name, lifecycle, resource)
            terraform_util.apply(self.application_name, lifecycle, resource)

    def undeploy(self, resource: str, lifecycle: str):
        if 'application' == resource:
            if config.EKS_CLUSTER_NAME:
                aws_util.update_kubeconfig()
            helm_util.update_repo()
            helm_util.delete(self.application_name, lifecycle)
        else:
            terraform_util.init(self.application_name, lifecycle, resource)
            terraform_util.destroy(self.application_name, lifecycle, resource)
