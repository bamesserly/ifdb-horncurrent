import optparse
import urllib2, sys
from datetime import datetime, tzinfo, timedelta
import time


class UTC(tzinfo):
    ZERO = timedelta(0)

    def utcoffset(self, dt):
        return self.ZERO

    def tzname(self):
        return "UTC"

    def dst(self, dt):
        return self.ZERO


def main():
    options = get_options()
    # month = options.month
    year = options.year if options.year else 2016
    month_range = 1 if year == 2017 else 12
    day_range = 2

    utc = UTC()

    start = time.time()

    for month in range(1, month_range + 1):
        horiz_outfile_name = "beamX_{year}{month}.txt".format(year=year, month=month)
        vert_outfile_name = "beamY_{year}{month}.txt".format(year=year, month=month)
        horiz_outfile = open(horiz_outfile_name, "w+")
        vert_outfile = open(vert_outfile_name, "w+")
        print("  Getting spot sizes for month", month)
        print("  horiz outfile = ", horiz_outfile)
        print("  vert outfile = ", vert_outfile)

        # for each day, get two data points
        for i in range(1, day_range):
            t0 = datetime(year, month, i, 0, 0, 1, tzinfo=utc).isoformat()
            t1 = datetime(year, month, i, 8, 0, 0, tzinfo=utc).isoformat()
            horiz_outfile.write(str(GetMeanSpotSize(t0, t1, "H")) + "\n")
            vert_outfile.write(str(GetMeanSpotSize(t0, t1, "V")) + "\n")

            t0 = datetime(year, month, i, 16, 00, 00, tzinfo=utc).isoformat()
            t1 = datetime(year, month, i, 23, 59, 59, tzinfo=utc).isoformat()
            horiz_outfile.write(str(GetMeanSpotSize(t0, t1, "H")) + "\n")
            vert_outfile.write(str(GetMeanSpotSize(t0, t1, "V")) + "\n")

            print("  done with day", i)

        horiz_outfile.close()
        vert_outfile.close()

        print("done with month", month)

    end = time.time()

    print("total time elapsed", end - start)


# components A, B, C, or D
def GetMeanSpotSize(t0, t1, dirn):
    url = "http://dbdata1vm.fnal.gov:9080/ifbeam/data/data?v=E:MTGT{dirn}S&e=e,a9&t0={t0}&t1={t1}&f=csv".format(
        dirn=dirn, t0=t0, t1=t1
    )
    print(url)
    data = urllib2.urlopen(url)
    count = 0
    spotsize = 0

    for line in data:
        count = count + 1
        if count == 1:
            continue  # skip header
        line = line.rstrip("\n")
        fields = line.split(",")
        spotsize = spotsize + float(fields[-1])
    count = count - 1
    try:
        spotsize = spotsize / count
    except ZeroDivisionError:
        spotsize = 0

    return spotsize


def get_options():
    parser = optparse.OptionParser()
    parser.add_option("--month", type=int, default=1)
    parser.add_option("--year", type=int, default=2015)
    (options, args) = parser.parse_args()
    return options


if __name__ == "__main__":
    main()
