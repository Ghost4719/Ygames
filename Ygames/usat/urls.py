# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'usat'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('logout/', views.log_out, name='log_out'),
    path('game/create/', views.create, name='create'),
    
    # Edit existing game (game_id is required)
    path('game/create/<int:game_id>/', views.create, name='edit'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('User/<str:username>/', views.change , name='change'),
    #path('play-game/<int:game_id>/', views.play_game, name='play_game')
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

