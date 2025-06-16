from pydantic import BaseModel
from typing import List, Optional

class ContainerInfo(BaseModel):
    id: str
    name: str
    status: str
    image: Optional[str]

class ContainerDetail(ContainerInfo):
    logs: Optional[str]
