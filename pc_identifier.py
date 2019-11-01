def getPC():
    f = open(".idea/computer.txt", "r")
    for line in f:
        pc = line
    return pc

def getRes():
    pc = getPC()
    if pc == "Desktop":
        geom = "1920x1080+-1920+0"
    elif pc == "Laptop":
        geom = "1920x1080+0+0"
    return geom

def getType():
    pc = getPC()
    if pc == "Desktop":
        return "zoomed"
    elif pc == "Laptop":
        return "normal"

