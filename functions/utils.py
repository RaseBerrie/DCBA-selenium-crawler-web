from main import db
from functions.models import ResDefData, ResGitData, ListComp, ListRoot, ListSub, TagFile, TagExp

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
    else:
        query = db.session.query(ResDefData)
        result = query_joiner(id, query, searchengine)
        
        if public: result = result.filter(ResDefData.tags != 'public')

    return result
        
def file_query(id):
    query = db.session.query(ResDefData, TagFile)\
        .join(TagFile, TagFile.id == ResDefData.id)
    result = query_joiner(id, query, searchengine="All")

    return result

def exp_query(id, searchengine):
    query = db.session.query(ResDefData, TagExp)\
        .join(TagExp, TagExp.id == ResDefData.id)
    result = query_joiner(id, query, searchengine)

    return result
    
def data_fining(datas):
    result = []
    for res_data in datas:
        try:
            line = res_data.ResDefData
        except:
            line = res_data

        tmp = []

        if line.searchengine == "G": tmp.append("Google")
        elif line.searchengine == "B": tmp.append("Bing")

        tmp.append(line.subdomain)
        tmp.append(line.res_title)
        tmp.append(line.res_url)
        try:
            tmp.append(res_data.TagExp.exp_content)
        except:
            tmp.append(line.res_content)
        
        result.append(tmp)
    return result

def file_fining(datas):
    result = []
    for line in datas:
        tmp = []

        if line.ResDefData.searchengine == "G": tmp.append("Google")
        elif line.ResDefData.searchengine == "B": tmp.append("Bing")
        
        tmp.append(line.ResDefData.subdomain)
        tmp.append(line.TagFile.filetype.upper())
        tmp.append(line.TagFile.title)
        tmp.append(line.TagFile.url)
        tmp.append("None")

        result.append(tmp)
    return result