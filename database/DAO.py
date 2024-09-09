from database.DB_connect import DBConnect
import mysql.connector

from model.destination import Destination
from model.offer import Offer
from model.tourist_attraction import Tourist_attraction
from model.traveler import Traveler
from model.trip_package import Trip_package


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getViaggiUtente(mail):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select tp.trip_package_id , d.name , tp.trip_start 
                    from reservation r, traveler t, trip_package tp , trip_package_has_destination tphd , destination d 
                    where r.Customer_id = t.traveler_id 
                    and t.email = %s
                    and r.trip_package_id = tp.trip_package_id 
                    and tp.trip_package_id = tphd.trip_package_id 
                    and d.destination_id = tphd.destination_id  
                    order by tp.trip_start asc
                            """

        cursor.execute(query, (mail,))

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
    def getUltimaDataP():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tp.trip_start 
                    from trip_package tp 
                    order by tp.trip_start desc 
                    limit 1
                                            """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row['trip_start'])


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getUltimaDataR():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tp.trip_end
                        from trip_package tp 
                        order by tp.trip_end desc 
                        limit 1
                                                """

        cursor.execute(query, ())

        for row in cursor:
            result.append(row['trip_end'])

        cursor.close()
        conn.close()
        return result

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
        query = """select tp.*
                    from trip_package tp, trip_package_has_destination th, destination d
                    where month(tp.trip_start) = %s
                    and year(tp.trip_start) = %s
                    and th.trip_package_id = tp.trip_package_id
                    and th.destination_id = d.destination_id
                    and d.country = %s
                    group by tp.trip_package_id
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

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.name , t.surname , t.age , t.address , t.phone , t.email , t.gender 
                        from traveler t 
                        where email = %s
                                            """

        cursor.execute(query, (email,))

        for row in cursor:
            result.append(Traveler(**row))

        cursor.close()
        conn.close()
        return result