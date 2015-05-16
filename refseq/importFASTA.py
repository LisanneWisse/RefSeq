from fasta.fastaParser import parseFastaRecord

def importfasta(input):
    buffer = []



    inpf = open(input)
    it = iter(inpf)

    buffer.append(next(it))

    fileid = 1
    insid = 0
    subid = 0

    seqtbl = None

    for line in it:
        if subid == 100:
            seqtbl.close()
            seqtbl = None
            subid = 0
            fileid += 1

        if seqtbl is None:
            seqtbl = open(input + ".sequences." + str(fileid) + ".sql", 'w')

        if line.startswith(">"):
            if insid == 0:
                seqtbl.write("INSERT INTO sequences VALUES ")

            parsed = parseFastaRecord(buffer)
            if insid < 100:
                seqtbl.write('("%s", %s, "%s", "%s", "%s", "%s"),\n' % (parsed['identifier_type'], parsed['identifier'], parsed['database'], parsed['database_id'], parsed['name'], parsed['sequence']))
                insid += 1
            else:
                seqtbl.write('("%s", %s, "%s", "%s", "%s", "%s");\n\n' % (parsed['identifier_type'], parsed['identifier'], parsed['database'], parsed['database_id'], parsed['name'], parsed['sequence']))
                insid = 0
                subid += 1

            buffer = [line]

        else:
            buffer.append(line)

    print("Finished!")
    seqtbl.close()
