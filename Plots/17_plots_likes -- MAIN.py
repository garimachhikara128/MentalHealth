# importing package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# create data
plt.style.use('seaborn')
plt.figure(figsize=(12,9))

x = [2017, 2018, 2019, 2020, 2021, 2022]

#### Likes all posts
y1 =[0.85, 2.5, 2.79, 2.38, 3.22, 4.93]
y2 =[3.36, 2.83, 1.01, 1.48, 1.66, 1.85]
y3 =[0.14, 0.24, 0.25, 2.22, 2.24, 1.42]
#### Likes dep. posts   #### change data
y1 = [1.3,0.9,1.36,2.22,3.29,6.53]
y2 = [15.45,5.64,1.49,2.21,2.62,3.88]
y3 = [0.16,0.21,0.24,1.87,2.34,1.68]

plt.plot(x, y1, c='green', label='Low')
plt.plot(x, y2, c='blue', label='Moderate')
plt.plot(x, y3, c='red', label='High')

size = 33
plt.xlabel("Year", fontsize=size)
plt.ylabel("Avg. number of likes per self-harm post", fontsize=size-5) ### change here
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.legend(fontsize=size, loc = "upper left")
### change name
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plots_like_sh.pdf", format="pdf", bbox_inches="tight")
plt.show()
