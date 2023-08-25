import csv

from Location import locationHash

# with open('WGUPS Distance File.csv') as distanceList:
#     distanceData = csv.reader(distanceList, delimiter=',')
#     next(distanceData)
#     next(distanceData)
#     for location in distanceData:
#         for j in range(27):
#             if location[j+2] != '' and float(location[j+2]) > 0.0:
#                 print("g.add_undirected_edge(vertex_" + location[0] + ", vertex_" + str(j + 1) + ", " + location[j + 2] + ")")
#
# output  = ""
# for i in range(1, 28):
#     output+=", milesToID"+str(i)
# print(output)
#
for i in range(0, 27):
    print("distanceList.append(float(location[" + str(i+3) +"]))")

