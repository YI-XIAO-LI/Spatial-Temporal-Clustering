import read_excel


# function groups trajectory points into stations spatially
def find_one_cluster(list, index):
    # define station, and add start point
    cluster_1 = []
    cluster_1.append(list[index])

    # starting index is j
    j = 1 + index

    while j < len(list):
        i = 0
        k = 0  # count close points to a station

        # compare next point to existing points in the station
        while i < len(cluster_1):
            # print(len(cluster_1))
            # if geo-distance to existing points in station smaller than 0.0025, increment k
            if 0 < abs(list[j][2] - cluster_1[i][2]) <= 0.0025 and abs(list[j][3] - cluster_1[i][3]) <= 0.0025:
                k += 1

            # if geo-distance to >=3 existing points in the station is smaller than 0.0025, add point to cluster
            if (len(cluster_1) == 1 and k == 1) or(len(cluster_1) == 2 and k == 2) or k >= 3:
                cluster_1.append(list[j])
                break

            # if current point does not belong to current station, search for next station
            if abs(list[j][2] - cluster_1[i][2]) > 0.5 or abs(list[j][3] - cluster_1[i][3]) > 0.5:
                j = len(list)
                break
            i += 1
        j += 1

    # return a clustered station
    return cluster_1


# function finds all stations(clusters)
def find_all_cluster(list, all_cluster):
    count = 0
    while count < len(list):
        # find each station(cluster) and add each station to all_cluster
        one_cluster = find_one_cluster(list, count)
        all_cluster.append(one_cluster)
        count = count + len(one_cluster)  # update next starting index for next station

    return all_cluster


# function takes the first point in each station as a representation of the station's lon and lat
def find_stations(all_cluster):
    station_l = []
    for each_c in all_cluster:
        # delete stations with less than three points
        if len(each_c) < 3:
            i = all_cluster.index(each_c)
            del all_cluster[i]
        else:
            station_l.append(each_c[1])
    return station_l


# for trajectories, function adds stay time at each clustered station
def add_stay_time(all_s):
    i = 1  # a counter
    linger = 0.0

    while i < len(all_s) and i != len(all_s) -1:
        # compute stay time at each station
        linger = read_excel.cal_time(all_s[i-1][1], all_s[i][1])
        all_s[i].append(linger)
        i += 1

    # compute the starting and ending stay time for the first and last stay
    all_s[0].append(read_excel.cal_time('2018/5/22 21:00', all_s[0][1]))
    all_s[len(all_s)-1].append(read_excel.cal_time(all_s[len(all_s)-1][1], '2018/5/24 5:00'))


if __name__ == "__main__":
    all_cluster_1 = []
    all_cluster_2 = []
    all_cluster_3 = []

    # read in all trajectory points in the excel file
    myList = read_excel.read_excel("test_update.xlsx", "test")
    myList_copy = myList[:]  # make a copy

    # assign all points to each id
    ID_1 = []
    ID_3 = []
    for each_c in myList:
        if each_c[0] == 1:
            ID_1.append(each_c)
        elif each_c[0] == 2:
            ID_3.append(each_c)

    # ID#1
    all_cluster_1 = find_all_cluster(ID_1, all_cluster_1)  # find all complete stations for ID 1
    # simplify by storing the first point in all clusters for ID 1
    station_l1 = find_stations(all_cluster_1)
    # add stay time for each station (in seconds)
    add_stay_time(station_l1)

    print("There are", len(station_l1), "station(s) in total for ID 1:", station_l1)

    # ID#3
    all_cluster_3 = find_all_cluster(ID_3, all_cluster_3)  # find all complete stations for ID 3

    # find all clusters for ID 1
    station_l3 = find_stations(all_cluster_3)
    # add stay time for each station (in seconds)
    add_stay_time(station_l3)

    print("There are", len(station_l3), "station(s) in total for ID 2:", station_l3)
    
"""
    # test validity
    station_l1_edit = [[1.0, '2018/5/23 08:17', 117.15309915, 35.0812937892], [1.0, '2018/5/23 15:32', 117.17507685, 35.0923061267], [1.0, '2018/5/23 19:52', 117.153597412, 35.0794417058], [1.0, '2018/5/23 21:32', 117.15230375, 35.0810298692]]
    station_l3_edit = [[2.0, '2018/5/23 02:59', 117.157108063, 35.097999856], [2.0, '2018/5/23 15:49', 117.177428804, 35.0922248874], [2.0, '2018/5/23 18:07', 117.156998263, 35.098559016], [2.0, '2018/5/23 19:46', 117.159542908, 35.1033125618], [2.0, '2018/5/23 21:35', 117.158113902, 35.0975736301]]
    add_stay_time(station_l1_edit)
    add_stay_time(station_l3_edit)

    all_cs = station_l1_edit + station_l3_edit  # + station_l2
    print(all_cs, '\n', station_l3_edit, '\n', station_l1_edit)
"""
