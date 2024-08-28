from main import db

from sqlalchemy import and_
from functions.models import ResData, ListComp, ListRoot, ListSub, TagFile

def def_temp_table(id, public, git=False):
    query = db.session.query(ResData)
    
    if id["comp"][0] == 0: pass

    elif id["root"][0] == 0:
        query = query.join(ListSub, ListSub.url == ResData.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .join(ListComp, ListComp.company == ListRoot.company)\
                    .filter(ListComp.id == id["comp"][0])

    elif id["sub"][0] == 0:
        query = query.join(ListSub, ListSub.url == ResData.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .filter(ListRoot.id == id["root"][0])

    else:
        query = query.join(ListSub, ListSub.url == ResData.subdomain)\
            .filter(ListSub.id == id["sub"][0])

    if git:
        result = query.filter(ResData.tags == 'git')
    else:
        if public:
            result = query.filter(and_(ResData.tags != 'public', ResData.tags != 'git'))
        else:
            result = query.filter(ResData.tags != 'git')

    return result
        
def file_temp_table(id):
    query = db.session.query(ResData, TagFile).join(TagFile, TagFile.id == ResData.id)

    if id["comp"][0] == 0: pass
    
    elif id["root"][0] == 0:
        query = query.join(ListSub, ListSub.url == ResData.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .join(ListComp, ListComp.company == ListRoot.company)\
                    .filter(ListComp.id == id["comp"][0])

    elif id["sub"][0] == 0:
        query = query.join(ListSub, ListSub.url == ResData.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .filter(ListRoot.id == id["root"][0])

    else:
        query = query.join(ListSub, ListSub.url == ResData.subdomain)\
            .filter(ListSub.id == id["sub"][0])

    return query
    
def data_fining(datas):
    result = []
    for res_data in datas:
        tmp = []

        if res_data.searchengine == "G": tmp.append("Google")
        elif res_data.searchengine == "B": tmp.append("Bing")

        tmp.append(res_data.subdomain)
        tmp.append(res_data.res_title)
        tmp.append(res_data.res_url)
        tmp.append(res_data.res_content)
        result.append(tmp)

    return result

def file_fining(datas):
    result = []
    for line in datas:
        tmp = []

        if line.ResData.searchengine == "G": tmp.append("Google")
        elif line.ResData.searchengine == "B": tmp.append("Bing")
        
        tmp.append(line.ResData.subdomain)
        tmp.append(line.TagFile.filetype.upper())
        tmp.append(line.TagFile.title)
        tmp.append(line.TagFile.url)
        tmp.append("None")

        result.append(tmp)
    return result