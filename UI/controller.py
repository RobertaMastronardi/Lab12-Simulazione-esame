import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        ratings=self._model.getRatings()
        ratingsDD=list(map(lambda x:ft.dropdown.Option(x), ratings))
        self._view._ddrating1.options=ratingsDD
        self._view._ddrating2.options=ratingsDD
        self._view.update_page()



    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        n, archi=self._model.getGraphDetails()
        top5=self._model.getTop5Archi()
        componente_connessa, componente_max=self._model.getInfoConnessa()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f'Numero di nodi: {n}'))
        self._view.txt_result.controls.append(ft.Text(f'Numero di archi: {archi}'))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for top in top5:
            self._view.txt_result.controls.append(ft.Text(f'{top[0]} -> {top[1]} : {top[2]["weight"]}'))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {componente_connessa} componenti connesse"))
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(componente_max)}"))
        for m in componente_max:
            self._view.txt_result.controls.append(ft.Text(m))
        self._view.update_page()



    def handleCammino(self, e):
        path=self._model.getBestPath()
        self._view.txt_result.controls.clear()
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()
