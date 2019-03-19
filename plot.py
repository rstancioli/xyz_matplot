import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from matplotlib.animation import FuncAnimation

print(matplotlib.get_backend())


df_columns = ['type','x','y','z','colors','vx','vy','vz','energy']
df_types = ['object', 'float', 'float', 'float', 'object', 'float', 'float', 'float', 'float']
dtypes = dict(zip(df_columns, df_types))
array_columns_spins = ['x','y','vx','vy']
array_columns_vertices = ['x','y']
spin_types = ['Al']
vertex_types = ['Cu', 'Mg', 'Fe', 'Hg', 'Au', 'Ag', 'Na']
vertex_shapes = ['circle', 'circle', 'square', 'diamond', 'circle', 'circle', 'square']
rd = {'large': .32, 'small': .2, 'vl': .35, 'vs': .2}
vertex_radius = [rd['large'], rd['large'], rd['large'], rd['large'], rd['small'], rd['small'], rd['small']]
#vertex_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
#vertex_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
cd = {'gr': '#0e7c57', 'ye': 'y', 'bl': '#4c80f0', 're': 'r'}
vertex_colors = [cd['bl'], cd['re'], cd['gr'], cd['ye'], cd['bl'], cd['re'], cd['gr']]


class FrameCollection():
    def __init__(self, file_name):
        self.collection = self.get_collection(file_name)

    def get_collection(self, file_name):
        #fp="/home/rodrigostancioli/Documents/asi2/asi/estados/ground/ground/obc/config/L004metacustom.xyz"
        fp = "./files/" + file_name + ".xyz"
        with open(fp) as f:
            file_lines = f.readlines()      
        elements = int(file_lines[0])
        last_line=len(file_lines)
        no_of_frames = int(last_line / (elements + 2))
        print('no of elements =', elements)
        print('number of frames: ', no_of_frames)
        collection = []
        for frame in range(0, no_of_frames):
            with open(fp) as f:
                data = pd.read_csv(f, sep=' ', names=df_columns, skiprows=2+(elements+2)*frame,
                    nrows=elements, skipinitialspace=True, dtype=dtypes)
                new_frame = Frame(data)
            collection.append(new_frame)
        return collection


class Frame():
    def __init__(self, data):
        self.spins = self.get_spins(data)
        self.vertices = self.get_vertices(data)
        self.colors = self.get_colors(data)

    def get_spins(self, data):
        spins = []
        for spin_type in spin_types:
            df = data.loc[data['type'] == spin_type]
            for col in df_columns:
                if col not in array_columns_spins:
                    df.pop(col)
            #df = df[df['vx'].abs() > 0]
            #df = df[df['vy'].abs() > 0]
            spins.append(df.to_numpy())
        return spins

    def get_vertices(self, data):
        vertices = []
        for vertex_type in vertex_types:
            df = data.loc[data['type'] == vertex_type]
            for col in df_columns:
                if col not in array_columns_vertices:
                    df.pop(col)
            vertices.append(df.to_numpy())
        return vertices

    def get_colors(self, data):
        colors = []
        for spin_type in spin_types:
            df = data.loc[data['type'] == spin_type]
            lista = df['colors'].to_list()
            for i, element in enumerate(lista):
                if element == 'atom_vector':
                    lista[i] = [0.6, 0.6, 0.6]
                if element == 'c':
                    lista[i] = [0., 0., 0.]
            colors.append(lista)
        return colors


class PlotLattice():

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.subplots()

    def plot_lattice(self, frame, save=False, file_name='untitled_lattice.pdf'):
        self.draw_plot(frame)
        if save:    
            self.fig.savefig('./output/' + file_name + '.pdf', format='pdf')
            print('Figure saved to file.')
        plt.show()

    def draw_plot(self, frame):
        plt.cla()
        self.ax.axis('off')
        self.ax.set_aspect('equal')
        for i, vertex_array in enumerate(frame.vertices):
            if vertex_shapes[i] == 'circle':
                shapes = [plt.Circle((xi,yi), radius=vertex_radius[i], linewidth=0, color=vertex_colors[i]) 
                    for xi,yi in zip(vertex_array[:,0], vertex_array[:,1])]
            elif vertex_shapes[i] == 'diamond':
                shapes = [patches.RegularPolygon((xi,yi), 4, radius=vertex_radius[i], linewidth=0, color=vertex_colors[i]) 
                    for xi,yi in zip(vertex_array[:,0], vertex_array[:,1])]
            elif vertex_shapes[i] == 'square':
                shapes = [patches.RegularPolygon((xi,yi), 4, radius=vertex_radius[i], orientation=.7854, linewidth=0, color=vertex_colors[i]) 
                    for xi,yi in zip(vertex_array[:,0], vertex_array[:,1])]
            #for shape in shapes:
            #    ax.add_artist(shape)
            c = PatchCollection(shapes, match_original=True)
            self.ax.add_collection(c)
        for i, spin_array in enumerate(frame.spins):
            colors = np.array(frame.colors[i], dtype=float)
            self.ax.quiver(spin_array[:,0], spin_array[:,1], spin_array[:,2], spin_array[:,3], color=colors,
                pivot='middle', units='x', width=.2, scale=1, headlength=3, headwidth=3,
                headaxislength=2.5)
        self.ax.set_xlim(left=0)
        self.ax.set_ylim(bottom=0)
        #return self.ax

    def save_gif(self, collection, file_name='untitled_lattice.gif'):
        #fig = draw_plot(collection[0])
        #fig = plt.figure()
        anim = FuncAnimation(self.fig, self.draw_plot, frames=collection)
        anim.save('./output/' + file_name + '.gif', dpi=80, writer='imagemagick')
        #plt.show()


if __name__ == "__main__":
    print(sys.argv)
    file_name = sys.argv[1]
    save = False
    gif = False
    output_file = None
    if len(sys.argv) > 2:
        if sys.argv[2] == 'save':
            save = True
        elif sys.argv[2] == 'gif':
            gif = True
        output_file = sys.argv[3]
    new_collection = FrameCollection(file_name)
    plt_lat = PlotLattice()
    if gif:
        print('gif')
        plt_lat.save_gif(new_collection.collection, file_name=output_file)
    else:
        print('image')
        plt_lat.plot_lattice(new_collection.collection[0], save=save, file_name=output_file)
    
    