import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

fp="/home/rodrigostancioli/Documents/asi2/asi/estados/ground/ground/obc/config/L004metacustom.xyz"
#fp="/home/rodrigostancioli/Documents/asi2/asi/estados/results/obc/bin2/L04/config/config_L=004_t=0.50000E=   -19.xyz"
#fp="/home/rodrigostancioli/Documents/asi2/asi/estados/ground/ground/obc/config/L004metateste.xyz"
with open(fp) as f:
    elements = int(f.readline())
    print('no of elements =', elements)

df_columns = ['type','x','y','z','separator','vx','vy','vz','energy']
array_columns_spins = ['x','y','vx','vy']
array_columns_vertices = ['x','y']
data = pd.read_csv(fp, sep=' ', names=df_columns, skiprows=[0,1],
    skipinitialspace=True)
spin_types = ['Al']
vertex_types = ['Cu', 'Mg', 'Fe', 'Hg', 'Au', 'Ag', 'Na']
vertex_shapes = ['circle', 'circle', 'square', 'diamond', 'circle', 'circle', 'square']
rd = {'large': .32, 'small': .2, 'vl': .35, 'vs': .2}
vertex_radius = [rd['large'], rd['large'], rd['large'], rd['large'], rd['small'], rd['small'], rd['small']]
#vertex_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink']
#vertex_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
cd = {'gr': '#0e7c57', 'ye': 'y', 'bl': '#4c80f0', 're': 'r'}
vertex_colors = [cd['bl'], cd['re'], cd['gr'], cd['ye'], cd['bl'], cd['re'], cd['gr']]


spins = []
for spin_type in spin_types:
    df = data.loc[data['type'] == spin_type]
    for col in df_columns:
        if col not in array_columns_spins:
            df.pop(col)
    spins.append(df.to_numpy())

vertices = []
for vertex_type in vertex_types:
    df = data.loc[data['type'] == vertex_type]
    for col in df_columns:
        if col not in array_columns_vertices:
            df.pop(col)
    vertices.append(df.to_numpy())

fig, ax = plt.subplots()
ax.axis('off')
ax.set_aspect('equal')

for i, vertex_array in enumerate(vertices):
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
    ax.add_collection(c)

for spin_array in spins:
    ax.quiver(spin_array[:,0], spin_array[:,1], spin_array[:,2], spin_array[:,3], 
        pivot='middle', units='x', width=.2, scale=1, headlength=3, headwidth=3,
        headaxislength=2.5)

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
    
plt.savefig('/home/rodrigostancioli/Documents/asi2/figures/config/meta1.pdf', format='pdf')
plt.show()