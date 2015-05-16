import mysql.connector
from db.functions import getgi
from orf.finduORFs import finduORFs

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='refseq')

cursor = cnx.cursor()

lines = [line.strip() for line in open('J:/refseq/input.txt')]

outfile = open("J:/refseq/output.txt", 'w')
errfile = open("J:/refseq/errors.txt", 'w')

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
                    errfile.write("ERROR: No sequence found for '" + gene[2] + "' (gi = " + str(gene[0]) + ")\n")

                if len(cds) == 0:
                    errfile.write("ERROR: No CDS found for '" + gene[2] + "' (gi = " + str(gene[0]) + ")\n")
            else:
                uorfs = finduORFs(seqs[0][5], int(cds[0][1]))

                overlap = False
                lens = []
                for uorf in uorfs:
                    if uorf['start'] < int(cds[0][1]) <= uorf['end']:
                        overlap = True
                    lens.append(uorf['end'] - uorf['start'])

                outfile.write(str(gene[0]) + "|" + gene[1] + "|" + gene[2] + "|" + seqs[0][4] + "|" + str(cds[0][1]) + ".." + str(cds[0][2]) + "|" + str(len(uorfs)) + "|" + str(overlap) + "|" + (",".join(str(x) for x in lens)) + "\n")

    else:
        errfile.write("ERROR: Gene '" + line + "' not found.\n")

cursor.close()
cnx.close()

