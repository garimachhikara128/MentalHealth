# importing package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# create data
plt.style.use('seaborn')
plt.figure(figsize=(12,9))

x = [2017, 2018, 2019, 2020, 2021, 2022]

#### Diversity
## Median -> Dep
y1 =[0.74, 0.8, 0.81, 0.75, 0.75, 0.75]
y2 =[0.68, 0.71, 0.7, 0.68, 0.7, 0.68]
y3 =[0.7, 0.71, 0.69, 0.7, 0.71, 0.75]
# Mean -> Dep
# y1 = [0.79,0.83,0.82,0.79,0.79,0.78]
# y2 = [0.71,0.73,0.73,0.73,0.73,0.71]
# y3 = [0.74,0.76,0.7,0.72,0.74,0.77]

## Median -> All
# y1 =[0.61, 0.61, 0.61, 0.61, 0.61, 0.61]
# y2 =[0.62, 0.6, 0.59, 0.59, 0.6, 0.59]
# y3 =[0.6, 0.6, 0.59, 0.6, 0.6, 0.59]
#Mean -> All
# y1 = [0.66,0.66,0.66,0.63,0.64,0.64]
# y2 = [0.64,0.63,0.63,0.62,0.62,0.63]
# y3 = [0.63,0.62,0.61,0.61,0.62,0.60]
plt.plot(x, y1, c='green', label='Low')
plt.plot(x, y2, c='blue', label='Moderate')
plt.plot(x, y3, c='red', label='High')

size = 33
plt.xlabel("Year", fontsize=size)
plt.ylabel("Avg. similarity per self-harm post", fontsize=size)
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.legend(fontsize=size, loc = "upper right")
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plots_similarity_median.pdf", format="pdf", bbox_inches="tight")
plt.show()
