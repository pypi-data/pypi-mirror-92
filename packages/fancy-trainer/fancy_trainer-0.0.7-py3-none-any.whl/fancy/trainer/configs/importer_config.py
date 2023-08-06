from cached_property import cached_property

import importlib
import re

from fancy import config as cfg


class ImporterConfig(cfg.BaseConfig):
    _import_statement: str = cfg.Option(required=True, name="import_statement", type=str)

    statement_re = r"from (\.*((\w+)\.)*\w+) import (\w+)"

    @cached_property
    def imported(self):
        _from, _import = self._split_from_and_import()
        return vars(importlib.import_module(_from))[_import]

    def _split_from_and_import(self):
        import_statement = self._import_statement.strip()
        result = re.fullmatch(self.statement_re, import_statement)
        if result is None:
            raise ValueError(f"Incorrect import_statement: {self._import_statement} ({self.statement_re})")
        g = result.groups()
        return g[0], g[3]
