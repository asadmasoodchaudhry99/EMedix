from re import template
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt # new
#from django.views.generic.base import TemplateView
from django.conf import settings # new
import stripe
from random import randint
import datetime
from twilio.jwt.access_token import AccessToken
from   twilio.jwt.access_token.grants import VideoGrant

from google.cloud import storage

#from django.core.files.storage import FileSystemStorage

# Create your views here.

#def testemail(request):
 #   testemail = EmailMessage(subject='Test',body="Test Email",to=['asadmchaudhry0@gmail.com'])
  #  testemail.send()

def home(request):
    context = {}
    if request.user.is_authenticated:
        context['userdetails'] = userinfo.objects.get(user = request.user)
    return render(request, 'EMedix_App/mainpage.html',context)
def login(request):
    template = 'EMedix_App/login.html'
    context = {}
    if request.method == 'POST':
        try:
            userobj = User.objects.get(username=request.POST['username-login'])
            if userobj.check_password(request.POST['password-login']):
                auth.login(request,userobj)
                usertypeobj = userinfo.objects.get(user = request.user)
                otp = 1000*randint(1,9) + 100*randint(1,9) + 10*randint(1,9) + randint(1,9)
                usertypeobj.otp = otp
                usertypeobj.save()
                otpemail = EmailMessage(subject='One-Time-Password',body="Your One Time Password is: {}".format(usertypeobj.otp),to=[request.user.email])
                otpemail.send()
                return redirect('/loginverification')
            else:
                context['message'] = 'Invalid Credentials'
                #wrong password

        except:
            context['message'] = 'Invalid Credentials'
            #wrong username 
    return render(request,template,context)

@login_required(login_url='/login')
def loginverification(request):
    context = {}
    usertypeobj = userinfo.objects.get(user = request.user)
    if usertypeobj.info_filled == True:
        template = 'EMedix_App/otp.html'
        context['message'] = ''
        if request.method == 'POST':
            if usertypeobj.otp == int(request.POST['otp']):
                usertypeobj.otp_status = True
                if usertypeobj.user_type == 'patient':
                    return redirect('/PatientDashboard')
                elif usertypeobj.user_type == 'doctor':
                    return redirect('/DoctorDashboard')
                else:
                    return redirect('/ClinicDashboard')
            else:
                context['message'] = 'Incorrect OTP Entered'
    else:
        if usertypeobj.user_type == 'patient':
            return redirect('/PaitentAccountDetails') 
        elif usertypeobj.user_type == 'doctor':
            return redirect('/DoctorAccountDetails')
        elif usertypeobj.user_type == 'clinic':
            return redirect('/clinicAccountdetails')
    return render(request,template,context)

@login_required(login_url='/login')
def resendOTP(request):
    usertypeobj = userinfo.objects.get(user = request.user)
    otp = 1000*randint(0,9) + 100*randint(0,9) + 10*randint(0,9) + randint(0,9)
    usertypeobj.otp = otp
    usertypeobj.save()
    otpemail = EmailMessage(subject='One-Time-Password',body="Your One Time Password is: {}".format(usertypeobj.otp),to=[request.user.email])
    otpemail.send()
    return redirect('/loginverification')

def signup(request):
    template = 'EMedix_App/signup.html'
    context = {
     
    }
    if request.method == 'POST':
        try:
            Usercheck = User.objects.get(username = request.POST['username-signup'])
            context['message'] = 'User Already Exists'
        except:    
            userobj = User()
            userobj.username = request.POST['username-signup']
            userobj.save()
            userobj.set_password(request.POST['password-signup'])
            userobj.save()
            infoobj = userinfo()
            infoobj.user = userobj
            infoobj.user_type = request.POST['signup-type']
            infoobj.save()
            auth.login(request, userobj)
            if(infoobj.user_type == 'patient'):
                return redirect('/PaitentAccountDetails')
            elif(infoobj.user_type == 'doctor'):
                return redirect('/DoctorAccountDetails')
            else:
                return redirect('/clinicAccountdetails')
    return render(request,template,context)

@login_required(login_url='/login')
def logout(request):
    usertypeobj = userinfo.objects.filter(user = request.user)[0]
    usertypeobj.otp_status = False
    usertypeobj.save()
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/login')
def UpdateProfilePatient(request):
    template = 'EMedix_App/updateProfile_patient.html'
    context = {}
    context['patientdetails'] = patient.objects.filter(user = request.user)[0]
    if request.method == 'POST':
        patientobj =  patient.objects.filter(user = request.user)
        patientobj.phone_number = request.POST['pnumber']
        patientobj.save()
        patientobj.age = request.POST['age']
        patientobj.save()
        patientobj.country = request.POST['country']
        patientobj.save()
        patientobj.state = request.POST['state']
        patientobj.save()
        patientobj.city = request.POST['city']
        patientobj.save()
        patientobj.address = request.POST['address']
        patientobj.save()
        return redirect('/PatientDashboard')
        
    return render(request,template,context)

@login_required(login_url='/login')
def patient_details(request):
    template = "EMedix_App/accountDetails_Patient.html"
    context = {}
    if request.method == 'POST':
        userobj = request.user
        usertypeobj = userinfo.objects.get(user = request.user)
        usertypeobj.info_filled = True
        usertypeobj.save()
        userobj.save()
        userobj.first_name = request.POST['fname']
        userobj.save()
        userobj.last_name = request.POST['lname']
        userobj.save()
        userobj.email = request.POST['email']    
        userobj.save()
        patientobj = patient()
        patientobj.user = userobj
        patientobj.phone_number = request.POST['pnumber']
        patientobj.save()
        patientobj.age = request.POST['age']
        patientobj.save()
        patientobj.country = request.POST['country']
        patientobj.save()
        patientobj.state = request.POST['state']
        patientobj.save()
        patientobj.city = request.POST['city']
        patientobj.save()
        patientobj.address = request.POST['address']
        patientobj.save()
        return redirect('/PatientDashboard')
        
        
    return render(request,template,context)

@login_required(login_url='/login')
def UpdateProfileDoctor(request):
    template = 'EMedix_App/updateProfile_doctor.html'
    context = {}
    context['doctordetails'] = doctor.objects.filter(user = request.user)[0]
    if request.method == 'POST':
        doctorobj =  doctor.objects.get(user = request.user)
        doctorobj.phone_number = request.POST['pnumber']
        doctorobj.save()
        doctorobj.age = request.POST['age']
        doctorobj.save()
        doctorobj.consultationcharges = request.POST['consultation_charges']
        doctorobj.save()
        doctorobj.country = request.POST['country']
        doctorobj.save()
        doctorobj.state = request.POST['state']
        doctorobj.save()
        doctorobj.city = request.POST['city']
        doctorobj.save()
        doctorobj.address = request.POST['address']
        doctorobj.save()
        return redirect('/DoctorDashboard')
        
        
    return render(request,template,context)

@login_required(login_url='/login')
def doctor_details(request):
    template = "EMedix_App/accountDetails_Doctor.html"
    context = {}
    if request.method == 'POST':
        userobj = request.user
        usertypeobj = userinfo.objects.get(user = request.user)
        usertypeobj.info_filled = True
        usertypeobj.save()
        userobj.first_name = request.POST['fname']
        userobj.save()
        userobj.last_name = request.POST['lname']
        userobj.save()
        userobj.email = request.POST['email']    
        userobj.save()
        doctorobj = doctor()
        doctorobj.user = userobj
        doctorobj.phone_number = request.POST['pnumber']
        doctorobj.save()
        doctorobj.age = request.POST['age']
        doctorobj.save()
        doctorobj.qualification = request.POST['qualification']
        doctorobj.save()
        doctorobj.department = request.POST['department']
        doctorobj.save()
        doctorobj.consultationcharges = request.POST['consultation_charges']
        doctorobj.save()
        doctorobj.country = request.POST['country']
        doctorobj.save()
        doctorobj.state = request.POST['state']
        doctorobj.save()
        doctorobj.city = request.POST['city']
        doctorobj.save()
        doctorobj.address = request.POST['address']
        doctorobj.save()
        return redirect('/DoctorDashboard')
        
        
    return render(request,template,context)

@login_required(login_url='/login')
def clinic_details(request):
    context = {}
    template = 'EMedix_App/accountDetails_Clinic.html'
    if request.method == 'POST':
        userobj = request.user
        usertypeobj = userinfo.objects.get(user = request.user)
        usertypeobj.info_filled = True
        usertypeobj.save()
        userobj.save()
        userobj.first_name = request.POST['clinic_name']
        userobj.save()
        userobj.last_name = request.POST['poc_name']
        userobj.save()
        userobj.email = request.POST['email']    
        userobj.save()
        clinicobj = clinic()
        clinicobj.user = userobj
        clinicobj.phone_number = request.POST['pnumber']
        clinicobj.save()
        clinicobj.registration_number = request.POST['registration_number']
        clinicobj.save()
        clinicobj.country = request.POST['country']
        clinicobj.save()
        clinicobj.state = request.POST['state']
        clinicobj.save()
        clinicobj.city = request.POST['city']
        clinicobj.save()
        clinicobj.address = request.POST['address']
        clinicobj.save()
        return redirect('/ClinicDashboard')
        
        
    return render(request,template,context)


@login_required(login_url='/login')
def ClinicDashboard(request):
    context={}
    template = 'EMedix_App/ClinicDashboard.html'
    if request.method == 'POST':
        obj = clinic.objects.get(user=request.user)
        obj.doctors.add(doctor.objects.get(pk=request.POST['doc']))
        obj.save()
    context['objs'] = doctor.objects.all()
    
    tot_earn = 0
    clinic_docs = clinic.objects.filter(user = request.user)[0].doctors.all()
    bobjs = BookingAppointment.objects.all()
    templist = []
    for i in bobjs:
        if i.doctor in clinic_docs:
            templist.append(i)
            tot_earn += i.doctor.consultationcharges
    context['objs2'] = clinic_docs
    context['tot'] = len(clinic_docs)
    context['totalearnings'] = tot_earn
    context['monthlydata'] = monthlyearnings(templist)
    context['currentmonthearning'] = context['monthlydata'][int(datetime.date.today().month)]
    return render(request,template, context )



@login_required(login_url='/login')
def PatientDashboard(request):
    objs = BookingAppointment.objects.filter(Paymentstatus = False)
    for i in objs:
        i.delete()
    context={}
    template = 'EMedix_App/PatientDashboard.html'
    bookingdata = {}
    doctorinformation = doctor.objects.all()
    for i in doctorinformation:
        if i.department in bookingdata.keys():
            bookingdata[i.department].append(i)
        else:
            bookingdata[i.department] = [i]

    
    context['departments'] = bookingdata.keys()
    context['doctordata'] = bookingdata
    context['bookinglist'] = BookingAppointment.objects.filter(patient__user = request.user)
    context['totalbookings'] = len(context['bookinglist'])
    context['upcomingbookings'] = len(BookingAppointment.objects.filter(patient__user = request.user, consultation_status = False ))
    
    return render(request,template, context )

def monthlyearnings(earnings):
    currentyear = datetime.date.today().year
    earningdata = {1 : 0,
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    7 : 0,
    8 : 0,
    9 : 0,
    10 : 0,
    11 : 0,
    12 : 0
    
    
    }
    for i in earnings:
        if int(i.timing.date().year) == int(currentyear):
            if i.timing.date().month in earningdata.keys():
                earningdata[int(i.timing.date().month)] += i.doctor.consultationcharges

    return earningdata


    


@login_required(login_url='/login') 
def DoctorDashboard(request):
    objs = BookingAppointment.objects.filter(Paymentstatus = False)
    for i in objs:
        i.delete()
    context={}
    template = 'EMedix_App/DoctorDashboard.html'
    context['bookinglist'] = BookingAppointment.objects.filter(doctor__user = request.user)
    context['upcomingbookings'] = len( BookingAppointment.objects.filter(doctor__user = request.user, consultation_status = False ))
    try:
        context['totalearnings'] = len(context['bookinglist'])*context['bookinglist'][0].doctor.consultationcharges
    except:
        context['totalearnings'] = '0' 
    context['monthlydata'] = monthlyearnings(context['bookinglist'])
    currentmonth = int(datetime.date.today().month)
    context['currentmonthearning'] = context['monthlydata'][currentmonth]
    print(context['monthlydata'])
    if request.method == 'POST':
        a = request.POST['id']
        appointmentobj = BookingAppointment.objects.get(pk = int(a))
        appointmentobj.prescription = request.POST['prescription']
        appointmentobj.prescription_status = True
        appointmentobj.save()

    return render(request,template,context )


def ConsultationCharges(request, doctorid):
    doctorobj = doctor.objects.get(pk =doctorid)
    return HttpResponse(doctorobj.consultationcharges)


@login_required(login_url='/login') 
def book_appointment(request):

    if request.method == 'POST':
        bookingobj = BookingAppointment()
        bookingobj.patient = patient.objects.filter(user = request.user)[0]
        bookingobj.doctor = doctor.objects.get(pk = int(request.POST['doctorname-' + request.POST['departmentname']]))
        bookingobj.bookingtype = request.POST['bookingtype']
        bookingobj.explaination = request.POST['explaination']
        bookingobj.timing = request.POST['timeofbooking']
        bookingobj.patient.booking_count += 1
        bookingobj.doctor.booking_count += 1
        bookingobj.save()

        
        return redirect('/create-checkout-session?payment_id={}'.format(bookingobj.id))
    return redirect('/PatientDashboard')




@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey' : settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe = False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        payment_id = request.GET['payment_id']
        domain_url = 'https://e-medix.uc.r.appspot.com/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            bookingObj = BookingAppointment.objects.filter(pk = payment_id)[0]
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'error/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': bookingObj.doctor.user.first_name,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': bookingObj.doctor.consultationcharges*100,
                    }
                ]
            )
            template = 'EMedix_App/create_checkout_session.html'
            context = {'sessionId' : checkout_session['id']}
            return render(request,template,context)
           
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required(login_url='/login') 
def success(request):
    bookingobj = list(BookingAppointment.objects.filter(patient__user = request.user))[-1]
    bookingobj.Paymentstatus = True
    bookingobj.save()
    emailpatient = EmailMessage(subject='Appointment Status',body="Your Appointment has been Booked. \n Doctor Name: {} \n Time: {} \n Consultation Charges = {} \n Thank you for booking an appointment through E-Medix. \n E-Medix(HealthCare anytime anywhere \n".format(bookingobj.doctor.user.get_full_name() ,bookingobj.timing, bookingobj.doctor.consultationcharges),to=[bookingobj.patient.user.email])
    emailpatient.send()
    emaildoctor = EmailMessage(subject='Appointment Status',body="You have a new patient booking. \n Patient Name: {}  \n Time: {} \n Consultation Charges = {} \n Thank you for using E-Medix. \n E-Medix(HealthCare anytime anywhere \n".format(bookingobj.patient.user.get_full_name() ,bookingobj.timing, bookingobj.doctor.consultationcharges),to=[bookingobj.doctor.user.email])
    emaildoctor.send()
    template = 'EMedix_App/success.html'
    
    return render(request,template)



@login_required(login_url='/login') 
def error(request):
    bookingobj = list(BookingAppointment.objects.filter(patient__user = request.user))[-1]
    emailpatient = EmailMessage(subject='Appointment Status',body="Your Payment could not be processed. Kindly try to book the appointment again.",to=[bookingobj.patient.user.email])
    emailpatient.send()
    bookingobj.delete()
    template = 'EMedix_App/error.html'
    return render(request,template)

@login_required(login_url='/login') 
def changepassword(request):
    template = 'EMedix_App/changepassword.html'
    context = {}
    if request.method == 'POST':
        userobj = request.user
        if userobj.check_password(request.POST['old-password']):
            if request.POST['new-password'] == request.POST['conf-password']:
                userobj.set_password(request.POST['new-password'])
                userobj.save()
                context['message'] = 'Password has been changed!'
                # Redirection needs to go here
            else:
                context['message'] = 'Could not confirm new Password!'
        else:
            context['message'] = 'Password not correct!'
    return render(request,template,context)


filenamecounter = 0
@login_required(login_url='/login') 
def uploadrecords(request):
    template = 'EMedix_App/uploadrecords.html'
    context = {}
    if request.method == 'POST':
        obj = medical_records()
        obj.user = request.user
        obj.desc = request.POST['filerecorddesc']
        global filenamecounter 
        image = request.FILES['filerecord']
        filename = str(filenamecounter) + image.name

        #print(filename)
        client = storage.Client('e-Medix')
        bucket = client.get_bucket('file-store-emedix')
        blob = bucket.blob(filename)
        blob.upload_from_string(image.file.read())
        obj.recordname = image.name
        obj.fileid = filenamecounter
 
        obj.save()

        #print(obj.recordname)
        
        #print(filenamecounter)
   
        filenamecounter += 1
        #print(filenamecounter)
     

     
        #fs = FileSystemStorage()
        #filename = fs.save(image.name, image)
        #obj.upfile = fs.url(filename)
        #obj.save()
        
        context['message'] ='File Successfully Uploaded!'
     
    context['objs'] = medical_records.objects.filter(user=request.user)
    context['patientdetails'] = patient.objects.filter(user = request.user)[0]
    
    print(context)
    return render(request,template,context)

@login_required(login_url='/login') 
def viewrecords(request,patid):
    context = {}
    template = 'EMedix_App/viewrecords.html'
    context['patientdetails'] = patient.objects.get(pk=patid)
    context['objs'] = medical_records.objects.filter(user = context['patientdetails'].user)
    return render(request,template,context)

@login_required(login_url='/login')  
def videochat(request):
    template = 'EMedix_App/patientvideo.html'
    return render(request,template)

@login_required(login_url='/login') 
def videocallstart(request):
    twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    twilio_api_key_sid = settings.TWILIO_API_KEY_SID
    twilio_api_key_secret = settings.TWILIO_API_KEY_SECRET
    if request.method == 'POST':
        username = request.get_json(force =True).get('username')
    if not username:
         print('hello')
    token = AccessToken(twilio_account_sid,twilio_api_key_sid,twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room = 'My Room'))
    return {'token': token.to_jwt().decode()}