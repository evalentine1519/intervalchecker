import time
from datetime import datetime
import feedparser
import matplotlib.pyplot as plt
from matplotlib.ticker import(AutoMinorLocator, MultipleLocator)
import numpy as np

def get_day(published_date):
    datewords = published_date.split()
    datewords_clean = datewords[1:5]
    datewords_clean = (' ').join(datewords_clean)
    print(datewords_clean)
    dateobj = datetime.strptime(datewords_clean, "%d %b %Y %H:%M:%S")
    timestamp = time.mktime(dateobj.timetuple())

    return timestamp

rss_url = input("Paste the feed to your podcast: ")
pod_interval = int(input("How many days are scheduled between each episode? "))
PodFeed = feedparser.parse(f"{rss_url}")
daylength = 86400
hourlength = 3600
pod_title = PodFeed.feed.title


episode_dates = []

episode_dates.append(time.mktime(datetime.now().timetuple()))
print(episode_dates)
for pod in PodFeed.entries:
    episode_dates.append(get_day(pod.published))

print(episode_dates[0])
print(episode_dates[1])
episode_dates.reverse()
episode_dates_clean = []
newer = episode_dates[0]

for date in episode_dates:
    older = newer
    newer = date
    result = newer - older
    episode_dates_clean.append(round((float(result/hourlength)/24.0), 2))

print(episode_dates_clean)
episode_num = [*range(1, len(PodFeed.entries)+2)]
xpoints = np.array(episode_num)
ypoints = np.array(episode_dates_clean)


if len(episode_num) > 35:
    xfigsize = len(episode_num)/5
else:
    xfigsize = 10

fig, ax = plt.subplots(figsize=(xfigsize, 8))
ax.set_xlim(0, episode_num[-1]+1)
ax.set_ylim(0, max(episode_dates_clean)+5)
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

plt.title(f"Intervals between Episodes of {pod_title}")
plt.xlabel("Episode Number")
plt.ylabel("Days since last episode")
plt.plot(xpoints, ypoints, marker='o')
plt.axhline(y=pod_interval, color='r', linestyle='-', label='Release schedule')
plt.axvline(x=episode_num[-1], color='g', linestyle='-', label='Current day')
plt.legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')

plt.savefig(f'{pod_title}_Interval.png')
