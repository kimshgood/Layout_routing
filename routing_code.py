

import numpy as np
import math
import sys
import pandas as pd
import matplotlib.pyplot as plt

import time


# change

## Router 를 어떻게 해야 하나
## 길을 찾는다. array 이 0 은 갈 수 있는 길이요.
## Array 0만 찾아서 길을 확보 하고.
## M1 , M2, M3, M4, M5  의 방향에 따라서  Lee 알고리즘에 맞혀 Array 에 수를 쓴다.
## 시작 점과 끝점에서 가작 작은 길이를 찾는다.
## 0 인 Array 에 숫자를 쓴다. 
## Metal Layer 를 변경 할 경우 저항 값 5를 더한다. 

## Channel 수 확인 방법 
##  1. Peri Heigth , Width  , Metal Layer Pitch 를 입력 하면 가용 Channel 수가 생성 된다 .
#def metal_channel_define (metal_pitch , metal_dir):
#    print("Metal channel initialization ")
#    # 각 Metal 의 Pitch , Vertical/Horizontal Line Check
#    # metal_map 에 "M1" , 
#    for metal in metal_map :
#        if 'h' in metal_dir[metal]:
#            print('Metale=',metal,'pitch = ',metal_pitch[metal])
#            print('Metale Pitch=',metal_pitch[metal])
#            # AC Signal Channel = 1, DC = 2등급 신호로 설정 
#                # 시작 :  끝  : 점프 
#            metal_map[metal][metal_pitch[metal]*1-1::metal_pitch[metal]*2] =1
#            metal_map[metal][metal_pitch[metal]*2-1::metal_pitch[metal]*2] =2
#            print(metal_map[metal])
#
#        elif   'v' in metal_dir[metal] :
#            print('Metale=',metal,'pitch = ',metal_pitch[metal])
#            metal_map[metal].T[metal_pitch[metal]*1-1::metal_pitch[metal]*2] =1
#            metal_map[metal].T[metal_pitch[metal]*2-1::metal_pitch[metal]*2] =2
#            print(metal_map[metal])

Metal_layer=5
#direction   M1  M2   M3  M4  M5
Metal_dir =   {'M1':'h','M2':'v','M3':'h','M4':'h','M5':'h'}
ac_dc = ['ac','dc']

Size_x=5600
Size_y= 220

H_line_order =['M5','M4','M3','M1']
V_line_order =['M2']

Used_line_h= []
Used_line_v= []
Valid_line_h= []
Valid_line_v= []
Option_line_h =[]
Option_line_v =[]
Selected_line_h = []
Selected_line_v = []

Metal_pitch = {\
               'M1_A': 130,'M1_B': 130,\
               'M2_A': 300,'M2_B': 180,\
               'M3_A': 300,'M3_B': 300,\
               'M4_A': 300,'M4_B': 300,\
               'M5_GIO': 440,'M5_CLK': 440,'M5_B': 360,\
              }
Metal_width = {\
               'M1_A':  65,'M1_B':  65,\
               'M2_A': 150,'M2_B':  90,\
               'M3_A': 150,'M3_B': 150,\
               'M4_A': 150,'M4_B': 150,\
               'M5_GIO': 260,'M5_CLK': 260,'M5_B': 180,\
              }
Metal_space = {\
               'M1_A':  65,'M1_B':  65,\
               'M2_A': 150,'M2_B':  90,\
               'M3_A': 150,'M3_B': 150,\
               'M4_A': 150,'M4_B': 150,\
               'M5_GIO': 260,'M5_CLK': 260,'M5_B': 180,\
              }
Metal_count_limit = {\
               'M1_A': 10000000,'M1_B': 1000000000,\
               'M2_A': 30000000,'M2_B': 1800000000,\
               'M3_A': 30000000,'M3_B': 3000000000,\
               'M4_A': 30000000,'M4_B': 3000000000,\
               'M5_GIO':    144,'M5_CLK':8,'M5_B': 3000000000,\
              }

# 위치 별로 어떤 Line  들이 깔려야 할지 선정
Metal_location_order ={\
    'M1':[[0,Size_y,['M1_A','M1_B']]],
    'M2':[[0,Size_x,['M2_A','M2_B']]],
    'M3':[[0,Size_x,['M3_A','M3_B']]],
    'M4':[[0,Size_x,['M4_A','M4_B']]],

    'M5':[[  0,20   ,['M5_B']],             \
          [ 20,100  ,['M5_GIO','M5_B']],    \
          [100,120  ,['M5_B','M5_CLK']],    \
          [120,200  ,['M5_GIO','M5_B']]      \
        ]
    }


def valid_metal_update ():
    print("channel Rule ")
    print("1. 첫 시작은 ac line으로 시작 하고 계속 반전 되어야 함. ")
    print("2. Grade 에 맞혀 Line은 반복 되어야 함. ")

    for layer in H_line_order:
        remain_size_y = Size_y*1000
        location = 0 
        print("해당 metal line의 grade 뭐가 있는지 확인")

        grade =[]
        metal_inform=[]
        for pitch in Metal_pitch:
            if layer in pitch :
                grade.append(pitch)

        while remain_size_y > location :
            print(location , remain_size_y)
            #현재 위치에 사용 가능 한 Line 확인 
            order_list = Metal_location_order[layer]

            for order in order_list :
                if order[0]*1000 <=location and location < order[1]*1000:

                    grade_list = order[2]

                    while order[0]*1000 <= location and location < order[1]*1000 :
                        for grade in grade_list :
                            #metal_inform.ap                
                            metal_center = int(location + Metal_space[grade] + Metal_width[grade]/2)

                            new_line = [ layer, grade ,[0, metal_center  ], [Size_x*1000, metal_center]]

                            Valid_line_h.append(new_line)

                            location = int(location + Metal_space[grade] + Metal_width[grade] + Metal_space[grade])

                            print("Metal Count Limit Check 부분 추가 필요 ")

                            Metal_count_limit[grade] 



valid_metal_update()
### Global Variable Define
Metal_list =["M1","M2","M3","M4",'M5']
#direction   M1  M2   M3  M4  M5

## Mission 1 : Valid 영역 표시 하기
## 1-1 : M1 Valid 영역 표시 하기 
#metal_channel_define( metal_map, layer_pitch, layer_dir,valid_metal,used_metal)
#metal_channel_define( metal_pitch, metal_dir)

metal_count = { "M1":0, "M2":0,"M3":0,"M4":0,"M5":0}
# Valid Channel 확인
for i in Valid_line_h :
    for metal in Metal_list :
        if metal in i :
            metal_count[metal] = metal_count[metal] + 1

for i in Valid_line_v :
    for metal in Metal_list :
        if metal in i :
            metal_count[metal] = metal_count[metal] + 1

for metal in Metal_list :
    print(metal_count[metal])


## Test 1 ##
###  M1 Layer 1,10 에  0 입력 해서 Line 2개 생기는지 Test
#metal_map['M1'][1][10] = 0
#valid_metal_update( metal_pitch, metal_dir)
#print()
#for i in valid_metal :
#    if "M1" in i :
#        print("M1 Channel",i)

## Test 2 ##
###  M1 으로  2-10 까지 Routing 가능 한 후보 Line Update 해보기 

def routing_option_h ( net ):
    #수평 Line 후보 찾기 
    ## 1차 후보 : 수직 Y1 , Y2 사이에 일직선으로 Line 있는지 확인 
    option_h_list =[]
    for valid in Valid_line_h :
        # 수평 Line net의 X1,X2[net[2][0]  , 
        if net[3][0] >= valid[2][0] and net[4][0] <= valid[3][0] :
            if net[1] == valid[0] and net[2] == valid[1] :
                #1차 후보: 수직 Point 들어 오는 
                if max(net[3][1],net[4][1]) >= max(valid[2][1],valid[3][1]) and min(net[3][1],net[4][1]) <=min(valid[2][1],valid[3][1]) :
                    print("This Line is option_h 1'st ",valid)
                    new_line = ["Opt1" , valid[0],valid[1],valid[2],valid[3]]
                    option_h_list.append(new_line)
                #2차 후보: 수직 Point를 벗어 나는 경우 
                else :
                    print("This Line is option_h 2nd ",valid)
                    new_line = ["Opt2" , valid[0],valid[1],valid[2],valid[3]]
                    option_h_list.append(new_line)
    return option_h_list

def routing_option_v ( line_h, net ):
    #print("#수직 Line 후보 찾기")
    option_v =[]
    #print("net = ",net)

    old_distance = 100000000 
    new_distance = 0 
    new_line = []

    for valid_v in Valid_line_v :
        #if (net[2][1] >= valid_v[2][1]) and (net[3][1] <= (valid_v[3][1])) and (net[0] in valid_v) :
        if (max(net[2][1],net[3][1]) <= max((valid_v[2][1],valid_v[3][1]))) and ((min(net[2][1],net[3][1])>=min(valid_v[2][1],valid_v[3][1]))):
            new_distance = abs(net[2][0] - valid_v[2][0])
            #1차 후보: 해당 X 좌표에 수직 Line 있는지 확인. 
            if ( new_distance ) == Metal_pitch[valid_v[0]] :
                print("matching 되는 것이 있으면 기존의 option_v 는 모두 제거 한다. ")
                print('contact  확인 필요.')
                line_v = ["Opt1" , valid_v[0],valid_v[1],valid_v[2],valid_v[3]]
                option_cont = routing_option_cont_check(line_h,line_v)
                print("This Line is option_v 1'st ",valid_v)

                if option_cont > 0 :
                    option_v.clear()
                    new_line = ["Opt1" , valid_v[0],valid_v[1],valid_v[2],valid_v[3]]
                    return option_v
            else :
                if old_distance > new_distance:
                    old_distance = new_distance 
                    if old_distance < Metal_pitch[valid_v[0]]*2:
                        print("matching 되는 것이 있으면 기존의 option_v 는 모두 제거 한다. ")
                        print('contact  확인 필요.')
                        line_v = ["Opt1" , valid_v[0],valid_v[1],valid_v[2],valid_v[3]]
                        option_cont = routing_option_cont_check(line_h,line_v)
                        if option_cont > 0 :
                            new_line = ["Opt2" , valid_v[0],valid_v[1],valid_v[2],valid_v[3]]
                    else:
                        new_line=[]
                else :
                    pass
    
    print("option_v 의 v_line 들과 line_h 사이에 들어 있는 Contact 이 있어야 하는 경우 검색 필요")

    if new_line != []:
        option_v.append(new_line)
    return option_v

# contact 연결이 되는지 확인 하고 해당 layer 를 return 한다. 
def routing_option_cont_check ( line_h, line_v ):

    cont_x = line_v[3][0]
    cont_y = line_h[3][1]

    low_layer = min(int(line_v[1].replace('M','')),int(line_h[1].replace('M','')))
    hi_layer  = max(int(line_v[1].replace('M','')),int(line_h[1].replace('M','')))
    cont_layer_list = []

    ## Contact 이 필요 한 경우 
    ## 1. 해당 위치에 Used_line_h/v 를 확인 한다. 
    ## 2. 해당 위치에 실제 사용 한 길이의 Option_cont


    if hi_layer - low_layer > 1:
        print("두개 Layer 사이에는 Contact 이 있어야 합니다. ",hi_layer,low_layer)
        for i in range( hi_layer - low_layer -1 ):
            cont_layer_list.append("M"+str(i+low_layer+1))
        print("수평  Line  찾아 보자.")
        print("우선 used_line 에서 해당 수평 line을 사용 했는지 부터. ")

        option_c =[]
        print("Cont. 의 X, Y 좌표 기준 해당 Layer의 Metal Width + Space  거리 내에 있는 Line 이 있는지 확인 ")
        print("horizontal line이 있는 경우 위/아래 영역에 해당 metal layer의 ( Width + Space * 2 ) 를 제거 한다. ")
        for cont_layer in cont_layer_list:
            # 1차 관문 
            # 사용 된 Line 중 해당 Contact 에 포함 된 Line이 있는가? 
            for used_h in Used_line_h :
                if cont_layer in used_h :
                    print("수평 Line 이기 때문에 해당 y 좌표 위 아래 에 해당 Layer Space 를 더하거나 뺀 값에")
                    print("수평 Line을 사용 하고 있는지 확인 해야 함")
                    if (used_h[3][1] <= cont_y + Metal_pitch[cont_layer]) and \
                       (used_h[3][1] >= cont_y - Metal_pitch[cont_layer]) :
                        print("이 Line은 Contact 의 Y 좌표 기준 +- Pitch 내에 사용 한  Line 이 있음.")

                        print(" 그럼 이 Line 의 X 좌표도 포함 되는 지 확인 해야 함.")
                        if (min(used_h[3][0],used_h[4][0]) <= cont_x+Metal_pitch[cont_layer]) and \
                           (max(used_h[3][0],used_h[4][0]) >= cont_x-Metal_pitch[cont_layer]) :
                            print("x , y 모두 포함 되어 있기 때문에 이 Contact 은 사용 불가!!")
                            return -1
            # 2차 관문 
            #사용 된 Line 중 해당 Contact 에 포함 된 Line이 있는가? 
            for used_v in Used_line_v :
                if cont_layer in used_v :
                    print("수직 Line 이기 때문에 해당 x 좌표 좌/우에 해당 Layer Space 를 더하거나 뺀 값에")
                    print("수직 Line을 사용 하고 있는지 확인 해야 함")
                    if used_v[3][0] <= cont_x + Metal_pitch[cont_layer] and used_v[3][0] > cont_x - Metal_pitch[cont_layer] :
                        print("이 Line은 Contact 의 Y 좌표 기준 +- Pitch 내에 사용 한  Line 이 있음.")

                        print(" 그럼 이 Line 의 y 좌표도 포함 되는 지 확인 해야 함.")
                        if (min(used_v[3][1],used_v[4][1]) <= cont_y+Metal_pitch[cont_layer]) and \
                           (max(used_v[3][1],used_v[4][1]) >= cont_y-Metal_pitch[cont_layer]) :
                            print("x , y 모두 포함 되어 있기 때문에 이 Contact 은 사용 불가!!")
                            return -1

        #1/2차 관문을 통과 (Used_line 중에 사용 된 것이 없음.)
    else :
        return 1

def routing_select_multi(net):
    # 여러개의 node 가 있는 Line 인 경우 어떻게 할것인가? 
    # node가 1개 이든, 2개이든, 3개이든 동작 할 수 있는 방법은 무엇일까??

    #  이 LINE의 Max(X), Max(Y), Min(X), MIN(Y)를 찾아 보자!!

    #수평 라인을 찾기 위해서 net의 Max.X  , Min.X 를 구한 후
    # 해당 Line 의 routing_option_h 를 찾는다. 
    # net 의 node 를 확인 한다. 

    # net 은  [ 'netname', '원하는 Metal', 'GRADE' , ' 좌표1', '좌표2', ....'좌표X' ]
    ## 이런 식으로 만들 것이다. 
    ## 따라서 MaxX , Min,X 는 net[3][0](좌표1) 부터 마지막 좌표n 까지 찾아 나선다. 
    net_x =[]
    net_y =[]
    for i in range(len(net)) :
        if i > 2 :
            net_x.append(net[i][0])
            net_y.append(net[i][1])

    max_x = -10000000000
    min_x = 100000000000

    max_y = -10000000000
    min_y = 100000000000

    print("max & min 값 찾아 보자 ")
    for i in range(len(net)) :
        if i > 2 :
            print("x좌표 시작",i)
            print(net[i])
            if max_x < net[i][0] :
                max_x = net[i][0]
            if min_x > net[i][0] :
                min_x = net[i][0]

            if max_y < net[i][1] :
                max_y = net[i][1]
            if min_y > net[i][1] :
                min_y = net[i][1]

    print(max_x,min_x,max_y,min_y)

    print("Line 중 가장 긴 h 라인을 찾는다. ")
    long_h = [net[0],net[1],net[2],[min_x,min_y],[max_x,max_y]]
    
    option_h_list = routing_option_h(long_h)
    print("option_h 중에서 가장 좋은건 어떤 것일까??")
    print("후보중 vertical 까지 연결 되는것을 우선 찾아 보자!")
    option_h_list.sort()

    print(" 현재 option_h 라인들 중에 vertical line 의 합이 가장 짧은 녀석을 선택을 찾자!")
    old_line_length = 0 
    new_line_length = 0 
    print("old line 과 new_line을 비교 해서 가장 짧은 line_h , line_v 를 저장 하고   ")
    print(" 해당 line 들을 selected_line 에 저장 한다. ")

    print("len(option_h_list)",len(option_h_list))

    print("find opt1 ")
    opt1_index = []
    for i in range(len(option_h_list)):
        if option_h_list[i][0] == "Opt1":
            opt1_index.append(i)

    for i in opt1_index:
        ## opt1 만 찾아 봅시다. 
        option_h = option_h_list[i]
        #print(h_split)
        line_y=int(option_h[3][1])
        pass_flag = 0
        # 선택 된 h_line 에 포함 된 option_v_list 확인. 
        # v_line 은 line_v_list 에 저장, option_v_list 
        option_v_list=[]
        line_v_list=[]

        print("vertical line 이 있는지 확인.")
        for i in range(len(net_x)):
            for metal in Metal_dir :
                if Metal_dir[metal] == 'v':
                    v_line = [ metal,net[2],[net_x[i],min(net_y[i],line_y)],[net_x[i],max(net_y[i],line_y)]]
                    option_v = routing_option_v(option_h,v_line)

            if option_v !=[]:
                pass_flag = 1
                # option_v type  =[[],[]]
                for option in option_v:
                    option_v_list.append(option)
                    new_line = [net[0],option[1],option[2],[net_x[i],min(net_y[i],line_y)],[net_x[i],max(net_y[i],line_y)]]
                    line_v_list.append(new_line)
            else:
                pass_flag = 0 
                option_v_list.clear()
                line_v_list.clear()

        #print("기존에 option_metal 과 비교를 하고 새로운 대안이 될지 확인 하자.")
        #print("vertical line 길이 총합이 짧은 녀석이 좋은 놈이다. ")
        if pass_flag ==1 :
            for line in line_v_list:
                new_line_length = new_line_length + abs(line[3][1] - line[4][1])

            if old_line_length == 0:
                old_line_length = new_line_length
                Option_line_h.clear()
                Option_line_v.clear()
                Selected_line_h.clear()
                Selected_line_v.clear()

                Option_line_h.append(option_h)
                for i in range(len(option_v_list)):
                    Option_line_v.append(option_v_list[i])

                new_x1 = min(long_h[3][0],long_h[4][0])
                new_x2 = max(long_h[3][0],long_h[4][0])
                new_h = [long_h[0],long_h[1],long_h[2], [new_x1,option_h[3][1]],[new_x2,option_h[4][1]]]
                Selected_line_h.append(new_h)
                for i in range(len(line_v_list)):
                    Selected_line_v.append(line_v_list[i])
            return 1

    print("Opt1 이 없는 경우 opt_2 찾아서 동일 하게 수행 ")
    opt2_index = []
    for i in range(len(option_h_list)):
        if option_h_list[i][0] == "Opt2":
            opt2_index.append(i)

    for i in opt2_index:
        option_h = option_h_list[i]
        #print(h_split)
        line_y=int(option_h[3][1])
        pass_flag = 0
        # 선택 된 h_line 에 포함 된 option_v_list 확인. 
        # v_line 은 line_v_list 에 저장, option_v_list 
        option_v_list=[]
        line_v_list=[]

        for i in range(len(net_x)):
            v_line = [ 'M2',net[2],[net_x[i],min(net_y[i],line_y)],[net_x[i],max(net_y[i],line_y)]]
            option_v = routing_option_v(v_line)

            if option_v !=[]:
                pass_flag = 1
                # option_v type  =[[],[]]
                for option in option_v:
                    option_v_list.append(option)
                    new_line = [net[0],option[1],option[2],[net_x[i],min(net_y[i],line_y)],[net_x[i],max(net_y[i],line_y)]]
                    line_v_list.append(new_line)
            else:
                pass_flag = 0 
                option_v_list.clear()
                line_v_list.clear()
        
        #print("기존에 option_metal 과 비교를 하고 새로운 대안이 될지 확인 하자.")
        #print("vertical line 길이 총합이 짧은 녀석이 좋은 놈이다. ")
        if pass_flag ==1 :
            for line in line_v_list:
                new_line_length = new_line_length + abs(line[3][1] - line[4][1])

            if old_line_length == 0:
                old_line_length = new_line_length
                Option_line_h.clear()
                Option_line_v.clear()
                Selected_line_h.clear()
                Selected_line_v.clear()

                Option_line_h.append(option_h)
                for i in range(len(option_v_list)):
                    Option_line_v.append(option_v_list[i])

                Selected_line_h.append(long_h)
                for i in range(len(line_v_list)):
                    Selected_line_v.append(line_v_list[i])
            elif old_line_length <= new_line_length :
                pass
            elif old_line_length > new_line_length :
                Option_line_h.clear()
                Option_line_v.clear()
                Selected_line_h.clear()
                Selected_line_v.clear()
                Option_line_h.append(option_h)

                for i in range(len(option_v_list)):
                    Option_line_v.append(option_v_list[i])

                Selected_line_h.append(long_h)
                for i in range(len(line_v_list)):
                    Selected_line_v.append(line_v_list[i])

        elif pass_flag == 0 :
            #print("이 h_line 은 vertical line이 없오.")
            pass


def routing_line(net):
    print("selected_line 들을 option_metal 에 있는 line으로 routiong 한다")
    print("selected_line 이 routing 되면 used_metal 에 저장 하고 selected_line은 제거 한다")
    
    order = 0 
    #option_line_h, selected_line_h 는 동일 한 순서로 저장 되기 때문에 
    # 해당 Line 순서 대로 선택 
    for i in range(len(Option_line_h)):
        #line_inform = str(line[1])+str(line[2])+str(line[3])+str(line[4])
        opt_inform = [Option_line_h[i][1],Option_line_h[i][2],Option_line_h[i][3],Option_line_h[i][4]]
        opt_split = Option_line_h[i]
        for j in range(len(Valid_line_h)) :
            #if line_inform in valid_line_h[i] and metal_dir[line_split[0]] == 'h' :
            #Valid_inform = str(valid_line_h[i][0])+str(valid_line_h[i][1])+str(valid_line_h[i][2])+str(valid_line_h[i][3])
            if opt_inform == Valid_line_h[j] :
                    print("해당 line은 selected_line 첫번째 line이  사용 한다.")
                    print("이 horizontal valid_metal line은 사용 할 것이니 지운다. ")
                    print(Valid_line_h[j])
                    del(Valid_line_h[j])

                    valid_x1 = int(min(opt_split[3][0],opt_split[4][0]))
                    valid_x2 = int(max(opt_split[3][0],opt_split[4][0]))

                    routing_x1 = int(min(Selected_line_h[i][3][0],Selected_line_h[i][4][0]))
                    routing_x2 = int(max(Selected_line_h[i][3][0],Selected_line_h[i][4][0]))

                    print(" 수평 Line 이기 때문에 잘려진 왼쪽, 잘려진 오른쪽 라인이 valid_line에 저장 된다.")
                    print(" Chop left의 우측은 routing 되기  때문에 -1 필요")
                    chop_left =  [valid_x1 , routing_x1-Metal_space[opt_split[1]]]
                    print(" Chop right의 좌측은  routing space  필요")
                    chop_right = [routing_x2+Metal_space[opt_split[1]], valid_x2]

                    print(" 수평 line의 길이가 Line 최소 길이 보다 짧은 경우 valid_line에 저장 안함 ")
                    if (chop_left[1] - chop_left[0] ) >= Metal_width[opt_split[1]] :
                        valid = [opt_split[1],opt_split[2],[chop_left[0],opt_split[3][1]],[chop_left[1],opt_split[4][1]]]
                        Valid_line_h.append(valid)

                    if (chop_right[1] - chop_right[0] ) >= Metal_width[opt_split[1]] :
                        valid = [opt_split[1],opt_split[2],[chop_right[0],opt_split[3][1]],[chop_right[1],opt_split[4][1]]]
                        Valid_line_h.append(valid)


        print("사용한 line에 수평 Line Update 하고, ")
        Selected_line_h[i][3][1]=opt_inform[2][1]
        Selected_line_h[i][4][1]=opt_inform[2][1]
        Used_line_h.append(Selected_line_h[i])

    for i in range(len(Option_line_v)):
        opt_inform = [Option_line_v[i][1],Option_line_v[i][2],Option_line_v[i][3],Option_line_v[i][4]]
        opt_split = Option_line_v[i]

        for j in range(len(Valid_line_v)) :
            #if line_inform in valid_line_h[i] and metal_dir[line_split[0]] == 'h' :
            #valid_inform = str(valid_line_h[i][0])+str(valid_line_h[i][1])+str(valid_line_h[i][2])+str(valid_line_h[i][3])
            if opt_inform == Valid_line_v[j] :
                    print("이  valid_metal line은 사용 할 것이니 지운다. ")
                    print(Valid_line_v[j],len(Valid_line_v))
                    del(Valid_line_v[j])
                    print(len(Valid_line_v))

                    valid_y1 = min(opt_split[3][1],opt_split[4][1])
                    valid_y2 = max(opt_split[3][1],opt_split[4][1])

                    routing_y1 = min(Selected_line_v[i][3][1],Selected_line_v[i][4][1])
                    routing_y2 = max(Selected_line_v[i][3][1],Selected_line_v[i][4][1])

                    print(" 수직 Line 이기 때문에 잘려진 위쪽, 잘려진 아래 라인이 valid_line에 저장 된다.")
                    print(" Chop dn의 위는  routing 되기  때문에 -1 필요")
                    chop_down =  [valid_y1 , routing_y1-Metal_space[opt_split[1]]]
                    print(" Chop up의 아래는   routing space  필요")
                    chop_up =    [routing_y2+Metal_space[opt_split[1]], valid_y2]

                    print(" 수평 line의 길이가 Line 최소 길이 보다 짧은 경우 valid_line에 저장 안함 ")
                    if (chop_down[1] - chop_down[0] ) >= Metal_width[opt_split[1]] :
                        valid = [opt_split[1],opt_split[2],[opt_split[3][0],chop_down[0]],[opt_split[4][0],chop_down[1]]]
                        Valid_line_v.append(valid)
                    print(Valid_line_v[len(Valid_line_v)-1])

                    if (chop_up[1] - chop_up[0] ) >= Metal_width[opt_split[1]] :
                        valid = [opt_split[1],opt_split[2],[opt_split[3][0],chop_up[0]],[opt_split[4][0],chop_up[1]]]
                        Valid_line_v.append(valid)
                    print(Valid_line_v[len(Valid_line_v)-1])
        #print("사용한 line에 수직 Line Update 하고, ")
        Selected_line_v[i][3][0]=opt_inform[2][0]
        Selected_line_v[i][4][0]=opt_inform[2][0]
        Used_line_v.append(Selected_line_v[i])
        print('used_line_v[i]=',Used_line_v[len(Used_line_v)-1])
    
            
    Selected_line_v.clear()
    Option_line_v.clear()
    Selected_line_h.clear()
    Option_line_h.clear()


            


net2=['net_1002','M3','A',[400,300],[1000,700],[10000,400]]
net3=['net_1003','M3','A',[11000,300],[1000,700],[10000,400],[100,20000]]
net4=['net_1004','M5','A',[11000,300],[1000,700],[10000,400],[100,20000]]
#net4=['net_1004','M5','A',[-11000,3000],[1000,7000],[10000,4000],[100,20000],[2000,100000]]

start = time.time()
routing_select_multi(net2)
routing_line(net2)
routing_select_multi(net3)
routing_line(net3)
routing_select_multi(net4)
routing_line(net4)
print("time:",time.time() - start)

## 최종 결과 

for line in Used_line_v:
    print(line)
for line in Used_line_h:
    print(line)

print(len(Valid_line_v))




