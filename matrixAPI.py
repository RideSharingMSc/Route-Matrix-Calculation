import urllib2
import json
import math

node_list_longitudes = []
node_list_latitudes = []
count1 = 0
loopCount = 70.0

with open('data.txt') as f:
    lines = f.readlines()
    for x in lines:
        node = x.split(",")
        node_list_latitudes.insert(count1, node[1])
        node_list_longitudes.insert(count1, node[2].split("\n")[0])
        count = count1 + 1

count = 0;
total = len(node_list_latitudes) * len(node_list_latitudes)
ceilVal = int(math.ceil(len(node_list_latitudes)/loopCount))

for z in range(0, ceilVal):
    sources = ""
    sourcesList = "?sources="
    sourceCount = 0

    if ceilVal - 1 == z:
        for a in range(z*int(loopCount), z*int(loopCount)+ len(node_list_latitudes) - z*int(loopCount), 1):
            sources = sources + node_list_latitudes[a] + "," + node_list_longitudes[a] + ";"
            if a == z*int(loopCount)+ len(node_list_latitudes) - z*int(loopCount) - 1 :
                sourcesList = sourcesList + str(sourceCount)
            else:
                sourcesList = sourcesList + str(sourceCount) + ";"
            sourceCount = sourceCount + 1
    else:
        for a in range(z * int(loopCount), z * int(loopCount) + int(loopCount)):
            sources = sources + node_list_latitudes[a] + "," + node_list_longitudes[a] + ";"
            if a == z * int(loopCount) + int(loopCount) -1 :
                sourcesList = sourcesList + str(sourceCount)
            else:
                sourcesList = sourcesList + str(sourceCount) + ";"
            sourceCount = sourceCount + 1

    for q in range(0, ceilVal):
        destinationsCount = 0
        destinationsList = "&destinations="

        matrix_file = open("matrix.txt", "a")
        destinationsCount = sourceCount

        if ceilVal - 1 == q:

            node_list = []
            urlContent = sources

            for x in range(q*int(loopCount), q*int(loopCount)+ len(node_list_latitudes) - q*int(loopCount), 1):
                if x == q*int(loopCount) + len(node_list_latitudes) - q*int(loopCount) - 1:
                    urlContent = urlContent + node_list_latitudes[x] + "," + node_list_longitudes[x]
                    destinationsList = destinationsList + str(destinationsCount)
                    destinationsCount = destinationsCount + 1
                else:
                    urlContent = urlContent + node_list_latitudes[x] + "," + node_list_longitudes[x] + ";"
                    destinationsList = destinationsList + str(destinationsCount) + ";"
                    destinationsCount = destinationsCount + 1

            url = "http://localhost:5000/table/v1/driving/" + urlContent + sourcesList + destinationsList
            print url

            content = urllib2.urlopen(url).read()
            json_data = json.loads(content)
            node_list = (json_data['durations'])

            for y in range (0, len(node_list)):
                node_list_temp = node_list[y]
                matrix_file.write(str(node_list_temp))
                matrix_file.write("\n")
                count = count + len(node_list[y])

            print (str(count) + "/" + str(total))
        else:

            node_list = []
            urlContent = sources

            for x in range(q * int(loopCount), q * int(loopCount) + int(loopCount)):
                if x == q * int(loopCount) + int(loopCount) - 1:
                    urlContent = urlContent + node_list_latitudes[x] + "," + node_list_longitudes[x]
                    destinationsList = destinationsList + str(destinationsCount)
                    destinationsCount = destinationsCount + 1
                else:
                    urlContent = urlContent + node_list_latitudes[x] + "," + node_list_longitudes[x] + ";"
                    destinationsList = destinationsList + str(destinationsCount) + ";"
                    destinationsCount = destinationsCount + 1

            url = "http://localhost:5000/table/v1/driving/" + urlContent + sourcesList + destinationsList
            print url

            content = urllib2.urlopen(url).read()
            json_data = json.loads(content)
            node_list = (json_data['durations'])

            for y in range(0, len(node_list)):
                node_list_temp = node_list[y]
                matrix_file.write(str(node_list_temp))
                matrix_file.write("\n")
                count = count + len(node_list[y])

            print (str(count) + "/" + str(total))

        matrix_file.write("\n")
        matrix_file.close()
