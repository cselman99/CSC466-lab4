def parseData(input_file):
    file = open(input_file, "r")
    lines = file.readlines()
    d = []
    restrictions = [int(li.strip()) for li in lines[0].split(",")]
    lines = lines[1:]
    for line in lines:
        line = line.strip().replace("\"", "")
        lineList = [int(li) for li in line.split(",")]
        if len(lineList) > 1:
            new_lines = []
            for li in range(len(lineList)):
                if restrictions[li] == 1:
                    new_lines.append(lineList[li])
            d += [new_lines]
    return d
