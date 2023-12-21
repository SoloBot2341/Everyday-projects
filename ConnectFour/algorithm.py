def checkForWinner(table, SCORE=4, NULL=0):
    full = True
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == NULL:
                full = False
                continue
            current_index = [i,j]
            if (checkDiagRight(current_index, table, SCORE) or
            checkDiagLeft(current_index, table, SCORE)or
            checkCol(current_index, table, SCORE)or
            checkRow(current_index, table, SCORE)):
                return True
    return False if not full else -1

def checkCol(current_index, table,SCORE=4):
    row,col = current_index[:]
    _sum = 1
    for i in range(1,SCORE):
        if col + i >= len(table[0]) or col - i < 0: break
        _sum += table[row][col+i] == table[row][col]  
        _sum += table[row][col-i] == table[row][col]
    return _sum >= SCORE

def checkRow(current_index, table,SCORE=4):
    row,col = current_index[:]
    _sum = 1
    for i in range(1, SCORE):
        if row+i >= len(table) or row-i < 0: break 
        _sum += table[row+i][col] == table[row][col]
        _sum += table[row-i][col] == table[row][col]
    return _sum >= SCORE

def checkDiagRight(current_index, table,SCORE=4):
    row,col = current_index[:]
    _sum = 1
    for i in range(1, SCORE):
        if row + i >= len(table) or col + i < 0:break
        _sum += table[row+i][col-i] == table[row][col]
    return _sum >= SCORE

def checkDiagLeft(current_index, table,SCORE=4):
    row,col = current_index[:]
    _sum = 1
    for i in range(1, SCORE):
        if row + i >= len(table) or col + i >= len(table[0]):break
        _sum += table[row+i][col+i] == table[row][col]
    return _sum >= SCORE