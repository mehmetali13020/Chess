grid = [[0 for i in range(8)]for j in range(8)]
for i in range(8):
    for j in range(8):
        if (i+j) %2 == 0:
            grid[i][j] = " "
        else:
            grid[i][j] = "#"