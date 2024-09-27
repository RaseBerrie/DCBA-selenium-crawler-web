from main import db
from functions.models import ResDefData, ResGitData, ResCacheData, ListComp, ListRoot, ListSub, TagFile, TagExp

def query_joiner(id, query, searchengine, git=False):
    if git: Data = ResGitData
    else: Data = ResDefData

    if id["comp"][0] == 0:
        result = query

    elif id["root"][0] == 0:
        result = query.join(ListSub, ListSub.url == Data.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .join(ListComp, ListComp.company == ListRoot.company)\
                    .filter(ListComp.id == id["comp"][0])
    elif id["sub"][0] == 0:
        result = query.join(ListSub, ListSub.url == Data.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .filter(ListRoot.id == id["root"][0])
    else:
        result = query.join(ListSub, ListSub.url == Data.subdomain)\
            .filter(ListSub.id == id["sub"][0])
    
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
        try: def_data = data.ResDefData
        except: def_data = data
        
        try: def_cache = data.url
        except: def_cache = None

        try: exp_data = data.TagExp
        except: pass

        tmp = list()

        if def_data.searchengine == "G": tmp.append("Google")
        elif def_data.searchengine == "B": tmp.append("Bing")

        try: tmp.append(def_data.res_url.split("/")[2].split(":")[1])
        except: tmp.append("default")

        tmp.append(def_data.subdomain)
        tmp.append(def_data.res_title)
        tmp.append(def_data.res_url)

        try: tmp.append(exp_data.exp_content)
        except: tmp.append(def_data.res_content)

        if def_cache is not None: tmp.append(1)
        else: tmp.append(0)
        
        result.append(tmp)
    return result

def file_fining(datas):
    result = []
    for line in datas:
        tmp = []

        if line.ResDefData.searchengine == "G": tmp.append("Google")
        elif line.ResDefData.searchengine == "B": tmp.append("Bing")
        
        try: tmp.append(line.TagFile.url.split("/")[2].split(":")[1])
        except: tmp.append("default")

        tmp.append(line.ResDefData.subdomain)
        tmp.append(line.TagFile.filetype.upper())
        tmp.append(line.TagFile.title)
        tmp.append(line.TagFile.url)
        tmp.append("None")

        result.append(tmp)
    return result