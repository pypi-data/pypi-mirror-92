from pathlib import Path
from typing import List

import inflection
from infra_deploy.models.argocd.chart import ArgoCharts
from infra_deploy.models.argocd.core import ArgoCD
from pydantic import BaseModel, DirectoryPath, PrivateAttr


class ArgoAggregate(BaseModel):
    """The single purpose of this class is to create every single one of the files for ArgoCD.
    
    The create class will run through a list of resource types in a list:
    
        >>> for x in resources:
        >>>     name = resource.name
        >>>     resource.config(type="yaml")
    """
    root_path: DirectoryPath = Path().cwd()
    _helm_root: Path = PrivateAttr(default=None)
    _templates_root: Path = PrivateAttr(default=None)
    argo_tasks: List[ArgoCD] = []
    parent_helm: ArgoCharts

    # helm_tasks: List[]
    @property
    def helm_roots(self) -> Path:
        return self._helm_root

    @property
    def template_root(self) -> Path:
        return self._helm_root

    def helm_root(self) -> Path:
        return self._helm_root

    def create_helm_folder(self):
        """Create Example Helm folder in root."""
        # This will be the argocd config
        helm_path = self.root_path / "argocd_config"
        helm_template = helm_path / 'templates'
        helm_path.mkdir(parents=True, exist_ok=True)
        helm_template.mkdir(parents=True, exist_ok=True)
        self.__update_helm_root(helm_path)
        self.__update_template_root(helm_template)

    def is_helm(self) -> bool:
        if self.helm_root() is None:
            return False
        return self.helm_root().exists()

    def is_template(self) -> bool:
        if self._templates_root is None:
            return False
        return self._templates_root.exists()

    def __update_helm_root(self, root: Path):
        """Sets the root of helm app. 
        """
        self._helm_root = root

    def __update_template_root(self, root: Path):
        """Sets the root of helm app. 
        """
        self._templates_root = root

    def create_file(self, root: Path, name: str, value: str):
        # NOTE: This can be moved to another class.
        if not self.is_helm():
            return
        created = root / name
        with created.open("w+") as f:
            f.seek(0)
            f.write(value)
            f.truncate()

    def add_task(self, task: 'ArgoCD'):
        self.argo_tasks.append(task)

    def __compile_charts(self):
        val_name: str = "values.yaml"
        ch_name: str = "Chart.yaml"

        self.create_file(
            self.helm_root(),
            ch_name,
            self.parent_helm.chart_yml()
        )
        self.create_file(
            self.helm_root(),
            val_name,
            self.parent_helm.value_yml()
        )

    def __compile_helm_charts(self):
        root = self._templates_root
        for task in self.argo_tasks:
            task.repo_url = self.parent_helm.repo_url
            task.server_url = self.parent_helm.server_url
            task.target_revision = self.parent_helm.target_revision
            self.create_file(root, f"{task.name}.yaml", task.to_yaml())

    def compile(self):
        self.__compile_charts()
        self.__compile_helm_charts()
