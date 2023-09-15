from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.functions import Upper

import requests



class CurrencyForm(forms.Form):
    # Делаю условие максимальной длинны 3, из-за аббревиатуры валют
    start_currency = forms.CharField(label='Изначальная валюта', max_length=3)
    finish_currency = forms.CharField(label='В какую перевести', max_length=3)
    ammount = forms.CharField(label='Сумма',max_length=200)

    # Необходимый ключ к API
    API_KEY = "f5a1bb69350ea54f35e9f8e2"
    # Делаем правильный юрл запрос с своим ключом
    URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    # Сохраняем данные с API в переменную, преобразовывая в JSON
    my_data = requests.get(URL).json()

    def clean(self) -> Dict[str,Any]:
        return super().clean()

    # Проверяем есть ли первая валюта в списке предстовляемых у ExchangerateAPI, если есть то возвращаем значение в форме
    def clean_start_currency(self):
        start_currency: str = self.cleaned_data['start_currency']
        valid_currency = self.my_data["conversion_rates"]
        if start_currency.upper() not in valid_currency.keys():
            raise ValidationError('Такой валюты нет')
        return self.data

    # Проверяем есть ли вторая валюта в списке предстовляемых у ExchangerateAPI, если есть то возвращаем значение в форме
    def clean_finish_currency(self):
        finish_currency: str = self.cleaned_data['finish_currency']
        valid_currency = self.my_data["conversion_rates"]
        if finish_currency.upper() not in valid_currency.keys():
            raise ValidationError('Такой валюты нет')
        return self.data
    