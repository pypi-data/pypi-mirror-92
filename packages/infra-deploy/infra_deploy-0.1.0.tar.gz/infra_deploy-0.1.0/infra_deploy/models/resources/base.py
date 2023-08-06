import yaml


class Resource:
    _name: str
    _config: dict

    def __init__(self, name: str, _config: dict) -> None:
        super().__init__()
        self._config = _config
        self._name = name

    def config(self, is_yaml: bool = False):
        if is_yaml:
            return yaml.dump(self._config)
        return self._config

    @property
    def name(self) -> str:
        return self._name