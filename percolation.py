import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation
from datetime import datetime
from IPython.display import HTML

# class for single percolation system
class Percolation_single:
#   0: blocked, 1: open, 2: pass through

    def __init__(self, n):
        #Initialize an n x n grid with all sites blocked
        self.grid = np.zeros((n, n)) 
        self.n=n
        #Initialize an array to store the parent of each site
        self.parent = [i for i in range(n**2)]
        #Initialize an array to store the size of each tree
        self.size = [1 for i in range(n**2)]
        


#   Open sites with specified probability
    def open(self, p):
        total_sites= self.n**2
        num_open=int(total_sites*p)
        self.open_sites = random.sample(range(total_sites), num_open)
        for num in self.open_sites:
            row = num // self.n
            col = num % self.n
            self.grid[row][col] = 1

#   Find parent (with path compression)
    def find(self, i):
        if i!=self.parent[i]:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
#   Check if two sites are connected
    def connected(self, x, y):
        return self.find(x)==self.find(y)
          
#   Union two sites
    def union(self, x, y):
        px, py=self.find(x),self.find(y)
        if px==py:
            return
        if self.size[px]<self.size[py]:
            self.parent[px]=self.parent[py]
            self.size[py]+=self.size[px]
        else:
            self.parent[py]=self.parent[px]
            self.size[px]+=self.size[py]

#   Union all opened sites
    def grid_union(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j]==1:
                    
                    if i<self.n-1 and self.grid[i+1][j]==1:
                        self.union(i*self.n+j,(i+1)*self.n+j)
                    
                    if j<self.n-1 and self.grid[i][j+1]==1:
                        self.union(i*self.n+j,i*self.n+j+1)
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j]==1:
                    if self.find(i*self.n+j)<self.n:
                        self.grid[i][j]=2


#   Check if the system percolates
    def percolates(self):
        for j in range(self.n):
            if self.grid[self.n-1][j]==2:
                return True
        return False

#   Visualize the system
    def show(self):
        cmap = LinearSegmentedColormap.from_list('custom', ['black', 'white', 'turquoise'])
        fig, ax = plt.subplots()
        im = ax.imshow(self.grid, cmap=cmap)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title('Percolation Plot')
        fig.canvas.manager.set_window_title('Percolation Plot')
        plt.show()

# class for percolation experiment
class Percolation_exp:

    def __init__(self, n):
        #Initialize an n x n grid with all sites blocked
        self.grid = np.zeros((n, n)) 
        self.n=n
        #Initialize an array to store the parent of each site
        self.parent = [i for i in range(n**2)]
        #Initialize an array to store the size of each tree
        self.size = [1 for i in range(n**2)]
        #Define open sequence
        self.open_seq = random.sample(range(n**2), n**2)
        self.percolated=False

    #   Find parent (with path compression)
    def find(self, i):
        if i!=self.parent[i]:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    #   Union two sites
    def union(self, x, y):
        px, py=self.find(x),self.find(y)
        if px==py:
            return
        if self.size[px]<self.size[py]:
            self.parent[px]=self.parent[py]
            self.size[py]+=self.size[px]
        else:
            self.parent[py]=self.parent[px]
            self.size[px]+=self.size[py]
    # check connected
    def connected(self, x, y):
        return self.find(x)==self.find(y)
    
    # open a site
    def open(self, site):
        row = site // self.n
        col = site % self.n
        self.grid[row][col] = 1
        #union the site with its neighbors
        if row<self.n-1 and self.grid[row+1][col]==1 and not self.connected(site,site+self.n):
            self.union(site,site+self.n) 
        if col<self.n-1 and self.grid[row][col+1]==1 and not self.connected(site,site+1):
            self.union(site,site+1) 
        if row>0 and self.grid[row-1][col]==1 and not self.connected(site,site-self.n):
            self.union(site,site-self.n)
        if col>0 and self.grid[row][col-1]==1 and not self.connected(site,site-1):
            self.union(site,site-1)
        

    def percolates(self):
        for j in range(self.n):
            if self.find(self.n**2-1-j) in [self.find(i) for i in range(self.n)]:
                return True

    # Update grid for animation
    def animate_grid(self, i):
        if self.percolated:
            return self.grid
        self.open(self.open_seq[i])
        
        if self.percolates():
            self.percolated=True
            top=[]
            root=[]
            for j in range(self.n):
                if self.grid[0][j]==1:
                    top.append(self.find(j))
            for j in range(self.n):
                r=self.find(self.n**2-1-j)
                if r in top:
                    root.append(r)
            for m in range(self.n):
                for n in range(self.n):
                    if self.find(m*self.n+n) in root:
                        self.grid[m][n]=2
            return self.grid
        return self.grid
    
    # Show animation (for display in jupyter notebook)
    def show_animation(self):
        cmap = LinearSegmentedColormap.from_list('custom', ['black', 'white', 'turquoise'])
        fig, ax = plt.subplots()
        im = ax.imshow(self.grid, cmap=cmap, vmin=0, vmax=2,  animated=True)
        ax.set_xticks([])
        ax.set_yticks([])
        title='Percolation Plot '+str(self.n)+'x'+str(self.n)
        plt.title(title)
        fig.canvas.manager.set_window_title(title)
        
        def animate(frame):
            im.set_array(self.animate_grid(frame))
            return [im]
        ani = animation.FuncAnimation(fig, animate, frames=self.n**2, interval=15, repeat=False, blit=True)
        #plt.show()  #uncomment this if you intend to run it in a python script
        return HTML(ani.to_html5_video()) #comment this if you intend to run it in a python script
    
    # Save animation (Try with a smaller n<80, to avoid long waiting time)
    def save_animation(self):
        cmap = LinearSegmentedColormap.from_list('custom', ['black', 'white', 'turquoise'])
        fig, ax = plt.subplots()
        im = ax.imshow(self.grid, cmap=cmap, vmin=0, vmax=2,  animated=True)
        ax.set_xticks([])
        ax.set_yticks([])
        title='Percolation Plot '+str(self.n)+'x'+str(self.n)
        plt.title(title)
        
        def animate(frame):
            im.set_array(self.animate_grid(frame))
            return [im]
        ani = animation.FuncAnimation(fig, animate, frames=self.n**2, interval=15, repeat=False, blit=True)
        current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename='./animations/N='+str(self.n)+'--'+current_datetime+'.gif'
        ani.save(filename, writer='pillow')
    
    # number of sites opened for percolation
    def exp(self):
       for i, site in enumerate(self.open_seq):
            self.open(site)
            if self.percolates():
                return i+1
        








    


    
        
        
        



    
    

     
