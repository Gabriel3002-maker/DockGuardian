import docker

class DockerClient:
    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self, all: bool = False):
        return self.client.containers.list(all=all)

    def get_container(self, container_id):
        return self.client.containers.get(container_id)
