# Example with obstacles    
from jps import *

set_visual(True)

# Image test to load a map from an image
m = load_obstacle_image('obstacle map.png', 0xff0000)
print("loaded image")
path = get_full_path(jps(m, 40, 20, 217, 100))  # calculate a path from (40, 20) to (607, 310). 
print("calculated shortest path")
draw_jps(m, path, 'obstacle map.png')
