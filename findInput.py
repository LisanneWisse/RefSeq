import mysql.connector


cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='refseq')

cursor = cnx.cursor()

lines = [line.strip() for line in open('J:/refseq/input.txt')]

for line in lines:

    query = "SELECT * FROM genes WHERE gene = '" + line + "'"

    cursor.execute(query)

    res = cursor.fetchall()

    if len(res) == 0:
        query = "SELECT * FROM synonyms WHERE synonym = '" + line + "'"
        cursor.execute(query)
        syns = cursor.fetchall()

        if len(syns) == 0:
            print(line)

cursor.close()
cnx.close()