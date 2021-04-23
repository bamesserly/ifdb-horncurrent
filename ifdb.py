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


def CalcMeanHornCurrent(t0, t1):
    current = 0
    current = current + GetCurrentComponent(t0, t1, "A")
    current = current + GetCurrentComponent(t0, t1, "B")
    current = current + GetCurrentComponent(t0, t1, "C")
    current = current + GetCurrentComponent(t0, t1, "D")
    return current


def GetCurrentComponent(t0, t1, component):
    url = "http://dbdata1vm.fnal.gov:9080/ifbeam/data/data?v=E:NSLIN{component}&e=e,a9&t0={t0}&t1={t1}&f=csv".format(
        component=component, t0=t0, t1=t1
    )
    data = urllib2.urlopen(url)
    count = 0
    current = 0

    for line in data:
        count = count + 1
        if count == 1:
            continue  # skip header
        line = line.rstrip("\n")
        fields = line.split(",")
        current = current + float(fields[-1])
    count = count - 1
    try:
        current = current / count
    except ZeroDivisionError:
        current = 0

    return current


def get_options():
    parser = optparse.OptionParser()
    parser.add_option("--month", type=int, default=1)
    parser.add_option("--year", type=int, default=2015)
    (options, args) = parser.parse_args()
    return options


def main():
    options = get_options()
    # month = options.month
    year = options.year if options.year else 2016
    month_range = 5 if year == 2017 else 12
    day_range = 29

    utc = UTC()

    start = time.time()

    for month in range(10, 12):
        outfile_name = "horncurrents_{year}{month}.txt".format(year=year, month=month)
        outfile = open(outfile_name, "w+")
        print("  Getting horncurrents for month", month)
        print("  outfile = ", outfile)

        for i in range(1, day_range):
            t0 = datetime(year, month, i, 0, 0, 1, tzinfo=utc).isoformat()
            t1 = datetime(year, month, i, 8, 0, 0, tzinfo=utc).isoformat()
            outfile.write(str(CalcMeanHornCurrent(t0, t1)) + "\n")

            # t0 = datetime(2017, 1, i, 8, 00, 01, tzinfo=utc).isoformat()
            # t1 = datetime(2017, 1, i, 15, 59, 59, tzinfo=utc).isoformat()
            # outfile.write(str(CalcMeanHornCurrent(t0, t1)) + "\n")

            t0 = datetime(year, month, i, 16, 00, 00, tzinfo=utc).isoformat()
            t1 = datetime(year, month, i, 23, 59, 59, tzinfo=utc).isoformat()
            outfile.write(str(CalcMeanHornCurrent(t0, t1)) + "\n")

            print("  done with day", i)

        outfile.close()

        print("done with month", month)

    end = time.time()

    print("total time elapsed", end - start)


if __name__ == "__main__":
    main()


# header_size = 36
# url = "http://ifb-data.fnal.gov:8089/ifbeam/data/data?b=NuMI_Physics_A9&t0=%s&t1=%s" % (t0, t1)

# f = urllib2.urlopen(url)
# print "Status code: %s\n" % (f.getcode(),)

# d = f.read(10000)
# while d:
#    sys.stdout.write(d)
#    d = f.read(10000)

# d = f.read(header_size)
# print "\n"
# d = f.read(46)
# sys.stdout.write(d)
# print "\n"
