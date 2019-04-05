import plot

file_name = 'vertices2'
new_collection = plot.FrameCollection(file_name)
bound={'left': 0, 'right': 50, 'bottom': 0, 'top': 20}
#bound={'left': None, 'right': None, 'bottom': None, 'top': None}
plt_lat = plot.PlotLattice(bound)
plt_lat.plot_lattice(new_collection.collection[0])