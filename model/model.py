import flet as ft

from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getViaggiUtente(self, mail_utente):
        dizio = DAO.getViaggiUtente(mail_utente)
        return dizio


    def valutaViaggio(self, trip_id, voto, mail):
        travelerID = self.getTravelerID(mail)
        return DAO.insertNewRating(trip_id, voto, travelerID)


    def getTravelerID(self, mail):
        return DAO.getCustomerID(mail)[0]


    def getUltimaDataP(self):
        return DAO.getUltimaDataP()[0]

    def getUltimaDataR(self):
        return DAO.getUltimaDataR()[0]

    def getStati(self):
        return DAO.getAllStati()

    def getCateCosto(self):
        return DAO.getCateCosti()