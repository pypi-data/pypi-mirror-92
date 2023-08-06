"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""
from pydantic import BaseModel


class MemCPU(BaseModel):
    memory: str
    cpu: str