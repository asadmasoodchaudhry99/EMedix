from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404
from django.conf import settings
import os
import json
from twilio.rest import Client
from twilio.rest.video.v1 import room
from .models import Person, Room
from .forms import PersonForm
from django.core.mail import EmailMessage

from video_app.helper_functions.get_participants import get_participants
from video_app.helper_functions.create_token import create_token

from .api_views import create_room, end_room
from django.contrib.auth.models import User

from EMedix_App.models import BookingAppointment

twilio_api_key_sid = settings.TWILIO_API_KEY_SID
twilio_api_key_secret = settings.TWILIO_API_KEY_SECRET
client = Client(twilio_api_key_sid, twilio_api_key_secret)


def HomeView(request):
    return render(request, 'home.html')
def PreHomeView(request):
    return render(request, 'pre_home.html')
    

class JoinRoomView(View):
    def get(self, request):
        room_data = create_room(request)
        request.session['room_data'] = room_data
        try:
            person_form = PersonForm()
            context = {
                "room_name": room_data['room_name'],
                "room_sid": room_data['room_sid'],
                "person_form": person_form
            }
            print("context = ", context)
            return render(request, 'join_room.html', context)
        except:
            raise Http404("Room not found")

    def post(self, request):
        room_data = request.session['room_data']
        room_name = room_data['room_name']
        person_form = PersonForm(request.POST)
        if person_form.is_valid():
            person_name = person_form.cleaned_data['person_name']
            person_token = create_token(person_name, room_name)
            request.session['person_data'] = {"person_name":person_name, "person_token":person_token}
            return redirect('video_app:room_view',  room_name)

def room_view(request, room_name, sid, name):
    #room_data = room_name #request.session['room_data']
    #person_data =  request.session['person_data']
    context = {
                "context": {
                    'person_name': name, #person_data['person_name'],
                    'person_token': create_token(name, room_name), #person_data['person_token'],
                    'room_name':room_name,
                    'room_sid': sid, #room_data['room_sid'],
                    'participantsList': get_participants(room_name),
                }
            }
    return render(request, 'in_room.html', context)


def video_start(request, docid, patid, bid):
    docobj = User.objects.get(pk=docid)
    patobj = User.objects.get(pk=patid)
    roomobj = create_room(request)
    emailobj = EmailMessage(
        subject='Video Consultancy Link',
        body='Kindly join the meeting for online consultancy : https://{}/room/{}/{}/{}'.format(request.get_host(),roomobj['room_name'],roomobj['room_sid'],patobj.first_name),
        to=[patobj.email]
    )
    emailobj.send()
    obj = BookingAppointment.objects.get(pk=bid)
    obj.consultation_status = True
    obj.save()
    return redirect('/room/{}/{}/{}'.format(roomobj['room_name'],roomobj['room_sid'],docobj.first_name))