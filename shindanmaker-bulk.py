#!/usr/bin/env python3
# shindanmaker-bulk.py - Get multiple result at once
import sys
from bs4 import BeautifulSoup
import requests

# ljustを全角に対応させたljust_ja
# from: http://d.hatena.ne.jp/hush_puppy/20090226/1235661269
import unicodedata

# 左寄せ
def ljust_ja(str, size, pad = " "):
    space = size - width_kana(str)
    if space > 0:
        str += pad * space
    return str

# 幅(半角基準)
def width_kana(str):
    all = len(str)      # 全文字数
    zenkaku = count_zen(str)        # 全角文字数
    hankaku = all - zenkaku     # 半角文字数

    return zenkaku * 2 + hankaku

# 全角文字数
def  count_zen(str):
    n = 0
    for c in str:
        wide_chars = u"WFA"
        eaw = unicodedata.east_asian_width(c)
        if wide_chars.find(eaw) > -1:
            n += 1
    return n


if len(sys.argv) < 3:
    print('Usage: {} id name1 name2 ...')
    sys.exit(1)

# set values
id = sys.argv[1]

names_dict = {
    'sakuramochi': ['さくらもち', 'sakuramochi_0', 'sakuramochi', 'sakuramochi0'],
    'hapi': ['愛乃めぐみ', 'めぐみちゃん', 'めぐみ', 'キュアラブリー',
              '白雪ひめ', 'ひめちゃん', 'ひめ', 'ヒメルダ・ウィンドウ・キュアクイーン・オブ・ザ・ブルースカイ', 'ヒメルダ',
              '大森ゆうこ', 'ゆうこ', 'ゆうゆう', 'キュアハニー',
              '氷川いおな', 'いおなちゃん', 'いおな', 'キュアフォーチュン',
              'リボン', 'ぐらさん', 'ブルー', '地球の神 ブルー', 
              'ナマケルダ', 'ホッシーワ', 'オレスキー', 'ファントム', 'アンラブリー', 'クイーンミラージュ', 'ディープミラー'],
    'doki': ['マナ', '六花', 'ありす', '真琴', 'あぐり', 'レジーナ',
             'マナちゃん', '六花ちゃん', 'ありすちゃん', 'まこぴー', 'あぐりちゃん',
             '岡田', 'ジョー岡田', 'ジョナサン', 'ジョナサン・クロンダイク', 'アン', 'マリー・アンジュ', 'ジョナサン大統領', 
             '相田マナ', '菱川六花', '剣崎真琴', '四葉ありす', '円亜久里',
             'キュアハート', 'キュアダイヤモンド', 'キュアロゼッタ', 'キュアソード', 'キュアエース',
             'シャルル', 'シャルルちゃん', 'ラケル', 'ラケルくん', 'ランス', 'ランスちゃん', 'ダビィ',
             'イーラ', 'マーモ', 'ベール', 'グーラ', 'リーヴァ', 'キングジコチュー'],
    'heart': ['花咲つぼみ', 'つぼみ', 'キュアブロッサム', '来海えりか', 'えりか', 'キュアマリン',
              '明堂院いつき', 'いつき', 'キュアサンシャイン', '月影ゆり', 'ゆり', 'キュアムーンライト',
              '花咲薫子', 'キュアフラワー',
              'シプレ', 'コフレ', 'ポプリ', 'コッペ様',
              'デューン', 'サバーク', 'サバーク博士', 'ダークプリキュア',
              'サソリーナ', 'クモジャキー', 'コブラージャ', 'スナッキー', 'デザトリアン',
              '来海ももか', '志久ななみ', '番ケンジ'],
              
    'rl': ['綾瀬なる', 'なる', '福原あん', 'あん', '涼野いと', 'いと', 'りんね', '荊千里', 'モモ', 'DJ.Coo',
           'ラブリン', 'ポップン', 'クルン', 'ピコック', 'フェミニ', 'エスニ', 'セシニ', 'スタン', 'ペンギン先生', '赤井めが姉ぇ', 'めが姉ぇ',
           '蓮城寺べる', '小鳥遊おとは', '森園わかな', 'べる', 'おとは', 'わかな',
           '速水ヒロ', 'ヒロ', '神浜コウジ', 'コウジ', '仁科カズキ', 'カズキ', '涼野弦',
           '天羽ジュネ', 'ジュネ', '氷室聖', '神浜奈津子',
           '法月仁', '田中さん'],

    'kinpri': [
        '一条シン', 'シン', 'シンくん', '香賀美タイガ', 'タイガ', 'タイガくん', '十王院カケル', 'カケル', 'カケルくん',
        '太刀花ユキノジョウ', 'ユキノジョウ', 'ユキ様', '西園寺レオ', 'レオ', 'レオくん',
        '高梁ミナト', 'ミナト', 'ミナトくん', '涼野ユウ', 'ユウ', 'ユウくん',
        '如月ルヰ', 'ルヰ', 'ルヰくん', '大和アレクサンダー', 'アレクサンダー', 'アレク',
        '山田さん',
    ],

'pripara': ['真中らぁら', '南みれぃ', '北条そふぃ', '東堂シオン', 'ドロシー・ウェスト', 'レオナ・ウェスト', 'ファルル',
            'クマ', 'ウサギ', 'ユニコン', '赤井めが姉ぇ', '赤井めが兄ぃ', '栄子ちゃん',
            'ななみ', 'きゅぴこん', '栃乙女愛', '香川いろは',
            '大神田グロリア', 'なおちゃん', '定子ちゃん', 'ちゃん子ちゃん',
            '雨宮くん', '真中のん', '北条コスモ']
    }

arg = sys.argv[2]
if arg in names_dict.keys():
    names = names_dict[arg]
elif arg.endswith('-couple'):
    arg = arg.replace('-couple', '')
    names = ['が'.join((i, j)) for i in names_dict[arg] for j in names_dict[arg] if i not in j and j not in i]
else:
    names = sys.argv[2:]

# get results
for name in names:
    url = 'https://shindanmaker.com/' + id
    r = requests.post(url, {'u': name})
    soup = BeautifulSoup(r.text, 'lxml')
    text = ' '.join(soup.select('#forcopy')[0].text.split('\n'))
    print('{} {}'.format(ljust_ja(name, 30), text))
