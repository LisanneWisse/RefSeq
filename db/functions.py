def getgi(gene, cursor):
    query = "SELECT gi, ref, gene, NULL as synonym FROM genes WHERE gene = '" + gene + "'"
    cursor.execute(query)
    res = cursor.fetchall()

    if len(res) == 0:
        query = "SELECT g.gi, g.ref, g.gene, s.synonym FROM synonyms s INNER JOIN genes g ON s.gi = g.gi WHERE synonym = '" + gene + "'"
        cursor.execute(query)
        syns = cursor.fetchall()
        return syns
    else:
        return res
