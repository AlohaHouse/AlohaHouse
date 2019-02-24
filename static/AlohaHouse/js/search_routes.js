$('#submit-btn').on('click', function(){

    $('#routes-form').submit();
});

$('.search-route-label').change(function(){

    var id = $(this).attr('id');
    $('.routes-box').find("[for='" + id + "']").parent().toggle();

});

var count = 0;
// PCでマウスホイールでのスクロール操作の制御
$(function(){

    var scrollRoutes = new ScrollRoutes();
    var btn = new MoreBtn();

    // 1秒後にcountをリセット
    setInterval(function(){
        count = 0;
    }, 200);

    if($("#route-conents").length) { 
      $(window).on('wheel',function(e){

        // イベント削除
        e.preventDefault();
        // スクロール感覚
        let scrollInterval = 700;

        // スクロール量を取得
        count += e.originalEvent.deltaY
        if (count > scrollInterval ) {

            scrollRoutes.addIndex(-1);
            count = 0;
            // 1秒後にcountをリセット
            setTimeout(function(){
                count = 0;
            }, 100);

        } else if(count < -scrollInterval) {
            
            scrollRoutes.addIndex(1);
            count = 0;
            // 1秒後にcountをリセット
            setTimeout(function(){
                count = 0;
            }, 100);
        }
      });
    } else {
      $(window).off('wheel');
    }

    // チェックされた時
    $('.ek-check').change(function(){
        let count = $('input[name="ek"]:checked').length;
        if(count > 0) {
            $('.submit-box').css("display", "block");
        } else {
            $('.submit-box').css("display", "none");
        }
    });
});


class ScrollRoutes {

    constructor() {
        this.$content = $("#route-conents");
        this.$routeList = this.$content.find("li");
        this.$stationFromBox = $('#station-form');
        this._trainSvg = new TrainSvg();
        this._colorBox = new ColorBox();
        this._routeObjectList = [];
        // 画面に表示する個数
        this._displayCount = 8;
        // 選択対象のインデックス
        this._baseIndex = 4;
        // 現在のインデックス
        this._fowardIndex = 13;

        // リストのオブジェクトを作成
        var self = this;
        var index = -9;
        this.$routeList.each(function() {

            let route = $(this);
            self._routeObjectList.push(new Route(route, self , self._trainSvg, index));
            index++;
        })
    }

    indicateContentAll() {

        for (let obj of this._routeObjectList) {
            obj.indicateContent();
        }
    }

    addIndex(index) {

        // 対象のインデックス番号
        let fowardIndex = this._fowardIndex - index;
        // 最大のインデックス番号
        let maxIndex = this.$routeList.length;
        if (fowardIndex <  maxIndex && fowardIndex >= 0) {

            for (let obj of this._routeObjectList) {
                obj.addIndex(index);
            }
            this._fowardIndex -= index;
            this.indicateContentAll();
        }
    }
}

class Route {

    constructor($content, scrollRoute, trainSvg, index) {
        this.$content = $content;
        this.$scrollRoute = scrollRoute;
        this.$stationForm = $("#" + this.$content.data('formid'));
        this._trainSvg = trainSvg;
        this._originalIndex = index;
        this._index = index;
        this._color = this.$content.css('border-color');
        // 角度
        this._baseDegree = 10;
        this._x = 0;
        this._y = 0;

        // クリックイベントを設定
        let self = this;
        this.$content.on('click', function(){

            let difference = self._index - self.$scrollRoute._baseIndex;
            self.$scrollRoute.addIndex(-difference);
        })

        // 電車のsvgを作成
        let train = $('.train-svg:first').clone();
        train.find('span').text(this.$content.data('name'));
        train.find('path').css("fill", this._color);
         // 電車のアイコン
        this._train = train;

        this.indicateContent();
    }

    setCss() {
        // this.$content.css("left", this._x + "px");
        // this.$content.css("top", this._y + "px");
        this.$content.animate({
            "left": this._x + "px",
            "top": this._y + "px"
        })

        // 選択されている時に適応するCSS
        if(this._index == this.$scrollRoute._baseIndex) {

            // アイコンサイズを大きく
            this.$content.animate({
                "width" : "140px",
                "height": "140px",
                "fontSize": "50px",
                "borderWidth" : "20px",
            })

            // 電車を表示
            this._trainSvg.add(this._train);
            this.$scrollRoute.$stationFromBox.html(this.$stationForm);
            // フォームを押したらいろを変更
            $('#station-form .station-label').on('click', function() {

                let color = $(this).find('span').css('border-color');
                if (color == "rgb(204, 204, 204)") {
                    $(this).find('span').css('border-color', "#da3c41")
                } else {
                    $(this).find('span').css('border-color', "#cccccc")
                }
            })
            this.$scrollRoute._colorBox.changeColor(this._color);
        } else {
            this.$content.animate({
                "width" : "70px",
                "height": "70px",
                "fontSize": "25px",
                "borderWidth" : "10px",
            })
        }
    }

    // xとyをセットし、画面の描画をかえる
    indicateContent() {
        this.setOvalPosition();
        this.setCss();
        
    }

    addIndex(index) {
        this._index += index; 
    }

    /**
     * 楕円の円周上の x, y 座標を返す
     *
     * @param  degree  角度
     * @param  radiusX  横半径
     * @param  radiusY  縦半径
     */
    setOvalPosition () {
        var obj = {};

        // 角度
        let degree = 90 - this._index * this._baseDegree;
        // ラジアンに変換
        var radian = degree * (Math.PI / 180);
        // 半径
        var radius = 850;
        var cos = Math.cos(radian);
        var sin = Math.sin(radian);

        this._x = radius - cos * radius;
        this._y = radius - sin * radius;
    }
}

class TrainSvg {

    constructor() {
        this.$content = $('#train-box');
        this.$trains = $('.train-svg');
    }

    add(trainSvg) {
        let width = $('.train-svg:last').width() + 200;
        trainSvg.css("left", width);
        this.$content.find('#trains').append(trainSvg);

        $('.train-svg').each(function(i, train){

            let left = $(train).position().left;
            $(train).animate({
                "left": left - width
            })

            width = $(train).width() +200;
        })

        setTimeout(() => {
            this.$content.find('div:first-child').find('div:first-child').remove();
        }, 200);
    }
}

class ColorBox {

    constructor() {

        this.$content = $('.color-box');
        this.$stationForm = $('#station-form');
        this.$content.each(function(i){
            $(this).addClass("rotate-" + (i + 1));
        })
    }

    changeColor(colorCode) {
        this.$content.last().css("background-color", colorCode);
        this.aminate();
    }

    aminate() {
        
        let stations = this.$stationForm;
        stations.addClass('no-rotate');
        this.$content.each(function(i){
            $(this).addClass("no-rotate");
            $(this).addClass("rotate-" + (i + 1));
            setTimeout(() => {
                $(this).removeClass("no-rotate");
            }, 600);
            
        })
        setTimeout(() => {
            stations.removeClass('no-rotate');
        }, 600);
    }
}


// ----------------------------------------------------
class MoreBtn {

    constructor() {
        this.$content = $('.more-btn ');
        this.$condition = $('.condition-box');
        
        let self = this;
        this.$content.on('click', function(e){

            e.preventDefault();
            // 現在の高さを取得
            let nowWidth = self.$condition.width();
            // 表示の切り替え
            if (nowWidth == 0) {
                self.$condition.animate({
                    "width" : "100vw",
                    "height": $('#routes-form').height()
                }, 500)
            } else {
                self.$condition.animate({
                    "width" : "0",
                    "height": "0"
                }, 500)
            }
           
        })
    }
}