from database.DB_connect import DBConnect
from model.actor import Actor


class DAO():
    @staticmethod
    def getRatings():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating from ratings r order by r.avg_rating asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getActorsByRatings(rating1, rating2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.id , n.name, n.date_of_birth 
                    from names n, role_mapping rm , movie m, ratings r
                    where n.id =rm.name_id and rm.movie_id =m.id and m.id=r.movie_id and r.avg_rating between %s and %s and n.date_of_birth is not null
                    """

        cursor.execute(query, (rating1, rating2))

        for row in cursor:
            result.append(Actor(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(rating1, rating2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.id as Actor1, t2.id as Actor2, sum(coalesce(t1.incasso, 0)) as peso
                    from (select  n.id , n.name, n.date_of_birth, m.id as film , cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '')as integer) as incasso
                    from names n, role_mapping rm , movie m, ratings r
                    where n.id =rm.name_id and rm.movie_id =m.id and m.id=r.movie_id and r.avg_rating between %s and %s and n.date_of_birth is not null
                    ) t1, (select  n.id , n.name, n.date_of_birth, m.id as film  , cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '')as integer) as incasso
                    from names n, role_mapping rm , movie m, ratings r
                    where n.id =rm.name_id and rm.movie_id =m.id and m.id=r.movie_id and r.avg_rating between %s and %s and n.date_of_birth is not null
                    ) t2
                    where t1.id>t2.id  and t1.film =t2.film 
                    group by t1.name, t2.name
                    having peso>0
         """


        cursor.execute(query, (rating1, rating2, rating1, rating2))

        for row in cursor:
            result.append((row["Actor1"], row["Actor2"], row["peso"]))

        cursor.close()
        conn.close()
        return result

