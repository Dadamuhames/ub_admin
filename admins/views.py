from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import Messages, SearchQuoteGroup, SearchQuotes
from .utils import *
from rest_framework import generics
from rest_framework.response import Response
from .serializers import MessagesSerializer
from datetime import datetime
# Create your views here.


# home admin
def home(request):
    return render(request, 'admin/base_template.html')

# based list view
class BasedListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(BasedListView, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context



# messages list
class MessagesList(BasedListView):
    model = Messages
    template_name = 'admin/messages_list.html'

    def get_queryset(self):
        queryset = Messages.objects.all().order_by("-date")
        end_list = set()
        quote_groups_ids = self.request.GET.getlist('quotes')
        date = self.request.GET.get('date', '')

        if date != '':
            if 'to' in str(date):
                from_date = datetime.strptime(date.split(" to ")[0], '%Y-%m-%d')
                to_date = datetime.strptime(date.split(' to ')[-1], '%Y-%m-%d')
                print(to_date, from_date)
                queryset = queryset.filter(
                    date__gte=from_date, date__lte=to_date)
            else:
                from_date = datetime.strptime(date, '%Y-%m-%d')
                queryset = queryset.filter(date__range=[from_date, datetime.today()])

        
        if quote_groups_ids:
            quote_groups = SearchQuoteGroup.objects.filter(id__in=[int(it) for it in quote_groups_ids if it != 0])

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
        context['selected_quotes'] = [int(item) for item in self.request.GET.getlist('quotes', [])]
        print(context['selected_quotes'])
        url = self.request.path + "?"

        if '&' in self.request.get_full_path():
            if 'page' in str(self.request.get_full_path()):
                url = '&'.join(self.request.get_full_path().split('&')[:-1]) + '&'
            else:
                url = self.request.get_full_path() + '&'

        context['url'] = url

        return context


# messages detail
class MessagesDetail(DetailView):
    model = Messages
    template_name = 'admin/messages_view.html'


# messages create
class MessagesCreate(generics.CreateAPIView):
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


# translations list
class QuotesList(ListView):
    model = SearchQuotes
    template_name = 'admin/translation_list.html'

    def get_queryset(self):
        queryset = SearchQuotes.objects.order_by("-id")
        query = self.request.GET.get("q")

        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuotesList, self).get_context_data(**kwargs)
        context['groups'] = SearchQuoteGroup.objects.all()
        context['url'] = search_pagination(self.request)

        # pagination
        context['objects'] = get_lst_data(
            self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)

        return context


# translation group
class QuoteGroupDetail(DetailView):
    model = SearchQuoteGroup
    template_name = 'admin/translation_list.html'

    def get_context_data(self, **kwargs):
        context = super(QuoteGroupDetail,
                        self).get_context_data(**kwargs)
        context['groups'] = SearchQuoteGroup.objects.all()
        lst_one = self.get_object().quotes.order_by('-id')

        # search
        query = self.request.GET.get("q")
        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['objects'] = dict(pairs=zip(lst_one, lst_two))

        return context


# add translation group
def add_trans_group(request):
    if request.method == 'POST':
        name = request.POST.get("name")

        try:
            transl_group = SearchQuoteGroup.objects.create(name=name)
            transl_group.full_clean()
            transl_group.save()
        except:
            return JsonResponse("error", safe=False)

        data = {
            'id': transl_group.id,
            'name': transl_group.name,
        }
        return JsonResponse(data)


# translation group udate
class TranslationGroupUdpate(UpdateView):
    model = SearchQuoteGroup
    template_name = 'admin/translation_edit.html'
    fields = '__all__'
    success_url = '/admin/translations'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupUdpate,
                        self).get_context_data(**kwargs)
        context['groups'] = SearchQuoteGroup.objects.all()
        lst_one = self.get_object().quotes.all()

        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['objects'] = dict(pairs=zip(lst_one, lst_two))

        return context

    def post(self, request, *args, **kwargs):
        transls = list(self.get_object().quotes.all())
        items_count = request.POST.get("item_count")

        for i in range(len(transls)):
            transls[i].quote = request.POST.get(f'quote[{i + 1}]', '')

            try:
                transls[i].full_clean()
                transls[i].save()
            except:
                pass

        for i in range(len(transls) + 1, int(items_count) + 1):
            new_trans = SearchQuotes()
            new_trans.quote = request.POST.get(f'quote[{i}]', '')
            new_trans.group = self.get_object()

            try:
                new_trans.full_clean()
                new_trans.save()
            except:
                pass

        return redirect('transl_group_detail', pk=self.get_object().id)
