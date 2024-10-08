import random

from database.DB_connect import DBConnect
import mysql.connector

from model.attraction import Attraction
from model.destination import Destination
from model.offer import Offer
from model.tourist_attraction import Tourist_attraction
from model.traveler import Traveler
from model.trip_package import Trip_package


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getViaggiUtente(mail, data):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select tp.trip_package_id , d.name , tp.trip_start 
                    from reservation r, traveler t, trip_package tp , trip_package_has_destination tphd , destination d 
                    where r.Customer_id = t.traveler_id 
                    and t.email = %s
                    and tp.trip_start < %s
                    and r.trip_package_id = tp.trip_package_id 
                    and tp.trip_package_id = tphd.trip_package_id 
                    and d.destination_id = tphd.destination_id  
                    order by tp.trip_start asc
                            """

        cursor.execute(query, (mail,data))

        for row in cursor:
            if row['trip_package_id'] not in result:
                result[row['trip_package_id']] = [(row['name'], row['trip_start'])]
            else:
                result[row['trip_package_id']].append((row['name'], row['trip_start']))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getCustomerID(mail):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.traveler_id 
                    from traveler t 
                    where t.email = %s
                                    """

        cursor.execute(query, (mail,))

        for row in cursor:
            result.append(row['traveler_id'])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def insertNewRating(trip_id, voto, traveler_id):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """insert into ratings values (%s, %s, %s)
                                            """

        esito = None
        try:
            cursor.execute(query, (traveler_id, trip_id, voto))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False



        cursor.close()
        conn.close()
        return esito


    @staticmethod
    def getAllStati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.country 
                    from destination d 
                    order by country 
                """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row['country'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCateCosti():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select package_cost_category as cost
                    from package_cost
                        """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row['cost'])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def ricercaTripPackage(mese, anno, destinazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow tp.*
                    from trip_package tp, trip_package_has_destination th, destination d
                    where month(tp.trip_start) = %s
                    and year(tp.trip_start) = %s
                    and th.trip_package_id = tp.trip_package_id
                    and th.destination_id = d.destination_id
                    and d.country = %s
                                """

        cursor.execute(query, (mese, anno, destinazione))

        for row in cursor:
            result.append(Trip_package(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getDestinazioniViaggio(trip_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select d.*
                    from destination d , trip_package_has_destination tphd 
                    where d.destination_id  = tphd.destination_id 
                    and tphd.trip_package_id = %s
                                        """

        cursor.execute(query, (trip_id,))

        for row in cursor:
            result.append(Destination(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getListaAttraction(trip_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select ta.*, tpha.travel_guide_employee_AM 
                    from trip_package_has_attraction tpha , tourist_attraction ta
                    where tpha.tourist_attraction_id = ta.tourist_attraction_id 
                    and tpha.trip_package_id = %s
                                            """

        cursor.execute(query, (trip_id,))

        for row in cursor:
            result.append(Tourist_attraction(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getInfoGuida(guide_id):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select e.name as nome, l.name as lingua
                    from travel_guide_has_languages tghl , employees e , languages l 
                    where tghl.travel_guide_employee_AM = e.employees_AM 
                    and tghl.languages_id = l.languages_id 
                    and tghl.travel_guide_employee_AM = %s
                                                """

        cursor.execute(query, (guide_id,))

        for row in cursor:
            if len(result) == 0:
                result[row['nome']] = [row['lingua']]
            else:
                result[row['nome']].append(row['lingua'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getOfferteViaggio(trip_id, data):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from offer o
                    where o.trip_package_id = %s
                    and o.offer_start <= %s
                    and o.offer_end >= %s
                                                """

        cursor.execute(query, (trip_id, data, data))

        for row in cursor:
            result.append(Offer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getInfoTraveler(email):
        conn = DBConnect.get_connection()

        result = ''

        cursor = conn.cursor(dictionary=True)
        query = """select t.name , t.surname , t.age , t.address , t.phone , t.email , t.gender 
                        from traveler t 
                        where email = %s
                                            """

        cursor.execute(query, (email,))

        for row in cursor:
            result = Traveler(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def aggiungiTraveler(name, surname, age, address, phone, email, gender):
        conn = DBConnect.get_connection()

        esito = None

        cursor = conn.cursor(dictionary=True)
        query = """insert into traveler(name, surname, age, address, phone, email, gender)
                    values (%s, %s, %s, %s ,%s ,%s ,%s)
                                                    """
        try:
            cursor.execute(query, (name, surname, age, address, phone, email, gender))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False
        cursor.close()
        conn.close()
        return esito


    @staticmethod
    def trovaCustomerID(email):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select traveler_id as id
                    from traveler
                    where email = %s                 
                    """

        cursor.execute(query, (email,))

        for row in cursor:
            result.append(row['id'])

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def prenota(trip_id, traveler_id, offerta, data):
        conn = DBConnect.get_connection()

        esito = None

        cursor = conn.cursor(dictionary=True)
        query = """insert into reservation(Customer_id, date, offer_id, trip_package_id) values
                            (%s, %s,%s,%s)
                                                                    """
        try:
            cursor.execute(query, (traveler_id, data, offerta, trip_id))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False
        cursor.close()
        conn.close()
        return esito

    @staticmethod
    def getLingue():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from languages   
                    order by name              
                    """

        cursor.execute(query, ())

        for row in cursor:
            result.append((row['languages_id'], row['name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(stato1, stato2, stato3):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select ta.tourist_attraction_id as id, ta.cost as cost , d.country as country , ta.name as nameAtt, d.name as nameDest, d.destination_id as dest_id
from tourist_attraction ta , destination d 
where ta.destination_id = d.destination_id 
and (d.country =%s or d.country =%s or d.country =%s)           
                            """

        cursor.execute(query, (stato1, stato2, stato3))

        for row in cursor:
            result.append(Attraction(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges(stato1, stato2, stato3):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.tourist_attraction_id as at1, t1.cost as c1, t1.country as st1, t1.attN as nameAtt1, t1.destN as nameDest1, t1.d_id as dest_id1,t2.tourist_attraction_id as at2, t2.cost as c2, t2.country as st2, t2.attN as nameAtt2, t2.destN as nameDest2, t2.d_id as dest_id2
from (select ta.tourist_attraction_id, ta.cost , d.country , ta.name as attN, d.name destN, d.destination_id as d_id 
			from tourist_attraction ta , destination d 
			where ta.destination_id = d.destination_id 
			and (d.country =%s or d.country =%s or d.country =%s)) t1,
			(select ta.tourist_attraction_id, ta.cost , d.country , ta.name as attN, d.name destN, d.destination_id as d_id 
			from tourist_attraction ta , destination d 
			where ta.destination_id = d.destination_id 
			and (d.country =%s or d.country =%s or d.country =%s)) t2
where t1.tourist_attraction_id < t2.tourist_attraction_id  
                            """

        cursor.execute(query, (stato1, stato2, stato3, stato1, stato2, stato3))

        for row in cursor:
            result.append((Attraction(row['at1'], row['c1'], row['st1'], row['nameAtt1'], row['nameDest1'], row['dest_id1']), Attraction(row['at2'], row['c2'], row['st2'],row['nameAtt2'], row['nameDest2'], row['dest_id2'])))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getMediaCosti():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select round( (avg(round(tp.cost_attraction / t1.c, 1 ))/(1+t2.m)), 1)  as c
                    from trip_package tp , 
                                            (select tpha.trip_package_id, count(tpha.tourist_attraction_id) as c
                                            from trip_package_has_attraction tpha
                                            group by tpha.trip_package_id) t1, (select round(avg(tg.cost_percentage) /100, 2) as m
																			from travel_guide tg) t2		
where tp.trip_package_id = t1.trip_package_id            
                                    """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row['c'])

        cursor.close()
        conn.close()
        return result[0]


    @staticmethod
    def getGuida(idLingua):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tghl.travel_guide_employee_AM as id, tg.cost_percentage as cost
                from travel_guide_has_languages tghl , languages l, travel_guide tg 
                where l.languages_id = %s
                and l.languages_id = tghl.languages_id 
                and tg.travel_guide_employee_AM = tghl.travel_guide_employee_AM           
                                            """

        cursor.execute(query, (idLingua,))

        for row in cursor:
            result.append((row['id'], row['cost']))

        cursor.close()
        conn.close()
        return random.choice(result)


    @staticmethod
    def creaTripPackage(data, costoAttraction, costoAccomodation, cost_category):
        conn = DBConnect.get_connection()

        esito = None

        cursor = conn.cursor(dictionary=True)
        query = """insert into trip_package(trip_start,cost_attraction,cost_accomodation,package_cost_category_id ) values
                                    (%s, %s,%s,%s)
                                                                            """
        try:
            cursor.execute(query, (data, costoAttraction, costoAccomodation, cost_category))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False
        cursor.close()
        conn.close()
        return esito


    @staticmethod
    def getIdTripPackage():
        conn = DBConnect.get_connection()

        result = ''

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from trip_package
                    order by trip_package_id desc
                    limit 1       
                     """

        cursor.execute(query, ())

        for row in cursor:
            result = Trip_package(**row)

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def aggiungiTripPackageHasDestination(trip_id, dest_id):
        conn = DBConnect.get_connection()

        esito = None

        cursor = conn.cursor(dictionary=True)
        query = """insert into trip_package_has_destination(trip_package_id, destination_id) values
                                            (%s, %s)
                                                                                    """
        try:
            cursor.execute(query, (trip_id, dest_id))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False
        cursor.close()
        conn.close()
        return esito

    @staticmethod
    def aggiungiTripPackageHasAttraction(trip_id, attr_id, guide_id):
        conn = DBConnect.get_connection()

        esito = None

        cursor = conn.cursor(dictionary=True)
        query = """insert into trip_package_has_attraction(trip_package_id,tourist_attraction_id,travel_guide_employee_AM) values
                                                (%s, %s, %s)
                                                                                        """
        try:
            cursor.execute(query, (trip_id, attr_id,guide_id))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False
        cursor.close()
        conn.close()
        return esito


    @staticmethod
    def getTripPackageRichiesto(trip_id):
        conn = DBConnect.get_connection()

        result = ''

        cursor = conn.cursor(dictionary=True)
        query = """select *
                            from trip_package
                            where trip_package_id = %s       
                             """

        cursor.execute(query, (trip_id,))

        for row in cursor:
            result = Trip_package(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def aggiornaDatiTraveler(name, surname, age, address, phone, email, gender):
        conn = DBConnect.get_connection()

        esito = None

        cursor = conn.cursor(dictionary=True)
        query = """update traveler
                    set name = %s , surname = %s, age= %s, address = %s, phone = %s, gender = %s
                    where email = %s
                    """
        try:
            cursor.execute(query, (name, surname, age, address, phone, gender, email))
            conn.commit()
            esito = True
        except mysql.connector.Error as err:
            esito = False
        cursor.close()
        conn.close()
        return esito



    @staticmethod
    def getVotiCitta():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select d.name , round(avg(r.rating), 1) as avg
                    from ratings r , trip_package_has_destination tphd , destination d 
                    where r.trip_package_id = tphd.trip_package_id 
                    and tphd.destination_id = d.destination_id 
                    group by d.name 
           
                                                    """

        cursor.execute(query, ())

        for row in cursor:
            result[row['name']] = row['avg']

        cursor.close()
        conn.close()
        return result