
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    #profile path
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),

    
    path('Index', views.INDEX, name='index'),
    path('Visitor', views.ADD_VISITOR, name='add_visitor'),
    path('ManageVisitor', views.MANAGE_VISITOR, name='manage_visitor'),
    path('UpdateVisitor/<str:id>', views.UPDATE_VISITOR, name='update_visitor'),
    
    path('UpdateVisitorRemark/Update', views.UPDATE_VISITOR_REMARK, name='update_visitor_remark'),
    path('DeleteVisitor/<str:id>', views.DELETE_VISITOR, name='delete_visitor'),
    path('BetweenDateReport', views.Between_Date_Report, name='between_date_report'),
    path('Search', views.Search, name='search'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),



]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
