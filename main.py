from Algorithm import IQACO
from Draw import GridPlot,IterationGraph
from Map import Map

m = Map()
m.load_map_file('res\\map_base_50.txt')
aco = IQACO(m.data, ant_num=50, start=[0,0], end=[49,49], max_iter=50)
aco.run()
fig = GridPlot(m.data)
fig.draw_path(aco.best_path_data)
fig = IterationGraph([aco.avg_path_lengths, aco.best_path_lengths])
fig.show()