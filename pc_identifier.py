def getRes():
    f = open(".idea/computer.txt", "r")
    for line in f:
        pc = line

    if pc == "Desktop":
        geom = "1920x1080+-1920+0"
    elif pc == "Laptop":
        geom = "1920x1080+0+0"
    return geom