import time
import sys
import numpy as np
import os

def sortSecond(val):
    return val[1]


def getIndexArray(data_file, column_index, ascending):
    data = []
    for data_line in data_file:
        line = data_line.strip().split(';')
        val = 0
        for column in column_index:
            val += float(line[column])
        data.append(val)
    numpy_data = np.array(data)
    if ascending:
        sorted_data = np.argsort(numpy_data)
    else:
        sorted_data = np.argsort(-numpy_data)
    return sorted_data


def binaryCount (num, column_index):
    num_str = str(format(num, 'b'))  # 1 1 1 1
    for i in range(len(num_str), column_index):
        num_str = '0' + num_str
    return num_str

def makeGoals(data):
    data_file = open(data, 'r')
    data_header = next(data_file).strip().split(';')
    num_col = len(data_header) - 1
    goals_strs = []
    goal_prefix = data + ' ASC '
    goal_binaries = []
    for i in range(1, num_col):
        binary_str = binaryCount(i, num_col)
        goal_binaries.append(binary_str)
        goals_strs.append(goal_prefix + binary_str)
    return goal_binaries, goals_strs

def makeColumnIndex(combination):
    column_index = []
    i = 0
    while i < len(combination):
        if combination[i] == '1':
            column_index.append(i + 1)  # 00101 -> [3,5
        i += 1
    return column_index

def runGoal(goal):
    data_file = open("data/" + goal[0], "r")
    next(data_file)
    result = ''
    column_combination = makeColumnIndex(goal)
    ascending = True
    if goal[2] == 'DESC':
        ascending = False
    index_array = getIndexArray(data_file, column_combination, ascending)
    data_file.close()
    data_file = open("data/" + goal[0], "r")
    next(data_file)
    i = 0
    for data_line in data_file:
        line = data_line.strip().split(';')
        if goal[2] == 'ASC':
            if i == int(index_array[int(goal[1])-1]):
                result = line[0]
        elif goal[2] == 'DESC':
            if i == int(index_array[int(goal[1])-1]):
                result = line[0]
        i += 1
    print(result)
    return result


def getAllCombinations(filename):
    file = open("data/" + filename, 'r')
    file_line = next(file).strip().split(';')
    number_of_columns = len(file_line) - 1
    combinations = []
    for i in range(1, pow(2, len(file_line) - 1)):
        combinations.append(binaryCount(i, number_of_columns))
    return combinations


def preProcess (filename_list):
    preprocess_matrix = {}
    for filename in filename_list:
        combinations = getAllCombinations(filename)
        file_arrays = []
        for combination in combinations:
            open_file = open("data/" + filename, 'r')
            next(open_file)
            column_index = makeColumnIndex(combination)
            index_array_ASC = getIndexArray(open_file, column_index, True)
            # index_array_DESC = getIndexArray(open_file, column_index, False)
            file_arrays.append(index_array_ASC)
            # file_arrays.append(index_array_DESC)
            open_file.close()
        preprocess_matrix[filename] = file_arrays  # pm['filename'][numbin*2+1][seek]

start = time.time()
output = open("results3.txt", "w+")

if len(sys.argv) > 1:
    if (sys.argv[1] == '-p'):
        file_list = os.listdir('data')
        preProcess(file_list)
        pass
    else:
        print('Invalid Command')
else:
    goal_file = open('goals.txt', "r")
    for goal_line in goal_file:
        goal = goal_line.strip().split()
        result = runGoal(goal)
        output.write(result)
        output.write("\n")
end = time.time()
print(end - start)

