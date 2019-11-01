def getRes():
    f = open(".idea/computer.txt", "r")
    for line in f:
        pc = line

    if pc == "Desktop":
        geom = "1280x720+-1600+100"
    elif pc == "Laptop":
        geom = "1280x720+300+150"
    return geom