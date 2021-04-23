import os, sys, fileinput
from shutil import copy


def main():
    f = "allhorncurrents.txt"
    copy(f, "allhorncurrents_calibrated.txt")

    # with open("allhorncurrents_calibrated.txt") as fcal:
    #  line = fcal.read().splitlines()
    # print line
    is_first_line = True
    for line in fileinput.input("allhorncurrents_calibrated.txt", inplace=1):
        if is_first_line:
            is_first_line = False
            sys.stdout.write(line)
            continue
        # line = line.rstrip('\n')
        line = line.split(",")
        line[1] = str(float(line[1]) / .9954) + "\n"
        line = ",".join(line)
        # print line

        sys.stdout.write(line)


if __name__ == "__main__":
    main()
