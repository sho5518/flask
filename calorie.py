
import MySQLdb

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="T318k512",
        db="calorietable",
        use_unicode=True,
        charset="utf8")
    return con

lists=[["軽いウォーキング・散歩(75~85m/m)","3.5","","",""],
       ["ヨガ・ストレッチ","2.5","","",""],
       ["ジョギング","7.0","","",""],
       ["自由枠","","","",""]]
for i in range(len(lists)):


    con =connect()


    cur = con.cursor()


    '''cur.execute("""
                CREATE TABLE calorietable.list
                (id MEDIUMINT NOT NULL AUTO_INCREMENT,
                works char(25),
                mets float(2,1),
                time int(3),
                weight float(3,1),
                calorie int(5),
                PRIMARY KEY(id))
                """)'''


    '''cur.execute("""INSERT INTO list
               (works,mets,time,weight,calorie)
               VALUES (%(works)s,%(mets)s,%(time)s,%(weight)s,%(calorie)s)""",
               {"works":lists[i][0], "mets":lists[i][1], "time":lists[i][2], "weight":lists[i][3], "calorie":lists[i][4]})'''



    con.commit()


    con.close()