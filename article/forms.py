from django import forms
from masterdata.models import Station, Route

# デバッグ
import pdb


# 検索用のクラス(バリデーションのため)
class SearchParams(object):
    
    # パラメータデータ格納
    params = {
            'mt' : '9999999',    # 専有面積　上限なし
            'shkr1' : '03',     # ?
            'shkr2' : '03',     # ?
            'shkr3' : '03',     # ?
            'shkr4' : '03',     # ?
            'fw2' : '',         # ?
            'rn' : '0005',
            'srch_navi' : '1',
            }


    def __init__(self, request):
        self.make_params(request)
        
    
    # リクエスト情報からparamsを変更
    def make_params(self, request):
        # 送信されたパラメータのみ変更
        for param_name in request:
            # csrfトークンは処理なし
            if param_name == 'csrfmiddlewaretoken':
                continue
            self.params[param_name] = request.getlist(param_name)


    # スーモに使用するURLを取得する
    def get_suumo_params(self):
        # 文字列連結用
        stringBuilder = []

        # クエリを作成
        for key, vals in self.params.items():
            if type(vals) is list:
                for val in vals:
                    stringBuilder.append(key + "=" + val)
            else:
                stringBuilder.append(key + "=" + vals)

        print("&".join(stringBuilder))
        return "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?" + "&".join(stringBuilder)