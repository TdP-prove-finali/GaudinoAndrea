import copy
import datetime
import math

import networkx as nx

import flet as ft

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo= nx.Graph()

    def getViaggiUtente(self, mail_utente, data):
        dizio = DAO.getViaggiUtente(mail_utente, data)
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


    def getTraveler(self, email):
        return DAO.getInfoTraveler(email)



    def aggiungiTraveler(self, name, surname, age, address, phone, email, gender):
        return DAO.aggiungiTraveler(name, surname, age, address, phone, email, gender)






    def getLingue(self):
        return DAO.getLingue()

    def creaViaggio(self, stato1, stato2, stato3, numeroAttr):
        self.grafo.clear()
        self.grafo.add_nodes_from(DAO.getAllNodes(stato1, stato2, stato3))
        for attrazione in list(self.grafo.nodes):
            for altra_attrazione in list(self.grafo.nodes):
                if attrazione.id != altra_attrazione.id and abs(
                        attrazione.cost - altra_attrazione.cost) <= 2:
                    self.grafo.add_edge(attrazione, altra_attrazione)
        stati = [stato1, stato2, stato3]
        statiNonNulli = [x for x in stati if x is not None]
        self.solBest = []
        self.bestCosto = float(math.inf)





        for i in list(self.grafo.nodes):
            parziale = [i]
            if int(numeroAttr) > len(self.grafo.nodes):
                numeroAttr = len(self.grafo.nodes)
            self.ricorsione(i, parziale, int(numeroAttr), statiNonNulli, costo=0)

        statiUsati = set()
        if self.solBest == []:
            self.bestCosto = 0
            for i in list(self.grafo.nodes):
                if i.country not in statiUsati:
                    self.solBest.append(i)
                    self.bestCosto += i.cost
                    statiUsati.add(i.country)

        return self.solBest, self.bestCosto



    def ricorsione(self, v, parziale, numeroAttr, stati, costo):
        #costo = sum([x.cost for x in parziale])
        if costo >= self.bestCosto:
            return
        if  len(parziale) == numeroAttr:
            statiDiversi = set(x.country for x in parziale)
            if len(statiDiversi) == len(stati):
                if costo < self.bestCosto:
                    self.solBest = copy.deepcopy(parziale)
                    self.bestCosto = costo


        vicini = list(nx.neighbors(self.grafo, v))
        viciniAmmissibili = self.getAmmissibili(vicini, parziale, numeroAttr)
        for v in viciniAmmissibili:
            parziale.append(v)
            newCosto = costo + v.cost
            self.ricorsione(v, parziale, numeroAttr, stati, newCosto)
            parziale.pop()



    def getAmmissibili(self, vicini, parziale, numeroAttr):
        if len(parziale) == numeroAttr:
            return []
        ammissibili = []

        for v in vicini:
            if v not in parziale:
                ammissibili.append(v)
        return ammissibili


    def getGuidaLingua(self, idLingua):
        return DAO.getGuida(idLingua)

    def creaTripPackage(self, data, costoAttraction, costoAccomodation, cost_category):
        if not DAO.creaTripPackage(data, costoAttraction, costoAccomodation, cost_category):
            return None
        return DAO.getIdTripPackage()


    def aggiungiTripPackageATabelle(self, trip_package, dizioAttrazioni):
        for i in dizioAttrazioni:
            DAO.aggiungiTripPackageHasDestination(trip_package.trip_package_id, i.dest_id)
            DAO.aggiungiTripPackageHasAttraction(trip_package.trip_package_id, i.id, dizioAttrazioni[i])



    def aggiornaDatiTraveler(self, name, surname, age, address, phone, email, gender):
        DAO.aggiornaDatiTraveler(name, surname, age, address, phone, email, gender)


    def getVotiCitta(self):
        return DAO.getVotiCitta()

