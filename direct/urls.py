from django.urls import path
from direct import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('directs/<username>/', views.directs, name='directs'),
    path('send_message/', views.send__message, name='send-message'),
    path('new/', views.user_search, name='user-search'),
    path('new/<username>', views.new_message, name='new-message'),
]