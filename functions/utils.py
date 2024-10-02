from main import db
from functions.models import ResDefData, ResGitData, ResCacheData, ListComp, ListRoot, ListSub, TagFile, TagExp
from urllib.parse import urlparse

def query_joiner(id, query, searchengine, git=False):
    Data = ResGitData if git else ResDefData

    if id["comp"][0] == 0: result = query
    else:
        result = query.join(ListSub, ListSub.url == Data.subdomain)
        if id["sub"][0] != 0: result = result.filter(ListSub.id == id["sub"][0])
        else:
            result = result.join(ListRoot, ListRoot.url == ListSub.rootdomain)
            if id["root"][0] != 0: result = result.filter(ListRoot.id == id["root"][0])
            else:
                result = result.join(ListComp, ListComp.company == ListRoot.company)
                if id["comp"][0] != 0: result = result.filter(ListComp.id == id["comp"][0])
        
    if searchengine != "All":
        result = result.filter(Data.searchengine == searchengine)

    return result

def def_query(id, public, searchengine, git=False):
    if git:
        query = db.session.query(ResGitData)
        result = query_joiner(id, query, searchengine, git=True)

        if public: result = result.filter(ResGitData.filtered == 1)
    else:
        query = db.session.query(ResDefData, ResCacheData.url)
        query = query.join(ResCacheData, ResCacheData.url == ResDefData.res_url, isouter=True)
        result = query_joiner(id, query, searchengine)
        
        if public: result = result.filter(ResDefData.tags != 'public')

    return result
        
def file_query(id, public):
    query = db.session.query(ResDefData, TagFile)\
        .join(TagFile, TagFile.id == ResDefData.id)
    result = query_joiner(id, query, searchengine="All")

    if public: result = result.filter(TagFile.is_link == '0')
    return result

def exp_query(id, searchengine):
    query = db.session.query(ResDefData, TagExp)\
        .join(TagExp, TagExp.id == ResDefData.id)
    result = query_joiner(id, query, searchengine)

    return result
    
def data_fining(datas):
    result = []
    for data in datas:
        def_data = getattr(data, 'ResDefData', data)
        def_cache = getattr(data, 'url', None)
        exp_data = getattr(data, 'TagExp', None)
        
        tmp = []
        tmp.append("Google" if def_data.searchengine in ["G", "g"] 
                   else "Bing" if def_data.searchengine in ["B", "b"]
                   else None)
        try:
            parsed_url = urlparse(def_data.res_url)
            port = parsed_url.port if parsed_url.port else "default"
            tmp.append(f"{port}")
        except:
            tmp.append("default")

        tmp.append(def_data.subdomain)
        tmp.append(def_data.res_title)
        tmp.append(def_data.res_url)

        tmp.append(exp_data.exp_content if exp_data else def_data.res_content)
        tmp.append(1 if def_cache is not None else 0)

        result.append(tmp)

    return result

def file_fining(datas):
    result = []

    for line in datas:
        tmp = []
        tmp.append("Google" if line.ResDefData.searchengine == "G"
                else "Bing" if line.ResDefData.searchengine == "B"
                else "default")
        try:
            parsed_url = urlparse(line.TagFile.url)
            port = parsed_url.port if parsed_url.port else "default"
            tmp.append(f"{port}")
        except:
            tmp.append("default")

        tmp.append(line.ResDefData.subdomain)
        tmp.append(line.TagFile.filetype.upper())
        tmp.append(line.TagFile.title)
        tmp.append(line.TagFile.url)
        tmp.append("None")

        result.append(tmp)

    return result