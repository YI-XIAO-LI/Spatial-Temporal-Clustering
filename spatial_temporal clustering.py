import station_finding
from math import radians, cos, sin, asin, sqrt
from datetime import datetime


# function compute the geo_distance between 2 points using lon and lat info
def geo_distance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2-lng1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    dis = 2*asin(sqrt(a))*6371*1000
    return dis


# function spatially clustered several stations identified in cluster_finding
def find_one_cluster(list):

    cluster_1 = []
    cluster_1.append(list[0])
    del list[0]

    # define cluster add first points into the cluster as starting lon/lat
    j = len(list) - 1
    while j >= 0:
        i = 0
        k = 0

        # compare existing points in the cluster
        while i < len(cluster_1):
            # if geo_dist <= 0.003, keep clustering
            if 0 < abs(list[j][2] - cluster_1[i][2]) <= 0.003 and abs(list[j][3] - cluster_1[i][3]) <= 0.003:
                k += 1

            # if geo-distance to >=3 existing points in the station is smaller than 0.0025, add point to cluster
            if (len(cluster_1) == 1 and k == 1) or k >= 2:
                cluster_1.append(list[j])
                del list[j]  # delete the clustered stations, to avoid repetitive clustering
                j -= 1
                break

            # if the station doesnt belong to the current cluster, test it with the next cluster
            elif i == len(cluster_1) - 1:
                j -= 1
            i += 1

    return cluster_1


# cluster all stations and return all_cluster
def find_all_cluster(list, all_cluster):

    while len(list) != 0:
        one_cluster = find_one_cluster(list)
        all_cluster.append(one_cluster)

    return all_cluster


# return the tyoes of all clusters for each id, define id characteristic by cluster types, return ID list
def time_cluster_all(all_c):
    count = 0
    ID_1 = []
    ID_2 = []

    for one_c in all_c:
        print("Cluster", count+1, ": ", one_c, "\nThis cluster is a " + time_attribute_cluster_one(all_c[count]) + " cluster")
        # return the types of all clusters of an id
        for each_p in one_c:
            if each_p[0] == 1:
                ID_1.append(time_attribute_cluster_one(all_c[count]))
            elif each_p[0] == 2:
                ID_2.append(time_attribute_cluster_one(all_c[count]))
        count += 1

    # print(count)

    # delete clusters without a type
    for type in ID_1:
        if type == '':
            index = ID_1.index(type)
            del ID_1[index]

    # print(ID_1,ID_2,ID_3)
    IDs = [ID_1, ID_2]
    return IDs


# based on cluster characteristics an id visited, give id characteristic
def id_sort(ID_1):
    identification_info = ''
    # define an id person type based on the cluster characteristics it visited
    if 'residential' in ID_1 and 'work place' in ID_1:
        identification_info = "This ID is a worker..."
    elif 'restaurant' in ID_1 and 'work place' not in ID_1:
        identification_info = "This ID is a restaurant cooker or a home worker..."
    elif 'entertain' in ID_1 and 'work place' not in ID_1:
        identification_info = "This ID works at entertaining centers(mall/park) or is a home worker..."
    return identification_info


# function gives each final clusters a characteristic
def time_attribute_cluster_one(one_c):
    work_place = []
    entertainment = []
    residential_area = []
    restaurant = []

    # for short stay clusters
    if one_c[0][4] <= 7200:
        for one_p in one_c:
            # residential area: arriving time evenings, early mornings
            if datetime.strptime('2018/05/23 5:59', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 6:59', "%Y/%m/%d %H:%M"):
                residential_area.append(one_p)

            # restaurant in the noon time or evening
            elif datetime.strptime('2018/05/23 11:00', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 13:30', "%Y/%m/%d %H:%M"):
                restaurant.append(one_p)
            elif datetime.strptime('2018/05/23 17:00', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 18:45', "%Y/%m/%d %H:%M"):
                restaurant.append(one_p)

            # work place in the day time
            elif datetime.strptime('2018/05/23 7:59', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 11:00', "%Y/%m/%d %H:%M") or datetime.strptime('2018/05/23 12:30', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 17:00', "%Y/%m/%d %H:%M"):
                work_place.append(one_p)

            # night time (evening) stay for short span
            elif datetime.strptime('2018/05/23 16:45', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 20:00', "%Y/%m/%d %H:%M"):
                entertainment.append(one_p)

    # for middle stay clusters
    elif 7200 <= one_c[0][4] <= 14400:
        for one_p in one_c:
            # day time, assume work place
            if datetime.strptime('2018/05/23 8:00', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 11:00', "%Y/%m/%d %H:%M") or datetime.strptime('2018/05/23 12:30', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 17:30', "%Y/%m/%d %H:%M"):
                work_place.append(one_p)

            # other majorly residential area
            elif datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") >= datetime.strptime('2018/05/23 17:00', "%Y/%m/%d %H:%M") or datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 4:00', "%Y/%m/%d %H:%M"):
                residential_area.append(one_p)

    # for long-stay clusters, all assume residential areas
    elif one_c[0][4] > 14400:
        for one_p in one_c:
            if datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") >= datetime.strptime('2018/05/23 19:00', "%Y/%m/%d %H:%M") or datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 5:00', "%Y/%m/%d %H:%M"):
                residential_area.append(one_p)
            if datetime.strptime('2018/05/23 8:00', "%Y/%m/%d %H:%M") <= datetime.strptime(one_p[1], "%Y/%m/%d %H:%M") <= datetime.strptime('2018/05/23 17:00', "%Y/%m/%d %H:%M"):
                work_place.append(one_p)

    # print(len(work_place))
    max_len = max(len(work_place), len(restaurant), len(entertainment), len(residential_area))
    if max_len == len(residential_area):
        # print("This cluster is a residential cluster")
        type = 'residential'
    elif max_len == len(restaurant):
        # print("This cluster is a restaurant cluster")
        type = 'restaurant'
    elif max_len == len(work_place):
        # print("This cluster is a working cluster")
        type = 'work place'
    elif max_len == len(entertainment):
        # print("This cluster is a entertaining cluster")
        type = 'entertain'

    return type


# based on stay-time similarities, temporally cluster each stations
def time_cluster(each_c):

    short_stay = []
    middle_stay = []
    long_stay = []

    # set 0-2h, 2-4h, >4h as a time cluster standard
    for each_s in each_c:
        if len(each_s) == 5:

            # cluster each station by time
            if each_s[4] <= 7200:
                short_stay.append(each_s)
            elif 7200 < each_s[4] <= 14400:
                middle_stay.append(each_s)
            elif 14400 < each_s[4]:
                long_stay.append(each_s)

    # renew cluster by stay time
    each_c = []
    each_c.append(short_stay)
    each_c.append(middle_stay)
    each_c.append(long_stay)

    return each_c


if __name__ == "__main__":
    with open('population_analysis_result.txt', 'w') as f:  # 结果写入txt
        all_cluster = []
        # all stations identified in station_finding.py
        myList = [[1.0, '2018/5/23 08:17', 117.15309915, 35.0812937892, 40620],
                  [1.0, '2018/5/23 15:32', 117.17507685, 35.0923061267, 26100],
                  [1.0, '2018/5/23 19:52', 117.153597412, 35.0794417058, 15600],
                  [1.0, '2018/5/23 21:32', 117.15230375, 35.0810298692, 26880],
                  [2.0, '2018/5/23 02:59', 117.157108063, 35.097999856, 21540],
                  [2.0, '2018/5/23 15:49', 117.177428804, 35.0922248874, 46200],
                  [2.0, '2018/5/23 18:07', 117.156998263, 35.098559016, 8280],
                  [2.0, '2018/5/23 19:46', 117.159542908, 35.1033125618, 5940],
                  [2.0, '2018/5/23 21:35', 117.158113902, 35.0975736301, 26700]]

        myList_copy = myList[:]  # make a copy

        # print(find_one_cluster(myList))
        all_cluster = find_all_cluster(myList, all_cluster)
        print("There are", len(all_cluster), "spatial cluster(s) in total:", all_cluster)  # print final spatial clusters
        # f.write("There are" + str(len(all_cluster)) + "spatial cluster(s) in total:" + str(all_cluster))

        all_c = all_cluster[:]  # make a copy

        # print new clusters
        final_cluster = []
        for each_c in all_c:
            small_break_down = time_cluster(each_c)

            # del empty cluster
            if not small_break_down[2]:
                del small_break_down[2]
            if not small_break_down[1]:
                del small_break_down[1]
            if not small_break_down[0]:
                del small_break_down[0]

            final_cluster += small_break_down

        print("There are", len(final_cluster), "spatial-temporal cluster(s) in total:", final_cluster)  # print final spatial-temporal clusters
        # f.write("There are" + str(len(final_cluster)) + "spatial-temporal cluster(s) in total:" + str(final_cluster))

        IDs = []
        IDs = time_cluster_all(final_cluster)  # return the clusters each id visited, write results into a txt file
        print("Three IDs include following cluster type(s) respectively: ", set(IDs[0]), set(IDs[1]))  #, set(IDs[2]))
        f.write("Three IDs include following cluster type(s) respectively: " + str(set(IDs[0])) + " " + str(set(IDs[1])) + "\n")  # + " " + str(set(IDs[2])) + "\n")

        count = 0
        id_list = [1, 2]

        # portray population characteristics based on the cluster an id visited
        for id in IDs:
            print("for ID#", id_list[count], ": ")
            f.write("for ID#" + str(id_list[count]) + ": ")
            print(id_sort(id))
            f.write(id_sort(id) + "\n")
            count += 1

    f.close()
