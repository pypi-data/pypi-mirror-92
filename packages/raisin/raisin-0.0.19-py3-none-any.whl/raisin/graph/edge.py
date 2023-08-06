#!/usr/bin/env python3

"""
|===============================|
| Represente une connection     |
| a travers le reseau ethernet. |
|===============================|

* C'est les arretes du graphe.
"""

import inspect

from . import vertex

class Edge:
    """
    |=============================|
    | Representation d'une arrete |
    | generique reliant 2 noeuds. |
    |=============================|

    * Cette arrete represente une arrette oriantee.

    Example
    -------
    >>> from raisin.graph import *
    >>> vs = vertex.Vertex()
    >>> vd = vertex.Vertex()
    >>> edge.Edge(vs, vd)
    Edge(Vertex(n=0), Vertex(n=1), n=0)
    >>> edge.Edge(vs, vd, name="arc", cost=0.5)
    Edge(Vertex(n=0), Vertex(n=1), name='arc', cost=0.5, n=1)
    >>>
    """
    def __init__(self, vs, vd, *, name="", cost=1, n=None):
        """
        :param vs: Vertex Source (Le depart de l'arette.)
        :type vs: vertex.Vertex
        :param vd: Vertex Destination (L'arrivee de l'arette.)
        :type vd: vertex.Vertex
        :param name: Nom de l'arette.
        :type name: str
        :param cost: Cout de l'arrette.
            -Soit int ou float.
            -Soit une fonction pour un cout plus subtil.
        :type cost: int, float, callable
        :param n: Identifiant de l'arette (gere tout seul)
        :type n: int
        """
        assert isinstance(vs, vertex.Vertex), \
            "'vs' have to be an instance of Vertex, not %s." \
            % type(vs).__name__
        assert isinstance(vd, vertex.Vertex), \
            "'vd' have to be an instance of Vertex, not %s." \
            % type(vd).__name__
        assert isinstance(name, str), \
            "'name' must be str. Not %s." % type(name).__name__
        assert isinstance(cost, int) or isinstance(cost, float) \
            or hasattr(cost, "__call__"), "'cost' have to be " \
            "int, float or callable. Not %s." % type(cost).__name__
        assert n == None or isinstance(n, int), \
            "'n' have to be str. Not %s." % tye(n).__name__

        self.vs = vs
        self.vd = vd
        self.name = name
        self.cost = cost
        self.n = n if n != None else next(counter)

    def __str__(self):
        """
        Retourne une chaine de caractere informelle
        donnant une jolie representation de l'arette.
        """
        return "Edge:\n\t%s" % "\n\t".join(
            "{}: {}".format(k, v) # ajouter :<12s dans le premier crochet.
            for k, v in {
                "n (id)": self.n,
                "name": self.name,
                "cost": self.cost,
                "start vertex": "\n\t" + "\n\t".join(str(self.vs).split("\n")[1:]),
                "end vertex": "\n\t" + "\n\t".join(str(self.vd).split("\n")[1:]),
            }.items() if v != None and v != "")
    
    def __repr__(self):
        """
        Representation de cette arrette directement
        evaluable par python dans un contexte donne.
        Toutes les informations y sont pour un debaugage
        precis.
        """
        return "Edge(%s)" % ", ".join(
            (repr(getattr(self, s.name))
            if s.kind == inspect.Parameter.POSITIONAL_ONLY
            or s.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            else "%s=%s" % (s.name, repr(getattr(self, s.name))))
            for s in list(inspect.signature(self.__init__).parameters.values())
            if s.default != getattr(self, s.name))

    def __hash__(self):
        """
        Appelee par les membres de collection haches.
        """
        return hash((self.vs, self.vd, self.cost))

    def __call__(self, *args, **kwargs):
        """
        |=================================|
        | Evaluation du cout de l'arette. |
        |=================================|

        * Si le cout est un nombre. Ce nombre
        est retourne directement.
        * Si le cout est un callable, la fonction
        de cout est evaluee et la valeur de retour
        de cette fonction de cout est renvoyee.

        entree
        ------
        :arg args: Les arguments de la fonction
            de cout 'self.cost'.
        :key kwargs: Le dictionaire de la
            fonction de cout 'self.cost.'

        sortie
        ------
        :return: La valeur de la fonction de cout.
        """
        try:
            return self.cost(*args, **kwargs)
        except TypeError: # Cas d'une fonction de cout non callable.
            return self.cost

    def __invert__(self):
        """
        Change le sens de l'arc. N'affecte pas self.
        Une copie est renvoyee.
        """
        new_edge = self.copy()
        if self.name:
            new_edge.name = "invert_" + new_edge.name
        new_edge.vs, new_edge.vd = new_edge.vd, new_edge.vs
        return new_edge

    def copy(self):
        """
        Retourne une copie de self.
        """
        return Edge(self.vs, self.vd, cost=self.cost, name=self.name)

counter = vertex.Counter()
