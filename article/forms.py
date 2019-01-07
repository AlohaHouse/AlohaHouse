from django import forms
from masterdata.models import Station, Route

import pdb



# 検索用のクラス(バリデーションのため)
class CheckSearchValidation():

    def __init__(self, request):
        self.message = {}
        self.stations = request['stations']


    def isValid(self):

        self.__check()

        if not self.message:
            return True
        else:
            return False

    def __check(self):
        print(self.stations)

class SearchForm(forms.Form):
    station = {}

    def __init__(self):
        routes = Route.objects.all()
        for route in routes:
            SearchForm.station = forms.ModelChoiceField(route.station_set.all(), label='駅', widget=forms.CheckboxSelectMultiple)
        super().__init__()

        # pdb.set_trace()
