import matplotlib.pyplot as plt
from matplotlib import style
import os

class visualization:
    def __init__(self, name="the graph", line1="loss", line2="percision"):
        
        '''
        Create a graph with a specific name and line names if there is two lines:
        Args:
            name: a string holds the graph name
            line1: a string holds the first line name
            line2: a string holds the seconde line name
            
        Shape:
            - Input: graph and lines names
            - Output: None
        Examples:
            p1 = visualization("graph_title","first_line","seconde_line")
        '''

        self.value1 = []
        self.value2 = []
        self.value3 = []
        self.line1 = line1
        self.line2 = line2
        self.name = name

        style.use('fivethirtyeight')

        fig = plt.figure(name)
        self.ax1 = fig.add_subplot(1, 1, 1)
        plt.ion()
        plt.show()
        # plt.show(block = False)

    def add_point_to_graph(self,new_value3,it,epoch):
        
        '''
        update the graph by adding the new point to it and print it 
        and check if the final step reached we save the figure into picture and print it:
        Args:
            new_value3: a new value to be added to the graph
            it: an integer holds the number of the iteration
            epoch: an integer holds the number of the iteration witch we stop at
            
        Shape:
            - Input: three integer values
            - Output: None
        Examples:
            p1.add_point_to_graph(5,1,100)
        '''

        self.value3.append(new_value3)


        if len(self.value3) > 1 :
            self.ax1.clear()
            # self.ax1.plot(self.counter, self.value , c='black')
            self.ax1.plot( self.value3 )
            # plt.draw()
            plt.pause(10E-9)
            plt.savefig(f"Loss/{it-2}.png")
        if it == epoch:
            plt.savefig(f"final Loss.png")
            os.startfile("final Loss.png")
            
    def add_two_points_to_graph(self,new_value1,new_value2):
        
        '''
        update the graph by adding two new points to it then print it:
        Args:
            new_value1: a new value to be added to the graph
            new_value2: a new value to be added to the graph
            
        Shape:
            - Input: two integer values
            - Output: None
        Examples:
            p1.add_two_points_to_graph(10,4)
        '''
        
        self.value1.append(new_value1)
        self.value2.append(new_value2)


        if len(self.value1) > 1 :
            self.ax1.clear()
            self.ax1.plot( self.value1 ,label=self.line1)
            self.ax1.plot(self.value2,label=self.line2)
            plt.legend()
            # plt.draw()
            plt.pause(10E-9)
