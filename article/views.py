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

        # URLにアクセスする htmlが返ってくる → <html><head><title></title></head><body....
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
            # relタグの属性を抽出
            rel = arg3.get('rel')
            article_images.append(rel)

        #建物の階数を取得（取得後2次元配列で保持）
        article_level_all = [] #全ての物件の階数全てを格納(2次元配列)
        article_levels = [] #１物件の階数全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(3)").text #nth-of-typeで何番目の要素なのか指定
                #改行コードが入ってしまうため取り除く
                text = arg4.replace('\n','')
                text = text.replace('\r','')
                text = text.replace('\t','')
                #改行コード取り除き完了
                article_levels.append(text)
            article_level_all.append(article_levels)
            article_levels = [] #1物件の階数全てを取得したので初期化
        
        #建物の賃料取得（取得後2次元配列で保持）
        article_rent_all = [] #全ての物件の階数全てを格納(2次元配列)
        article_rents = [] #１物件の階数全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(4)") #nth-of-typeで何番目の要素なのか指定
                arg5 = arg4.find("span", class_="cassetteitem_other-emphasis").text
                article_rents.append(arg5)
            article_rent_all.append(article_rents)
            article_rents = [] #1物件の賃料全てを取得したので初期化


        context["article_names"] = article_names
        context["addresses"] = addresses
        context["article_images"] = article_images
        context["article_level_all"] = article_level_all
        context["article_rent_all"] = article_rent_all
        return context
