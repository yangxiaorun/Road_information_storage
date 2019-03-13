#使用说明
#num_list[i][j]  路口信息是一个字典有五个键值对  分别是路口id 以及东南西北
#num_list[i][j]['方向']  道路信息 是一个列表其中第一个元素是int类型表示道路id，第二个元素是字典表示道路的信息
#num_list[i][j]['方向'][1]['道路信息']   该字典有7个键值对，分别是'roadid','length''speed','channel','from'，'to'，'isDuplex'
#道路信息唯一备份存储：例如路口1、2中都存有5001道路的信息，当路口1中5001道路信息更改，路口2存储的5001道路信息随之更改
num_list = [ [0] * 6 for i in range(6)]
f = open('cross.txt')
count = 0
i = 5
j = 0
for line in f:
    p = line.strip('\n')
    if p.startswith('#') == False :#字符串是否已某个字符开头 startswith('#')  endswith()
        p = p.strip('()')#去除首尾的字符
        p = p.split(',')#以“，”分割
        dict = {'crossingid': int(p[0]), 'north': [int(p[1])], 'east':[int(p[2])],'south': [int(p[3])],'weat':[int(p[4])]}
        #上述建立一个字典，对应一个路口的相关信息其中dict['crossingid']是路口id，dict['north']是一个首项为道路id列表
        #下面将路口排成矩阵
        if count == 0:
            count = 1
            num_list[5][0] = dict #将1号路口放到左下角，以后随着道路变化可能需要调整
        if num_list[i][j]['north'] == dict['south'] and dict['south'] != [-1]:#下一个路口在前一个路口的北面
            i -=1
            num_list[i][j] = dict
        elif num_list[i][j]['east'] == dict['weat'] and dict['weat'] != [-1]:#下一个路口在前一个路口的东面
            j +=1
            num_list[i][j] = dict
        elif num_list[i][j]['weat'] == dict['east'] and dict['east'] != [-1]:#下一个路口在前一个路口的西面
            j -=1
            num_list[i][j] = dict
        elif num_list[i][j]['south'] == dict['north'] and dict['north'] != [-1]:#下一个路口在前一个路口的南面
            i +=1
            num_list[i][j] = dict
        elif num_list[-1][j]['east'] == dict['weat'] and dict['weat'] != [-1]:##下一个路口在前一列底部路口的东面
            j +=1
            i = 5
            num_list[i][j] = dict
f.close()
#num_list
print('生成路口矩阵完成')

#注意该程序段必须被正确执行一次（不能多次）
r = open('road.txt')
for line in r:
    road = line.strip('\n')
    if road.startswith('#') == False :#字符串是否已某个字符开头 startswith('#')  endswith()
        road = road.strip('()')#去除首尾的字符
        road = road.split(',')#以“，”分割
        roadinfo = {'roadid':int(road[0]),'length':int(road[1]),'speed':int(road[2]),'channel':int(road[3]),'from':int(road[4]),'to':int(road[5]),'isDuplex':int(road[6])}
        name = locals()#为生成动态变量名做准备
        name['n'+str(int(road[0]))]= roadinfo
        #print(name['n'+str(int(road[0]))])
        i = 0
        while i < 6:#将生成的动态变量（表示道路的字典）加到路口字典的道路列表中
            j = 0
            while j < 6:
                #print(num_list[i][j]['north'][0])
                #print(int(road[0]))
                if num_list[i][j]['north'][0] == int(road[0]):
                    num_list[i][j]['north'].append(name['n'+str(int(road[0]))])
                    #if 增强鲁棒性可以判断该路口信息是否已经被加入
                if num_list[i][j]['east'][0] == int(road[0]):
                    num_list[i][j]['east'].append(name['n'+str(int(road[0]))])
                if num_list[i][j]['weat'][0] == int(road[0]):
                    num_list[i][j]['weat'].append(name['n'+str(int(road[0]))])
                if num_list[i][j]['south'][0] == int(road[0]):
                    num_list[i][j]['south'].append(name['n'+str(int(road[0]))])
                j +=1
            i +=1
r.close()

#结果输出至文件，文本需要手动回车
file = open('路口矩阵.txt','w')
file.write(str(num_list))
file.close()
