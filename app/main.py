from http.client import HTTPException
from fastapi import FastAPI
from typing import List
from app.docker_client import DockerClient
from app.schemas import ContainerInfo
import threading
import time

app = FastAPI()
docker_client = DockerClient()


class ContainerService:
    def __init__(self, docker_client: DockerClient):
        self.docker_client = docker_client
        self._last_states = {}
        self._alerts = []

    def list_containers(self) -> List[ContainerInfo]:
        containers = self.docker_client.list_containers()
        return [
            ContainerInfo(
                id=c.id[:12],
                name=c.name,
                status=c.status,
                image=c.image.tags[0] if c.image.tags else None
            ) for c in containers
        ]

    def _check_container_states(self):
        alerts = []
        containers = self.docker_client.list_containers(all=True)
        for c in containers:
            current_state = c.status
            last_state = self._last_states.get(c.id)
            if last_state is not None and last_state != current_state:
                if current_state in ["exited", "dead", "paused"]:
                    alert_msg = f"🚨 Contenedor '{c.name}' ({c.id[:12]}) cambió a estado '{current_state}'"
                    alerts.append(alert_msg)
            self._last_states[c.id] = current_state
        self._alerts = alerts

    def start_monitoring(self, interval: int = 10):
        def monitor_loop():
            while True:
                self._check_container_states()
                time.sleep(interval)

        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()

    def get_alerts(self) -> List[str]:
        return self._alerts
    
    


container_service = ContainerService(docker_client)
container_service.start_monitoring()


@app.get("/containers")
def list_containers():
    return container_service.list_containers()

@app.get("/alerts")
def get_alerts():
    alerts = []
    for container in docker_client.list_containers():
        if container.status.lower() not in ("running", "created"):
            alerts.append(f"{container.name} está en estado '{container.status}'")
    return alerts

@app.get("/containers/{container_id}/logs")
def get_logs(container_id: str):
    try:
        container = docker_client.get_container(container_id)
        logs = container.logs(tail=50).decode("utf-8")
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Contenedor no encontrado")