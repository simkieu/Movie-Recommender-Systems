def format_matrix(A):
    for row in A:
        for col in range(len(row)):
            row[col] = float("{0:.8f}".format(row[col]))
    return A