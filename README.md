# xyz_matplot
Matplotlib routine to plot spin models in a lattice (xyz files).

`plot.py` is the main file and can be used as a module. When used as a main program, it takes three arguments from command line:
1. Name of the input file (mandatory). The input file should be placed in the `./input/` directory. 
It should have the same structure as the files included as examples and have the `.xyz` extension.
2. `save` or `gif` (optional). If `save`, the first frame is written to a file. If `gif`, an animation is written to a file.
3. Output file (optional). If `save` or `gif` has been chosen, the file will be saved in the `./output/` folder with the chosen name.

**Example:** `python plot.py L4gr_mod2 save teste0419`

`plot_mono.py` and `vertices.py` use the `plot.py` module to do specific things.
