import mysql.connector
from db.functions import getgi
from orf.findORFs import findORFs

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='refseq')

cursor = cnx.cursor()

lines = ["Trib3"]

for line in lines:
    gi = getgi(line, cursor)

    if len(gi) > 0:
        for gene in gi:
            query = "SELECT * FROM sequences WHERE identifier = " + str(gene[0]) + " LIMIT 0,1"
            cursor.execute(query)
            seqs = cursor.fetchall()

            query = "SELECT * FROM cds WHERE gi = " + str(gene[0]) + " LIMIT 0,1"
            cursor.execute(query)
            cds = cursor.fetchall()

            if len(seqs) == 0 or len(cds) == 0:
                if len(seqs) == 0:
                    print("ERROR: No sequence found for '" + gene[2] + "' (gi = " + str(gene[0]) + ")\n")

                if len(cds) == 0:
                    print("ERROR: No CDS found for '" + gene[2] + "' (gi = " + str(gene[0]) + ")\n")
            else:
                orfs = findORFs(seqs[0][5])
                print("ORFs:")
                print("+-------|-------+")
                print("| Start\t| Stop\t|")
                print("+-------|-------+")
                for orf in orfs:
                    print("| " + str(orf['start']) + "\t| " + str(orf['end']) + "\t| ")
                print("+-------|-------+")


    else:
        print("ERROR: Gene '" + line + "' not found.\n")

cursor.close()
cnx.close()

