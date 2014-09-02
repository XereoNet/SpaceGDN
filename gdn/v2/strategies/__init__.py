from .find import Find
from .aggregate import Aggregate
from .rawfind import RawFind
from ...app import app

raw_strategies = {
    'find': Find,
    'aggregate': Aggregate,
    'rawfind': RawFind
}

strategies = {}

for key, value in raw_strategies.items():
    if key in app.config['ENABLED_STRATEGIES']:
        strategies[key] = value