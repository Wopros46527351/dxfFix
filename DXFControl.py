import time
from collections import defaultdict 
from utility import get_distance,intersect
from graph import Graph
from LWPUtils import *











if __name__=="__main__":
    '''filename = input("Введите имя файла dxf")
    if not filename.endswith(".dxf"):
        filename+=".dxf"
    source_dxf = ezdxf.readfile(filename)
    if check_dxf_info(source_dxf):
        source_dxf = fix_polylines(source_dxf)
    result = redraw_figure_way(source_dxf)'''
    result = test_line()
    filename = "test.dxf"
    '''filename = input("Введите имя файла dxf")
    if not filename.endswith(".dxf"):
        filename+=".dxf"
    source_dxf = ezdxf.readfile(filename)
    if check_dxf_info(source_dxf):
        source_dxf = fix_polylines(source_dxf)
    print(len(source_dxf.modelspace()))
    source_dxf = fix_dupes(source_dxf)
    print(len(source_dxf.modelspace()))
    result = redraw_path_way_vertical(source_dxf)'''
    result.saveas(f'{filename[:-4:]}-r.dxf')
    input("ENTER для выхода")



