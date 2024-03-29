import ezdxf
import time
from collections import defaultdict 
from utility import get_distance,intersect
from graph import Graph
from LWPUtils import *
from figure import figure
import matplotlib.pyplot as plt
'''
filename = "111.dxf"
sourceDxf = ezdxf.readfile(filename)
check_dxf_info(sourceDxf)
msp = sourceDxf.modelspace()
figs = [figure(i) for i in msp]
for f in figs:
    f.drawFigurePlt()
    f.drawCenter()
plt.axis('equal')
plt.show()'''
def prepare_for_deepnest(filename,sizeX,sizeY,save_filename = "result.dxf"):
    print("Step 1: prepare for deepnest")
    source_dxf = ezdxf.readfile(filename)
    check_dxf_info(source_dxf)
    msp = source_dxf.modelspace()
    draw_box(msp,sizeX,sizeY)
    source_dxf.saveas(save_filename)
    print("Done!")
    return source_dxf

def show_file(filename):
    filename = "result.dxf"
    sourceDxf = ezdxf.readfile(filename)
    #check_dxf_info(sourceDxf)
    msp = sourceDxf.modelspace()
    figs = [figure(i) for i in msp]
    for f in figs:
        f.drawFigurePlt()
        f.drawCenter()
    plt.axis('equal')
    plt.show()
    plt.clf()

def fix(filename):
    print("Load nested dxf")
    filename = "nest.dxf"
    sourceDxf = ezdxf.readfile(filename)
    #check_dxf_info(sourceDxf)
    new_dxf = fix_polylines(sourceDxf)
    check_dxf_info(new_dxf)
    nmsp = new_dxf.modelspace()
    figs = [figure(i) for i in nmsp]
    print(f"total {len(figs)} figs")
    for f in figs:
        f.drawFigurePlt()
        f.drawCenter()
    plt.axis('equal')
    plt.show()
    plt.clf()
    return new_dxf

def redraw_draw(filename):
    print("Connecting figures tree way")
    sourceDxf = ezdxf.read(filename)
    result = redraw_figure_way(sourceDxf)
    result.saveas("tree.dxf")
    check_dxf_info(result)
    msp = result.modelspace()
    figs = [figure(i) for i in msp]
    print(f"total {len(figs)} figs")
    for f in figs:
        f.drawFigurePlt()
        f.drawCenter()
    plt.axis('equal')
    plt.show()
    plt.clf()

print("Redraw box way")


if __name__ == "__main__":
    filename = "111.dxf"
    prepare_for_deepnest(filename,2000,1000)
    source_dxf = fix("nest.dxf")
    source_dxf.saveas("fixed.dxf")
    redraw_draw("fixed.dxf")


'''if __name__=="__main__":
    filename = input("Введите имя файла dxf")
    if not filename.endswith(".dxf"):
        filename+=".dxf"
    source_dxf = ezdxf.readfile(filename)
    if check_dxf_info(source_dxf):
        source_dxf = fix_polylines(source_dxf)
    result = redraw_figure_way(source_dxf)
    result = test_line()
    filename = "test.dxf"
    filename = input("Введите имя файла dxf")
    if not filename.endswith(".dxf"):
        filename+=".dxf"
    source_dxf = ezdxf.readfile(filename)
    if check_dxf_info(source_dxf):
        source_dxf = fix_polylines(source_dxf)
    print(len(source_dxf.modelspace()))
    source_dxf = fix_dupes(source_dxf)
    print(len(source_dxf.modelspace()))
    result = redraw_path_way_vertical(source_dxf)
    result.saveas(f'{filename[:-4:]}-r.dxf')
    input("ENTER для выхода")'''



