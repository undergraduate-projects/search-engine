from django.http import HttpResponse, JsonResponse
from client.client import es, INDEX


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
    assert request.method == "GET"
    resp = es.search(index="case-data", 
                    query={
                        "query_string": {
                            "query": request.GET["query"],
                    }},
                    fields=["自定义*", "全文*", "法条"],
                    highlight={
                        "fields": {
                            "自定义*": {},
                            "全文*": {},
                            "法条": {}
                        }
                    },
                    from_=request.GET["offset"])
    data = []
    for hit in resp['hits']['hits']:
        source = hit['_source']
        highlight = hit['highlight']
        for (key, val) in highlight.items():
            update_key(key.split('.'), val[0], source)
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
        'offset': request.GET["offset"],
        'data': data
    }, json_dumps_params={'ensure_ascii':False})
    
