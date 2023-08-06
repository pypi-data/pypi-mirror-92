# TODO: There is a bug when the output_type = "dot" -> The code to generate the content of the dot file is outdated!
"""
import os

import pytest

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from ..calls import one_nop


@pytest.fixture
def graphviz(temp):
    g = GraphvizOutput()
    g.output_file = temp
    g.output_type = "dot"
    return g


def test_simple(graphviz):
    with PyCallGraph(output=graphviz):
        one_nop()
    dot = open(graphviz.output_file).read()
    os.unlink(graphviz.output_file)

    assert "digraph G" in dot
    assert '__main__ -> "calls.one_nop"' in dot
"""
