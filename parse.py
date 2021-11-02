def parseData(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    d = []
    restrictions = [int(li.strip()) for li in lines[0].split(",")]
    lines = lines[1:]
    lineList = []
    for line in lines:
        line = line.strip().replace("\"", "")
        lineList.append([float(li) for i, li in enumerate(line.split(",")) if restrictions[i] == 1])
    return lineList


def parseGTData(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    d = []
    restrictions = [int(li.strip()) for li in lines[0].split(",")]
    lines = lines[1:]
    iris_dict = {}
    for line in lines:
        line = line.strip().replace("\"", "")
        lineList = []
        cat = None
        for i, li in enumerate(line.split(",")):
            if len(li) == 0:
                continue
            if restrictions[i] == 0:
                cat = li
            elif restrictions[i] == 1:
                lineList.append(float(li))
        if len(lineList) > 1:
            iris_dict[tuple(lineList)] = cat
            d += [lineList]
    return d, iris_dict

