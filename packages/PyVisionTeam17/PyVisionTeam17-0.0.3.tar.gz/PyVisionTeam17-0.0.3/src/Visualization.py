import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from PIL import Image
import numpy as np
import pandas as pd


class visualization:

    def __init__(self):
        style.use('seaborn')
        pass

    def view_photo_sample(self,sample,width,height,rgb):
        """
        :Description: 
        Displays an RGB or gray scale image from an input array and saves it in sample.jpg file.

        :parameter sample: input sample as an array of pixels.
        :type sample: array of float or int with image size and any shape.
        :parameter w: required image width.
        :type w: int.
        :parameter h: required image height.
        :type h: int.
        :parameter rgb: states wether the image is rgb or gray scale.
        :type rgb: bool.
        :returns:  none.
        """
        if rgb:
            data = (np.array(sample)*255).reshape(width,height,3)
            img = Image.fromarray(data.astype(np.uint8), 'RGB')
        else:
            data = (np.array(sample)*255).reshape(width,height)
            img = Image.fromarray(data.astype(np.uint8), 'L')

        img.show()
        img.save("sample.jpg")

    def __init(self):
      pass

        

    def __animate(self,i,values,xs,ys,title):
        """
        :Description: 
        A private helper method called by Funcanimate every time interval .

        :parameter i: frame number.
        :type i: int.
        :parameter values: values to be plotted.
        :type values: array of int.
        :parameter xs: empty array to be filled each frame with the frame number.
        :type xs: array of float.
        :parameter ys: empty array to be filled each frame from the values array with the coresponding value.
        :type ys: array of float.
        :parameter title: figure title.
        :type title: str.
        :returns: none.
        """
        xs.append(i)
        ys.append(values[i])
        plt.cla()
        plt.title(title)
        plt.xlabel("iteration")
        plt.ylabel(title)
        plt.plot(xs,ys,color='purple')
        
        

    def live_visualization(self,values):
        """
        :Description: 
        Plots a live visualization for the input vs the number of iterations.

        :parameter values: input values to be graphed.
        :type values: dictionary whose key is the label(str)  and whose items are the values(float) of that label.
        :returns: none.
        """
        title = list(values.keys())[0]
        size = len(values[title])
        xs = []
        ys = []
        ani = animation.FuncAnimation(plt.gcf(), self.__animate,init_func=self.__init, interval=1000,frames=size,fargs=(values[title],xs,ys,title),repeat=False).save(f'{title}.gif', writer='pillow')
        plt.tight_layout()
        plt.show()
        


    def visualize(self,X,Y):
        """
        :Description: 
        plots a graph for the given x,y values and can plot multiple y values for the given x value.

        :parameter X: The label and values on the x axis.
        :type X: dictionary whose key is the label(str)  and whose items are the values(float) of that label.
        :parameter Y: The values on the y axis associated with its name
        :type Y: dictionary each key is the label(str)  and each associated items are the values(float) of that label.
        :returns: none.
        """

        plt.xlabel(list(X.keys())[0])
        for lab,y in Y.items():
            plt.plot(list(X.values())[0],y,label=lab)
        plt.legend()
        plt.show()

    def visualize_multiple_XY(self,xlabel,ylabel,d):
        """
        :Description: 
        plots a graph for the given input.

        :parameter xlabel: The value printed on the x axis.
        :type xlabel: str.
        :parameter ylabel: The value printed on the y axis.
        :type ylabel: str.
        :parameter d: The x and y values for each graph.
        :type d: dictionary with each sub graph label(str) and its x,y(float) values.
        :returns: none.
        """
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        for lab,p in d.items():
            x=p[0]
            y=p[1]
            plt.plot(x,y,label=lab)
        plt.legend()
        plt.show()
    
    def draw_table(self,dic):
      d={'Predict/true':list(dic.keys())}
      d.update(dic)
      df = pd.DataFrame(d)
      data = df
      cell_text = np.array(data)
      row_labels = data.index
      col_labels = data.columns
      ytable = plt.table(cellText=cell_text, colLabels=col_labels, loc="center right")
      plt.axis("off")
      plt.grid(False)
      plt.savefig('table.png')
    
    def visualize_PR(self,xlabel,ylabel,X,Y):
      plt.xlabel(xlabel)
      plt.ylabel(ylabel)
      for (labx,x), (laby,y) in zip(X.items(), Y.items()):
          plt.plot(x,y,label=laby)
      plt.legend()
      plt.show()	



