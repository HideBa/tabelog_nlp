import requests
import re
class GCP_analyze:
    def __init__(self):
        pass

    def gcp_analyzer(text, key):
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