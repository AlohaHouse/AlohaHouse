from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .forms import CheckSearchValidation, SearchForm
from masterdata.models import Company
from django.views import View
from bs4 import BeautifulSoup
from collections import Counter

import pdb
import urllib


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

"""検索結果コントローラ"""
class ResultView(TemplateView):

    template_name = 'article/result.html'

    def get_context_data(self, **kwargs):
        # アクセスするURL（実際はセッションから取得）
        url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=000525620&rn=0005"

        # URLにアクセスする htmlが返ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
        html = urllib.request.urlopen(url=url)

        #viewに受け渡すための変数
        context = super().get_context_data(**kwargs)

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        #配列の初期化
        article_names = []

        # 物件情報を取得(classは予約語なのでアンダースコアで回避)
        cassetteitems = soup.find_all("div", class_="cassetteitem")

        #物件名取得（取得後配列で保持）
        article_names = [] #配列の初期化
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-detail")
            arg2 = arg1.find("div", class_="cassetteitem-detail-body")
            arg3 = arg2.find("div", class_="cassetteitem_content-title").text
            article_names.append(arg3)

        #住所取得（取得後配列で保持）
        addresses = [] #配列の初期化
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-detail")
            arg2 = arg1.find("div", class_="cassetteitem-detail-body")
            arg3 = arg2.find("div", class_="cassetteitem_content-body")
            arg4 = arg3.find("li", class_="cassetteitem_detail-col1").text
            addresses.append(arg4)

        #建物の画像取得（取得後配列で保持）
        article_images = [] #配列の初期化
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-detail")
            arg2 = arg1.find("div", class_="cassetteitem-detail-object")
            arg3 = arg1.find("img")
            # relタグの値を抽出
            rel = arg3['rel']
            article_images.append(rel)

        context["article_names"] = article_names
        context["addresses"] = addresses
        context["article_images"] = article_images
        return context
