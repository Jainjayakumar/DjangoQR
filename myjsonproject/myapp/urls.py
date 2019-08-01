from django.urls import path
from .views import my_view, methodinfo, myview, homePageView
#from .views import homePageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('hello', myview, name='GET'),
    path('qrid', my_view, name='Post'),
    path('info',methodinfo)
]
