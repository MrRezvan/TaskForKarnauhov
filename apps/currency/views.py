# Django
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import View


# Python
import requests

# Local
from currency.forms import CurrencyForm


class MainView(View):
    
    # В методе GET мы просто предоставляем пользователю страничку
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CurrencyForm()
        return render(
            request=request,
            template_name='main.html',
            context={
                'form': form
            }
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CurrencyForm(request.POST)
        if form.is_valid():
            # Вытаскиваю значения с форм, после прохождения валидации
            start_currency = form.cleaned_data['start_currency']['start_currency'].upper()
            finish_currency = form.cleaned_data['finish_currency']['finish_currency'].upper()
            ammount: str = form.cleaned_data['ammount']
            # Делаю запрос к API на основе введённых пользователем данных
            API_KEY = "f5a1bb69350ea54f35e9f8e2"
            URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{start_currency}/{finish_currency}/{ammount}"
            my_data = requests.get(URL).json()
            answer = my_data['conversion_result']
            # В случае успеха вывожу пользователю финальную версию странички 
            return render(
                    request=request,
                    template_name='main.html',
                    context={
                        'form': form,
                        'answer': answer
                    }
                )
        return HttpResponse ('Вы ввели некоректные данные, пожалуйста попробуйте ещё раз')