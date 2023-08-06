#!/usr/bin/env python3

"""
|===========================|
| Modelisation du cluster   |
| de travail par un graphe. |
|===========================|

* Cela permet de modeliser et de representer
les connection qu'il peut y avoir entre
les differentes machines d'un reseau.
* Cette partie permet de pouvoir optimiser la
repartition des taches en se basant sur la theorie
des graphes.
* De facon generale, avoir une information precise
des machines environante est necessaire pour
pouvoir faire du travail en grappe.
"""

__all__ = ["edge", "graph", "vertex"]
