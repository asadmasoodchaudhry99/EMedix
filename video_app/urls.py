from django.urls import path
from .views import HomeView, JoinRoomView, PreHomeView, room_view, video_start
from .api_views import create_room, end_room
app_name = 'video_app'

urlpatterns = [
    # path('', CreateRoomView, name = "CreateRoomView"),
    path('home/', HomeView, name="HomeView"),
    path('', PreHomeView, name="PreHomeView"),
    path('create_room/', create_room, name="create_room"),
    path('end_room/<room_sid>', end_room, name="end_room"),
    path('join_room/', JoinRoomView.as_view(), name="JoinRoomView"),
    path('room/<room_name>/<sid>/<name>', room_view , name="room_view"),

    path('goto-room/<docid>/<patid>/<bid>', video_start),

]
