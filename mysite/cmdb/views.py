from django.shortcuts import render

from django.shortcuts import HttpResponse

from cmdb import models

# Create your views here.

# user_list = [
#     {'user': 'jack', 'pwd': 'abc'},
#     {'user': 'tom', 'pwd': 'ABC'}
# ]


def index(request):
    # return HttpResponse('Hello world')
    if request.method == 'POST':
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        # 添加数据到数据库
        models.UserInfo.objects.create(user=username, pwd=password)

    user_list = models.UserInfo.objects.all()
    return render(request, 'index.html', {'data': user_list})
