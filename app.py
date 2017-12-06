from waitress import serve
import mimetypes
import os
import os.path
import urllib.parse

here = os.path.dirname(os.path.abspath(__file__))
with open('project/data.txt') as f:
    data = eval(f.read())
def uniBytes2str(s):
    return s.encode('iso-8859-1').decode('utf-8')
def app(env, rsFn):
    #------------------static file -----------------------------
    urlpath = 'index.html' if env['PATH_INFO'] == '/' or  env['PATH_INFO'] == '' else env['PATH_INFO']
    urlpath = uniBytes2str(urlpath)
    # print(urlpath)
    # urlpath = urllib.parse.urlparse(urlpath).path ##decode unicode in original path
    if urlpath.startswith('/'): urlpath_temp = urlpath[1:]
    wantedfile = os.path.join(here, *urlpath.split('/') )
    response_headers = []
    if os.path.isfile(wantedfile):
        status = '200 ok'
        extension = urlpath.split('/')[-1]
        contentType = mimetypes.guess_type(extension)[0]
        if 'text' in contentType and 'charset' not in contentType:
            contentType = contentType + '; charset=utf-8'
        response_headers.append( ('Content-Type', contentType))
        rsFn(status, response_headers)
        f = open(wantedfile,'rb')
        return env['wsgi.file_wrapper'](f)
    
    #-----------------named json data-----------------------------
    if urlpath.startswith('/api/name/'): # return this name's data
        name = urlpath[10:]
        over = [i[name] if name in i else 0 for i in data[0]]
        below = [i[name] if name in i else 0 for i in data[1]]
        rstr = '{}'.format([over[i] + below[i] for i in range(len(over))])
        status = '200 ok'
        response_headers = [('Content-Type', 'text/plain; charset=utf-8')]
        rsFn(status,response_headers)
        return [rstr if isinstance(rstr, bytes) else rstr.encode('utf-8')]

    response_body = ['{} is {} <br>'.format(i, env[i]) for i in env]
    response_body.append(os.getcwd())
    status = '200 ok'
    response_headers = [
        ('Content-Type', 'text/html; charset=utf-8')
    ]
    rsFn(status,response_headers)
    return [i if isinstance(i, bytes) else i.encode('utf-8') for i in response_body]


serve(app, listen='*:8080')
