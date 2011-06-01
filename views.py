from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from shortenurl.forms import UrlForm
import redis

HOST_URL = 'http://localhost:8000/'
KEYS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def convert(number, keys=KEYS):
    if (number==0):
        return keys[0]
    arr = []
    while number:
        rem = number % 62
        number = number // 62
        arr.append(keys[rem])
    arr.reverse()
    return ''.join(arr)

def trevnoc(key, keys=KEYS):
    number = 0
    for i in range(len(key)):
        number = number + (keys.find(key[len(key)-1-i]) * (62**i))
    return number

def redirect(request, key):
    db = redis.Redis('localhost')
    redirectURI = db.get(key)
    if redirectURI == None:
        return HttpResponse("that url does not exist")
    else:
        return HttpResponseRedirect(redirectURI)

def urlForm(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            url = cd['url']
            db = redis.Redis('localhost')
            counter = int(db.get('counter'))
            urlkey = convert(counter)
            if db.set(urlkey, url):
                db.incr('counter')
                urlid = urlkey
            else:
                urlid = 'error'
            return HttpResponseRedirect('/shorten/?urlid='+urlid)
    else:
        form = UrlForm()
    return render_to_response('urlform.html', {'form': form})

def shorten(request, hosturl=HOST_URL):
    urlid = request.GET['urlid']
    url = redis.Redis('localhost').get(urlid)
    if urlid == 'error' or url == None:
        return HttpResponse('there was an error in shortening that url')
    else:
        return HttpResponse(hosturl+urlid+' ---> '+url)
