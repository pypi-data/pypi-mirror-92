#!/usr/bin/env python3

"""
|===========================|
| Manipulation d'un graphe. |
|===========================|

* Un graphe represente tout un cluster
de calcul.
* Il est donc constitue de machines reliees
entre elles par le reseau internet.
* Offre de nombreuses methodes qui permetent
de modifier, de creer et d'explorer intelligement
tout un cluster, de facon a optimiser les calculs.
"""

import inspect

import numpy as np

from . import edge as mod_edge
from . import vertex as mod_vertex


class Graph:
    """
    |===============================|
    | Graphe abstrait mathematique. |
    |===============================|

    Example
    -------
    In [1]: from raisin.graph import *
       ...: vs = [vertex.Vertex() for i in range(5)]
       ...: es = [edge.Edge(vs[0], v) for v in vs]
       ...: gr = graph.Graph()
       ...: [gr.add_edge(e) for e in es]
       ...: gr
    Out[1]: Graph(edges=[
                Edge(Vertex(n=0), Vertex(n=0), n=0),
                Edge(Vertex(n=0), Vertex(n=1), n=1),
                Edge(Vertex(n=0), Vertex(n=2), n=2),
                Edge(Vertex(n=0), Vertex(n=3), n=3),
                Edge(Vertex(n=0), Vertex(n=4), n=4)])
    """
    def __init__(self, *, edges=[], directed=True):
        """
        |=========================|
        | Construction du graphe. |
        |=========================|

        entree
        ------
        :param edges: Toutes les arettes a jouter au graphe.
        :type edges: iterable
        :param directed: Si c'est un graphe oriente.
            -True -> Le graphe est oriente.
            -False -> Les arretes sont symetriques.
        :type directed: boolean
        """
        assert all(isinstance(e, mod_edge.Edge) for e in edges), \
            "'toutes' les arettes doivent etre de type 'Edge'."
        assert isinstance(directed, bool), \
            "'directed' have to be boolean, not %s." \
            % type(directed).__name__

        # Initialisation.
        self.directed = directed
        self.id2vertex = {} # A chaque id (n), associ l'objet noeud.
        self.id2edge = {} # A chaque id (n), associ l'objet arette.
        self.graph = {} # La clef represente le noeud d'id n.
            # Chaque valeur est un dictionaire donc la clef est un
            # noeud successeur, et la valeur l'arete reliant le
            # noeud numero i au noeud d'id 'la clef'.

        # Remplissage.
        self.add_edges(*edges)

    def __contains__(self, obj):
        """
        |========================================|
        | Recherche si other est dans le graphe. |
        |========================================|

        * Methode apellee par le mot clef 'in'.

        entree
        ------
        :param obj: Noeud ou Arette.
        :type obj: Vertex, Edge

        sortie
        ------
        :return: True si obj est contenu dans self.
            False sinon.
        :rtype: boolean
        """
        if isinstance(obj, mod_vertex.Vertex):
            return obj.n in self.id2vertex
        elif isinstance(obj, mod_edge.Edge):
            return obj.n in self.id2edge
        raise TypeError("Argument of type '%s' is not "
            "containable in a graph." % type(obj).__name__)

    def __call__(self, *args, **kwargs):
        """
        |================================|
        | Retourne la matrice des couts. |
        |================================|

        entree
        ------
        :arg args: Les arguments de la fonction
            de cout 'self.cost' de chacune des arettes..
        :key kwargs: Le dictionaire de la
            fonction de cout 'self.cost.' des arettes.

        sortie
        ------
        :return: Une matrice carre tel que:
            M[i, j] est le cout de l'arette
            allant de i vers j.
            La taille de la matrice est de n*n avec
            n le nombre de sommets.
        :rtype: np.ndarray

        Example
        -------
        In [2]: print(gr())
        Out[2]: [[ 1.  1.  1.  1.  1.]
                 [inf inf inf inf inf]
                 [inf inf inf inf inf]
                 [inf inf inf inf inf]
                 [inf inf inf inf inf]]
        """
        size = max(self.id2vertex) + 1 # Taille du graphe.
        matrix = np.zeros((size, size))
        matrix[...] = np.inf
        for vertex_id, successors in self.graph.items():
            for successor_id, edge_id in successors.items():
                matrix[vertex_id, successor_id] = self.id2edge[edge_id](*args, **kwargs)
        return matrix

    def __repr__(self):
        """
        Renvoi une representation evaluable de ce graphe.
        """
        return "Graph(edges=[%s])" % ", ".join(map(repr, self.get_edges()))

    def add_vertex(self, vertex):
        """
        |============================|
        | Ajoute un noeud au graphe. |
        |============================|

        * Le noeud ajoute n'est relie a rien d'autre.

        entree
        ------
        :param vertex: Le nouveau noeud a ajouter.
        :type vertex: vertex.Vertex

        sortie
        ------
        :return: None
        :raises KeyError: Si le sommet est deja present
            dans ce graphe.
        """
        assert isinstance(vertex, mod_vertex.Vertex), \
            "'vertex' have to an instance of Vertex. Not %s." \
            % type(vertex).__name__
        if vertex in self:
            raise KeyError("Le noeud %s est deja dans le graphe." % repr(vertex))

        self.id2vertex[vertex.n] = vertex
        self.graph[vertex.n] = {}

    def add_vertices(self, *vertices):
        """
        |==================================|
        | Attach vertices VERTICES to the  |
        | graph while avoiding duplicates. |
        |==================================|

        :seaalso: self.add_vertex
        """
        for v in vertices:
            self.add_vertex(v)

    def add_edge(self, edge):
        """
        |===============================|
        | Ajoute une arrette au graphe. |
        |===============================|

        * Les noeuds relies par l'arrette sont deja
        contenus dans l'objet 'edge'

        entree
        ------
        :param edge: Nouvelle arrette a ajouter.
        :type edge: edge.Edge

        sortie
        ------
        :return: None
        :raises KeyError: Si Une arrette reliant
            ces 2 noeuds existe deja.
        """
        assert isinstance(edge, mod_edge.Edge), \
            "'edge' have to an instance of Edge. Not %s." \
            % type(edge).__name__
        if edge in self:
            raise KeyError("L'arette %s est deja dans presente." % repr(edge))

        if edge.vs not in self:
            self.add_vertex(edge.vs)
        if edge.vd not in self:
            self.add_vertex(edge.vd)
        
        self.id2edge[edge.n] = edge
        self.graph[edge.vs.n][edge.vd.n] = edge.n
        if not self.directed:
            inv_edge = -edge
            self.id2edge[inv_edge.n] = inv_edge
            self.graph[inv_edge.vs.n][inv_edge.vd.n] = inv_edge.n
        
    def add_edges(self, *edges):
        """
        |=======================================|
        | Ajoute toutes les arrettes d'un coup. |
        |=======================================|

        :seaalso: self.add_edge
        """
        for e in edges:
            self.add_edge(e)

    def get_vertices(self):
        """
        Return all vertices in the graph as a list.

        sortie
        ------
        :return: Toutes les sommets.
        :rtype: list
        """
        return list(self.id2vertex.values())

    def get_edges(self):
        """
        Return all edges in the graph as a list.

        sortie
        ------
        :return: Tous les sommets.
        :rtype: Toutes les aretes.
        """
        return list(self.id2edge.values())

    def predecessors(self, vertex):
        """
        |=============================|
        | Recherche les voisins qui   |
        | peuvent acceder a ce noeud. |
        |=============================|

        entree
        ------
        :param vertex: Le noeud concidere.
        :type vertex: Vertex

        sortie
        ------
        :return: Tous les noeuds ayant l'acces.
        :rtype: list
        """
        assert isinstance(vertex, mod_vertex.Vertex), \
            "'vertex' have to be of Vertex type, not %s." \
            % type(vertex).__name__
        assert vertex in self, "'vertex' n'est pas dans ce graphe."

        if not self.directed: # Si le graph n'est pas oriante
            return self.successors() # Les predecesseur sont aussi les successeurs.
        return  [self.id2vertex[vertex_id] for vertex_id in
                    [vi for vi, successors in self.graph.items()
                    if vertex.n in successors]
                ] # On recherche tous les noeuds dons 'vertex' est un successeur.

    def successors(self, vertex):
        """
        |================================|
        | Recherche les voisins qui sont |
        | accessible par ce noeud.       |
        |================================|

        entree
        ------
        :param vertex: Le noeud concidere.
        :type vertex: Vertex

        sortie
        ------
        :return: Tous les noeuds accessibles.
        :rtype: list
        """
        assert isinstance(vertex, mod_vertex.Vertex), \
            "'vertex' have to be of Vertex type, not %s." \
            % type(vertex).__name__
        assert vertex in self, "'vertex' n'est pas dans ce graphe."

        return [self.id2vertex[vertex_id] for vertex_id in self.graph[vertex.n].keys()]

    def neighbors(self, vertex):
        """
        |=============================|
        | Recherche tous les voisins. |
        |=============================|

        * C'est les noeuds que l'on peut atteindre
        et les noeuds qui peuvent nous atteindre.
        """
        if not self.directed: # Si le graph n'est pas oriante.
            return self.successors() # Les voisins sont les successeurs.
        return list(set(self.predecessors()) | set(self.successors()))

