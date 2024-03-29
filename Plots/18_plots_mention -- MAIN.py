# importing package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# create data
plt.style.use('seaborn')
plt.figure(figsize=(12,9))

x = [2017, 2018, 2019, 2020, 2021, 2022]

#### Mention all
# y1 =[0.89, 1.29, 1.29, 1.21, 1.13, 1.05]
# y2 =[0.61, 1.14, 1.6, 1.29, 0.84, 0.92]
# y3 =[0.53, 0.58, 0.37, 1.37, 2.01, 1.84]
#### Mention depressive
y1 = [0.67,2.89,1.78,1.75,1.02,0.93]
y2 = [0.15,1.68,4.25,2.41,0.45,0.85]
y3 = [0.57,0.45,0.23, 5.47,4.46,6.73]

plt.plot(x, y1, c='green', label='Low')
plt.plot(x, y2, c='blue', label='Moderate')
plt.plot(x, y3, c='red', label='High')

size = 33
plt.xlabel("Year", fontsize=size)
plt.ylabel("Avg. number of mentions per self-harm post", fontsize=size-5)
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.legend(fontsize=size, loc = "upper left")
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plots_mention_sh.pdf", format="pdf", bbox_inches="tight")
plt.show()
