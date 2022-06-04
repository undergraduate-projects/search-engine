from django.http import HttpResponse, JsonResponse
from client.client import es, INDEX
from .utils import tc_wv_model, stop_words
import xml.etree.ElementTree as ET
import numpy as np
import jieba
import json


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


def update_key(key_list, val, dic):
    key = key_list[0]
    try:
        v = dic[key]
        if isinstance(v, dict) and len(key_list) > 1:
            key_list.remove(key)
            update_key(key_list, val, v)
        elif isinstance(v, list):
            target = val.replace("<em>", "")
            target = target.replace("</em>", "")
            for idx in range(len(v)):
                if v[idx] == target:
                    dic[key][idx] = val
                    break
        elif isinstance(v, str):
            dic[key] = val
    except:
        print(f"exception at dic: {dic}")


def search_basic(request):
    if request.method != "GET":
        return HttpResponse("Only GET method is supported.")
    resp = es.search(index=INDEX, 
                    query={
                        "query_string": {
                            "query": request.GET.get("query", "no"),
                    }},
                    fields=["自定义*", "全文*", "法条", "案例属性*"],
                    highlight={
                        "fields": {
                            "自定义*": {},
                            "全文*": {},
                            "法条": {},
                            "案例属性*": {},
                        }
                    },
                    from_=request.GET.get("offset", 0))
    data = []
    for hit in resp['hits']['hits']:
        source = hit['_source']
        highlight = hit['highlight']
        for (key, val) in highlight.items():
            update_key(key.split('.'), val[0], source)
        val_set = set()
        unique_highlight = dict()
        for (key, val) in highlight.items():
            v = val[0] if len(val) == 1 else ''.join(val)
            if v not in val_set:
                val_set.add(v)
                unique_highlight[key] = val
        data.append({
            'id': hit['_id'],
            'source': source,
            'highlight': highlight
        })
    print(len(data))
    # res = [case['_source'] for case in case_list]
    return JsonResponse(data={
        'total': resp['hits']['total']['value'],
        'size': 10,
        'offset': request.GET.get("offset", 0),
        'data': data
    }, json_dumps_params={'ensure_ascii':False})
    

def AY_search(AY):
    resp = es.search(index=INDEX,
                    from_=0,
                    size=20,
                    query={
                        "match": {
                            "案例属性.案由": AY,
                    }},
                    highlight={
                        "fields": {
                            "案例属性.案由": {},
                        }
                    }
            )
    return resp['hits']['hits']


def JBFY_search(JBFY):
    resp = es.search(index=INDEX,
                    from_=0,
                    size=20,
                    query={
                        "match": {
                            "案例属性.经办法院": JBFY,
                    }},
                    highlight={
                        "fields": {
                            "案例属性.经办法院": {},
                        }
                    }
            )
    return resp['hits']['hits']


def FGCY_serach(FGCY):
    assert isinstance(FGCY, list)
    resp = es.search(index=INDEX,
                    from_=0,
                    size=20,
                    query={
                        "match": {
                            "案例属性.法官成员": " ".join(FGCY),
                    }},
                    highlight={
                        "fields": {
                            "案例属性.法官成员": {},
                        }
                    }
            )
    return resp['hits']['hits']


def knn_search(query_vector, k=20, num_candidates=100):
    resp = es.knn_search(index=INDEX, 
                knn={
                    "field": "vec",
                    "query_vector": query_vector,
                    "k": k,
                    "num_candidates": num_candidates
                }
            )
    return resp['hits']['hits']


def search_recommend(request):
    if request.method != "GET":
        return HttpResponse("Only GET method is supported.")
    query_vector = request.GET.get("query_vector", "")
    AY = request.GET.get("AY", "")
    JBFY = request.GE.get("JBFY", "")
    FGCY = request.GET.get("FGCY", [])
    knn_data = knn_search(query_vector)
    AY_data = AY_search(AY)
    JBFY_data = JBFY_search(JBFY)
    FGCY_data = FGCY_serach(FGCY)
    return JsonResponse(data={
        'total': len(knn_data) + len(AY_data) + len(JBFY_data) + len(FGCY_data),
        'size': 10,
        'offset': 0,
        'data': {
            'knn': knn_data,
            'AY': AY_data,
            'JBFY': JBFY_data,
            'FGCY': FGCY_data
        }
    }, json_dumps_params={'ensure_ascii':False})


def search_by_case(request):
    if request.method != "GET":
        return HttpResponse("Only GET method is supported.")
    # print(request.body)
    body = json.loads(request.body)
    xml_str = body["xml_str"]
    # print(xml_str)
    root = ET.fromstring(xml_str)
    text = root.find('QW').attrib['value']
    # print(text)
    text = list(filter(lambda x:x not in stop_words, jieba.lcut(text)))
    query_vector = np.zeros(100)
    for word in text:
        try:
            query_vector += np.array(tc_wv_model[word])
        except:
            continue
    query_vector /= len(text)
    data = knn_search(query_vector, k=50, num_candidates=200)
    return JsonResponse(data={
        'total': len(data),
        'size': 10,
        'offset': 0,
        'data': data
    }, json_dumps_params={'ensure_ascii':False})


def search_by_id(request):
    if request.method != "GET":
        return HttpResponse("Only GET method is supported.")
    try:
        resp = es.get(index="case-data", id=request.GET.get("id", 0))
        return JsonResponse(data={
                'data': resp['_source']
            }, json_dumps_params={'ensure_ascii':False})
    except:
        return HttpResponse("No such id.")
    