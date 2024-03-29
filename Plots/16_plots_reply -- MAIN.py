# importing package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# create data
plt.style.use('seaborn')
plt.figure(figsize=(12,9))

x = [2017, 2018, 2019, 2020, 2021, 2022]

#### Reply all posts
# y1 =[0.18, 0.25, 0.30, 0.26, 0.32, 0.42]
# y2 =[0.14, 0.26, 0.22, 0.19, 0.28, 0.28]
# y3 =[0.17, 0.06, 0.03, 0.25, 0.18, 0.21]
#### Reply dep. posts   #### change data
y1 =[0.67, 2.89, 1.78, 1.75, 1.02, 0.93]
y2 =[0.15, 1.68, 4.25, 2.41, 0.45, 0.85]
y3 =[0.57, 0.45, 0.23, 5.47, 4.46, 13.2]
plt.plot(x, y1, c='green', label='Low')
plt.plot(x, y2, c='blue', label='Moderate')
plt.plot(x, y3, c='red', label='High')

size = 33
plt.xlabel("Year", fontsize=size)
plt.ylabel("Avg. number of replies per self-harm post", fontsize=size-5) ### change here
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.legend(fontsize=size, loc = "upper left")
### change name
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plots_reply_sh.pdf", format="pdf", bbox_inches="tight")
plt.show()
