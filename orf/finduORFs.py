from orf.findORFs import findORFs

def finduORFs(sequence, cdsStart):
    orfs = findORFs(sequence)

    uorfs = []


    for orf in orfs:
        if orf['start'] < cdsStart:
            uorfs.append(orf)

    return uorfs