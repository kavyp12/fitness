from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  
    path('signin/', views.signin, name='signin'),  
    path('signout/', views.signout, name='signout'),  
    path('step/', views.step, name='step'),  
    path('auth/', include('social_django.urls', namespace='social')),
    path('googlefit/auth/', views.googlefit_auth, name='googlefit_auth'),
    path('googlefit/auth/callback/', views.googlefit_auth_callback, name='googlefit_auth_callback'),
    path('error_page/', views.error_page, name='error_page'),
    path('dailyset/', views.dailyset, name='dailyset'),
    path('reminders/', views.reminders, name='reminders'),
    path('step_count_email/', views.step_count_email, name='step_count_email'),
    path('congrats/', views.congrats, name='congrats'),
    path('delete_reminder/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('back/', views.back, name='back'),
    path('biceps/', views.biceps, name='biceps'),
    path('triceps/', views.triceps, name='triceps'),
    path('shoulder/', views.shoulder, name='shoulder'),
    path('chest/', views.chest, name='chest'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


