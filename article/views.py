from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from .forms import SearchParams
from masterdata.models import Company, Route
from django.views import View

import pdb


"""路線選択フォーム"""
class SearchRoutesView(View):
    # 路線一覧ページ
    template_name = 'article/search_routes.html'
    # 駅選択画面
    success_url = 'article:search'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        # 路線を選択している場合
        if 'routes' in request.POST:
            # セッションに路線情報を格納
            request.session['routes'] = request.POST.getlist('routes')
            return redirect(self.success_url)
        else:
            context = self.get_context_data()
            # メッセージ設定
            context['messages'] = "路線を選択してください"
            return render(request, self.template_name, context)


    def get_context_data(self):
        context = {}
        # 路線会社一覧を格納
        context['company_list'] = Company.objects.all()
        return context


"""駅選択フォーム"""
class SearchView(View):
    # 駅、こだわり選択画面
    template_name = 'article/search.html'
    # 物件一覧画面
    success_url = 'article:list'


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        # 路線情報が設定されていない場合
        if not context:
            # 路線選択画面へ
            return redirect('article:search_routes')
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        # 情報格納変数
        model = {}
        if 'ek' in request.POST:
            search_data = SearchParams(request.POST)
            # 駅を選択しているか確認
            request.session['search_data'] = search_data
            # 検索結果一覧画面へ
            return redirect(self.success_url)
        else:
            context = self.get_context_data(request)
            context['messages'] = model['messages']
            return render(request, self.template_name, context)
   
    

    def get_context_data(self, request):
        context = {}
        # セッションに路線情報がない場合
        if not 'routes' in request.session:
            return None
        # 路線のIDを取得
        route_id_list = request.session['routes'] 
        # 選択された路線を取得
        context['route_list'] = Route.objects.in_bulk(id_list=route_id_list, field_name='pk')
        return context

class ArticleListView(TemplateView):
    template_name = 'article/article_list.html'


    def get(self, request):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def get_context_data(self, request):
        context = {}
        data = request.session['search_data']
        context['article_url'] = data.get_suumo_params()
        return context

