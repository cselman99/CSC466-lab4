def parseData(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    d = []
    restrictions = lines[0].split(",")
    lines = lines[1:]
    for i, line in enumerate(lines):
        if restrictions[i] == 0:
            continue
        line = line.strip().replace("\"", "")
        lineList = line.split(",")
        if len(lineList) > 1:
            d += [lineList]
    return d
