from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView
from .forms import SearchParams
from masterdata.models import Company, Route, ConditionsGroup
from django.views import View
from bs4 import BeautifulSoup
from collections import Counter

import pdb
import urllib


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
    success_url = 'article:result'


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        # 路線情報が設定されていない場合
        if not context:
            # 路線選択画面へ
            return redirect('article:search_routes')
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        # 情報格納変数
        if 'ek' in request.POST:
            search_data = SearchParams(request.POST)
            # 駅を選択しているか確認
            request.session['search_data'] = search_data
            # 検索結果一覧画面へ
            return redirect(self.success_url)
        else:
            context = self.get_context_data(request)
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
        context['condition_group_list'] = ConditionsGroup.objects.filter(is_active=True)
        return context


"""検索結果コントローラ"""
class ResultView(TemplateView):

    template_name = 'article/result.html'

    # requestを使用する為にオーバーライド
    def get(self, request, **kwargs):
        context = self.get_context_data(request)
        return self.render_to_response(context)


    def get_context_data(self,request, **kwargs):
        # アクセスするURL（実際はセッションから取得）
        data = request.session['search_data']
        # suumoのURLを取得
        url = data.get_suumo_params()
        # url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=000525620&rn=0005"

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

        #交通手段取得（取得後2次元配列で保持）
        transportation_all = []
        transportations = [] 
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-detail")
            arg2 = arg1.find("div", class_="cassetteitem-detail-body")
            arg3 = arg2.find("div", class_="cassetteitem_content-body")
            arg4 = arg3.find("li", class_="cassetteitem_detail-col2")
            arg5 = arg4.find_all("div", class_="cassetteitem_detail-text")
            for arg6 in arg5:
                transportations.append(arg6.text)
            transportation_all.append(transportations)
            transportations = []

        #築年数、階建取得（取得後配列で保持）
        years = [] 
        stories = []
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-detail")
            arg2 = arg1.find("div", class_="cassetteitem-detail-body")
            arg3 = arg2.find("div", class_="cassetteitem_content-body")
            arg4 = arg3.find("li", class_="cassetteitem_detail-col3")
            year = arg4.select_one("div:nth-of-type(1)").text
            story = arg4.select_one("div:nth-of-type(2)").text
            years.append(year)
            stories.append(story)

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
        article_rent_all = [] #全ての物件の賃料全てを格納(2次元配列)
        article_rents = [] #１物件の賃料全てを格納
        article_administration_all = [] #全ての物件の階数全てを格納(2次元配列)
        article_administrations = [] #１物件の階数全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(4)") #nth-of-typeで何番目の要素なのか指定
                arg5 = arg4.find("span", class_="cassetteitem_other-emphasis").text
                article_rents.append(arg5)
            article_rent_all.append(article_rents)
            article_rents = [] #1物件の賃料全てを取得したので初期化

        #建物の管理費取得（取得後2次元配列で保持）
        article_administration_all = [] #全ての物件の階数全てを格納(2次元配列)
        article_administrations = [] #１物件の階数全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(4)") #nth-of-typeで何番目の要素なのか指定
                arg5 = arg4.find("span", class_="cassetteitem_price--administration").text
                article_administrations.append(arg5)
            article_administration_all.append(article_administrations)
            article_administrations = [] #1物件の管理費全てを取得したので初期化

        #建物の敷金、礼金取得（取得後2次元配列で保持）
        article_deposit_all = [] #全ての物件の敷金全てを格納(2次元配列)
        article_deposits = [] #１物件の敷金全てを格納
        article_gratuity_all = [] #全ての物件の礼金全てを格納(2次元配列)
        article_gratuitys = [] #１物件の礼金全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(5)") #nth-of-typeで何番目の要素なのか指定
                deposit = arg4.find("span", class_="cassetteitem_price--deposit").text
                gratuity = arg4.find("span", class_="cassetteitem_price--gratuity").text
                article_deposits.append(deposit)
                article_gratuitys.append(gratuity)
            article_deposit_all.append(article_deposits)
            article_gratuity_all.append(article_gratuitys)
            article_deposits = [] #1物件の敷金全てを取得したので初期化
            article_gratuitys = [] #1物件の礼金全てを取得したので初期化

        #間取画像取得（取得後2次元配列で保持）
        floor_picture_all = [] #全ての間取の写真全てを格納(2次元配列)
        floor_pictures = [] #１物件の間取の写真全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.find("img")
                # srcタグの属性を抽出
                src = arg4.get('src')
                floor_pictures.append(src)
            floor_picture_all.append(floor_pictures)
            floor_pictures = [] #1物件の階数全てを取得したので初期化
        
        #部屋の面積を取得（取得後2次元配列で保持）
        article_area_all = [] #全ての物件の面積全てを格納(2次元配列)
        article_areas = [] #１物件の面積全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(6)") #nth-of-typeで何番目の要素なのか指定
                arg5 = arg4.find("span", class_="cassetteitem_menseki").text
                text = arg5.replace('m2','')
                article_areas.append(text)
            article_area_all.append(article_areas)
            article_areas = [] #1物件の階数全てを取得したので初期化

        #部屋の間取を取得（取得後2次元配列で保持）
        floor_plan_all = [] #全ての部屋の間取全てを格納(2次元配列)
        floor_plans = [] #１部屋の間取全てを格納
        for cassetteitem in cassetteitems:
            arg1 = cassetteitem.find("div", class_="cassetteitem-item")
            arg2 = cassetteitem.find_all("tbody")
            for arg3 in arg2:
                arg4 = arg3.select_one("tr td:nth-of-type(6)") #nth-of-typeで何番目の要素なのか指定
                arg5 = arg4.find("span", class_="cassetteitem_madori").text
                floor_plans.append(arg5)
            floor_plan_all.append(floor_plans)
            floor_plans = [] #1物件の階数全てを取得したので初期化


        context["article_names"] = article_names
        context["addresses"] = addresses
        context["article_images"] = article_images
        context["article_level_all"] = article_level_all
        context["article_rent_all"] = article_rent_all
        context["floor_picture_all"] = floor_picture_all
        context["article_area_all"] = article_area_all
        context["floor_plan_all"] = floor_plan_all
        context["article_administration_all"] = article_administration_all
        context["article_deposit_all"] = article_deposit_all
        context["article_gratuity_all"] = article_gratuity_all
        context["transportation_all"] = transportation_all
        context["years"] = years
        context["stories"] = stories
        return context
