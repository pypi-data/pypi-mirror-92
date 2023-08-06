# from lib2to3.pytree import Base
from typing import List, Any

import addict as adt
import yaml
from pydantic import BaseModel


class ArgoCharts(BaseModel):
    ch_api_version: str = "v1"
    ch_app_version: str = "1.0"
    ch_description: str = "Applications"
    ch_name: str = "applications"
    ch_version: str = "0.1.0"

    repo_url: str
    server_url: str
    target_revision: str

    def __init__(__pydantic_self__, **data: Any) -> None:

        super().__init__(**data)

    def chart_yml_dict(self) -> dict:
        return dict(
            apiVersion=self.ch_api_version,
            appVersion=self.ch_app_version,
            description=self.ch_description,
            name=self.ch_description,
            version=self.ch_version,
        )

    def value_dict(self) -> dict:
        dd = adt.Dict()
        dd.spec.destination.server = self.server_url
        dd.spec.source.repoUrl = self.repo_url
        dd.spec.source.targetRevision = self.target_revision
        return dd.to_dict()

    def chart_yml(self) -> str:
        return yaml.dump(self.chart_yml_dict())

    def value_yml(self) -> str:
        return yaml.dump(self.value_dict())