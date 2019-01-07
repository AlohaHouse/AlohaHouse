from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .forms import CheckSearchValidation, SearchForm
from masterdata.models import Company
from django.views import View

import pdb


"""物件検索フォーム"""
class SearchView(View):
    template_name = 'article/search.html'
    success_url = '/article/list'

    def get(self, request, *args, **kwargs):
        context = {}
        context['company_list'] = Company.objects.all()
        context['form'] = SearchForm()
        # pdb.set_trace()
        return render(request, self.template_name, context)



    def post(self, request, *args, **kwargs):
        checker = CheckSearchValidation(request.POST)
        if checker.isValid():
            return render(request, self.template_name, {})
        else:
            return render(request, self.template_name, {})



class ArticleListView(TemplateView):
    template_name = 'article/article_list.html'
