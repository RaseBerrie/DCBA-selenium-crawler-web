from main import db

class ListComp(db.Model):
    __tablename__ = 'list_company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'''
        <ListComp id={self.id} company={self.company}>'''
    
class ListRoot(db.Model):
    __tablename__ = 'list_rootdomain'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'''
        <ListComp id={self.id} company={self.company} url={self.url}>'''
    
class ListSub(db.Model):
    __tablename__ = 'list_subdomain'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rootdomain = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    is_root = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'''
        <ListComp id={self.id} rootdomain={self.rootdomain} url={self.url}, is_root={self.is_root}>'''

class ResDefData(db.Model):
    __tablename__ = 'res_data_def'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    searchengine = db.Column(db.String(1), nullable=False)
    subdomain = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(100), nullable=False, default="") 
    res_title = db.Column(db.String(100), nullable=False)
    res_url = db.Column(db.Text, nullable=False)
    res_content = db.Column(db.Text)
    update_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'''
        <ResDefData id={self.id} searchengine={self.searchengine} subdomain={self.subdomain} tags={self.tags}
        res_title={self.res_title} res_url={self.res_url} res_content={self.res_content} update_time={self.update_time}>'''
    
class ResGitData(db.Model):
    __tablename__ = 'res_data_git'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    searchengine = db.Column(db.String(1), nullable=False)
    subdomain = db.Column(db.String(50), nullable=False)
    res_title = db.Column(db.String(100), nullable=False)
    res_url = db.Column(db.Text, nullable=False)
    res_content = db.Column(db.Text)
    update_time = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'''
        <ResGitData id={self.id} searchengine={self.searchengine} subdomain={self.subdomain}
        res_title={self.res_title} res_url={self.res_url} res_content={self.res_content} update_time={self.update_time}>'''

    
class ReqKeys(db.Model):
    __tablename__ = 'req_keys'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(50), nullable=False)
    g_def = db.Column(db.Enum('notstarted', 'processing', 'finished', name='status_enum'), default='notstarted', nullable=False)
    b_def = db.Column(db.Enum('notstarted', 'processing', 'finished', name='status_enum'), default='notstarted', nullable=False)
    g_git = db.Column(db.Enum('notstarted', 'processing', 'finished', name='status_enum'), default='notstarted', nullable=False)
    b_git = db.Column(db.Enum('notstarted', 'processing', 'finished', name='status_enum'), default='notstarted', nullable=False)

    def __repr__(self):
        return f"<ReqKeys id={self.id} key={self.key} g_def={self.g_def} b_def={self.b_def} g_git={self.g_git} b_git={self.b_git}>"
    
class TagExp(db.Model):
    __tablename__ = 'res_tags_expose'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    restype = db.Column(db.Enum('error', 'sample', 'servinfo', 'others', name='restype_enum'))

    def __repr__(self):
        return f"<TagExp id={self.id} url={self.url} restype={self.restype}>"
    
class TagFile(db.Model):
    __tablename__ = 'res_tags_file'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)
    filetype = db.Column(db.Enum('pdf','pptx','xlsx','docx','others'))
    title = db.Column(db.String(200))
    moddate = db.Column(db.TIMESTAMP)
    data = db.Column(db.Text)

    def __repr__(self):
        return f'''
        <TagFile id={self.id} url={self.url} filetype={self.filetype}
        title={self.title} moddate={self.moddate} data={self.data}>'''