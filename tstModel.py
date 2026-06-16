from model.model import Model

mymodel=Model()
mymodel.buildGraph(7.4, 7.8)
print(mymodel.getGraphDetails())
componenti_connesse, max_componente=mymodel.getInfoConnessa()
for m in max_componente:
    print(m)
