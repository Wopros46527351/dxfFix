import ezdxf
import sys

#Тут все стандартные функции, открываем файлы, читаем содержимое

def open_file(file_name = ""):
    """Открываем файл

    Returns:
        [type]: [description]
    """
    #Немного интерфейса для человека,сделать его не составит труда позднее, а сейчас можете просто его указывать
    if not file_name:
        #https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
        pass
    try:
        doc = ezdxf.readfile(file_name)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)
    return doc

def read_dxf(msp):
    #Где доки??
    print('Количество деталей в файле - ', len(msp))
    figures = {}
    # В цикле сразу считайте колличество фигур
    for e in msp:
        if e.dxftype() in figures.keys():
            figures[e.dxftype()] += 1
        else:
            figures[e.dxftype()] = 0
    for i in figures.keys():
        print(i, figures[i])
    return None