import os, sys, fileinput
from shutil import copy

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


# line format = {D}-{MMM}-{YY},{current}
# used for input of numpy.plotfile
def fix_files(playlist, year):
    for m, f in playlist.items():
        print(m, f)
        back_up(f)
        date = 0
        switch = True
        for line in fileinput.input(f, inplace=1):
            if switch:
                date = date + 1
                switch = False
            else:
                switch = True

            line = "{dd}-{mm}-{yy},".format(dd=date, mm=m, yy=year) + line

            sys.stdout.write(line)


def back_up(path):
    path = path
    i = 0
    while i < 100:
        if not os.path.exists(path + "{0}".format(i)):
            new_backup = path + "{0}".format(i)
            copy(path, new_backup)
            break
        i += 1


def main():
    yr2013 = {}
    yr2014 = {}
    yr2015 = {}
    yr2016 = {}
    yr2017 = {}
    for i in range(1, 13):
        yr2013[months[i]] = "data/horncurrents_2013{:02d}.txt".format(i)
        yr2014[months[i]] = "data/horncurrents_2014{:02d}.txt".format(i)
        yr2015[months[i]] = "data/horncurrents_2015{:02d}.txt".format(i)
        yr2016[months[i]] = "data/horncurrents_2016{:02d}.txt".format(i)

    for i in range(1, 6):
        yr2017[months[i]] = "data/horncurrents_2017{:02d}.txt".format(i)

    fix_files(yr2013, "13")
    fix_files(yr2014, "14")
    fix_files(yr2015, "15")
    fix_files(yr2016, "16")
    fix_files(yr2017, "17")


if __name__ == "__main__":
    main()
