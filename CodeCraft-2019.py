# -*- coding: utf-8 -*-

import logging
import sys

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


# 对道路分类，根据不同的速度


def diff_speed_graph(speed: list, road_path):
    graph = [[0] * 64 for i in range(64)]
    r = open(road_path)
    for line in r:
        road = line.strip('\n')
        if road.startswith('#') is False:  # 字符串是否已某个字符开头 startswith('#')  endswith()
            road = road.strip('()')  # 去除首尾的字符
            road = road.split(',')  # 以“，”分割
            # roadinfo = {'roadid':int(road[0]),'length':int(road[1]),'speed':int(road[2]),
            # 'channel':int(road[3]),'from':int(road[4]),'to':int(road[5]),'isDuplex':int(road[6])}
            # print(int(road[4])-1, int(road[5])-1)
            if int(road[2]) in speed:
                graph[int(road[4])-1][int(road[5])-1] = int(road[0])
                if int(road[6]):
                    graph[int(road[5])-1][int(road[4])-1] = graph[int(road[4])-1][int(road[5])-1]
    r.close()
    return graph


# 求一辆车的最短路线，[] 代表不能到达


def from_to(car_from, car_to, passed, lengh, graph):
    lengh += 1
    if lengh > 14:
        return []
    if graph[car_from][car_to] != 0:
        return [graph[car_from][car_to]]
    k = 0
    ans = []
    passed_temp = passed[:]
    # 从矩阵graph的car_from 到car_to 行
    for i in range(0, 64):
        if i not in passed and graph[car_from][i] != 0:
            # if i == car_to:
            #     return [A[car_from][i]]
            passed_temp.append(i)
            i_to = from_to(i, car_to, passed_temp, lengh, graph)
            if i_to:
                ans.append([])
                ans[k].append(graph[car_from][i])
                # print(passed)
                # ans[k].append(from_to(i, car_to, passed))
                ans[k] += i_to
                k += 1
    if ans:
        answer_temp = ans[0]
        for a in ans:
            if len(a) < len(answer_temp):
                answer_temp = a
        return answer_temp
    return ans


def run(car_path, answer_path, road_path):
    """
    ll = [[8,16,24,32,40,48,56,64],
            [7,15,23,31,39,47,55,63],
            [6,14,22,30,38,46,54,62],
            [5,13,21,29,37,45,53,61],
            [4,12,20,28,36,44,52,60],
            [3,11,19,27,35,43,51,59],
            [2,10,18,26,34,42,50,58],
            [1,9,17,25,33,41,49,57]]
    carsX = []#从左到右的车与上下直行的车
    carsY = []#从右到左的车
    ff = open(car_path)
    for line in ff:
        cars = line.strip('\n')
        if cars.startswith('#') == False :#字符串是否已某个字符开头 startswith('#')  endswith()
            cars = cars.strip('()')#去除首尾的字符
            cars = cars.split(',')#以“，”分割
            cars = [ int(x) for x in cars ]#cars[0]表示车辆id、cars[1]表示表示车辆出发地、cars[2]表示车辆目的地、cars[3]表示车速、cars[4]表示出发时间
            #print(cars)
            i = 0
            jfrom = 0
            jto = 0
            while i < len(ll):
                j = 0
                while j < len(ll[0]):
                    if ll[i][j] == cars[1]:#匹配出发地
                        jfrom = j
                    if ll[i][j] == cars[2]:#匹配目的地
                        jto = j
                    j +=1
                i +=1
            if jfrom <= jto:
                carsX.append(cars)
            else:
                carsY.append(cars)
    ff.close()
    #  print(len(carsX))
    #  print(len(carsY))
    """

    carsX = []#从左到右的车与上下直行的车
    carsY = []#从右到左的车
    ff = open(car_path)
    for line in ff:
        cars = line.strip('\n')
        if cars.startswith('#') == False :#字符串是否已某个字符开头 startswith('#')  endswith()
            cars = cars.strip('()')#去除首尾的字符
            cars = cars.split(',')#以“，”分割
            cars = [ int(x) for x in cars ]#cars[0]表示车辆id、cars[1]表示表示车辆出发地、cars[2]表示车辆目的地、cars[3]表示车速、cars[4]表示出发时间
            #print(cars)
            jfrom = (cars[1] - 1)%8
            jto = (cars[2] - 1)%8
            if jfrom <= jto:
                carsX.append(cars)
            else:
                carsY.append(cars)
    ff.close()

    """
    carsXspeed2 = []
    carsXspeed4 = []
    carsXspeed6 = []
    carsXspeed8 = []
    carsYspeed2 = []
    carsYspeed4 = []
    carsYspeed6 = []
    carsYspeed8 = []
    """
    carsXspeed = []
    carsYspeed = []
    for i in range(4):
        carsXspeed.append([])
        carsYspeed.append([])

    for x in carsX:
        if x[-2] == 2:
            carsXspeed[3].append(x)
        if x[-2] == 4:
            carsXspeed[2].append(x)
        if x[-2] == 6:
            carsXspeed[1].append(x)
        if x[-2] == 8:
            carsXspeed[0].append(x)
    for x in carsY:
        if x[-2] == 2:
            carsYspeed[3].append(x)
        if x[-2] == 4:
            carsYspeed[2].append(x)
        if x[-2] == 6:
            carsYspeed[1].append(x)
        if x[-2] == 8:
            carsYspeed[0].append(x)


    answer = []
    j = 0  # answer[j] 第j 辆车的答案
    k = 0  # 分批次
    num = 0  # 计数
    nums = 0  # 每批次数量
    time_before = 0  # 每批次最后出发车的时间
    time = 0  # 每辆车出发时间

    speed = [8, 6, 4]
    A = []
    for k in range(1, 4):
        A.append(diff_speed_graph(speed[0:k], road_path))


    for i in range(4):
        r = k
        while carsXspeed[i]:
            le = len(carsXspeed[i])
            for m in range(le):
                car = carsXspeed[i].pop(0)
                lengh = abs((car[1] - 1) // 8 - (car[2] - 1) // 8) + abs((car[1] - 1) % 8 - (car[2] - 1) % 8)
                # 最短路程的路线含有的道路数
                # print(car[0],lengh,k,r,i)
                if i in [2,3]:
                    ans = from_to(car[1] - 1, car[2] - 1, [car[1] - 1], 12-lengh, A[2])
                    # A[2]是全图 最长走lengh+2条路
                else:
                    ans = from_to(car[1]-1, car[2]-1, [car[1]-1], 12-lengh, A[k-r+i])
                    # A[0] A[1]是高速图 最长走lengh+2 条路
                if ans:
                    answer.append([])
                    answer[j].append(car[0])
                    time = (j - num)//15 + time_before
                    #time += 1
                    if time < car[4]:
                        answer[j].append(car[4])
                    else:
                        answer[j].append(time)
                    answer[j] += ans
                    j += 1
                else:
                    carsXspeed[i].append(car)
            k += 1
            nums = j - num
            num = j
            time_before = time

    for i in range(4):
        r = k
        while carsYspeed[i]:
            le = len(carsYspeed[i])
            for m in range(le):
                car = carsYspeed[i].pop(0)
                lengh = abs((car[1] - 1) // 8 - (car[2] - 1) // 8) + abs((car[1] - 1) % 8 - (car[2] - 1) % 8)
                # 最短路程的路线含有的道路数
                # print(car[0],lengh,k,r,i)
                if i in [2,3]:
                    ans = from_to(car[1] - 1, car[2] - 1, [car[1] - 1], 12-lengh, A[2])
                    # A[2]是全图 最长走lengh+2条路
                else:
                    ans = from_to(car[1]-1, car[2]-1, [car[1]-1], 12-lengh, A[k-r+i])
                    # A[0] A[1]是高速图 最长走lengh+2 条路
                if ans:
                    answer.append([])
                    answer[j].append(car[0])
                    time = (j - num)//15 + time_before
                    #time += 1
                    if time < car[4]:
                        answer[j].append(car[4])
                    else:
                        answer[j].append(time)
                    answer[j] += ans
                    j += 1
                else:
                    carsYspeed[i].append(car)
            k += 1
            nums = j - num
            num = j
            time_before = time


    # 结果输出至文件
    # 每一行是一辆车的最短路线
    file = open(answer_path,'w')
    for i in range(len(answer)):
        file.write('(' + str(answer[i])[1:-1] + ')' +'\n')
    file.close()



def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

# to read input file
# process
# to write output file
    run(car_path, answer_path, road_path)


if __name__ == "__main__":
    main()
