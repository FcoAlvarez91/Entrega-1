def sortSecond(val):
    return val[1]

goal_file = open("goals.txt", "r")

for goal_line in goal_file:
    goal = goal_line.strip().split()
    data_file = open("data/" + goal[0], "r")
    data = []
    column_num = []
    i = 3
    while i < len(goal):
        if goal[i] == '1':
            column_num.append(i - 2)
        i += 1
    next(data_file)
    for data_line in data_file:
        individual_data = []
        tup = data_line.strip().split(';')
        val = 0
        for column in column_num:
            val += float(tup[column])
        individual_data.append(tup[0])
        individual_data.append(val)
        data.append(individual_data)
    if goal[2] == 'ASC':
        rev = False
    if goal[2] == 'DESC':
        rev = True
    data.sort(key = sortSecond, reverse = rev)

    print(goal)
    print(column_num)
    print(data)

    print("result: " + str(data[int(goal[1])-1][0]))