from gbff.GBFFParser import parsegbff

def importgbff(input):
    buffer = []

    genestbl = open(input + ".genes.sql", 'w')
    cdstbl = open(input + ".cds.sql", 'w')
    synonymstbl = open(input + ".synonyms.sql", 'w')

    genestbl.write("INSERT INTO genes VALUES ");
    cdstbl.write("INSERT INTO cds VALUES ");
    synonymstbl.write("INSERT INTO synonyms VALUES ");

    for line in open(input):
        buffer.append(line)
        if line.startswith("//"):
            parsed = parsegbff(buffer)

            print("Processing '" + parsed['gene']['gene'] + "'")

            genestbl.write("(%s, \"%s\", \"%s\"),\n" % (parsed['gi'], parsed['ref'], parsed['gene']))

            for synonym in parsed['gene']['synonyms']:
                synonymstbl.write("(%s, \"%s\"),\n" % (parsed['gi'], synonym))

            for cds in parsed['cds']:
                cdstbl.write("(%s, %s, %s),\n" % (parsed['gi'], cds['range'][0], cds['range'][1]))

            buffer = []

    print("Finished!")
    genestbl.close()
    cdstbl.close()
    synonymstbl.close()
