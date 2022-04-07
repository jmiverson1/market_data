import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime


def read_csv(directory):
    dframe_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            #print('csv Found: ', os.path.join(directory, filename))
            dframe = pd.read_csv(os.path.join(directory, filename))
            df_filtered = dframe.loc[dframe['Close'] != 0.0]
            df_filtered['Trade Date'] = df_filtered['Trade Date'].apply(lambda x:
                                                                        datetime.datetime.strptime(x, '%Y-%m-%d'))
            temp_max_dt = max(df_filtered['Trade Date'])
            df_filtered['max_date'] = temp_max_dt
            dframe_list.append(df_filtered)
            print(df_filtered.head())
        else:
            print('Non-csv Found: ', os.path.join(directory, filename))
    return dframe_list


dframe_vx = pd.concat(read_csv('C:/Users/jmive/Google Drive/VIX'))
max_dt = max(dframe_vx['Trade Date'])
vx_filtered = dframe_vx.loc[dframe_vx.max_date == max_dt]
print(vx_filtered.head())
pivot_vx = vx_filtered.pivot(index='Trade Date', columns='Futures', values='Close')
pivot_vx.to_excel("C:/Users/jmive/Google Drive/VIX/Summary.xlsx")
pivot_vx.plot()
plt.show()
