import matplotlib.pyplot as plt

plt.plotfile(
    "./allhorncurrents_calibrated.txt",
    ("date", "current"),
    subplots=False,
    marker="o",
    linestyle="",
    markersize=2,
)

# add a line at -200
plt.axhline(-200., color="k", zorder=0)

# limits, titles, etc
plt.xlabel("two data points per day, for days 1-28 of each month")
plt.ylabel("horncurrent (kA)")
plt.ylim((-202, -198))

plt.show()
