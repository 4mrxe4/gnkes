# plugins/FinalMusic/fm_plugins/__init__.py
# Exports the list of music sub-modules. cluster.py loads each one
# ISOLATED per bot via load_module_isolated — no eager dynamic imports here
# (they would create circular imports with the parent cluster lifecycle).
from pathlib import Path


def _list_modules():
    mod_dir = Path(__file__).parent
    modules = []

    for file in mod_dir.rglob("*.py"):
        if file.is_file() and file.name != "__init__.py":
            relative_path = file.relative_to(mod_dir)
            module_path = str(relative_path.with_suffix('')).replace('\\', '.').replace('/', '.')
            modules.append(module_path)

    return modules


all_modules = frozenset(sorted(_list_modules()))

__all__ = ['all_modules']
