
import MySQLdb

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="T318k512",
        db="timetable",
        use_unicode=True,
        charset="utf8")
    return con



con = connect()


cur = con.cursor()


'''cur.execute("""
            CREATE TABLE timetable.list
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            date DATE,
            time int(3),
            work char(25),
            calorie int(5),
            PRIMARY KEY(id))
            """)'''


cur.execute("""INSERT INTO list
            (date,time,work,calorie)
            VALUES ('2022-10-17', '60', 'ジョギング', '')""")


con.commit()


con.close()