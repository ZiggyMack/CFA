"""Preserve saved take histories across a local catalog rebuild."""
from copy import deepcopy
import importlib.util


def apply_take_history(catalog, root, review, previous=None):
    previous = previous or {}
    sources = [previous, review]
    if any('storyboardTakes' in source for source in sources):
        path = root / 'apps/creative_studio/storyboard_takes.py'
        spec = importlib.util.spec_from_file_location('_cfa_take_intake', path)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        catalog['storyboardTakes'] = helper.merge(*(source.get('storyboardTakes', helper.empty()) for source in sources))
    if any('storyboardTakeBackups' in source for source in sources):
        retained = []
        for source in sources:
            backups = source.get('storyboardTakeBackups', [])
            if not isinstance(backups, list):
                raise ValueError('Storyboard take backups must be a list.')
            for item in backups:
                if item not in retained:
                    retained.append(deepcopy(item))
        catalog['storyboardTakeBackups'] = retained
