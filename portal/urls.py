from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dealer/<str:dealer_id>/', views.dealer_details, name='dealer_details'),
    path('dealer/<str:dealer_id>/review/', views.add_review, name='add_review'),
    path('filter/', views.filter_by_state, name='filter_by_state'),
    path('analyze/', views.analyze_sentiment, name='analyze_sentiment'),

    # AUTH
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
]
