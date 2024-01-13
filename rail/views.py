
from random import randint
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail

from datetime import datetime

from time import sleep
from rail.models import booking_details, history, train, user_info

#some utility functions------------------------------------------------------
def otp(digits):
    result=''
    for i in range(digits):
        ott=randint(0,9)
        result=result+str(ott)
    return result

def date():
    now=datetime.now()
    return now.strftime('%d/%m/%y %H:%M:%S')

def pass_generator(length):
    chars='abcdefghijklmnopqrstuvwxyz1234567890!@#&ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    password=''
    for i in range(length):
        password+=random.choice(chars)
    return password


#-------------------------------------------------------------------------------



# Create your views here.
def signin(request):
    user=request.POST.get('username')
    passw=request.POST.get('password')
    email=request.POST.get('email')
    #DUPLICATE ENTRY-----------------------------------------
    data=user_info.objects.filter(username=user)
    if len(data)>0:
        return JsonResponse("USER ALREADY EXISTS",safe=False)
    #--------------------------------------------------------------
    ot=otp(4)
    send_mail('mail regarding otp verification','The otp for your email verification is::'+ot+'.Kindly do not share this with anyone else.','sendermail33@gmail.com',[email])
    object=user_info(username=user,password=passw,email=email,otp=ot)
    object.save()
    return JsonResponse('RECORDS HAVE BEEN INSERTED SUCCESSFULLY',safe=False)

def email_verification(request):
    user=request.POST.get('username')
    otp_u=int(request.POST.get('otp'))
    data=user_info.objects.filter(username=user)
    if len(data)==0:
        return JsonResponse("user not found",safe=False)
    otp_d=int(data[0].otp)
    if otp_u==otp_d:
        user_info.objects.filter(username=user).update(is_verified=1)
        return HttpResponse("EMAIL VERIFIED SUCCESSFULLY")
    else:
        return JsonResponse("WRONG OTP",safe=False)
    
def login(request):
    user=request.POST.get('username')
    passw=request.POST.get('password')
    data=user_info.objects.filter(username=user,password=passw)
    
    if len(data)==0:
        return JsonResponse('BAD CREDENTIALS',safe=False)
    verification_status=data[0].is_verified
    if verification_status==0:
        return JsonResponse('PLEASE VERIFY YOUR EMAIL FIRST!!',safe=False)
    current=date()
    
    user_info.objects.filter(username=user,password=passw).update(last_login=current)

    return render(request,'index.html')
    # return JsonResponse('welcome '+user,safe=False)

def demo_login(request):
    user=request.POST.get('username')
    passw=request.POST.get('password')
    data=user_info.objects.filter(username=user,password=passw)
    
    if len(data)==0:
        return 0
    verification_status=data[0].is_verified
    if verification_status==0:
        return 0
    # updating last_login time in database-------------------------------------
    current=date()
    user_info.objects.filter(username=user,password=passw).update(last_login=current)
    
    #---------------------------------------------------------------------------
    return 1
    

def forget_password(request):
    username=request.POST.get('username')
    
    data=user_info.objects.filter(username=username)
    if len(data)==0:
        return JsonResponse('USER NOT FOUND',safe=False)
    new_password=pass_generator(6)
    data1=user_info.objects.filter(username=username)
    em=data[0].email
    user_info.objects.filter(username=username).update(password=new_password)
    send_mail('Indian Rail','Your New password is '+ str(new_password)+' Kindly Login in with this password. You are requested to reset your password as soon as possible for security reasons\n Thank You','sendermail33@gmail.com',[em])
    return HttpResponse('PASSWORD UPDATED SUCCESSFULLY, KINDLY CHECK YOUR EMAIL FOR NEW PASSWORD.')

def reset_password(request):
    output=demo_login(request)
    if output==0:
        return JsonResponse("ENETR VALID USERNAME OR PASSWORD",safe=False)
    new_password=request.POST.get('new_pass')
    user=request.POST.get("username")
    user_info.objects.filter(username=user).update(password=new_password)
    return HttpResponse("PASSWORD UPDATED SUCCESSFULLY")





def train_info(request):
    train_nm=request.GET.get('name')
    train_no=request.GET.get('no')
    tickets=request.GET.get('tickets')
    coach=request.GET.get('coach')
    from_st=request.GET.get('from')
    to_st=request.GET.get('to')
    data=train.objects.filter(train_no=train_no)
    if len(data)==0:

        object=train(train_name=train_nm,train_no=train_no,no_tickets=tickets,coach=coach,from_st=from_st,to_st=to_st)
        object.save()
        return JsonResponse('RECORDS SAVED',safe=False)
    else:
        
        tnm=data[0].train_name
        if tnm!=train_nm:
            return JsonResponse('TWO TRAINS CAN NOT HAVE SAME TRAIN NUMBER',safe=False)
        
        else:
            # f_st=data[0].from_st
            # t_st=data[0].to_st
            # coach1=data[0].coach
            for i in range(len(data)):
                
                f_st=data[i].from_st
                t_st=data[i].to_st
                coach1=data[i].coach
                print(f_st,t_st)
                if ((f_st==from_st) and (t_st==to_st)):
                    if coach1==coach:
                        return HttpResponse('THAT PARTICULAR RECORD HAS ALREADY BEEN ADDED')
                    else:
                        object=train(train_name=train_nm,train_no=train_no,no_tickets=tickets,coach=coach,from_st=from_st,to_st=to_st)
                        object.save()
                        return JsonResponse('RECORDS SAVED562',safe=False)
                else:
                    object=train(train_name=train_nm,train_no=train_no,no_tickets=tickets,coach=coach,from_st=from_st,to_st=to_st)
                    object.save()
                    return JsonResponse('RECORDS SAVED123',safe=False)
        
def check_seat_availability(request):
    train_no=request.GET.get('no')
    coach=request.GET.get('coach')
    from_st=request.GET.get('from')
    to_st=request.GET.get('to')
    data=train.objects.filter(train_no=train_no)
    if len(data)==0:
        return JsonResponse("NO RECORD OF TRAIN NO "+str(train_no)+" IS AVAILABLE",safe=False)
    data1=train.objects.filter(train_no=train_no,coach=coach,from_st=from_st,to_st=to_st)
    if len(data1)==0:
        return JsonResponse("NO SUCH RECORD FOUND!  KINDLY CHECK STARTING AND TERMINAL STATIONS OF YOUR JOURNEY OR THE SELECTED COACH",safe=False)
    nt=data1[0].no_tickets
    return HttpResponse(nt)


    

def booking_seats(request):
    output=demo_login(request)
    print(output)
    if output==0:
        return JsonResponse('LOGIN FAILED',safe=False)
    
    JsonResponse('LOGIN SUCCESSFULL',safe=False)
    
    
    username=request.GET.get('username')
    #email=request.GET.get('email')
    train_no=request.GET.get('no')
    coach=request.GET.get('coach')
    from_st=request.GET.get('from')
    to_st=request.GET.get('to')

    
    
    data=train.objects.filter(train_no=train_no)
    if len(data)==0:
        return JsonResponse("NO RECORD OF TRAIN NO "+str(train_no)+" IS AVAILABLE",safe=False)
    data1=train.objects.filter(train_no=train_no,coach=coach,from_st=from_st,to_st=to_st)
    if len(data1)==0:
        return JsonResponse("NO SUCH RECORD FOUND!  KINDLY CHECK STARTING AND TERMINAL STATIONS OF YOUR JOURNEY OR THE SELECTED COACH",safe=False)
    nt=int(data1[0].no_tickets)
    
    passenger_name=request.GET.get("passenger names(separated with ',')")
    list_passenger=passenger_name.split(',')


    req_seats=len(list_passenger)
    if req_seats>nt:
        return JsonResponse("SORRY THE NO OF SEATS ARE NOT AVAILABLE!!",safe=False)
    new_seats=nt-req_seats

    #fetching email of logged in user------------------------------------------
    data2=user_info.objects.filter(username=username)
    em=data2[0].email

    #--------------------------------------------------------------------------
    # history part--------------------------------------------------------------
    object=history(username=username,email=em,train_no=train_no,from_st=from_st,to_st=to_st,no_tickets=req_seats,coach=coach)
    object.save()

    #-----------------------------------------------------------------------
    # passenger_details ---------------------------------------------------
    
    # data=booking_details.objects.all()
    # list=[]
    # for i in range(len(data)):
    #     list.append(data[i].seat_no)
    # print(list)
    def fun2():
        def sleeper_fun():
            coach_list_sleeper=['s1','s2','s3']
            temp_list=[]
            temp_coach=random.choice(coach_list_sleeper)
            
            data=booking_details.objects.filter(coach_no=temp_coach)
            print(len(data))
            if len(data)==0:
                print('no data buddy in the randomly selected coach')
                pass
            else:   
                for i in range(len(data)):
                    temp_list.append(data[i].seat_no)
                    print(data[i].seat_no)
            print(temp_list)
            return temp_list,temp_coach
        
        def ac1_fun():
            coach_list_ac1=['h1','h2','h3']
            
            temp_list=[]
            temp_coach=random.choice(coach_list_ac1)
            
            data=booking_details.objects.filter(coach_no=temp_coach)
            print(len(data))
            if len(data)==0:
                print('no data buddy in the randomly selected coach')
                pass
            else:   
                for i in range(len(data)):
                    temp_list.append(data[i].seat_no)
                    print(data[i].seat_no)
            print(temp_list)
            return temp_list,temp_coach
        
        def ac2_fun():
            coach_list_ac2=['k1','k2','k3']
            temp_list=[]
            temp_coach=random.choice(coach_list_ac2)
            
            data=booking_details.objects.filter(coach_no=temp_coach)
            print(len(data))
            if len(data)==0:
                print('no data buddy in the randomly selected coach')
                pass
            else:   
                for i in range(len(data)):
                    temp_list.append(data[i].seat_no)
                    print(data[i].seat_no)
            print(temp_list)
            return temp_list,temp_coach
        
        def ac3_fun():
            
            coach_list_ac3=['b1','b2','b3']
            temp_list=[]
            temp_coach=random.choice(coach_list_ac3)
            
            data=booking_details.objects.filter(coach_no=temp_coach)
            print(len(data))
            if len(data)==0:
                print('no data buddy in the randomly selected coach')
                pass
            else:   
                for i in range(len(data)):
                    temp_list.append(data[i].seat_no)
                    print(data[i].seat_no)
            print(temp_list)
            return temp_list,temp_coach
        if coach=='sleeper':
            output_list,output_coach_no=sleeper_fun()
            return output_list,output_coach_no
        elif coach=='ac1':
            output_list,output_coach_no=ac1_fun()
            return output_list,output_coach_no
        elif coach=='ac2':
            output_list,output_coach_no=ac2_fun()
            return output_list,output_coach_no
        elif coach=='ac3':
            output_list,output_coach_no=ac3_fun()
            return output_list,output_coach_no
    list,coach_no=fun2()
    # function for assigning unique seat no to each passenger-----------------
    def fun1():
            seat_assigned=random.randint(1,81)
            if seat_assigned in list:
                fun1()
            else:
                list.append(seat_assigned)
                return seat_assigned
    #-----------------------------------------------------------------------
    #just for reference----------------------------------------    
    coach_list_sleeper=['s1','s2','s3']
    coach_list_ac1=['h1','h2','h3']
    coach_list_ac2=['k1','k2','k3']
    coach_list_ac3=['b1','b2','b3']
    #--------------------------------------------------------

    for i in list_passenger:
        output_seat=fun1()
        pnr_no=int(otp(10))
        object1=booking_details(username=username,train_no=train_no,pnr_no=pnr_no,passenger_name=i,seat_no=output_seat,coach_no=coach_no)
        object1.save()
    #--------------------------------------------------------------------------
    #seat update part----------------------------------------------------------
    train.objects.filter(train_no=train_no,coach=coach,from_st=from_st,to_st=to_st).update(no_tickets=new_seats)
    #--------------------------------------------------------------------------
    #sending confirmation mail-------------------------------------------------
    send_mail('Regarding Booking Confirmation','YOUR '+str(req_seats)+' SEATS FROM '+str(from_st)+' TO '+str(to_st)+' HAS BEEN BOOKED IN '+str(coach)+' COACH IN TRAIN NO'+str(train_no),'sendermail33@gmail.com',[em])
    #--------------------------------------------------------------------------
    return HttpResponse('YOUR '+str(req_seats)+' SEATS FROM '+str(from_st)+' TO '+str(to_st)+' HAS BEEN BOOKED IN '+str(coach)+' COACH IN TRAIN NO '+str(train_no))
    
   

def seat_history(request):
    username=request.GET.get('username')
    data=history.objects.filter(username=username)
    if len(data)==0:
        return JsonResponse('USER HAS NOT BOOKED ANY TICKETS YET',safe=False)

    j={}
    for i in range(len(data)):
        us=data[i].username
        em=data[i].email
        fr=data[i].from_st
        to=data[i].to_st
        tno=data[i].train_no
        ch=data[i].coach
        ntk=data[i].no_tickets
        d={'username':us,'email':em,'from_st':fr,'to_st':to,'train_no':tno,'coach':ch,'no_tickets':ntk}
        j[i+1]=d
        
    return JsonResponse(j)
    
def testing(request):
    coach=request.GET.get('coach')
    def fun2():
        coach_list_sleeper=['s1','s2','s3']
        temp_list=[]
        def fun3():
            temp_coach=random.choice(coach_list_sleeper)
            return temp_coach
        temp_coach=fun3()
        data=booking_details.objects.filter(coach_no=temp_coach)
        print(len(data))
        if len(data)>80:
            temp_coach=fun3()
        if len(data)<=0:
            print('no data buddy in the randomly selected coach')
            print(f'no data and list is ::{temp_list} and selected coach is::{temp_coach}')
        else:   
            for i in range(len(data)):
                temp_list.append(data[i].seat_no)
                print(data[i].seat_no)
        print(temp_list)
        return temp_list

    if coach=='sleeper':
        output=fun2()
        return HttpResponse(output)
    else:
        return JsonResponse('enter valid coach for testing',safe=False)




    


