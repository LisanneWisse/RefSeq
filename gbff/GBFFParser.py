
def parsegbff(lines):
    context = getcontext(lines[0], "")

    buffer = []

    result = {
        'ref': "",
        'gi': "",
        'gene': "",
        'cds': []
    }

    for line in lines:

        linecontext = getcontext(line, context)

        if linecontext != context:
            output = [x[12:len(x)] for x in buffer]
            if context == "VERSION":
                parsedversion = parseversion(output)
                result['ref'] = parsedversion['ref']
                result['gi'] = parsedversion['gi']
            elif context == "FEATURES.CDS":
                result['cds'].append(parsecds(output))
            elif context == "FEATURES.gene":
                result['gene'] = parsegene(output)
            context = linecontext
            buffer = []
        buffer.append(line)

    return result


def parsegene(data):
    synmode = False
    buffer = ""

    gene = ""
    synonyms = ""

    for line in data:
        if line.strip().startswith("/gene="):
            gene = line.strip().replace("/gene=\"", "").replace("\"", "")

        elif line.strip().startswith("/gene_synonym="):
            if line.strip().endswith("\""):
                synonyms = getsynonyms(line.strip())
            else:
                buffer += line.strip()
                synmode = True

        elif synmode and line.strip().endswith("\""):
            synmode = False
            buffer += line.strip()
            synonyms = getsynonyms(buffer)

        elif synmode:
            buffer += line.strip()

    return {
        'gene': gene,
        'synonyms': synonyms
    }

def getsynonyms(data):
    synonyms = data\
        .replace("/gene_synonym=\"", "")\
        .replace("\"", "")\
        .split(";")
    return[x.strip() for x in synonyms]

def parsecds(data):
    range = [None, None]
    synonyms = []
    if data[0].find("..") != -1 and data[0][0:1] != "/":
        x = data[0].strip().split("..")

        range[0] = int(x[0].replace("<", "").replace(">", "").replace("join(", ""))

        if x[1].find(",") != -1:
            range[1] = int(x[1][0:x[1].find(",")])
        else:
            range[1] = int(x[1].replace(">", ""))

    return {
        'range': range
    }


def parseversion(data):
    x = data[0].split("  GI:")
    return {
        'ref': x[0],
        'gi': int(x[1])
    }


def getcontext(line, context):
    if line[0:2] == "//":
        return line[0:2]
    elif line[0:12] == "            ":
        return context
    elif line[0:2] == "  ":
        pos = context.find(".")
        if pos != -1:
            return context[0:pos] + "." + line[0:12].strip()
        else:
            return context + "." + line[0:12].strip()
    else:
        return line[0:12].strip()

