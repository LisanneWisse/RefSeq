def findORFs(sequence):
    stopcodons = ["TAG", "TAA", "TGA"]
    startcodon = "ATG"
    i = 0
    stepSize = 1
    startIndex = 0
    endIndex = 0
    results = []

    while i < len(sequence):
        if stepSize == 1 and sequence[i:i+3] == startcodon:
            stepSize = 3
            startIndex = i + 1
        elif stepSize == 3 and sequence[i:i+3] in stopcodons:
            i = i + stepSize - 1
            stepSize = 1
            endIndex = i + 1
            results.append({
                'start': startIndex,
                'end': endIndex,
                'subSequence': sequence[startIndex:endIndex]
            })

        i += stepSize

    return results
