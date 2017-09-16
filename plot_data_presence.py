import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

df = pickle.load(open('nhl/pickles/table_games.pickle','rb'))
dates   = pd.DataFrame(mdate.datestr2num(i) for i in df.date)
nums    = ~df.isin(['NULL'])
nums    = nums.replace(False,np.nan)
headers = list(df)

fig = plt.figure(figsize=(15,8))
ax = fig.add_subplot(111)
ax.yaxis.tick_right()
for i in range(len(headers)): plt.plot(dates,i*nums[headers[i]],linewidth=12.0)
ax.xaxis.set_tick_params(reset=True)
ax.xaxis.set_major_locator(mdate.YearLocator(1))
ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y'))
plt.yticks(np.arange(len(headers)),headers)
plt.ylim((0,len(headers)))
plt.title('Data Presence')
plt.xlabel('Date')
plt.grid()
plt.show()