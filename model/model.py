import copy
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._attori=[]
        self._idMapA={}
        self._bestPath=[]
    #è il solito meccanismo di backtracking però, non avendo un nodo di partenza specificato
    #come in altri esercizi dove selezionavamo da un menù a tendina la sorgente da cui
    #far partire il cammino, dobbiamo inizializzare la sorgente è l'unico modo è il metodo sotto scritto.
    #non sarà necessario fare parziale.pop() perche non facciamo ad ogni ciclo un append, semplicemente
    #ad ogni iterazione parziale avrà un nuovo start, ma sarà sempre una lista da un elemento come facevamo
    #negli altri esercizi in cui aggiungevano un nodo v e poi lo rimuovevamo con pop()
    def getBestPath(self, ):
        self._bestPath=[]
        for start in self._graph.nodes():
            parziale=[start]
            self._ricorsione(parziale)
        return self._bestPath
    def _ricorsione(self, parziale):
        if len(parziale)>len(self._bestPath):
            self._bestPath=copy.deepcopy(parziale)
        current=parziale[-1]
        for _, successore in self._graph.edges(current):
            if successore not in parziale and successore.date_of_birth>current.date_of_birth:
                parziale.append(successore)
                self._ricorsione(parziale)
                parziale.pop()

    def buildGraph(self, rating1, rating2):
        self._graph.clear()
        self._attori=DAO.getActorsByRatings(rating1, rating2)
        for a in self._attori:
            self._idMapA[a.id]=a
        self._graph.add_nodes_from(self._attori)
        self._archi=DAO.getAllEdges(rating1, rating2)
        for a1, a2, peso in self._archi:
            self._graph.add_edge(self._idMapA[a1], self._idMapA[a2], weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        top5=sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]
        return top5
    #RICORDA
    def getInfoConnessa(self):
        componenti=list(nx.connected_components(self._graph))
        largest_cc=max(componenti, key=len)
        return len(componenti), largest_cc

    def getRatings(self):
        return DAO.getRatings()