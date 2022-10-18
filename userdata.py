
import MySQLdb

def connect():
    con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="T318k512",
        db="usertable",
        use_unicode=True,
        charset="utf8")
    return con



con =connect()


cur = con.cursor()


'''cur.execute("""
            CREATE TABLE usertable.list
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            username VARCHAR(30),
            sex char(1),
            age int(2),
            password VARCHAR(30),
            PRIMARY KEY(id))
            """)'''


'''cur.execute("""INSERT INTO list
            (username,sex,age,password)
            VALUES ('ショウ', 'M', 21, '****')""")'''

cur.execute("""
            UPDATE list SET password='****'
            """)

con.commit()


con.close()