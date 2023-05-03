#Libraries
import tkinter
import tkinter.ttk
import datetime
import math
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import time
#import RPi.GPIO as GPIO #🍓
import sys
from threading import * 
#✏️ 전역변수###################################

FONT_TITLE=('나눔고딕',25,'bold')
FONT_NAME=('나눔고딕',13,'bold')
FONT_DETAIL=('나눔고딕',11)
FONT_INFO=('나눔고딕',8)#🪄

TITLE_ONTIMEREPORT='실시간 리포트'
TITLE_DAILYREPORT='✨ 데일리 리포트'
TITLE_FEEDSETTING='❤ 사료량 설정'
TITLE_FOODINFO='✍ 사료칼로리 계산기'
TITLE_FEEDSETTING='⚙️사료량 설정'

date_time=datetime.datetime.now()#🪄
user_time=0
###############################################
#⚙ 기본 함수##########################################################################

#창 기본 설정
def WindowMaker(title:str,WindowSize="800x400"):
    window=tkinter.Tk() #창 실행
    window.title(title)
    window.geometry(WindowSize)
    window.resizable(False,False)
    return window

#제목
def Title(window, title):
    title_label=tkinter.Label(window, text=title,font=FONT_TITLE)
    title_label.place(x=70,y=25)
    
#🪄오늘일자
#🪄 : 시간과 일자를 받아오는 객체가 같아서 전역변수로 설정.
def Today(window, date_time):
    date_label = tkinter.Label(window, text=f"{date_time:%Y-%m-%d}", font=FONT_NAME)
    date_label.place(x=70,y=70)

#####################################################################################

#창##################################################################
window=WindowMaker('Main')
notebook=tkinter.ttk.Notebook(window, width=800, height=480)
notebook.pack()

FeedSettingWindow=tkinter.Frame(window)
notebook.add(FeedSettingWindow, text=TITLE_FEEDSETTING)

FoodInfoWindow=tkinter.Frame(window)
notebook.add(FoodInfoWindow, text=TITLE_FOODINFO)

OntimeReportWindow=tkinter.Frame(window)
notebook.add(OntimeReportWindow, text=TITLE_ONTIMEREPORT)

DailyReportWindow=tkinter.Frame(window)
notebook.add(DailyReportWindow, text=TITLE_DAILYREPORT)



#####################################################################

#⏰1.실시간리포트##################################################################

Title(OntimeReportWindow,TITLE_ONTIMEREPORT)#제목
#Today(OntimeReportWindow)#오늘 날짜

#표
treeview=tkinter.ttk.Treeview(OntimeReportWindow, columns=["0","1","2","3"],
                             displaycolumns=["0","1","2","3"])
treeview.place(x=70, y=130)
#필드명 --------------------------------------------------
treeview.column("0",width=150, anchor="center")
treeview.heading("0",text="급여시간",anchor="center")

treeview.column("1",width=150, anchor="center")
treeview.heading("1",text="급여량(g)",anchor="center")

treeview.column("2",width=150, anchor="center")
treeview.heading("2",text="섭취시간(분)",anchor="center")

treeview.column("3",width=150, anchor="center")
treeview.heading("3",text="섭취량(g)",anchor="center")

treeview["show"]="headings" #만든 컬럼만 보여줌
#----------------------------------------------------------



#✨2.데일리리포트#####################################################################

Title(DailyReportWindow,TITLE_DAILYREPORT)#제목
    #Today(DailyReportWindow)#오늘 날짜



label2=tkinter.Label(DailyReportWindow,text="권장 식사량" ,font=FONT_NAME)
label2.place(x=80, y=105)

label3=tkinter.Label(DailyReportWindow,text="1회 식사량" ,font=FONT_NAME)
label3.place(x=80, y=195)

label5=tkinter.Label(DailyReportWindow, text="급식 횟수" ,font=FONT_NAME)
label5.place(x=420,y=35)

label6=tkinter.Label(DailyReportWindow,text="식사 횟수" ,font=FONT_NAME)
label6.place(x=420,y=105)


#모터&로드셀🍓#########################################################
servoPin=2
SERVO_MAX_DUTY=12
SERVO_MIN_DUTY=2.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

servo=GPIO.PWM(servoPin,50)
servo.start(0)

EMULATE_HX711=False
referenceUnit=490

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.clenaup()

    print("Bye!")

hx = HX711(20,16)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()

hx.tare()
initial_weight=int(hx.get_weight(5))
print("Tare done! Add weight now...", initial_weight)


#####################################################################

#시연용 시간조절창###################################################

timesetter = Tk()
timesetter.title("Time Setter")
timesetter.geometry("250x100+500+400")
feed_done=0 #0이면 안준거고 1이면 준거야

month=0
day=0
hour=0
min=0
hour_feed, min_feed=0,0#🪄급여시간용

return_feed_timetable=[]
feed_done=0#급여했어 안했어?
feed_time, feed_amount, ate_time, ate_amount=0,0,0,0 #⏰실시간 리포트용 변수
treeValueList=[]#⏰실시간 리포트용 변수

      
def print_user_time_control():#🪄사용자 시간제어 + 급여동작

    global user_time
    global return_feed_timetable
    user_time_min=min

    if user_time_min<10:
        user_time_min='0'+str(user_time_min)
    user_time_min=str(user_time_min)

    user_time=str(hour)+":"+user_time_min#lst이용 x
    print('user_time',user_time)
    return_feed_timetable=print_feed_timetable()

    return user_time, return_feed_timetable

def print_feed_timetable():#🪄급여 시간 시간표리스트

    #now_time=date_time.strftime('%H:%M') #🪄현재시간 - 예시 :15:46

    feed_min=min_feed
    if feed_min<10:
        feed_min='0'+str(feed_min)
    feed_min=str(feed_min)

    str_feed_timetable=[str(x)+":"+feed_min for x in feed_timetable] # format str 22:30
    #print('급여시간표 - str_feed_timetable:',str_feed_timetable)#test : 설정한 급여 시작시간표 출력
    #print('시스템시간 - now_time:',now_time)#test: 현재시간 출력
    return str_feed_timetable

def motor_weight():#🍓일정무게가 될때까지 모터 실행
    global feed_time, feed_amount, ate_time, ate_amount#⏰실시간리포트용
    global feed_done

    def servo_control(degree):
        duty=SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
        print("Degree=",degree,"duty=",duty)
        servo.ChangeDutyCycle(duty)
        time.sleep(1)#sleep없으면 안돌아가,,숫자 작게해도 첫 로드 시간과는 무관

    user_time, return_feed_timetable=print_user_time_control()

    global initial_weight
    print("Add weight now...", initial_weight)

    recent_weight = initial_weight #무게 측정
    print('recent_weight:', recent_weight)
    print('foodamountsetting:', foodamountsetting)

    print('feed_done', feed_done)
    if user_time in return_feed_timetable and recent_weight<=foodamountsetting and feed_done==0:
        while recent_weight<=foodamountsetting:
            
            for i in range(0,360,180):
                print("돌려")
                servo_control(i)

            recent_weight = hx.get_weight(5) #무게를 재
            print("weight",recent_weight)
            
            hx.power_down()
            hx.power_up()
            time.sleep(0.3)    
        initial_weight+=recent_weight

        feed_done=1 
        feed_time=user_time #⏰실시간리포트 : 급여시간
        feed_amount=int(recent_weight)#⏰실시간리포트 : 급여량
        treeValueList.append([str(feed_time),feed_amount,str(ate_time), ate_amount])#⏰실시간리포트 : (급여시간, 급여량, 0,0) 형태로 저장
        print('treevaluelist',treeValueList)#⏰실시간리포트 :확인용
        treeview.delete(*treeview.get_children())#기존 있는 표 삭제하고 다시 넣어
        #⏰실시간 리포트 표 삽입---------------------------------------------------------------
        for i in range(len(treeValueList)):
            treeview.insert("","end",text="",values=treeValueList[i],iid=i)
        #-------------------------------------------------------------------------------------

def eating(): #아무것도 안하고 있을때 하는짓짓

    global initial_weight
    global user_time
    global return_feed_timetable
    print("--EATING_START--")
    ate_times=[]
    
    while True:
        '''
        if ate_start_time==0:#섭취시작 시간이 비어있으면 
            ate_start_time=user_time#⏰실시간리포트 : 먹기시작한 시간 ;  while밖에 있으면 계속 0만찍혀
        #test
        print('eating/while/ate_start_time', ate_start_time)#값을 한번 받고 고정되어야함.
        ate_time=user_time#얘는 바뀌는게 맞아
        print('eating/while/ate_time',ate_time)#얘는 시간을 바꾸는대로 바뀌어야함.
        '''

        ontime_weight=int(hx.get_weight(5))
        if initial_weight>ontime_weight:#이전 값인 initial_weight보다 받아오는 무게가 작다== 먹는 중이다
            print(f"-- 먹는 중 -- initial_weight {initial_weight}, 실시간 무게 : ontime_weight:{ontime_weight}")
            feed_time, feed_amount=0,0

            ate_amount=int(initial_weight-ontime_weight)#⏰실시간리포트 : 먹은양= 초기값-실시간측정무게
            ate_time=user_time#얘는 바뀌는게 맞아
            
            #먹은 시간이 계속 같으면 먹은 무게를 더해
            ate_time_=str(ate_time)#문자열 취급한 먹은시간 ate_time_에 할당하고
            ate_times.append(ate_time_)#일단 먹은 시간 저장
            feed_sum_sametime=0#먹은 무게 더하는용도로 0으로 초기화, 다시 돌아오면 0으로 자동 초기화
            if ate_time_ in ate_times:#먹은 시간들 저장하는거에 ate_time_이 있다면
                feed_sum_sametime+=ate_amount#먹은 무게를 더해줄꺼야
                treeValueList.append([str(feed_time),feed_amount,ate_time_, feed_sum_sametime])#⏰(0,0, 먹기시작한시간,먹은양) 형태로 저장 실시간 리포트용리스트에 올려
                print('treevaluelist',treeValueList)#⏰실시간리포트 :확인용

                treeview.delete(*treeview.get_children())#⏰실시간리포트 :기존 있는 표내용 삭제
                #⏰실시간 리포트 표 삽입---------------------------------------------------------------
                for i in range(len(treeValueList)):
                    treeview.insert("","end",text="",values=treeValueList[i],iid=i)
                #-------------------------------------------------------------------------------------
            
            else:#먹은 시간들 저장하는거에 ate_time이 없다면
                treeValueList.append([str(feed_time),feed_amount,ate_time_,ate_amount])#⏰(0,0, 먹기시작한시간,먹은양) 형태로 저장 실시간 리포트용리스트에 올려
                print('treevaluelist',treeValueList)#⏰실시간리포트 :확인용

                treeview.delete(*treeview.get_children())#⏰실시간리포트 :기존 있는 표내용 삭제
                #⏰실시간 리포트 표 삽입---------------------------------------------------------------
                for i in range(len(treeValueList)):
                    treeview.insert("","end",text="",values=treeValueList[i],iid=i)
                #-------------------------------------------------------------------------------------
            
            initial_weight=ontime_weight

        hx.power_down()
        hx.power_up()
        time.sleep(1)
        if user_time in return_feed_timetable:#사용자 지정 시간==설정한 급여 시간
            motor_weight()#🍓

        
        if user_time == "21:00":
            #데이터 삽입 ----------------------------------
            label10=tkinter.Label(DailyReportWindow, text=f"{foodamountsetting}g",font=FONT_DETAIL)
            label10.place(x=100, y=135)
            #foodamountsetting

            ate_all=0
            for i in range(len(treeValueList)):
                ate_all+=treeValueList[i][3]
            ate_avg=int(ate_all/(len(treeValueList)))

            label11=tkinter.Label(DailyReportWindow, text=f"{ate_avg}g",font=FONT_DETAIL)
            label11.place(x=100, y=235)
            #합산해서 평균

            
            feed_count=0
            for i in range(len(treeValueList)):
                print('treevaluelist[i][0]',treeValueList[i][0])
                if treeValueList[i][0]!='0':#급여시간 부분이 0이 아니면 급여한거잖아
                    feed_count+=1 #급여시간 횟수
            print(f'급여 횟수 : {feed_count}')
            label13=tkinter.Label(DailyReportWindow, text=f"{feed_count}번" ,font=FONT_DETAIL)
            label13.place(x=440,y=70)

            ate_count=0
            for i in range(len(treeValueList)):
                print('treevaluelist[i][2]',treeValueList[i][2])
                if treeValueList[i][2]!='0':#섭취시간 부분이 0이 아니면 섭취한거잖아
                    ate_count+=1 #급여시간 횟수
            print(f'섭취 횟수 : {ate_count}')

            label14=tkinter.Label(DailyReportWindow, text=f"{ate_count}번" ,font=FONT_DETAIL)
            label14.place(x=440,y=135)
        #리스트개수



######################################################################################

            
        


def 급여시간계산(count):
            start_feed_hour=hour_feed #급여 시작 시간 기준 hour변수
            global feed_timetable                
            #데일리리포트 보내는 시간이 21시이므로, 급여 시작시간~20시까지의 시간을 count로 나누기
            #급여 마지막시간 20:00
            feed_time_unit=int(math.trunc((20-start_feed_hour)/(count-1))) #몇시간 마다 급여할꺼야? 21-8=13
            #print(feed_time_unit)
            feed_timetable=list(reversed([x for x in range(start_feed_hour,21,feed_time_unit)]))

            return feed_timetable



def monthup():
    global month
    global feed_done
    month+=1
    if month==13:
        month=1
        labelmonth=tkinter.Label(timesetter, text="    ")
        labelmonth.place(x=10,y=30)
        labelmonthO=tkinter.Label(OntimeReportWindow, text="    ", font= FONT_NAME)
        labelmonthO.place(x=70,y=70)
        labelmonthD=tkinter.Label(DailyReportWindow, text="    ", font=FONT_NAME)
        labelmonthD.place(x=70,y=70)
    labelmonth=tkinter.Label(timesetter, text=str(month))
    labelmonth.place(x=10,y=30)

    datetimeMONTHOlabel=tkinter.Label(OntimeReportWindow, text=str(month),font=FONT_NAME)
    datetimeMONTHOlabel.place(x=70,y=70)
    datetimeMONTHDlabel=tkinter.Label(DailyReportWindow, text=str (month), font=FONT_NAME)
    datetimeMONTHDlabel.place(x=70, y=70)
    feed_done=0

def dayup():
    global day
    global feed_done
    day+=1
    if day==32:
        day=1
        labelday=tkinter.Label(timesetter, text="    ")
        labelday.place(x=70,y=30)
        labeldayO=tkinter.Label(OntimeReportWindow, text="    ",font=FONT_NAME)
        labeldayO.place(x=110,y=70)
        labeldayD=tkinter.Label(DailyReportWindow, text="    ", font=FONT_NAME)
        labeldayD.place(x=110, y=70)
    labelday=tkinter.Label(timesetter, text=str(day))
    labelday.place(x=70,y=30)
    
    datetimeDAYOlabel=tkinter.Label(OntimeReportWindow, text=str(day),font=FONT_NAME)
    datetimeDAYOlabel.place(x=110,y=70)
    datetimeDAYDlabel=tkinter.Label(DailyReportWindow, text=str(day),font=FONT_NAME)
    datetimeDAYDlabel.place(x=110,y=70)
    feed_done=0
def hourup():
    global hour
    global feed_done
    hour+=1
    if hour==24:
        hour=0
        labelhour=tkinter.Label(timesetter, text="    ")
        labelhour.place(x=130,y=30)
        labelhourO=tkinter.Label(OntimeReportWindow, text="    ",font=FONT_NAME)
        labelhourO.place(x=150,y=70)
        
    labelhour=tkinter.Label(timesetter, text=str(hour))
    labelhour.place(x=130,y=30)
    datetimeHOUROlabel=tkinter.Label(OntimeReportWindow, text=str(hour),font=FONT_NAME)
    datetimeHOUROlabel.place(x=150,y=70)
    print_user_time_control()#🪄 사용자 지정 시간 출력
    feed_done=0

def minup():
    global min
    global feed_done
    min+=5
    if min==60:
        min=0
        labelmin=tkinter.Label(timesetter, text="    ")
        labelmin.place(x=190,y=30)
        labelminO=tkinter.Label(OntimeReportWindow, text="    ",font=FONT_NAME)
        labelminO.place(x=190,y=70)
        
    labelmin=tkinter.Label(timesetter, text=str(min))
    labelmin.place(x=190,y=30)
    datetimeMINOlabel=tkinter.Label(OntimeReportWindow, text=str(min),font=FONT_NAME)
    datetimeMINOlabel.place(x=190,y=70)
    print_user_time_control()#🪄 사용자 지정 시간 출력
    feed_done=0


labelMONTH=tkinter.Label(timesetter, text="MONTH")
labelMONTH.place(x=10,y=10)
label월=tkinter.Label(timesetter, text="월")
label월.place(x=30,y=30)
labelMONTHO=tkinter.Label(OntimeReportWindow, text=month,font=FONT_NAME)
labelMONTHO.place(x=70,y=70)
label월O=tkinter.Label(OntimeReportWindow, text="월",font=FONT_DETAIL)
label월O.place(x=94,y=70)
label월D=tkinter.Label(DailyReportWindow, text="월",font=FONT_DETAIL)
label월D.place(x=94,y=70)

labelDAY=tkinter.Label(timesetter, text="DAY")
labelDAY.place(x=70,y=10)
label일=tkinter.Label(timesetter, text="일")
label일.place(x=90,y=30)
labelDAYO=tkinter.Label(OntimeReportWindow, text=day,font=FONT_NAME)
labelDAYO.place(x=110,y=70)
label일O=tkinter.Label(OntimeReportWindow, text="일",font=FONT_DETAIL)
label일O.place(x=134,y=70)
label일D=tkinter.Label(DailyReportWindow, text="일",font=FONT_DETAIL)
label일D.place(x=134,y=70)

labelHOUR=tkinter.Label(timesetter, text="HOUR")
labelHOUR.place(x=130,y=10)
label시=tkinter.Label(timesetter, text="시")
label시.place(x=150,y=30)
labelHOURO=tkinter.Label(OntimeReportWindow, text=hour,font=FONT_NAME)
labelHOURO.place(x=150,y=70)
label시O=tkinter.Label(OntimeReportWindow, text="시",font=FONT_DETAIL)
label시O.place(x=174,y=70)


labelMIN=tkinter.Label(timesetter, text="MIN")
labelMIN.place(x=190,y=10)
label분=tkinter.Label(timesetter, text="분")
label분.place(x=210,y=30)
labelMINO=tkinter.Label(OntimeReportWindow, text=min,font=FONT_NAME)
labelMINO.place(x=190,y=70)
label분O=tkinter.Label(OntimeReportWindow, text="분",font=FONT_DETAIL)
label분O.place(x=214,y=70)



buttonMONTH=tkinter.Button(timesetter, text="⬆️", command=monthup)
buttonMONTH.place(x=10,y=50)

buttonDAY=tkinter.Button(timesetter, text="⬆️", command=dayup)
buttonDAY.place(x=70,y=50)

buttonHOUR=tkinter.Button(timesetter, text="⬆️", command=hourup)
buttonHOUR.place(x=130,y=50)

buttonMIN=tkinter.Button(timesetter, text="⬆️", command=minup)
buttonMIN.place(x=190,y=50)


timeset=[month,day,hour,min]


#####################################################################



#4.사료칼로리 계산기 창########################################################
Title(FoodInfoWindow,TITLE_FOODINFO)


#라벨&entry----------------------------------------------------------

label1=tkinter.Label(FoodInfoWindow,text="조단백질" ,font=FONT_NAME)
label1.place(x=80, y=100)

label2=tkinter.Label(FoodInfoWindow,text="조지방" ,font=FONT_NAME)
label2.place(x=80, y=200)

label3=tkinter.Label(FoodInfoWindow,text="조섬유" ,font=FONT_NAME)
label3.place(x=80,y=300)

label4=tkinter.Label(FoodInfoWindow, text="조회분" ,font=FONT_NAME)
label4.place(x=420,y=100)

label7=tkinter.Label(FoodInfoWindow,text="수분" ,font=FONT_NAME)
label7.place(x=420,y=200)

ent1=tkinter.Entry(FoodInfoWindow)#조단백질
ent1.config(width=10)
ent1.place(x=150, y=130)

ent2=tkinter.Entry(FoodInfoWindow)#조지방
ent2.config(width=10)
ent2.place(x=150, y=220)

ent3=tkinter.Entry(FoodInfoWindow)#조섬유
ent3.config(width=10)
ent3.place(x=150, y=320)

ent4=tkinter.Entry(FoodInfoWindow)#조회분
ent4.config(width=10)
ent4.place(x=490, y=120)

ent7=tkinter.Entry(FoodInfoWindow)#수분
ent7.config(width=10)
ent7.place(x=490, y=220)

label30=tkinter.Label(FoodInfoWindow,text="%" ,font=FONT_DETAIL)
label30.place(x=225, y=130)

label31=tkinter.Label(FoodInfoWindow,text="%" ,font=FONT_DETAIL)
label31.place(x=225, y=220)

label32=tkinter.Label(FoodInfoWindow,text="%" ,font=FONT_DETAIL)
label32.place(x=225, y=320)

label34=tkinter.Label(FoodInfoWindow,text="%" ,font=FONT_DETAIL)
label34.place(x=565, y=120)

label35=tkinter.Label(FoodInfoWindow,text="%" ,font=FONT_DETAIL)
label35.place(x=565, y=220)

#사료칼로리 계산 함수-------------------------------------------

kcal=0

def 칼로리계산():
    global kcal
    
    if f'{ent1.get()}' == "" or f'{ent2.get()}' == "" or f'{ent3.get()}' == "" or f'{ent4.get()}' == "" or f'{ent7.get()}' == "" :
        messagebox.showinfo(title="앗!", message="모두 입력하여 주세요") 
    else:
        label41=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
        label41.place(x=420, y= 110)
        protain=int(ent1.get())/(100-int(ent7.get()))*100
        fat=int(ent2.get())/(100-int(ent7.get()))*100
        ash=int(ent4.get())/(100-int(ent7.get()))*100
        carb=100-protain-fat-ash

        



        
        kcal=math.ceil(protain*4+fat*9+carb*4)

        labelBMR=tkinter.Label(FeedSettingWindow, text='                  ', font=FONT_DETAIL)    
        labelBMR.place(x=560,y=130)
        labelKCAL=tkinter.Label(FeedSettingWindow, text=str(kcal)+'kcal',font=FONT_DETAIL)
        labelKCAL.place(x=560,y=130)
        notebook.select(FeedSettingWindow)

    
    
    


#계산때리는버튼------------------------------------------------- 
btn3=tkinter.Button(FoodInfoWindow, text='확인', command=칼로리계산)
btn3.config(width = 8, height = 1)
btn3.place(x=500, y=300)

##############################################################################








#3.사료 급여창########################################################################################



#계산 함수==============================================================================





#강아지,고양이버튼눌럿을때 하는 함수-----------------------------
animal = 0

def 강아지():

    global animal
    animal = "dog"
    labelDOG=tkinter.Label(FeedSettingWindow, text='강아지 입니다!',font=FONT_DETAIL)
    #주안:글씨색바꾸면 좋을듯
    labelDOG.place(x=170,y=190)
    
def 고양이():

    global animal
    animal = "cat"
    labelCAT=tkinter.Label(FeedSettingWindow, text='고양이 입니다!',font=FONT_DETAIL)
    #주안:글씨색바꾸면 좋을듯
    labelCAT.place(x=170,y=190)
n=0
def 칼로리계산기():
    global count

    #무언가 비엇음
    if animal == 0 or kcal == 0 or f'{ent8.get()}' == "" or f'{ent9.get()}' == "" or f'{ent10.get()}' == "" :
        #동물선택?
        if animal == 0:
            label40=tkinter.Label(FeedSettingWindow, text="⚠️", foreground="red", font=FONT_NAME)
            label40.place(x=80,y=140)
        else:
            label40=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
            label40.place(x=80 ,y=140)
        #몸무게?
        if f'{ent8.get()}' == "":
            label42=tkinter.Label(FeedSettingWindow, text="⚠️", foreground="red", font=FONT_NAME)
            label42.place(x=80 ,y=250)
        else:
            label42=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
            label42.place(x=80 ,y=250)
        #나이?
        if f'{ent9.get()}' == "":
            label43=tkinter.Label(FeedSettingWindow, text="⚠️", foreground="red", font=FONT_NAME)
            label43.place(x=210 ,y=250)
        else:
            label43=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
            label43.place(x=210 ,y=250)
        #사료선택?
        if kcal == 0:
            label41=tkinter.Label(FeedSettingWindow, text="⚠️", foreground="red", font=FONT_NAME)
            label41.place(x=420, y= 110)
        else:
            label41=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
            label41.place(x=420, y= 110)
        #급식횟수?
        if f'{ent10.get()}' == "":
            label44=tkinter.Label(FeedSettingWindow, text="⚠️", foreground="red", font=FONT_NAME)
            label44.place(x=150, y= 320)
        else:
            label44=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
            label44.place(x=150, y= 320)    
    #다 채워졋다!
    else:
        #경고표시 다 지우고~
        label40=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
        label40.place(x=80 ,y=260)
        label42=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
        label42.place(x=80 ,y=260)
        label43=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
        label43.place(x=210 ,y=260)
        label41=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
        label41.place(x=420, y= 110)
        label44=tkinter.Label(FeedSettingWindow, text="    ", font=FONT_NAME)
        label44.place(x=190, y= 410)

        #진행시켜!
        weight=float(ent8.get())
        if weight > 100 :
            messagebox.showinfo(title="적이요..", message="몸무게 제대로 쓰세요!")           
        else:
            
            age=int(ent9.get())
            if weight<2:
                BMR=math.ceil(70*weight*0.75)
            else:
                BMR=math.ceil(weight*30+70)

            labelBMR=tkinter.Label(FeedSettingWindow, text='                            ',font=FONT_DETAIL)
            labelBMR.place(x=460, y= 190)
            labelBMR=tkinter.Label(FeedSettingWindow, text=str(BMR)+'kcal',font=FONT_DETAIL)
            labelBMR.place(x=460, y= 190)
            #print("BMR= ",BMR)#주안:확인용


            #주아니가쓴 함수(권장칼로리계산함수)
            
            if animal == "dog":

                if age<4:
                    DER=math.ceil(BMR*3)
                    #print("DER= ",DER)#주안:확인용
                    labelDER=tkinter.Label(FeedSettingWindow, text='                            ',font=FONT_DETAIL)
                    labelDER.place(x=460, y= 260)
                    labelDER=tkinter.Label(FeedSettingWindow, text=str(DER)+'kcal',font=FONT_DETAIL)
                    labelDER.place(x=460, y= 260)
                elif age >= 4:
                    DER=math.ceil(BMR*2)
                    #print("DER= ",DER)#주안:확인용
                    labelDER=tkinter.Label(FeedSettingWindow, text='                            ',font=FONT_DETAIL)
                    labelDER.place(x=460, y= 260)
                    labelDER=tkinter.Label(FeedSettingWindow, text=str(DER)+'kcal',font=FONT_DETAIL)
                    labelDER.place(x=460, y= 260)
                else:
                    print("개의 권장칼로리 계산에 뭔가 문제가 잇음 ㅠ")#주안:오류코드
            elif animal == "cat":
                DER=math.ceil(BMR*2.5)
                
                labelDER=tkinter.Label(FeedSettingWindow, text='              ',font=FONT_DETAIL)
                labelDER.place(x=460, y= 260)
                labelDER=tkinter.Label(FeedSettingWindow, text=str(DER)+'kcal',font=FONT_DETAIL)
                labelDER.place(x=460, y= 260)
            elif animal == 0:
                print("동물이 선택되지 않음")
                #messagebox.showinfo(title="앗!", message="동물을 선택해 주세요!")
                
            else:
                print("동물의 권장칼로리 계산에 뭔가 문제가 있음 ㅠ")#주안:오류코드

            #print("animal=",animal)#주안:확인용

            #용주가쓴 함수(총 계산 출력)
            #print("kcal= ",kcal)
            global foodamountsetting
            foodperday=DER/(kcal/100) #하루에 급여해야하는양=DER/(1g당 kcal)
            count=int(ent10.get())#하루 급여 횟수
            foodamountsetting=math.ceil(foodperday/count)#🪄 여기 틀려서 고칩니다 : foodperday/3 -> foodperday/count
            
            labelfoodamountsetting=tkinter.Label(FeedSettingWindow,text="        ", font=('나눔고딕',18))
            labelfoodamountsetting.place(x=330, y= 320)

            labelfoodamountsetting=tkinter.Label(FeedSettingWindow,text=str(foodamountsetting), font=('나눔고딕',18))
            labelfoodamountsetting.place(x=340, y= 320)
            global n
            n=1
        

        #창 기본 설정
        def WindowMaker(title:str,WindowSize="400x300"):
            window=tkinter.Tk() #창 실행
            window.title(title)
            window.geometry(WindowSize)
            window.resizable(False,False)
            return window

        def 급여시작시간입력():
            global feed_timetable
            start_feed_min=min_feed #급여 시작 시간 기준 min 변수
            timetable=급여시간계산(count)

            #목록에서 급여시작 시간표 출력
            for i in range(0,len(timetable)):
                lstbox_feed_timetable.insert(0,str(timetable[i])+"시 "+str(start_feed_min)+"분")
            feed_timetable=timetable
            print_feed_timetable()
            #print('급여시작시간입력',feed_timetable)#계산된 급여시간 확인용

            
        def 급여시간설정창닫기():

            feeding_time_setting_window.destroy()
            
        #주안이 코드 : timesetter에서 시, 분 가져옴############################################################
        def hourup():
            global hour_feed
            hour_feed+=1
            if hour_feed==24:
                hour_feed=0
                labelhour=tkinter.Label(feeding_time_setting_window, text="    ")
                labelhour.place(x=150,y=120)
            labelhour=tkinter.Label(feeding_time_setting_window, text=str(hour_feed))
            labelhour.place(x=150,y=120)

        def minup():
            global min_feed
            min_feed+=5
            if min_feed==60:
                min_feed=0
                labelhour=tkinter.Label(feeding_time_setting_window, text="    ")
                labelhour.place(x=200,y=120)
            labelmin=tkinter.Label(feeding_time_setting_window, text=str(min_feed))
            labelmin.place(x=200,y=120)
        #####################################################################################################``

        feeding_time_setting_window=WindowMaker('급여시간 설정')
        Title(feeding_time_setting_window, "급여시간 설정")

        #시작 시간 입력 tkinter
        lbl_start_feed_time=tkinter.Label(feeding_time_setting_window, text="급여 시작 시간",font=FONT_NAME)
        btn_start_feed_time=tkinter.Button(feeding_time_setting_window, text="확인",command=급여시작시간입력)
        lbl_start_feed_time.place(x=20, y=100)
        btn_start_feed_time.place(x=250, y=140)

        #주안이 코드 : timesetter에서 시, 분 가져옴############################################################
        labelHOUR=tkinter.Label(feeding_time_setting_window, text="HOUR")
        labelHOUR.place(x=150,y=100)
        label시=tkinter.Label(feeding_time_setting_window, text="시")
        label시.place(x=165,y=120)

        labelMIN=tkinter.Label(feeding_time_setting_window, text="MIN")
        labelMIN.place(x=200,y=100)
        label분=tkinter.Label(feeding_time_setting_window, text="분")
        label분.place(x=215,y=120)

        buttonHOUR=tkinter.Button(feeding_time_setting_window, text="⬆️", command=hourup)
        buttonHOUR.place(x=150,y=140)

        buttonMIN=tkinter.Button(feeding_time_setting_window, text="⬆️", command=minup)
        buttonMIN.place(x=200,y=140)
        ####################################################################################################


        #계산한 급여 시간 tkinter
        lbl_feed_timetable=tkinter.Label(feeding_time_setting_window, text='이 시간에 급여합니다!', font=FONT_NAME)
        lstbox_feed_timetable=tkinter.Listbox(feeding_time_setting_window, width=20, height=5)
        lstbox_feed_timetable.place(x=30,y=210)
        lbl_feed_timetable.place(x=20, y=190)

        #창닫기
        btn_shutdown=tkinter.Button(feeding_time_setting_window,text="닫기", command=급여시간설정창닫기)
        btn_shutdown.place(x=200, y=260)

        feeding_time_setting_window.mainloop()
        
#4번창으로 이동하는 함수----------------------------
def 사료칼로리계산기():
    notebook.select(FoodInfoWindow)#창 바꾸기



#사료 설청창 라벨========================================================================
Title(FeedSettingWindow,TITLE_FEEDSETTING)#제목

#반려동물 타입--------------------------------------------
label18=tkinter.Label(FeedSettingWindow, text="반려동물 타입",font=FONT_NAME)
label18.place(x=155, y= 110)

btn1 = tkinter.Button(FeedSettingWindow, text = 'btn', background = 'white',command=강아지)
btn1.config(width = 10, height = 2)
btn1.config(text = "강아지")
btn1.place(x=120,y=140)

btn2 = tkinter.Button(FeedSettingWindow, text = 'btn', background = 'white',command=고양이)
btn2.config(width = 10, height = 2)
btn2.config(text = "고양이")
btn2.place(x=220,y=140)

#몸무게 입력----------------------------------------------
label19=tkinter.Label(FeedSettingWindow, text="몸무게 입력",font=FONT_NAME)
label19.place(x=90, y= 220)

ent8 = ttk.Entry(FeedSettingWindow)

ent8.config(width=10)
ent8.place(x=110,y=250)


label1=tkinter.Label(FeedSettingWindow,text="kg" ,font=FONT_DETAIL)
label1.place(x=190, y=250)

#나이 입력------------------------------------------------
label20=tkinter.Label(FeedSettingWindow, text="나이 입력",font=FONT_NAME)
label20.place(x=230, y= 220)

ent9 = tkinter.Entry(FeedSettingWindow)
ent9.config(width=10)
ent9.place(x=240,y=250)



label2=tkinter.Label(FeedSettingWindow,text="개월" ,font=FONT_DETAIL)
label2.place(x=305, y= 250)

#사료선택-------------------------------------------------
label21=tkinter.Label(FeedSettingWindow, text="사료 선택",font=FONT_NAME)
label21.place(x=460, y= 70)

btn3=tkinter.Button(FeedSettingWindow, text=TITLE_FOODINFO, background = 'white',command=사료칼로리계산기)
btn3.place(x=460, y=100)

label26=tkinter.Label(FeedSettingWindow,text="100g당 칼로리" ,font=FONT_DETAIL)
label26.place(x=460,y=130)

#기초대사량-----------------------------------------------
label22=tkinter.Label(FeedSettingWindow, text="기초대사량",font=FONT_NAME)
label22.place(x=460, y= 165)

#권장칼로리-----------------------------------------------
label23=tkinter.Label(FeedSettingWindow, text="하루 권장 섭취 칼로리",font=FONT_NAME)
label23.place(x=460, y= 235)

#결과확인버튼---------------------------------------------
btn4=tkinter.Button(FeedSettingWindow, text = 'btn', background = 'white',command=칼로리계산기)
btn4.config(width = 8, height = 1)
btn4.config(text = "확인")
btn4.place(x=685,y=325)

#최종결론-------------------------------------------------
label24=tkinter.Label(FeedSettingWindow, text="하루",font=('나눔고딕',18))
label24.place(x=190, y= 320)

ent10=tkinter.Entry(FeedSettingWindow)
ent10.config(width=8)
ent10.place(x=250, y= 325)

label25=tkinter.Label(FeedSettingWindow, text="번",font=('나눔고딕',18))
label25.place(x=300, y= 320)

label26=tkinter.Label(FeedSettingWindow, text="g씩 급여할께요!",font=('나눔고딕',18))
label26.place(x=405, y= 320)


################################################################################################
  
#숫자패드###############

#number_entry = 0

def button_pressed8(value):
    ent8.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed9(value):
    ent9.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed10(value):
    ent10.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed1(value):
    ent1.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed2(value):
    ent2.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed3(value):
    ent3.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed4(value):
    ent4.insert("end",value)

    #대충 entry에 숫자 입력하라는 말
    print(value)

def button_pressed7(value):
    ent7.insert("end",value)
    
    #대충 entry에 숫자 입력하라는 말
    print(value)


def backspace_8():
    ent8.delete(len(ent8.get())-1, tkinter.END)

def backspace_9():
    ent9.delete(len(ent9.get())-1, tkinter.END)

def backspace_10():
    ent10.delete(len(ent10.get())-1, tkinter.END)

def backspace_1():
    ent1.delete(len(ent1.get())-1, tkinter.END)

def backspace_2():
    ent2.delete(len(ent2.get())-1, tkinter.END)

def backspace_3():
    ent3.delete(len(ent3.get())-1, tkinter.END)

def backspace_4():
    ent4.delete(len(ent4.get())-1, tkinter.END)

def backspace_7():
    ent7.delete(len(ent7.get())-1, tkinter.END)

def ent8number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed8('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed8('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed8('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed8('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed8('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed8('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed8('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed8('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed8('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_8)
    button_backspace.grid(row=2, column=4)
    
    new_window.mainloop()

new_window_button = tkinter.Button(FeedSettingWindow, text="몸무게입력", command=ent8number)
new_window_button.place(x=120,y=270)



def ent9number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed9('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed9('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed9('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed9('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed9('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed9('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed9('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed9('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed9('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_9)
    button_backspace.grid(row=2, column=4)
    new_window.mainloop()

new_window_button = tkinter.Button(FeedSettingWindow, text="나이입력", command=ent9number)
new_window_button.place(x=250,y=270)



def ent10number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed10('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed10('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed10('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed10('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed10('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed10('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed10('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed10('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed10('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)
    
    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_10)
    button_backspace.grid(row=2, column=4)
    
    new_window.mainloop()

new_window_button = tkinter.Button(FeedSettingWindow, text="횟수입력", command=ent10number)
new_window_button.place(x=250, y= 345)


def ent1number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed1('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed1('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed1('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed1('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed1('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed1('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed1('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed1('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed1('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_1)
    button_backspace.grid(row=2, column=4)
    new_window.mainloop()

new_window_button = tkinter.Button(FoodInfoWindow, text="조단백질입력", command=ent1number)
new_window_button.place(x=250, y=130)


def ent2number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed2('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed2('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed2('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed2('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed2('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed2('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed2('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed2('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed2('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_2)
    button_backspace.grid(row=2, column=4)
    new_window.mainloop()

new_window_button = tkinter.Button(FoodInfoWindow, text="조지방입력", command=ent2number)
new_window_button.place(x=250, y=220)

def ent3number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed3('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed3('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed3('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed3('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed3('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed3('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed3('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed3('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed3('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_3)
    button_backspace.grid(row=2, column=4)
    
    new_window.mainloop()

new_window_button = tkinter.Button(FoodInfoWindow, text="조섬유입력", command=ent3number)
new_window_button.place(x=250, y=320)


def ent4number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed4('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed4('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed4('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed4('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed4('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed4('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed4('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed4('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed4('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_4)
    button_backspace.grid(row=2, column=4)
    new_window.mainloop()

new_window_button = tkinter.Button(FoodInfoWindow, text="조회분입력", command=ent4number)
new_window_button.place(x=590, y=120)

def ent7number():
    new_window = tkinter.Toplevel()
    entry_value = StringVar(new_window, value='')

    #global number_entry
    
    buttonN7 = tkinter.Button(new_window, text="7", command = lambda:button_pressed7('7'))
    buttonN7.grid(row=1, column=0)
    buttonN8 = tkinter.Button(new_window, text="8", command = lambda:button_pressed7('8'))
    buttonN8.grid(row=1, column=1)
    buttonN9 = tkinter.Button(new_window, text="9", command = lambda:button_pressed7('9'))
    buttonN9.grid(row=1, column=2)
     
    buttonN4 = tkinter.Button(new_window, text="4", command = lambda:button_pressed7('4'))
    buttonN4.grid(row=2, column=0)
    buttonN5 = tkinter.Button(new_window, text="5", command = lambda:button_pressed7('5'))
    buttonN5.grid(row=2, column=1)
    buttonN6 = tkinter.Button(new_window, text="6", command = lambda:button_pressed7('6'))
    buttonN6.grid(row=2, column=2)
     
    buttonN1 = tkinter.Button(new_window, text="1", command = lambda:button_pressed7('1'))
    buttonN1.grid(row=3, column=0)
    buttonN2 = tkinter.Button(new_window, text="2", command = lambda:button_pressed7('2'))
    buttonN2.grid(row=3, column=1)
    buttonN3 = tkinter.Button(new_window, text="3", command = lambda:button_pressed7('3'))
    buttonN3.grid(row=3, column=2)
    buttonEnter=tkinter.Button(new_window, text="Enter",command= new_window.destroy)
    buttonEnter.grid(row=3,column=4)

    button_backspace=tkinter.Button(new_window, text='BS',command=backspace_7)
    button_backspace.grid(row=2, column=4)

    new_window.mainloop()

new_window_button = tkinter.Button(FoodInfoWindow, text="수분입력", command=ent7number)
new_window_button.place(x=590, y=220)
#####################################################################################################
t2=Thread(target=eating)
t2.start()

timesetter.mainloop()
window.mainloop()