from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden
from hashlib import blake2b
from os import urandom
from .models import ShortLink
from urllib import parse
from json import dumps
from django.utils.datastructures import MultiValueDictKeyError

def add_link(link : ShortLink, named_link : bool) -> str:
    if named_link:
        dup = ShortLink.objects.filter(id=link.id)
        if dup:
            return HttpResponseBadRequest()
    else:
        dup = ShortLink.objects.filter(link=link.link)
        if dup:
            return HttpResponse(dup[0].id)
    link.save()
    return HttpResponse(link.id)

def get_info_about_link(request : HttpRequest):
    find = ShortLink.objects.filter(id=request.path.lstrip("/"))
    if not find:
        return HttpResponseNotFound()
    finded_link = find[0]
    return HttpResponse(dumps({"link":finded_link.link, "datetime_creation": str(finded_link.created_date), "visited_counter": finded_link.visited_counter}))

def index(request : HttpRequest):
	return render(request, "index.html")

def info(request : HttpRequest):
    return render(request, "info.html")

def redirector(request : HttpRequest):
    if "info" in request.GET:
        return get_info_about_link(request)
    find = ShortLink.objects.filter(id=request.path.lstrip("/"))
    if not find:
        return HttpResponseNotFound()
    finded_link = find[0]
    finded_link.visited_counter += 1
    finded_link.save()
    return HttpResponseRedirect(finded_link.link)

def generator(request : HttpRequest):
    # Всё очень просто, и как id, хэшируем ссылку и компенсируем коллизию blake2b 8 байтовой солью
    # и добавляем в db
    link = request.POST["link"]
    if not link:
        return HttpResponseBadRequest()
    if(len(link) >= 200):
        return HttpResponseBadRequest()
    source_link = parse.urlparse(link, scheme="https", allow_fragments=False).geturl()
    final_link = None
    print(request.POST)
    try:
        if request.POST["personal_link"]:
            return add_link(ShortLink(id=request.POST["personal_link"], link=source_link, visited_counter=0), True)
    except MultiValueDictKeyError:
        final_link = blake2b(source_link.encode("utf-8"), digest_size=2, salt=urandom(8)).hexdigest()
    
    return add_link(ShortLink(id=final_link, link=source_link, visited_counter=0), False)