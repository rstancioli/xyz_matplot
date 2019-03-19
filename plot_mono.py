import plot
import pandas as pd

df_columns = ['type','x','y','z','colors','vx','vy','vz','energy']
df_types = ['object', 'float', 'float', 'float', 'object', 'float', 'float', 'float', 'float']
dtypes = dict(zip(df_columns, df_types))

#file_name = 'L080_peq_redux2'
file_name = 'L080_redux'
#file_name = 'L4gr_mod2'

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
        data.loc[data['vx'] < -.1, 'colors'] = 'c'
        new_frame = plot.Frame(data)
    collection.append(new_frame)

plt_lat = plot.PlotLattice()
plt_lat.save_gif(collection, 'teste_mono')


for i in range(4,len(collection)):
    frame = collection[i]
    plt_lat = plot.PlotLattice()
    #plt_lat.plot_lattice(frame, save=False, file_name='untitled_lattice.pdf',
    #            left=131.906, right=149.73, bottom=135.574, top=144.05)
    plt_lat.plot_lattice(frame, save=False, file_name='untitled_lattice.pdf',
                left=131.906, right=149.73, bottom=135.574, top=145.223)