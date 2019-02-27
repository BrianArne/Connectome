fi = open("aal.csv") #TODO: allow for differing names
i = 0 #1?
size = "1"
data_string = ""
data = fi.readlines() #assuming same format for all of the .csv files, else: import re, re.compile(REGEX)

#where would the 'size' parameter be calculated from?

for line in data:
    x, y, z, region = line.split(",")
    #size = ??
    data_string = data_string + x + "\t" + y + "\t" + z + "\t" + str(i) + "\t" + size + "\t" + region #assumes '\n', since grabbing lines (include a checker?)

    i = i + 1

#print(data_string)

fi.close()

fo = open("ex.node", "w+")
fo.write(data_string) #weird spacing/tabbing?
fo.close()
