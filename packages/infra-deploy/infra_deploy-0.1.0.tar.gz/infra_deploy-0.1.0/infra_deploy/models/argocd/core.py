from typing import Any, List, Optional

import addict as adt
import yaml
from pydantic import BaseModel


class ArgoCD(BaseModel):
    version: str = "argoproj.io/v1alpha1"
    kind: str = "Application"
    argo_namespace: str = "argocd"
    finalizers: List[str] = ["resources-finalizer.argocd.argoproj.io"]
    project: str = "default"

    name: str
    # Should be a relative path from the url
    rel_path: str
    repo_url: Optional[str]
    server_url: Optional[str]
    target_revision: Optional[str]

    # namespace: str

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

    def group(self):
        values = self.version.split("/")
        return values[0]

    def api_version(self):
        values = self.version.split("/")
        return values[1]

    def to_dict(self) -> dict:
        dd = adt.Dict()
        dd.apiVersion = self.version
        dd.kind = self.kind
        dd.metadata.name = self.name
        dd.metadata.namespace = self.argo_namespace
        dd.metadata.finalizers = self.finalizers
        dd.spec.project = self.project
        dd.spec.destination.namespace = self.name
        dd.spec.destination.server = self.server_url
        dd.spec.source.path = self.rel_path
        dd.spec.source.repoUrl = self.repo_url
        dd.spec.source.targetRevision = self.target_revision
        dd.spec.syncPolicy.automated.prune = True
        dd.spec.syncPolicy.automated.selfHeal = True
        return dd.to_dict()

    def to_yaml(self) -> str:
        """Returns a Yaml Representation Of ArgoCD Code Base

        Returns:
            str: a Yaml Representation of the resource.
        """
        return yaml.dump(self.to_dict())