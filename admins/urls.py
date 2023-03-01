from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = [
    path('', views.home, name='home'),
    path('login', LoginView.as_view(
        template_name='admin/sing-in.html',
        success_url='/admin/',
    ), name='login_admin'),
    path("messages", views.MessagesList.as_view(), name='messages_list'),
    path("messages/<int:pk>", views.MessagesDetail.as_view(), name='messages_detail'),
    #path('quotes', views.QuotesList.as_view(), name='quotes_list'),
    #path('quotes/create', views.QuotesCreate.as_view(), name='quotes_create'),
    #path('quotes/<int:pk>/edit', views.QuotesUpdateView.as_view(), name='quotes_edit'),
    #path("quotes_group", views.QuotesGroupList.as_view(), name='quote_group_list'),
    #path('quotes_group/create', views.QuoteGroupCreate.as_view(), name='quotes_group_create'),
    #path("quotes_group/<int:pk>/edit", views.QuoteGroupEdit.as_view(), name='quotes_group_edit'),
    path('api/message/save', views.MessagesCreate.as_view()),
    path('quotes', views.QuotesList.as_view(), name='quotes_list'),
    path("quotes/<int:pk>", views.QuoteGroupDetail.as_view(), name='transl_group_detail'),
    path("quotes/<int:pk>/edit", views.TranslationGroupUdpate.as_view(), name='transl_group_edit'),
    path("translation_group/create", views.add_trans_group, name='transl_group_create'),

    path("delete", views.delete_item, name='delete'),
]
