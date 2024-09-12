import time

from database.DAO import DAO
from model.model import Model

my_model = Model()
dao = DAO()
stati = dao.getAllStati()


#tempi di esecuzione della ricorsione

#con uno stato solo
def tempiUnoStato(stati, numAttr):
    nomeFile = "tempiConNumeroDiAttrazioni"+str(numAttr)+".txt"
    output = open(nomeFile, "w", encoding='utf-8')
    for s in stati:
        start = time.time()
        my_model.creaViaggio(s, None, None, numAttr)
        end = time.time()
        print(f"\"{s}\"", end-start, file=output)






