from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),  # Ensure trailing slashes for consistency
    path('signin/', views.signin, name='signin'),  # Ensure trailing slashes for consistency
    path('signout/', views.signout, name='signout'),  # Ensure trailing slashes for consistency
    path('step/', views.step, name='step'),  # Ensure trailing slashes for consistency
    path('auth/', include('social_django.urls', namespace='social')),
    path('googlefit/auth/', views.googlefit_auth, name='googlefit_auth'),
    path('googlefit/auth/callback/', views.googlefit_auth_callback, name='googlefit_auth_callback'),
    path('error_page/', views.error_page, name='error_page'),
    path('dailyset/', views.dailyset, name='dailyset'),
    path('reminders/', views.reminders, name='reminders'),
    path('step_count_email/', views.step_count_email, name='step_count_email'),
    path('congrats/', views.congrats, name='congrats'),
    path('delete_reminder/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    # path('step/data/', views.step_data, name='step_data'),   # new URL for getting step data


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


