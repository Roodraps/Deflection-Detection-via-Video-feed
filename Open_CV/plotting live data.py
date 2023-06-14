import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')


index = count()

def animate(i):
    data =pd.read_csv('data.csv')
    x = data.iloc[-500:-1,0]
    y1 = data.iloc[-500:-1,1]
    
    plt.cla()  #clear access
    plt.plot(x,y1,label='channel 1')
    plt.legend(loc = 'upper left')


animation = FuncAnimation( plt.gcf(),animate,1)    # gcf =  get current figure 

plt.show()


