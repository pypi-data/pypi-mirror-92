import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  
import numpy as np


class draw:
    def __init__(self, epochs,file_name):
          self.fig = plt.figure()          
          self.ax1 = self.fig.add_subplot()
          self.epoch = epochs
          self.max = None
          self.min = None
          self.file = file_name
          if (self.file == "animation_loss.txt"):
              plt.title("Loss Animation")
              plt.xlabel('Epochs')
              plt.ylabel('Loss')
          elif (self.file == "animation_acc.txt"):
              plt.title("Accuracy Animation")
              plt.xlabel('Epochs')
              plt.ylabel('Accuracy')
          
    def terminate(self):
        open(self.file, "w").close()
        plt.close(self.fig)

        
    def save_gif(self):
          anim = FuncAnimation(self.fig, self.animate , interval=10000, frames  = self.epoch , repeat = True, blit=True)
          writer = PillowWriter(fps=50)  
          gif_name = self.file.replace(".txt","")+ ".gif"
          anim.save(gif_name, writer=writer)
          
    def read (self):
          
        graph_data = open(self.file,'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(float(x))
                ys.append(float(y))
        self.max = np.max(ys)
        self.min = np.min(ys)
       
        return xs,ys
        
    def animate(self,i):
        
        if (self.file == "animation_loss.txt"):
            self.ax1.set(xlim=(0,self.epoch), ylim=(0,self.max))
            
        elif (self.file == "animation_acc.txt"):
            self.ax1.set(xlim=(0,self.epoch), ylim=(self.min,100))
        
        line_1, = self.ax1.plot([], []) 
        xs , ys = self.read()
    
        line_1.set_data(xs[:i],ys[:i])
        line1 = []
        return line1


 

