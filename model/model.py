import datetime

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




    def getStati(self):
        return DAO.getAllStati()

    def getCateCosto(self):
        return DAO.getCateCosti()


    def cercaViaggi(self, mese, anno, destinazione, costo):
        viaggi = DAO.ricercaTripPackage(mese, anno, destinazione)
        dizio_viaggi = {}
        for v in viaggi:
            if costo == 'Qualsiasi':
                lista_destinazioni = DAO.getDestinazioniViaggio(v.trip_package_id)
                lista_attraction = DAO.getListaAttraction(v.trip_package_id)
                guide = {}
                for a in lista_attraction:
                    if a.travel_guide_employee_AM is not None:
                        info = DAO.getInfoGuida(a.travel_guide_employee_AM)
                        guide[a.travel_guide_employee_AM] = info
                dizio_viaggi[v] = [lista_destinazioni, lista_attraction, guide]
            elif v.package_cost_category_id == int(costo) or v.package_cost_category_id == int(costo) + 1 or v.package_cost_category_id == int(costo) - 1:
                lista_destinazioni = DAO.getDestinazioniViaggio(v.trip_package_id)
                lista_attraction = DAO.getListaAttraction(v.trip_package_id)
                guide = {}
                for a in lista_attraction:
                    if a.travel_guide_employee_AM is not None:
                        info = DAO.getInfoGuida(a.travel_guide_employee_AM)
                        guide[a.travel_guide_employee_AM] = info
                dizio_viaggi[v] = [lista_destinazioni, lista_attraction, guide]

        return dizio_viaggi

    def cercaOfferteViaggio(self, trip_id, data):
        return DAO.getOfferteViaggio(trip_id, data)


    def autoCompila(self, email):
        return DAO.getInfoTraveler(email)



    def aggiornaTraveler(self, name, surname, age, address, phone, email, gender):
        if gender == 'other':
            return DAO.aggiornaTraveler(name, surname, age, address, phone, email, None)
        else:
            return DAO.aggiornaTraveler(name, surname, age, address, phone, email, gender)




    def reservation(self, trip_id, email, offerta, name, surname, age, address, phone, gender):
        customerId = DAO.trovaCustomerID(email)
        if customerId:
            id = customerId[0]
        else:
            if not DAO.registraNuovoCliente(name, surname, age, address, phone, email, gender):
                return False
        id = DAO.trovaCustomerID(email)[0]
        return DAO.prenota(trip_id, id, offerta, datetime.date.today())



