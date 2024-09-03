from database.DB_connect import DBConnect
import mysql.connector
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