import MeCab
from collections import Counter, defaultdict
import json
import re
import requests
class Analyzer:

    

    def __init__(self):
        self.tagger = MeCab.Tagger("-Ochasen")
        self.tagger.parse("")

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
    
    def feature_analysis(self, content, json_file):
        f = open(json_file, "r")
        json_data = json.load(f)
        jiku_list = json_data["all_jiku"]["all_jiku_list"]
        #['赤酢', '握り', 'シャリ']
        pare = defaultdict(int)
        n = 0
        dic = defaultdict(int)
        content = re.sub("[♪！!？… \. \?]", "。", content)
        content = re.sub("。+","。",content)
        sentences = re.split("[♪。！!？… \. \?]", content)
        #sentences = content.split("。")
        l = []
        #一つのレビューを文単位に分割
        for sentence in sentences:
            t = self.tokenize(sentence)
            n += len(t)
            for jiku in jiku_list:
                jiku_group = json_data["all_jiku"][jiku]["jiku_group"]
                #['握り', 'にぎり', 'ニギリ']
                syusyoku_list = json_data["all_jiku"][jiku]["syusyoku"]["syusyoku_list"]
                #['大きい', '小さい', '創作']
                for tt in t:
                    if tt in jiku_group:
                        dic[jiku] += 1
                for syusyoku in syusyoku_list:
                    syusyoku_group = json_data["all_jiku"][jiku]["syusyoku"][syusyoku]
                    #[['大きい'], ['でかい'], ['大きめ'], ['ビッグ']]
                    for tt in t:
                        if tt in jiku_group:
                            for s in syusyoku_group:
                                if len(list(set(s) & set(t))) == len(s):
                                    pare[(jiku, syusyoku)] += 1
        for jiku in jiku_list:
            ll = []
            ll.append(jiku)
            ll.append(dic[jiku])
            for syusyoku in json_data["all_jiku"][jiku]["syusyoku"]["syusyoku_list"]:
                ll.append([syusyoku, pare[(jiku, syusyoku)]])
            l.append(ll)
        return l
    
    def gcp_analyzer(self, text, key):
        url = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=' + key
        header = {'Content-Type': 'application/json'}
        text_ = re.sub("[♪！!？… \. \?]", "。", text)
        text__ = re.sub("。+","。",text_)
        result = []
        body = {
                "document": {
                    "type": "PLAIN_TEXT",
                    "language": "JA",
                    "content": text__
                },
                "encodingType": "UTF8"
            }
        response = requests.post(url, headers=header, json=body).json()
        for i in response["sentences"]:
            result.append([i["text"]["content"],i["sentiment"]["magnitude"],i["sentiment"]["score"]])
            #文の中身,magnitude,score
        return result

    def get_posinega(self, text_dic, json_file):
        f = open(json_file, "r")
        json_data = json.load(f)
        jiku_list = json_data["all_jiku"]["all_jiku_list"]
        #['赤酢', '握り', 'シャリ']
        posinega_dic = defaultdict(float)
        for text in text_dic:
            t = self.tokenize(text[0])
            for jiku in jiku_list:
                jiku_group = json_data["all_jiku"][jiku]["jiku_group"]
                #['握り', 'にぎり', 'ニギリ']
                syusyoku_list = json_data["all_jiku"][jiku]["syusyoku"]["syusyoku_list"]
                #['大きい', '小さい', '創作']
                for ji in jiku_group:
                    if ji in t:
                        for syusyoku in syusyoku_list:
                            syusyoku_group = json_data["all_jiku"][jiku]["syusyoku"][syusyoku]
                            #[['大きい'], ['でかい'], ['大きめ'], ['ビッグ']]
                            for s in syusyoku_group:
                                if len(list(set(s) & set(t))) == len(s):
                                    if text[2] > 0:
                                        positive_dic[(jiku,syusyoku)] += text[1]*text[2]
                                    elif text[2] < 0:
                                        positive_dic[(jiku,syusyoku)] += -text[1]*text[2]
        return positive_dic, negative_dic  