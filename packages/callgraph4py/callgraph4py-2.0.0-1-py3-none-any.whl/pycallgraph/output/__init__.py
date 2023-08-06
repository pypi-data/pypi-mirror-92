import collections

from .graphviz import GraphvizOutput
from .output import Output

# from .gephi import GephiOutput
# from .ubigraph import UbigraphOutput


outputters = collections.OrderedDict(
    [
        ("graphviz", GraphvizOutput),
        # ('gephi', GephiOutput),
        # ('ubigraph', UbigraphOutput),
    ]
)
