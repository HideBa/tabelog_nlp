import MeCab
from collections import Counter, defaultdict
class Analyzer:
    akazu = ["赤酢"]
    nigiri = ["握り","にぎり","ニギリ"]
    shari = ["シャリ","コメ","米","ライス","こめ","しゃり"]
    maguro = ["まぐろ","マグロ","鮪","赤身","トロ","とろ"]
    wine = ["ワイン"]

    akazu_ad = [["強い","強め","きつい","つよい","つよめ","効く"],
        ["あっさり","シンプル"],
        ["酸っぱい","すっぱい","酸味"]]

    nigiri_ad = [["大きい","でかい","大きめ","ビッグ"],
            ["小さい","小ぶり","小さめ"],
            ["創作","奇想天外","工夫","独特","意外","面白い","おもしろい"]]

    shari_ad = [["大きい","でかい","大きめ","ビッグ"],
           ["小さい","小ぶり","小さめ"],
           ["パラパラ","少ない"],
           ["塩気","塩","しょっぱい"],
           ["甘い","甘め","あまい","あまめ","砂糖"],
           ["酢","米酢","白酢"]]

    maguro_ad = [["うまい","美味","美味しい","おいしい","良い","よい","いい"],
            ["臭い","くさい","生臭い"],
            ["あっさり"],
            ["こってり"],
            ["とろける","消える"],
            ["酸味"],
            ["熟成"]]

    wine_ad = [["多い","豊富","品揃え","品ぞろえ","取り揃え"],
            ["相性","マリアージュ", "合う"]]
    
    features = [akazu, nigiri, shari, maguro, wine]
    features_ad = [akazu_ad, nigiri_ad, shari_ad, maguro_ad, wine_ad]
    all_features = [[akazu, akazu_ad], [nigiri,nigiri_ad],[shari, shari_ad],
    [maguro, maguro_ad], [wine, wine_ad]]
    def __init__(self):
        self.tagger = MeCab.Tagger("-Ochasen \
        -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd \
         -u /Users/yuki/foo/bar/user_dic2.dic")
        
        self.tagger.parse("")
        self.features = features
        self.features_ad = features_ad
        self.all_features = all_features


    def _tokenize_ja(self, text):
        node = self.tagger.parseToNode(str(text)) #分かち書きしたのが入っている。イテレータ
        while node:
            surface = node.surface.lower() #surfaceは単語の見た目　例：トろ
            feature = node.feature.split(",")
            hinshi = feature[0]
            genkei = feature[6]
            if surface != "" and hinshi in ["形容詞", "動詞", "副詞", "助動詞", "接続詞", "連体詞", "感動詞", "接頭詞"]:
                yield genkei
            elif surface != "" and hinshi == "名詞":
                yield surface
            node = node.next
    
    def tokenize(self, content):
        return [token for token in self._tokenize_ja(content)]
    
    def add_features(self, feature_list, feature_ad_list):
        self.features.append(feature_list)
        self.features_ad.append(feature_ad_list)
    
