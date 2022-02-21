from django.shortcuts import render
from django.http import HttpResponse
import copy
from .models import event

import mysql.connector
from mysql.connector import Error

import hashlib

#Global variables
email=None
name=None
eves = None
max_seats = 6  # Number of seats in the stadium
max_seat_id = None

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='stadium',
                                         user='root',
                                         password='Qwertyuiop@12')
    if connection.is_connected():
        cursor = connection.cursor()
        
except Error as e:
    print("Error while connecting to MySQL", e)




def signin(request):
    return render(request, 'login.html', {'welcome1': '', 'welcome2': 'User Login'})


def verify_user(request):
    global email 
    global name
    email= request.POST['mail']
    pwd= request.POST['pwd']
    cursor.execute("select email from customer")
    m=cursor.fetchall()
    mails=[]
    for i in  range(len(m)):
         mails.append(str(m[i][0]))
    if email not in mails:
        return render(request, 'login.html', {'welcome1': 'Incorrect Email.', 'welcome2': 'User Login'})
    cursor.execute("select password from customer where email=%s",(email,))
    result = str(cursor.fetchall()[0][0])
    if result ==hashlib.md5(pwd.encode()).hexdigest():
        cursor.execute("select name  from customer where email=%s",(email,))
        name=str(cursor.fetchall()[0][0])
        return render(request, 'index_login.html', {'name': name})  #the homepage again with the username specified
    else:
        return render(request, 'login.html', {'welcome1': 'Incorrect Password', 'welcome2': 'User Login'})


def signup(request):
    return render(request, 'signup_index.html',{'welcome1':'New Account ?', 'e1': "", 'e2': "", 'e3': "", 'e4': ""})

def store_user(request):
    global name
    names = request.POST['name']
    global email 
    email= request.POST['mail']
    phn = request.POST['phn']
    pwd= request.POST['pwd']
    e1 = ""
    e2 = ""
    e3 = ""
    e4 = ""
    flag = 0

    if len(names) == 0:
        flag = 1
        e1 = "Enter Your Name"
    if len(phn) < 10:
        flag = 1
        e2 = "Enter Valid Phone Number"
    if len(email) == 0:
        flag = 1
        e3 = "Enter Valid Email"
    if len(pwd) < 8:
        flag = 1
        e4 = "Password should be greater than 8 characters"
    if flag == 1:
        return render(request, 'signup_index.html',
                      {'welcome1': 'New Account ?', 'e1': e1, 'e2': e2, 'e3': e3, 'e4': e4})

    cursor.execute("select email from customer")
    m=cursor.fetchall()
    mails=[]
    for i in  range(len(m)):
        mails.append(str(m[i][0]))
    if email in mails:
        return render(request,'signup_index.html',{'welcome1':'User already exist. Please login/enter another email.'})
    else:
        cursor.execute("insert into customer  (`Name`,`password`,email,contact_no) values (%s,%s,%s,%s)", (names, hashlib.md5(pwd.encode()).hexdigest(), email, phn))
        connection.commit()
        name=names
        return render(request,'index_login.html',{'name':name})
    

def info(request):
    cursor.execute("select name  from customer where email=%s",(email,))
    name=str(cursor.fetchall()[0][0])
    cursor.execute("select contact_no  from customer where email=%s",(email,))
    phone=str(cursor.fetchall()[0][0])
    return render(request,'info.html',{'name':name,'mail':email,'phone':phone})


def update_index(request):
    return render(request,'update.html')

def update_pwdindex(request):
    return render(request,'updatepwd.html')


def update(request):
    flag = 0
    global email
    pwd= request.POST['pwd']
    cursor.execute('select password from customer where email=%s',(email,))
    pas=str(cursor.fetchall()[0][0])
    phn= request.POST['phn']
    mail= request.POST['mail']
    if pas==hashlib.md5(pwd.encode()).hexdigest():
        if len(phn) < 10:
            flag = 1
            return render(request,'update.html',{'e1':"Enter Valid Phone Number"})
        if len(mail)==0 :
            flag = 1
            return render(request,'update.html',{'e2':"Enter Valid Email"})

        cursor.execute('''update customer
                      set contact_no=%s
                      where email=%s;''',(phn,email))

        
        cursor.execute('''update customer
                      set email=%s
                      where email=%s;''',(mail,email))
                      
        email=mail
        connection.commit()
        cursor.execute("select name  from customer where email=%s",(email,))
        name=str(cursor.fetchall()[0][0])
        return render(request,'index_Login.html',{'name':name})
    else:
        return render(request,'update.html',{'e3':'Incorrect password. Try again.'})




def update_pwd(request):
    global email
    op= request.POST['op']
    np= request.POST['np']
    cursor.execute('select password from customer where email=%s',(email,))
    pas=str(cursor.fetchall()[0][0])
    if pas==hashlib.md5(op.encode()).hexdigest():
        if len(np)<8:
            return render(request,'updatepwd.html',{'e2':'Password should be greater than 8 characters'})
        cursor.execute('''update customer
                      set password=%s
                      where email=%s;''',(hashlib.md5(np.encode()).hexdigest(),email))
        connection.commit()
        return render(request,'index_Login.html',{'name': name})
    else:
        return render(request,'updatepwd.html',{'e1':'Wrong password.'})



def home(request):
    return render(request,'index_Login.html',{'name':name})


def records(request):

    #SQL QUERY TO FETCH RECORDS OF  A PARTICULAR CUSTOMER
    cursor.execute('''select distinct (e.ev_id),e.ev_name,e.date,e.time,e.price,a.seat_id
               from event e,attends a
               where (e.ev_id ,a.seat_id) in
               (select a.ev_id,a.seat_id
               from attends a
               where a.cust_id in(
               (select c.cust_id
                from customer c
                where c.email = %s)))
                order by date
                desc limit 10''',(email,))


    e=cursor.fetchall()

    objects = []

    #list of objects of class event 
    for i in range(len(e)):
         objects.append(event())



    for i in range(len(e)):
        objects[i].ev_id=e[i][0]
        objects[i].ev_name =e[i][1]
        objects[i].date =e[i][2]
        objects[i].time = e[i][3]
        objects[i].price=e[i][4]
        objects[i].seat=e[i][5]

    events=[]
    for i in range(len(objects)):
        events.append(objects[i])

    return render(request,'record.html',{'name':name,'events':events})

def contact(request):
    #SQL QUERY TO FETCH RECORDS OF  A PARTICULAR CUSTOMER
    cursor.execute('''select d.Dname,e.`Name`,e.contact_no,e.email
                        from department d , employee e
                        where d.mgrid=e.emp_id;''')


    e=cursor.fetchall()

    objects = []

    #list of objects of class event 
    for i in range(len(e)):
         objects.append(event())



    for i in range(len(e)):
        objects[i].Dname=e[i][0]
        objects[i].mgrname =e[i][1]
        objects[i].phone=e[i][2]
        objects[i].mail= e[i][3]

    depts=[]
    for i in range(len(objects)):
        depts.append(objects[i])

    return render(request,'contact.html',{'depts':depts})

def events(request):
    # SQL QUERY TO FETCH ALL THE UPCOMING EVENTS
    cursor.execute("select * from event e where e.date>=curdate() order by e.date asc")
    global eves
    eves = []
    e = cursor.fetchall()

    objects = []

    # list of objects of class event
    for i in range(len(e)):
        objects.append(event())

    for i in range(len(e)):
        objects[i].ev_id = e[i][0]
        objects[i].ev_name = e[i][1]
        objects[i].date = e[i][2]
        objects[i].time = e[i][3]
        objects[i].price = e[i][6]

    for i in range(len(objects)):
        eves.append(objects[i])

    return render(request, 'events.html', {'events': eves})


def select_event(request):
    return render(request, 'select_event.html', {'events': eves, 'welcome2': 'Seat Booking'})



def login_book(request):
    global email
    global name
    email = request.POST['mail']
    pwd = request.POST['pwd']
    global sel_event
    sel_event = request.POST['selected_event']
    global num_seats
    num_seats = (request.POST['NumberOfSeats'])
    global max_seat_id
    book_event = None

    cursor.execute("select email from customer")
    m = cursor.fetchall()

    mails = []
    for i in range(len(m)):
        mails.append(str(m[i][0]))

    if email not in mails:
        return render(request, 'select_event.html',
                      {'welcome1': 'You Need To Sign Up First', 'welcome2': 'Seat Booking',
                       'welcome3': '', 'events': eves})

    cursor.execute("select `password` from customer where email=%s",(email,))
    result = str(cursor.fetchall()[0][0])
    cursor.execute("select seats_req from `event` where ev_name=%s",(sel_event,))
    max_seats = int(cursor.fetchall()[0][0])

    if result ==hashlib.md5(pwd.encode()).hexdigest():
        cursor.execute("select name  from customer where email=%s",(email,))
        name=str(cursor.fetchall()[0][0])

        for eve in eves:
            if eve.ev_name == sel_event:
                book_event = eve


        if len(num_seats) == 0:
            return render(request, 'select_event.html', {'welcome1': '', 'welcome2': 'Seat Booking',
                                                             'welcome3': 'Enter Number of Seats', 'events': eves})
        num_seats = int(num_seats)
            # find max_seat_id first
        cursor.execute(
                "select max(seat_id) from attends where ev_id = (select ev_id from event where ev_name = %s)",
                (sel_event,))

        max_seat_id = int(cursor.fetchall()[0][0])
        if max_seats - max_seat_id == 0:
            return render(request, 'select_event.html',
                              {'welcome1': 'No Seats Available for {}'.format(sel_event),
                               'welcome2': 'Seat Booking',
                               'welcome3': '', 'events': eves})

        if max_seat_id + num_seats > max_seats:
            return render(request, 'select_event.html', {'welcome1': 'Only {} Seats Available for {}'.format(max_seats - max_seat_id, sel_event), 'welcome2': 'Seat Booking',
                                                             'welcome3': '', 'events': eves})
        return render(request, 'payment.html',
                          {'name': name,
                           'seats': num_seats,
                           'date': book_event.date,
                           'time': book_event.time,
                           'total': num_seats * book_event.price,
                           'evname': sel_event
                           }
                          )  # the homepage again with the username specified

    else:
        return render(request, 'select_event.html',
                      {'welcome1': 'Incorrect  Password', 'welcome2': 'Seat Booking',
                       'welcome3': '', 'events': eves})
    
    


def booked(request):
    book_event = None
    for eve in eves:
        if eve.ev_name == sel_event:
            book_event = eve


    cursor.execute("select cust_id from customer where email = %s", (email,))
    cust_id = cursor.fetchall()[0][0]

    booked_events = []
    for i in range(num_seats):
        booked_events = booked_events + [copy.copy(book_event)]
        booked_events[i].seat = max_seat_id+i+1

    for i in range(num_seats):
        cursor.execute("insert into attends  (`cust_id`,`ev_id`,`seat_id`) values (%s,%s,%s)",
                       (cust_id, booked_events[i].ev_id, max_seat_id + i + 1))

    connection.commit()

    cursor.execute("select name from customer where email=%s", (email,))
    name = str(cursor.fetchall()[0][0])

    #ev_name , date , time , e_price, seat_id

    return render(request, 'booked.html', {'name': name, 'events': booked_events})