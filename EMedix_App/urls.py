from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
#Home_Page
path('', views.home, name='home'),
path('logout', views.logout, name='logout'),
#Login_Page
path('login', views.login, name='login'),
#OTP Verification
path('loginverification', views.loginverification, name = 'loginverification'),
#Resend OTP
path('otpresend', views.resendOTP, name = 'otpresend'),
#Signup_Page
path('signup', views.signup, name='signup'),
#AccountDetails Patient
path('PaitentAccountDetails', views.patient_details, name='patient_details'),
#AccountDetails Doctor
path('DoctorAccountDetails', views.doctor_details, name='doctor_details'),
#AccountDetails Clinic
path('clinicAccountdetails', views.clinic_details, name='clinic_details'),
#Patient Dashbpard
path('PatientDashboard', views.PatientDashboard, name='PatientDashboard'),
#Doctor Dashbpard
path('DoctorDashboard', views.DoctorDashboard, name='DoctorDashboard'),
#Clinic Dashboard
path('ClinicDashboard', views.ClinicDashboard, name='ClinicDashboard'),

#Consultation Charges
path('ConsultationCharges/<int:doctorid>', views.ConsultationCharges, name='ConsultationCharges'),
#Book Appointment
path('BookAppointment', views.book_appointment, name="BookAppointment"),

#Payment
path('config/',views.stripe_config),
path('create-checkout-session', views.create_checkout_session), # new
path('success', views.success , name = 'SuccessPayment') ,
path('error', views.error , name = 'ErrorPayment') , # new


#Update Profiles
path('updateProfile_patient' , views.UpdateProfilePatient, name= 'updateProfile_patient'), 
path('updateProfile_doctor' , views.UpdateProfileDoctor, name= 'updateProfile_doctor'), 

#change Password
path('changepassword' , views.changepassword, name= 'changepassword'), 

#Upload Records
path('uploadrecords' , views.uploadrecords, name= 'uploadrecords'), 
#View Records
path('viewrecords/<patid>' , views.viewrecords, name= 'viewrecords'), 
]