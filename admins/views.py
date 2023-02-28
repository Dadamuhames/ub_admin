from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import Messages, SearchQuoteGroup, SearchQuotes
from .utils import *
from rest_framework import generics
from rest_framework.response import Response
from .serializers import MessagesSerializer
# Create your views here.


# home admin
def home(request):
    return render(request, 'admin/base_template.html')

# based list view
class BasedListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(BasedListView, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(
            self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context



# messages list
class MessagesList(BasedListView):
    model = Messages
    template_name = 'admin/messages_list.html'

    def get_queryset(self):
        queryset = Messages.objects.all()
        end_list = set()
        quote_groups_ids = self.request.GET.getlist('quotes')
        quote_groups = SearchQuoteGroup.objects.filter(id__in=[int(it) for it in quote_groups_ids])

        for gr in quote_groups:
            quotes = gr.quotes.all()
            for q in quotes:
                q_set = queryset.filter(text__iregex=q.quote)
                for item in q_set:
                    end_list.add(item)


        queryset = list_to_queryset(list(end_list))
        print(quote_groups)
    
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['objecs_count'] = len(qs)
        users_set = set()

        for item in qs:
            users_set.add(item.user)

        context['user_count'] = len(list(users_set))
        context['quotes'] = SearchQuoteGroup.objects.all()

        return context


# messages detail
class MessagesDetail(DetailView):
    model = Messages
    template_name = 'admin/messages_view.html'



# searches list
class QuotesList(BasedListView):
    queryset = SearchQuotes.objects.all()
    template_name = 'admin/quotes.html'


# quotes cteate
class QuotesCreate(CreateView):
    model = SearchQuotes
    fields = '__all__'
    success_url = '/admins/quotes'
    template_name = 'admin/quotes_edit.html'

    def get_context_data(self, **kwargs):
        context = super(QuotesCreate, self).get_context_data(**kwargs)
        context['groups'] = SearchQuoteGroup.objects.all()

        return context


# quotes update view
class QuotesUpdateView(UpdateView):
    model = SearchQuotes
    fields = '__all__'
    template_name = '/admins/quotes'
    success_url = 'admin/quotes_edit.html'

    def get_context_data(self, **kwargs):
        context = super(QuotesUpdateView, self).get_context_data(**kwargs)
        context['groups'] = SearchQuoteGroup.objects.all()

        return context


# searches group list
class QuotesGroupList(BasedListView):
    models = SearchQuoteGroup
    queryset = SearchQuoteGroup.objects.all()
    template_name = 'admin/quote_groups.html'


# quote group create
class QuoteGroupCreate(CreateView):
    model = SearchQuoteGroup
    fields = '__all__'
    template_name = 'admin/quote_gr_form.html'
    success_url = '/admins/quotes_group'


# quote group edit
class QuoteGroupEdit(UpdateView):
    model = SearchQuoteGroup
    fields = '__all__'
    template_name = 'admin/quote_gr_form.html'
    success_url = '/admins/quotes_group'


# messages create
class MessagesCreate(generics.CreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer


# delete model item
def delete_item(request):
    model_name = request.POST.get("model_name_del")
    app_name = request.POST.get('app_name_del')
    id = request.POST.get('item_id')
    url = request.POST.get("url")

    try:
        model = apps.get_model(model_name=model_name, app_label=app_name)
        model.objects.get(id=int(id)).delete()
    except:
        pass

    return redirect(url)
