from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,re,urllib.request,html
from session import ROOT,HERE,record,sha
bib=(ROOT/'references.bib').read_text(encoding='utf-8')
entries=re.split(r'(?m)^@',bib)[1:]
def fetch(entry):
    key=re.match(r'\w+\{([^,]+)',entry).group(1)
    doi=re.search(r'\bdoi\s*=\s*\{([^}]+)',entry)
    arxiv=re.search(r'\beprint\s*=\s*\{([^}]+)',entry)
    if doi: url='https://api.crossref.org/works/'+doi.group(1)
    elif arxiv: url='https://arxiv.org/abs/'+arxiv.group(1)
    else: url=re.search(r'\burl\s*=\s*\{([^}]+)',entry).group(1)
    try:
        request=urllib.request.Request(url,headers={'User-Agent':'ManuscriptBibliographyReview/1.0'})
        data=urllib.request.urlopen(request,timeout=35).read().decode('utf-8')
        if doi:
            m=json.loads(data)['message']
            info={k:m.get(k) for k in ['title','author','published','container-title','volume','issue','page','article-number','DOI']}
        else:
            info={}
            for name,content in re.findall(r'<meta\s+name="([^"]+)"\s+content="([^"]*)"',data):
                if name.startswith('citation_'): info.setdefault(name,[]).append(html.unescape(content))
            if not info: info={'page_text':re.sub('<[^>]+>',' ',data)[:18000]}
        return {'key':key,'url':url,'status':'retrieved','metadata':info}
    except Exception as e: return {'key':key,'url':url,'status':'failed','error':str(e)}
with ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(fetch,entries))
out=HERE/'reference_metadata.json'
out.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
record('Primary reference metadata retrieved',{'artifact':str(out.relative_to(ROOT)),'sha256':sha(out),'entries':len(results),'failures':[x for x in results if x['status']=='failed']})
for r in results:
    m=r.get('metadata',{})
    print(json.dumps({'key':r['key'],'status':r['status'],'title':m.get('title',m.get('citation_title')),'venue':m.get('container-title'),'year':m.get('published',m.get('citation_date')),'volume':m.get('volume'),'page':m.get('page',m.get('article-number')),'authors':m.get('author',m.get('citation_author'))},ensure_ascii=True))
