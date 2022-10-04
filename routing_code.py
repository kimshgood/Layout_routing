

import numpy as np
import math
import sys
import pandas as pd
import matplotlib.pyplot as plt
import cv2
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
ac_dc = ['AC','DC']

# unit [um]
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
               'M1_A_AC': 130,'M1_B_AC': 130,\
               'M2_A_AC': 300,'M2_B_AC': 180,\
               'M3_A_AC': 300,'M3_B_AC': 300,\
               'M4_A_AC': 300,'M4_B_AC': 300,\
               'M5_GIO_AC': 440,'M5_CLK_AC': 440,'M5_B_AC': 360,\
               'M1_A_DC': 130,'M1_B_DC': 130,\
               'M2_A_DC': 300,'M2_B_DC': 180,\
               'M3_A_DC': 300,'M3_B_DC': 300,\
               'M4_A_DC': 300,'M4_B_DC': 300,\
               'M5_B_DC': 360,\
              }
Metal_width = {\
               'M1_A_AC':  65,'M1_B_AC':  65,\
               'M2_A_AC': 150,'M2_B_AC':  90,\
               'M3_A_AC': 150,'M3_B_AC': 150,\
               'M4_A_AC': 150,'M4_B_AC': 150,\
               'M5_GIO_AC': 260,'M5_CLK_AC': 260,'M5_B_AC': 180,\
               'M1_A_DC':  65,'M1_B_DC':  65,\
               'M2_A_DC': 150,'M2_B_DC':  90,\
               'M3_A_DC': 150,'M3_B_DC': 150,\
               'M4_A_DC': 150,'M4_B_DC': 150,\
               'M5_B_DC': 180,\
              }

Metal_space = {\
               'M1_A_AC':  65,'M1_B_AC':  65,\
               'M2_A_AC': 150,'M2_B_AC':  90,\
               'M3_A_AC': 150,'M3_B_AC': 150,\
               'M4_A_AC': 150,'M4_B_AC': 150,\
               'M5_GIO_AC': 180,'M5_CLK_AC': 180,'M5_B_AC': 180,\
               'M1_A_DC':  65,'M1_B_DC':  65,\
               'M2_A_DC': 150,'M2_B_DC':  90,\
               'M3_A_DC': 150,'M3_B_DC': 150,\
               'M4_A_DC': 150,'M4_B_DC': 150,\
               'M5_B_DC': 180,\
              }
Metal_cont_pitch = {\
               'M1': 130,\
               'M2': 300,\
               'M3': 300,\
               'M4': 300,\
               'M5': 360\
                }

Metal_count = {\
               'M1_A_AC'   : 0,'M1_B_AC'  : 0,\
               'M2_A_AC'   : 0,'M2_B_AC'  : 0,\
               'M3_A_AC'   : 0,'M3_B_AC'  : 0,\
               'M4_A_AC'   : 0,'M4_B_AC'  : 0,\
               'M5_GIO_AC' : 0,'M5_CLK_AC':0,'M5_B_AC': 0,
               'M1_A_DC'   : 0,'M1_B_DC'  : 0,\
               'M2_A_DC'   : 0,'M2_B_DC'  : 0,\
               'M3_A_DC'   : 0,'M3_B_DC'  : 0,\
               'M4_A_DC'   : 0,'M4_B_DC'  : 0,\
               'M5_B_DC': 0
                }

Metal_count_limit = {\
               'M1_A_AC': 10000000,'M1_B_AC': 1000000000,\
               'M2_A_AC': 30000000,'M2_B_AC': 1800000000,\
               'M3_A_AC': 30000000,'M3_B_AC': 3000000000,\
               'M4_A_AC': 30000000,'M4_B_AC': 3000000000,\
               'M5_GIO_AC':    144,'M5_CLK_AC':8,'M5_B_AC': 3000000000,\
               'M1_A_DC': 10000000,'M1_B_DC': 1000000000,\
               'M2_A_DC': 30000000,'M2_B_DC': 1800000000,\
               'M3_A_DC': 30000000,'M3_B_DC': 3000000000,\
               'M4_A_DC': 30000000,'M4_B_DC': 3000000000,\
               'M5_B_DC': 3000000000\
              }

# PERI  영역 별로 어떤 Line 어떤 순서로 배치 될지 정의 한다. 
Metal_grade_order ={\
    'M1':[[0,Size_y,['M1_A_AC','M1_B_DC']]],

    'M2':[[0,Size_x,['M2_A_AC','M2_B_DC']]],

    'M3':[[0,Size_y,['M3_A_AC','M3_B_DC']]],
    'M4':[[0,Size_y,['M4_A_AC','M4_B_DC']]],

    'M5':[[  0,20   ,['M5_B_AC','M5_B_DC']],             \
          [ 20,100  ,['M5_GIO_AC','M5_B_DC']],    \
          [100,120  ,['M5_B_DC','M5_CLK_AC']],    \
          [120,200  ,['M5_GIO_AC','M5_B_DC']],    \
          [200,220  ,['M5_B_AC','M5_B_DC']]      
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
            #print(location , remain_size_y)
            #현재 위치에 사용 가능 한 Line 확인 
            order_list = Metal_grade_order[layer]
            #order_list = [ start , end , [ metal_1st , metal_2nd ]]
            for order in order_list :
                    grade_list = order[2]

                    while order[0]*1000 <= location and location < order[1]*1000 :
                        for grade in grade_list :
                            #metal_inform.ap               
                            pre_grade = grade

                            try :
                                pre_grade = Valid_line_h[len(Valid_line_h)-1][1]
                            except:
                                print('첫번째 Valid_line_h')

                            max_space = max( Metal_space[grade] , Metal_space[pre_grade])
                            metal_center = int(location + max_space + Metal_width[grade]/2)
                            location = int(location + max_space + Metal_width[grade])

                            #print("Metal Count Limit Check 부분 추가 필요 ")
                            new_line = [ layer, grade,[0, metal_center  ], [Size_x*1000, metal_center]]
                            if Metal_count[grade] < Metal_count_limit[grade]:
                                Valid_line_h.append(new_line)
                                Metal_count[grade] = Metal_count[grade] + 1
                                #print("pintch=",Valid_line_h[len(Valid_line_h)-1][1],Valid_line_h[len(Valid_line_h)-1][2][1] - Valid_line_h[len(Valid_line_h)-2][2][1])

    for layer in V_line_order:
        remain_size_x = Size_x*1000
        location = 0 
        print("해당 metal line의 grade 뭐가 있는지 확인")

        grade =[]
        metal_inform=[]
        for pitch in Metal_pitch:
            if layer in pitch :
                grade.append(pitch)

        while remain_size_x > location :
            #현재 위치에 사용 가능 한 Line 확인 
            order_list = Metal_grade_order[layer]
            #order_list = [ start , end , [ metal_1st , metal_2nd ]]
            for order in order_list :
                    grade_list = order[2]

                    while order[0]*1000 <= location and location < order[1]*1000 :
                        for grade in grade_list :
                            #metal_inform.ap               
                            pre_grade = grade

                            try :
                                pre_grade = Valid_line_v[len(Valid_line_v)-1][1]
                            except:
                                print('첫번째 Valid_line_v')

                            max_space = max( Metal_space[grade] , Metal_space[pre_grade])
                            metal_center = int(location + max_space + Metal_width[grade]/2)
                            location = int(location + max_space + Metal_width[grade])

                            #print("Metal Count Limit Check 부분 추가 필요 ")
                            new_line = [ layer, grade,[metal_center,0 ], [metal_center,Size_x*1000]]
                            if Metal_count[grade] < Metal_count_limit[grade]:
                                Valid_line_v.append(new_line)
                                Metal_count[grade] = Metal_count[grade] + 1
                                #print("pintch=",Valid_line_v[len(Valid_line_v)-1][1],Valid_line_v[len(Valid_line_v)-1][2][1] - Valid_line_v[len(Valid_line_v)-2][2][1])


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
                    #print("This Line is option_h 1'st ",valid)
                    new_line = ["Opt1" , valid[0],valid[1],valid[2],valid[3]]
                    option_h_list.append(new_line)
                #2차 후보: 수직 Point를 벗어 나는 경우 
                else :
                    #print("This Line is option_h 2nd ",valid)
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

    # vertical line 거리가 가까운 순으로 진행 하자!!
    # 단, 거리가 일정 수준 이상 멀어지면 해당 Line 은 vertical line이 없음. 
    index_vertical =[]

    for i in range(len(Valid_line_v)-1) :
        distance = abs(Valid_line_v[i][2][0] - net[2][0])

        index_vertical.append((i,distance))

    index_vertical.sort(key= lambda x:x[1])
    for i in index_vertical :
        distance = i[1]
        valid_v = Valid_line_v[i[0]]
        option_v = []

        while int(i[1]) < int(Metal_pitch[valid_v[1]])*2 :
            opt = ""
            if int(i[1]) < (Metal_pitch[valid_v[1]]*1):
                opt = "Opt1"
            elif int(i[1]) < (Metal_pitch[valid_v[1]]*2):
                opt = "Opt2"
            else :
                1

            option_v = [opt, valid_v[0],valid_v[1],valid_v[2],valid_v[3]]
            option_cont = routing_option_cont_check(line_h,option_v)
            if option_cont ==1:
                return option_v
            else :
                option_v=[]
                return option_v
        else :
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
        #print("두개 Layer 사이에는 Contact 이 있어야 합니다. ",hi_layer,low_layer)
        for i in range( hi_layer - low_layer -1 ):
            cont_layer_list.append("M"+str(i+low_layer+1))
        #print("수평  Line  찾아 보자.")
        #print("우선 used_line 에서 해당 수평 line을 사용 했는지 부터. ")

        option_c =[]
        #print("Cont. 의 X, Y 좌표 기준 해당 Layer의 Metal Width + Space  거리 내에 있는 Line 이 있는지 확인 ")
        #print("horizontal line이 있는 경우 위/아래 영역에 해당 metal layer의 ( Width + Space * 2 ) 를 제거 한다. ")
        for cont_layer in cont_layer_list:
            # 1차 관문 
            # 사용 된 Line 중 해당 Contact 에 포함 된 Line이 있는가? 
            for used_h in Used_line_h :
                if cont_layer in used_h :
                    #print("수평 Line 이기 때문에 해당 y 좌표 위 아래 에 해당 Layer Space 를 더하거나 뺀 값에")
                    #print("수평 Line을 사용 하고 있는지 확인 해야 함")
                    metal_pitch = Metal_pitch

                    if (used_h[3][1] <= cont_y + Metal_cont_pitch[cont_layer]) and \
                       (used_h[3][1] >= cont_y - Metal_cont_pitch[cont_layer]) :
                        #print("이 Line은 Contact 의 Y 좌표 기준 +- Pitch 내에 사용 한  Line 이 있음.")

                        #print(" 그럼 이 Line 의 X 좌표도 포함 되는 지 확인 해야 함.")
                        if (min(used_h[3][0],used_h[4][0]) <= cont_x+Metal_cont_pitch[cont_layer]) and \
                           (max(used_h[3][0],used_h[4][0]) >= cont_x-Metal_cont_pitch[cont_layer]) :
                            #print("x , y 모두 포함 되어 있기 때문에 이 Contact 은 사용 불가!!")
                            return -1
            # 2차 관문 
            #사용 된 Line 중 해당 Contact 에 포함 된 Line이 있는가? 
            for used_v in Used_line_v :
                if cont_layer in used_v :
                    #print("수직 Line 이기 때문에 해당 x 좌표 좌/우에 해당 Layer Space 를 더하거나 뺀 값에")
                    #print("수직 Line을 사용 하고 있는지 확인 해야 함")
                    if used_v[3][0] <= cont_x + Metal_cont_pitch[cont_layer] and used_v[3][0] > cont_x - Metal_cont_pitch[cont_layer] :
                        #print("이 Line은 Contact 의 Y 좌표 기준 +- Pitch 내에 사용 한  Line 이 있음.")

                        #print(" 그럼 이 Line 의 y 좌표도 포함 되는 지 확인 해야 함.")
                        if (min(used_v[3][1],used_v[4][1]) <= cont_y+Metal_cont_pitch[cont_layer]) and \
                           (max(used_v[3][1],used_v[4][1]) >= cont_y-Metal_cont_pitch[cont_layer]) :
                            #print("x , y 모두 포함 되어 있기 때문에 이 Contact 은 사용 불가!!")
                            return -1

        #1/2차 관문을 통과 (Used_line 중에 사용 된 것이 없음.)
        else :
            return 1
    else:
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
    grade = "M2"
    if "A_AC" in net[2] or "GIO" in net[2] or "CLK" in net[2] :
        grade = "M2_A_AC"
    elif "B_AC" in net[2] :
        grade = "M2_B_AC"
    elif "B_DC" in net[2] :
        grade = "M2_B_DC"
    
    option_h_list = routing_option_h(long_h)
    print("option_h 중에서 가장 좋은건 어떤 것일까??")
    print("후보중 vertical 까지 연결 되는것을 우선 찾아 보자!")
    option_h_list.sort()

    print(" 현재 option_h 라인들 중에 vertical line 의 합이 가장 짧은 녀석을 선택을 찾자!")
    old_line_length = 0 
    print("old line 과 new_line을 비교 해서 가장 짧은 line_h , line_v 를 저장 하고   ")
    print(" 해당 line 들을 selected_line 에 저장 한다. ")

    print("len(option_h_list)",len(option_h_list))

    print("find opt1 ")
    opt1_index = []
    for i in range(len(option_h_list)):
        #if option_h_list[i][0] == "Opt1":
        total_length = 0
        for y_pos in net_y :
            total_length = total_length + abs( option_h_list[i][3][1] - y_pos)
        line = ( i , total_length)
        opt1_index.append(line)
    opt1_index.sort(key=lambda x:x[1])

    for i in opt1_index:
        ## opt1 만 찾아 봅시다. 
        print(i[0])
        print(i[1])
        option_h = option_h_list[i[0]]
        #print(h_split)
        line_y=int(option_h[3][1])
        pass_flag = 0
        # 선택 된 h_line 에 포함 된 option_v_list 확인. 
        # v_line 은 line_v_list 에 저장, option_v_list 
        option_v_list=[]
        line_v_list=[]

        #print("vertical line 이 있는지 확인.")
        for i in range(len(net_x)):
            for metal in Metal_dir :
                if Metal_dir[metal] == 'v':
                    v_line = [ metal,grade,[net_x[i],min(net_y[i],line_y)],[net_x[i],max(net_y[i],line_y)]]
                    option_v = routing_option_v(option_h,v_line)

                    if option_v !=[]:
                        pass_flag = 1
                        # option_v type  =[[],[]]
                        #for option in option_v:
                        option_v_list.append(option_v)
                        new_line = [net[0],option_v[1],option_v[2],[net_x[i],min(net_y[i],line_y)],[net_x[i],max(net_y[i],line_y)]]
                        line_v_list.append(new_line)
                    else:
                        pass_flag = 0 
                        option_v_list.clear()
                        line_v_list.clear()

        #print("기존에 option_metal 과 비교를 하고 새로운 대안이 될지 확인 하자.")
        #print("vertical line 길이 총합이 짧은 녀석이 좋은 놈이다. ")
        if pass_flag ==1 :
            new_line_length = 0 
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
                    chop_left =  [valid_x1 , routing_x1-Metal_space[opt_split[2]]]
                    print(" Chop right의 좌측은  routing space  필요")
                    chop_right = [routing_x2+Metal_space[opt_split[2]], valid_x2]

                    print(" 수평 line의 길이가 Line 최소 길이 보다 짧은 경우 valid_line에 저장 안함 ")
                    if (chop_left[1] - chop_left[0] ) >= Metal_width[opt_split[2]] :
                        valid = [opt_split[1],opt_split[2],[chop_left[0],opt_split[3][1]],[chop_left[1],opt_split[4][1]]]
                        Valid_line_h.append(valid)

                    if (chop_right[1] - chop_right[0] ) >= Metal_width[opt_split[2]] :
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
                    chop_down =  [valid_y1 , routing_y1-Metal_space[opt_split[2]]]
                    print(" Chop up의 아래는   routing space  필요")
                    chop_up =    [routing_y2+Metal_space[opt_split[2]], valid_y2]

                    print(" 수평 line의 길이가 Line 최소 길이 보다 짧은 경우 valid_line에 저장 안함 ")
                    if (chop_down[1] - chop_down[0] ) >= Metal_width[opt_split[2]] :
                        valid = [opt_split[1],opt_split[2],[opt_split[3][0],chop_down[0]],[opt_split[4][0],chop_down[1]]]
                        Valid_line_v.append(valid)
                    print(Valid_line_v[len(Valid_line_v)-1])

                    if (chop_up[1] - chop_up[0] ) >= Metal_width[opt_split[2]] :
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


            


net2=['net_1002','M3','M3_A_AC',[400,300],[1000,700],[10000,400]]
net2_clone=['net_1002_copy','M3','M3_A_AC',[400,300],[1000,700],[10000,400]]
net3=['net_1003','M4','M4_A_AC',[11000,300],[1000,700],[10000,400],[100,20000]]
net4=['net_1004','M5','M5_B_AC',[11000,300],[1000,700],[10000,400],[100,20000]]
net5=['net_1005','M5','M5_GIO_AC',[110000,300],[1000,700],[10000,400],[100,20000]]
net6=['net_1006','M5','M5_GIO_AC',[210000,300],[1000,700],[10000,400],[100,20000]]
net7=['net_1006','M5','M5_GIO_AC',[210000,300],[400000,700],[10000,400],[100,20000]]

start = time.time()
routing_select_multi(net2)
routing_line(net2)
routing_select_multi(net2_clone)
routing_line(net2_clone)
routing_select_multi(net3)
routing_line(net3)
routing_select_multi(net4)
routing_line(net4)
routing_select_multi(net5)
routing_line(net5)
routing_select_multi(net6)
routing_line(net6)
routing_select_multi(net7)
routing_line(net7)

print("time:",time.time() - start)


## 최종 결과 
def draw_line(used_line_list) :
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0

    for line in used_line_list :
        x1 = int(line[3][0]/1000)
        x2 = int(line[4][0]/1000)
        y1 = int(line[3][1]/1000)
        y2 = int(line[4][1]/1000)
        max_x = max(max_x,x1,x2)
        min_x = min(min_x,x1,x2)
        max_y = max(max_y,y1,y2)
        min_y = min(min_y,y1,y2)


    R,G,B = ( 0 , 0 , 255) , ( 0,255,0), (255,0,0)
    #RG    = ( 0 , 255 , 255) , ( 0,255,0)
    img = np.zeros((max_y -min_y,max_x-min_x,3),np.uint8)
    img[:] = ( 255,255,255)

    for line in used_line_list:
        x1 = int(line[3][0]/1000)
        x2 = int(line[4][0]/1000)
        y1 = int(line[3][1]/1000)
        y2 = int(line[4][1]/1000)
        if 'M2' in line :
            cv2.line(img,(x1,y1),(x2,y2),R+G,1)

        elif 'M1' in line :
            cv2.line(img,(x1,y1),(x2,y2),R+G+B,1)
        elif 'M3' in line :
            cv2.line(img,(x1,y1),(x2,y2),R,2)
        elif 'M4' in line :
            cv2.line(img,(x1,y1),(x2,y2),G,2)
        elif 'M5' in line :
            cv2.line(img,(x1,y1),(x2,y2),B,2)

    cv2.imshow('Line',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#draw_line(Used_line_h)

#print(len(Valid_line_v))



def check_max_loading(used_line_h,used_line_v):
    max_loading = {}
    for line_h  in used_line_h:
        net = line_h[0]
        max_loading[net]=0

    for line_h in used_line_h:
        print(line_h)
        net = line_h[0]
        for net_l in max_loading :
            max_loading[net] = max_loading[net] + abs(line_h[3][0] - line_h[4][0])

    print(max_loading)
    for line_v in used_line_v:
        net = line_v[0]
        for net_l in max_loading :
            max_loading[net] = max_loading[net] + abs(line_v[3][1] - line_v[4][1])

    print(max_loading)

#check_max_loading(Used_line_h,Used_line_v)


def count_max_line_h(used_line_h):
    metal_grade = []
    for line_h in used_line_h:
        same = 0 
        for grade in metal_grade :
            if grade == line_h[2] :
                same =1
        if same == 0 :
            metal_grade.append(line_h[2])

    rows = len(metal_grade)
    metal_count =[]

    for i in range( rows ):
        metal_count.append([])
        for j in range(Size_x):
            metal_count[i].append(0)
    #metal_count = [[0]*Size_x] * rows
    metal_count[0][0] =1

    for line in  used_line_h :
        for i in range(len(metal_grade)) :
            if line[2] == metal_grade[i]:
                for x in range(Size_x) :
                    if min(line[3][0] , line[4][0]) <= x < max(line[3][0],line[4][0]):
                        metal_count[i][x] = int(metal_count[i][x])+1
    print(metal_grade[0],max(metal_count[0]))
    print(metal_grade[1],max(metal_count[1]))
    print(metal_grade[2],max(metal_count[2]))
    print(metal_grade[3],max(metal_count[3]))

    metal_count_return ={}
    for i in range( len(metal_grade)):
        metal_count_return[metal_grade[i]]=max(metal_count[i])
    return metal_count_return

metal_count = count_max_line_h(Used_line_h)

print(metal_count)


