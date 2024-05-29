from django.shortcuts import render
from .models import Contact,User
from django.conf import settings
from django.core.mail import send_mail
import random
# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			remarks=request.POST['remarks']
			)
		msg="Contact Saved Successfully"
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'contacts':contacts})
def signup(request):
	if request.method=="POST":
		try:
		    User.objects.get(email=request.POST['email'])
		    msg="Email Already Registered"
		    return render(request,'signup.html',{'msg':msg})
		except:
		    if request.POST['password']==request.POST['cpassword']:
		        User.objects.create(
		            	fname=request.POST['fname'],
		            	lname=request.POST['lname'],
		            	email=request.POST['email'],
		            	mobile=request.POST['mobile'],
		            	address=request.POST['address'],
		            	password=request.POST['password'],
		            	profile_picture=request.FILES['profile_picture']
		            )
		        msg="User Sign Up Successfully"
		        return render(request,'signup.html',{'msg':msg})
		    else:
		        msg="Password & Confirm Password Does Not Matched"
		        return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')



def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'index.html')
			else:
				msg="Incorrect Password"
				return render(request,"login.html",{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		msg="User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})
	except:
		return render(request,'login.html')

def change_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.session['email'])
			if user.password==request.POST['old_password']:
				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					msg="Password Changed Successfully"
					del request.session['email']
					del request.session['fname']
					return render(request,'login.html',{'msg':msg})
				else:
					msg="New Password & Confirm New Password Does Not Matched"
					return render(request,'change-password.html',{'msg':msg})
			else:
				msg="Old Password Does Not Matched"
				return render(request,'change-password.html',{'msg':msg})
		except:
			pass
	else:
		return render(request,'change-password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(10000,99999)
			subject = 'welcome to GFG world'
			message = 'Hello '+user.fname+"You OTP for Forgot Password Is "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			request.session['email1']=user.email
			request.session['otp']=otp
			return render(request,'otp.html')
		except:
			msg="Email Not Registered"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
	    return render(request,'forgot-password.html')

def verify_otp(request):
	otp=int(request.POST['otp'])
	otp2=int(request.session['otp'])


	if otp==otp2:
	    return render(request,'new-password.html')
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(email=request.session['email1'])
		user.password=request.POST['new_password']
		user.save()
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New Password & Confirm New Password Does Not Matched"
		return render(request,'new-password.html',{'msg':msg})