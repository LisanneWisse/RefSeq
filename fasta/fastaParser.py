# Parses a single FASTA record
# input should contain one FASTA record
def parseFastaRecord(lines):

    # Take the first line, throw away the > and split it on |
    headerline = lines[0][1:].split("|")
    sequence = []

    # Assemble the (multi line) sequence into one list
    iterlines = iter(lines)
    next(iterlines)
    for line in iterlines:
        sequence.append(line.strip())

    return {
        'identifier_type': headerline[0],
        'identifier': headerline[1],
        'database': headerline[2],
        'database_id': headerline[3],
        'name': headerline[4].strip(),
        'sequence': "".join(sequence)
    }
