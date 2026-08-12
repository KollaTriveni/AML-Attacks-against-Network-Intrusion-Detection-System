"""
URL configuration for Network_Intrusion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from admins import views as admin_views

urlpatterns = [
    path('dj-admin/', admin.site.urls),  
    path('',user_views.home_page,name='home'),
    path('about/',user_views.about_page,name='about'),
    path('contact/',user_views.contact_page,name='contact'),
    path('user-login/',user_views.user_login_page,name='user-login'),
    path('admin-login/',admin_views.admin_login_page,name='admin-login'),

    path('user/check-login/', user_views.check_user_credentials),
    path('user/check-register/', user_views.check_register_fields),

    path('user/send-otp/', user_views.user_send_otp, name='user_send_otp'),
    path('user/verify-otp/', user_views.user_verify_otp, name='user_verify_otp'),
    path('user/login/', user_views.user_login, name='user_login_check'),
    path('user/register/', user_views.user_register, name='user_register'),
    path('user-dashboard/',user_views.user_dashboard,name='user-dashboard'),

    path('admin_dashboard/',admin_views.admin_dashboard,name='admin_dashboard'),

    path('admin/send-otp/', admin_views.send_otp, name='send_otp'),
    path('admin/verify-otp/', admin_views.verify_otp, name='verify_otp'),
    path('admin/login/', admin_views.admin_login, name='admin_login_check'),
    path('pending_users/',admin_views.pending_users,name='pending_users'),
    path('accepted_users/',admin_views.accepted_users,name='accepted_users'),
    path('rejected_users/',admin_views.rejected_users,name='rejected_users'),
     
    path('rejected_users/<int:user_id>/',admin_views.rejected_user,name='rejected_user'),
    path('all_users/',admin_views.all_users,name='all_users'),
    path('accepted_users/<int:user_id>/',admin_views.accept_user, name='accepted_users'),
    path('upload_dataset/',admin_views.upload_dataset,name='upload_dataset'),
    path('view_dataset',admin_views.view_dataset,name='view_dataset'),
    path('decision_tree/',admin_views.decision_tree,name='decision'),
    path('train_decision_tree/',admin_views.train_decision_tree,name='train_decision_tree'),
    path('svm/',admin_views.svm,name='svm'),
    path('train_svm/',admin_views.train_svm,name='train_svm'),
    path('random_forest/',admin_views.random_forest,name='random'),
    path('logistic/',admin_views.logistic_regression,name='logistic'),
    path('k-nearest',admin_views.k_nearest,name='k_nearest'),
    path('naive_bayes',admin_views.naive_bayes,name='naive'),
    path('neural_network',admin_views.neural_network,name='neural'),
    path('aml_attack',admin_views.aml_attack,name='aml_attack'),
    path('graph_analysis',admin_views.graph_analysis,name='graph'),
    path('decision_result/',admin_views.decision_result,name='decision_result'),
    path('svm_result',admin_views.svm_result,name='svm_result'),
    path('logistic_result',admin_views.logistic_result,name='logistic_result'),
    path('knn_result',admin_views.knn_result,name='knn_result'),
    path('naive_result',admin_views.naive_result,name='naive_result'),
    path('neural_result',admin_views.neural_result,name='neural_result'),
    path('random_result/',admin_views.random_result,name='random_result'),
    path('aml_result/',admin_views.aml_result,name='aml_result'),
    path('user_predict/',user_views.user_predict,name='user_predict'),
    path('user_profile/',user_views.user_profile,name='user_profile'),
]
