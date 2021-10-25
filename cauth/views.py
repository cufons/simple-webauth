from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import binascii
from .models import *


def checkauth(request):
    return HttpResponse("Not yet implemented!")


class AuthOnly():
    def __init__(self, view):
        self.view = view

    def __call__(self, request):
        authid = request.COOKIES.get('chi_auth_id')
        authkey = request.COOKIES.get('chi_auth_key')
        redir_url = f"/auth?redirect={request.path}"
        if authid is None or authkey is None:
            return HttpResponseRedirect(redir_url)

        authid = binascii.a2b_base64(authid)
        authkey = binascii.a2b_base64(authkey)
        try:
            session = Session.objects.get(identifier=authid)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(redir_url)

        if not session.validate(authkey):
            return HttpResponseRedirect(redir_url)

        return self.view(request)
# TODO validate login | done
# TODO add registration

def login(request):
    MAXCREDLEN = 30
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        redir_success = request.POST['redirect']
        redir_url = f'/auth/fail?redirect={redir_success}'
        try:
            account = Account.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(redir_url)

        if len(username) > MAXCREDLEN or len(password) > MAXCREDLEN or not account.checkpass(password):
            return HttpResponseRedirect(redir_url)
        s = Session.objects.create()
        tokens = s.initialize()
        s.save()
        r = HttpResponseRedirect(redir_success)
        r.set_cookie('chi_auth_id', binascii.b2a_base64(
            tokens['id'], newline=False).decode(), httponly=True, secure=True, max_age=24*3600)
        r.set_cookie('chi_auth_key', binascii.b2a_base64(
            tokens['key'], newline=False).decode(), httponly=True, secure=True, max_age=24*3600)
        return r
    else:
        return HttpResponseForbidden()


def loginfailed(request):
    return loginview(request, failed=True)


def loginview(request, failed=False):
    context = {'error': failed,
               'redir_success': request.GET.get('redirect') or '/'}
    return render(request, 'login.html', context=context)
