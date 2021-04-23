import os, sys, fileinput
from shutil import copy
from math import sqrt


def main():

    # set_mean = -200.005186657   #total
    # set_mean = -199.821688849 #before shutdown
    set_mean = -200.221950151  # after shutdown

    print("Using mean =", set_mean, "to calculate std deviaton")

    # with open("allhorncurrents_calibrated.txt") as fcal:
    #  line = fcal.read().splitlines()
    # print line
    n_above_zero = 0
    n_below_zero = 0
    current_sum = 0
    n_data_points = 0
    std_dev = 0
    is_first_line = True
    for line in fileinput.input("allhorncurrents_calibrated.txt", inplace=0):
        if is_first_line:
            is_first_line = False
            continue
        line = line.split(",")

        c = float(line[1].rstrip("\n"))
        d = line[0].split("-")

        month = d[1]
        year = int(d[2])

        before = False
        before = year < 16 and not (
            year == 15 and (month == "Dec" or month == "Nov" or month == "Oct")
        )
        if before:
            continue
        if c < -190:
            n_data_points = n_data_points + 1
            current_sum = current_sum + c
            std_dev = std_dev + (c - set_mean) ** 2
            if c > 0:
                n_above_zero = n_above_zero + 1
            else:
                n_below_zero = n_below_zero + 1

    measured_mean = current_sum / n_data_points
    std_dev = sqrt(std_dev / n_data_points)

    print("total counts:          ", n_data_points)
    print("above zero:            ", n_above_zero)
    print("below zero:            ", n_below_zero)
    print("total current:         ", current_sum)
    print("measured mean current: ", measured_mean)
    print("standard deviation =   ", std_dev)


if __name__ == "__main__":
    main()
