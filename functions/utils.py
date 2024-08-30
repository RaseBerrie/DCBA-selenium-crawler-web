from main import db

from sqlalchemy import and_
from functions.models import ResDefData, ResGitData, ListComp, ListRoot, ListSub, TagFile

def def_temp_table(id, public, git=False):
    if git:
        query = db.session.query(ResGitData)
        
        if id["comp"][0] == 0: result = query

        elif id["root"][0] == 0:
            result = query.join(ListSub, ListSub.url == ResGitData.subdomain)\
                .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                    .join(ListComp, ListComp.company == ListRoot.company)\
                        .filter(ListComp.id == id["comp"][0])
        elif id["sub"][0] == 0:
            result = query.join(ListSub, ListSub.url == ResGitData.subdomain)\
                .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                    .filter(ListRoot.id == id["root"][0])
        else:
            result = query.join(ListSub, ListSub.url == ResGitData.subdomain)\
                .filter(ListSub.id == id["sub"][0])
    else:
        query = db.session.query(ResDefData)
        
        if id["comp"][0] == 0: pass

        elif id["root"][0] == 0:
            query = query.join(ListSub, ListSub.url == ResDefData.subdomain)\
                .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                    .join(ListComp, ListComp.company == ListRoot.company)\
                        .filter(ListComp.id == id["comp"][0])
        elif id["sub"][0] == 0:
            query = query.join(ListSub, ListSub.url == ResDefData.subdomain)\
                .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                    .filter(ListRoot.id == id["root"][0])
        else:
            query = query.join(ListSub, ListSub.url == ResDefData.subdomain)\
                .filter(ListSub.id == id["sub"][0])

        if public: result = query.filter(ResDefData.tags != 'public')
        else: result = query

    return result
        
def file_temp_table(id):
    query = db.session.query(ResDefData, TagFile).join(TagFile, TagFile.id == ResDefData.id)

    if id["comp"][0] == 0: pass
    
    elif id["root"][0] == 0:
        query = query.join(ListSub, ListSub.url == ResDefData.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .join(ListComp, ListComp.company == ListRoot.company)\
                    .filter(ListComp.id == id["comp"][0])

    elif id["sub"][0] == 0:
        query = query.join(ListSub, ListSub.url == ResDefData.subdomain)\
            .join(ListRoot, ListRoot.url == ListSub.rootdomain)\
                .filter(ListRoot.id == id["root"][0])

    else:
        query = query.join(ListSub, ListSub.url == ResDefData.subdomain)\
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

        if line.ResDefData.searchengine == "G": tmp.append("Google")
        elif line.ResDefData.searchengine == "B": tmp.append("Bing")
        
        tmp.append(line.ResDefData.subdomain)
        tmp.append(line.TagFile.filetype.upper())
        tmp.append(line.TagFile.title)
        tmp.append(line.TagFile.url)
        tmp.append("None")

        result.append(tmp)
    return result