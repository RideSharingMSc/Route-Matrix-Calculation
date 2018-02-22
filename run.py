import urllib2
import json

node_list_longitudes = []
node_list_latitudes = []
count = 0
loopCount = 1

with open('data.txt') as f:
    lines = f.readlines()
    for x in lines:
        node = x.split(",")
        node_list_latitudes.insert(count, node[1])
        node_list_longitudes.insert(count, node[2].split("\n")[0])
        count = count + 1

count = 0;
total = len(node_list_latitudes) * len(node_list_latitudes)

for z in range(0, len(node_list_latitudes)):
    matrix_file = open("matrix.txt", "a")
    route_file = open("route.txt", "a")

    for x in range(0, len(node_list_latitudes), loopCount):

        route_file.write(str(z) + "," + str(x) + ",")

        node_list = []
        duration_list = []
        test_list = []
        #example url
        #http://104.197.181.232/route/v1/driving/79.928669,6.846257;79.896562,6.864980?annotations=true

        urlContent = ""
        urlContent = urlContent + node_list_latitudes[z] + "," + node_list_longitudes[z] + ";"
        urlContent = urlContent + node_list_latitudes[x] + "," + node_list_longitudes[x]

        url = "http://104.197.181.232/route/v1/driving/" + urlContent + "?annotations=true"

        content = urllib2.urlopen(url).read()
        json_data = json.loads(content)
        node_list = (json_data['routes'][0]["legs"][0]["annotation"]["nodes"])
        duration_list = (json_data['routes'][0]["legs"][0]["annotation"]["duration"])
        duration = (json_data['routes'][0]["legs"][0]["duration"])

        if x == len(node_list_latitudes) - 1 :
            matrix_file.write(str(duration))
        else:
            matrix_file.write(str(duration) + ",")


        duration_local = 0
        for d in range(0, len(duration_list)):
            duration_local = duration_local + duration_list[d]


        duration_one = (duration - duration_local)/2

        if duration_one >= 0 :
            duration_30 = duration_one
        else:
            duration_30 = 0

        for d in range(0, len(duration_list)):
            duration_temp = duration_30;
            duration_30 = duration_30 + duration_list[d]

            if duration_30 >= 30 :
                up_diff = abs(duration_30 - 30)
                down_diff = abs(30 - duration_temp)

                if up_diff <= down_diff:
                    route_file.write(str(node_list[d]) + ",")
                    duration_30 = 0;
                else:
                    route_file.write(str(node_list[d-1]) + ",")
                    duration_30 = duration_list[d];

        route_file.write("\n")
    
        count = count + 1
        print (str(count) + "/" + str(total))


    matrix_file.write("\n")
    matrix_file.close()
    route_file.close()
