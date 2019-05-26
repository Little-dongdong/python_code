import csv
from matplotlib import pyplot as plt
from datetime import datetime

#获取文件中的日期，最高气温和最低气温
filename = 'death_valley_2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            current_date = datetime.strptime(row[0], "%Y-%m-%d")
            high = int(row[1])
            low = int(row[3])
        except ValueError:
            print(current_date, "missing data")
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

#根据数据绘制图形
fig = plt.figure(dpi = 128, figsize = (10, 6))
plt.plot(dates, highs, c = 'red', alpha = 1)
plt.plot(dates, lows, c = 'blue', alpha = 1)
plt.fill_between(dates, highs, lows, facecolor = 'orange', alpha = 0.5)

#设置图形的格式
plt.title("Dail high and low temperatures - 2014", fontsize = 24)
plt.xlabel("", fontsize = 16)
fig.autofmt_xdate()    #绘制斜的日期标签
plt.ylabel("Temperature (F)", fontsize = 16)
plt.tick_params(axis = 'both', which = 'major', labelsize = 16)

plt.show()
