<!--
SPDX-License-Identifier: GPL-3.0-only
SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>
-->

# Co-citation graph generator

[![REUSE status](https://api.reuse.software/badge/gitlab.com/vi.le/co-citation)](https://api.reuse.software/info/gitlab.com/vi.le/co-citation)
[![pipeline status](https://gitlab.com/vi.le/co-citation/badges/master/pipeline.svg)](https://gitlab.com/vi.le/co-citation/-/commits/master)
[![PyPI version](https://img.shields.io/pypi/v/co-citation.svg)](https://pypi.python.org/pypi/co-citation)

Generate a co-citation graph from an article list in two steps:

1. Get the references of each article and their corresponding journals
2. Generate the co-citation pairs and add them the graph. The weights are the
   number of times the journals are co-cited.

## Example


```python
from co_citation import CoCitation

cites = CoCitation(
    [
        "arxiv:1602.05112",
        "pubmed:8113053",
        "sciencedirect:S0167923610001703",
        "scopus:10.1016/j.cmet.2020.11.014",
    ],
    data_type="journal", # or "article", "institution"
    wait=None, # None or the time to wait between requests (in seconds)
    retries=None, # None or the number of retries for HTTPS requests
    first_last_author=False, # Set to True to only get the institution of the first and last authors
    node_weights="eigenvector", # Or "betweenness"
)
cites.write_graph_edges("graph")
cites.plot_graph(
    display=False,
    k=10, # The spacing between the nodes
    seed=42, # Use the seed argument for reproducibility
    margin=dict(b=0, l=110, r=150, t=40)
)
```

## Documentation

See [the documentation](http://vi.le.gitlab.io/co-citation/).
