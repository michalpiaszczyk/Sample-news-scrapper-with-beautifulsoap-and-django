from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import News
from datetime import datetime
from django.utils import timezone
from .forms import NewsFilterForm
from .constants import zrodla
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.db.models import Q
import locale
import configparser
import babel.dates
import docx2txt
from django.core.mail import send_mail

# Create your views here.

def home(request):
    #is new
    now = timezone.now()
    #filter
    form = NewsFilterForm(request.GET)
    news_list = News.objects.all().order_by('-data')
    if form.is_valid():
        title = form.cleaned_data['tytul']
        start_date = form.cleaned_data['data_od']
        end_date = form.cleaned_data['data_do']
        sources = form.cleaned_data['source']
        if title:
            news_list = news_list.filter(tytul__icontains=title)
        if start_date:
            news_list = news_list.filter(data__gte=start_date)
        if end_date:
            news_list = news_list.filter(data__lte=end_date)
        if sources:
            news_list = news_list.filter(source__in=sources)

    helper = FormHelper()
    helper.form_class = 'form-inline'
    helper.form_method = 'GET'
    helper.form_action = ''
    helper.layout = Layout(
        Row(
            Column('tytul', css_class='form-group col-md-3 mb-0'),
            Column('data_od', css_class='form-group col-md-3 mb-0'),
            Column('data_do', css_class='form-group col-md-3 mb-0'),
            Column('source', css_class='form-group col-md-3 mb-0'),
            css_class='form-row align-items-center'
        ),
        Submit('submit', 'Filtruj', css_class='btn btn-primary')
    )
    
    #źródła
    
    news_with_sources = []
    for news in news_list:
        source = zrodla[news.source]
        news.is_new = (now - news.data) < timezone.timedelta(days=1)
        news_with_sources.append({'news': news, 'source': source, 'new':news.is_new})

    config = configparser.ConfigParser()
    #należy podać ścieżkę do pliku nws\nius\config.ini
    # config.read(r'D:\OneDrive\Python\news\nws\nius\config.ini')
    config.read(r'D:\Code\news\nws\nius\config.ini')
    
    start_date_str = config.get('DEFAULT', 'start_date')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    # Ustawienie lokalizacji na polską dla nazw miesięcy
    locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')
    formatted_date = babel.dates.format_date(start_date, 'd MMMM yyyy', locale='pl_PL')
    return render(request, 'home.html', {'news_list':news_list,'dzis':now,'news_with_sources': news_with_sources,'form':form,'helper': helper,'start_date': formatted_date} )

def brak(request):
    return render(request, 'brak.html')
def sent(request):
    return render(request, 'sent.html')
def about(request):
    path = r'D:\OneDrive\Python\news\nws\nius\pliki\about.docx'
    file_content = docx2txt.process(path)
    return render(request, 'about.html',{'file_content': file_content})

def sendemail(request, news_id):
    news = get_object_or_404(News, id = news_id)
    if request.method == "POST":
        sub = news.tytul
        msg = f"{news.opis} \nPrzeczytaj więcej na stronie {news.url}"
        email = request.POST.get('email')
        send_mail(
            sub, msg,'michal.na.wsb@gmail.com',
            [email]
        )
        return render(request, 'sent.html')
    return render(request, 'form.html')

