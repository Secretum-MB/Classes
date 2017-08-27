def max_stock_profit(trading_info):
    """given list of trading values where indices are minutes
        past opening time and values is stock price, determine
        when best time is to buy and sell. Must sell after buy."""
    best_profit = None

    for price in range(len(trading_info)-1):
        potential = - trading_info[price] + max(trading_info[price+1:])
        # find best profit
        if best_profit == None or potential > best_profit:
            best_profit = potential
    return best_profit


# Interview Question 2
# given an array of arbitrary number of arrays, all of the same lenght.
# elements are all intergers. print elements in a spiral fashion starting at [0][0]

example_1 = [[1,2,3,4],
             [5,6,7,8],
             [9,10,11,12],
             [13,14,15,16]]
# output should be: [1,2,3,4,8,12,16,15,14,13,9,5,6,7,11,10]

def spiralPrintArray(array_of_arrays):
    result_list = []
    result_list.append(array_of_arrays[0][0])
    coordinate1 = 0
    coordinate2 = 0
    cord1_max = len(array_of_arrays) - 1
    cord2_max = len(array_of_arrays[0]) - 1
    cord1_min = 0
    cord2_min = 0

    while len(result_list) < (len(array_of_arrays) * len(array_of_arrays[0])):
        while coordinate2 < cord2_max:
            coordinate2 += 1
            result_list.append(array_of_arrays[coordinate1][coordinate2])
        cord1_min += 1

        while coordinate1 < cord1_max:
            coordinate1 += 1
            result_list.append(array_of_arrays[coordinate1][coordinate2])
        cord2_max -= 1

        while coordinate2 > cord2_min:
            coordinate2 -= 1
            result_list.append(array_of_arrays[coordinate1][coordinate2])
        cord1_max -= 1

        while coordinate1 > cord1_min:
            coordinate1 -= 1
            result_list.append(array_of_arrays[coordinate1][coordinate2])
        cord2_min += 1
    return result_list


# LeetCode Contest 8/19
import math
def imageSmoother(two_D_array):
    def allPerm(x, y, x_max, y_max):
        result = []
        i_min = 0
        i_max = x_max
        j_max = y_max
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i >= i_min and i < i_max and j <= j_max and j >= i_min:
                    result.append((i,j))
        return result

    result = []
    outer_len = len(two_D_array)
    inner_len = len(two_D_array[0])

    for row in range(outer_len):
        inner_result = []
        for number in range(inner_len):
            adjacents = allPerm(row,number,outer_len,inner_len-1)
            total = 0
            for coordinate in adjacents:
                total += two_D_array[coordinate[0]][coordinate[1]]
            inner_result.append(int(math.floor(total/len(adjacents))))
        result.append(inner_result)
    return result



print(imageSmoother([[1,1,1],[1,0,1],[1,1,1]]))
