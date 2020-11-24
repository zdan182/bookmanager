from django.shortcuts import render, redirect
from app01 import models
from django.views import View

# Create your views here.

PUB_ERROR_EMPTY = '出版社名称不能为空'
PUB_ERROR_DUPLICATE = '您输入的出版社名称已经存在'
BOOK_ERROR_EMPTY = '书籍名称不能为空'
BOOK_ERROR_DUPLICATE = '您输入的书籍名称已经存在'


def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'root' and pwd == '123':
            return redirect('publist')
        else:
            error = '用户名或密码错误'
    return render(request, 'login.html', locals())


def publisher_list(request):
    all_publishers = models.Publisher.objects.all()
    # all_publishers = models.Publisher.objects.all().order_by('-id')
    return render(request, 'publisher_list.html', {'publisher_list': all_publishers})


# FBV写法
# def publisher_add(request):
#     if request.method == 'POST':
#         pub_name = request.POST.get('pub_name')
#         if not pub_name:
#             return render(request, 'publisher_add.html', {'error': PUB_ERROR_EMPTY})
#         if models.Publisher.objects.filter(name=pub_name):
#             return render(request, 'publisher_add.html', {'error': PUB_ERROR_DUPLICATE})
#         models.Publisher.objects.create(name=pub_name)
#         return redirect('/publisher_list/')
#     return render(request, 'publisher_add.html')

# CBV写法
class PublishAdd(View):
    def dispatch(self, request, *args, **kwargs):
        # 执行get和post方法之前的操作
        ret = super().dispatch(request, *args, **kwargs)  # 调用父类View中的dispatch方法
        # 执行get和post方法之后的操作
        return ret

    def get(self, request):
        return render(request, 'publisher_add.html')

    def post(self, request):
        pub_name = request.POST.get('pub_name')
        if not pub_name:
            return render(request, 'publisher_add.html', {'error': PUB_ERROR_EMPTY})
        if models.Publisher.objects.filter(name=pub_name):
            return render(request, 'publisher_add.html', {'error': PUB_ERROR_DUPLICATE})
        models.Publisher.objects.create(name=pub_name)
        return redirect('publist')


def publisher_del(request):
    nid = request.GET.get('nid')
    models.Publisher.objects.filter(pk=nid).delete()
    return redirect('publist')


# def publisher_edit(request, nid):
# *args接收位置参数，**kwargs接收关联参数
def publisher_edit(request, *args, **kwargs):
    nid = kwargs.get('nid')
    # nid = request.GET.get('nid')
    pub_obj = models.Publisher.objects.get(id=nid)
    if request.method == 'GET':
        return render(request, 'publisher_edit.html', {'pub_obj': pub_obj})
    else:
        former_name = request.POST.get('publisher_edit')
        if not former_name:
            return render(request, 'publisher_edit.html', {'error': PUB_ERROR_EMPTY})
        elif models.Publisher.objects.filter(name=former_name):
            return render(request, 'publisher_edit.html', {'error': PUB_ERROR_DUPLICATE})
        else:
            pub_obj.name = former_name
            pub_obj.save()
            return redirect('publist')


def book_list(request):
    all_books = models.Book.objects.all()
    return render(request, 'book_list.html', {'book_list': all_books})


def book_add(request):
    all_publishers = models.Publisher.objects.all()
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        if not book_name:
            return render(request, 'book_add.html', {'error': BOOK_ERROR_EMPTY, 'all_publishers': all_publishers})
        if models.Book.objects.filter(name=book_name):
            return render(request, 'book_add.html', {'error': BOOK_ERROR_DUPLICATE, 'all_publishers': all_publishers})
        models.Book.objects.create(name=book_name, publisher_id=pub_id)
        # models.Book.objects.create(name=book_name, publisher=models.Publisher.objects.get(pk=pub_id))
        return redirect('booklist')
    return render(request, 'book_add.html', {'all_publishers': all_publishers})


def book_del(request):
    nid = request.GET.get('nid')
    models.Book.objects.filter(pk=nid).delete()
    return redirect('booklist')


def book_edit(request):
    all_publishers = models.Publisher.objects.all()
    nid = request.GET.get('nid')
    book_obj = models.Book.objects.get(pk=nid)
    book_name = book_obj.name
    pub_id = book_obj.publisher_id
    if request.method == 'GET':
        return render(request, 'book_edit.html',
                      {'book_name': book_name, 'all_publishers': all_publishers, 'pub_id': pub_id})
    else:
        book_edit_name = request.POST.get('book_edit')
        if not book_edit_name:
            all_publishers = models.Publisher.objects.all()
            return render(request, 'book_edit.html',
                          {'error': BOOK_ERROR_EMPTY, 'all_publishers': all_publishers, 'pub_id': pub_id})
        if models.Book.objects.filter(name=book_edit_name):
            all_publishers = models.Publisher.objects.all()
            return render(request, 'book_edit.html', {'error': BOOK_ERROR_DUPLICATE, 'all_publishers': all_publishers,
                                                      'book_name': book_edit_name, 'pub_id': pub_id})
        pub_edit_id = request.POST.get('pub_id')
        book_edit_obj = models.Book.objects.get(pk=nid)
        book_edit_obj.name = book_edit_name
        book_edit_obj.publisher_id = pub_edit_id
        book_edit_obj.save()
        return redirect('booklist')


def author_list(request):
    all_authors = models.Author.objects.all()
    return render(request, 'author_list.html', {'all_authors': all_authors})


def author_add(request):
    # 获取所有书籍信息
    all_books = models.Book.objects.all()
    if request.method == 'POST':
        # 获取用户提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')
        # 向数据库中插入数据
        # 判断作者姓名是否为空
        if not author_name:
            return render(request, 'author_add.html', {'all_books': all_books, 'error': '作者信息不能为空'})
        # 判断数据库中是否有重复的作者姓名
        if models.Author.objects.filter(name=author_name):
            return render(request, 'author_add.html', {'all_books': all_books, 'error': '不能添加重复的作者信息'})
        # 向作者表中插入作者信息
        author_obj = models.Author.objects.create(name=author_name)
        # 该作者和提交的书籍绑定多对多的关系
        author_obj.books.set(book_ids)
        # 返回重定向的页面
        return redirect('authorlist')
    return render(request, 'author_add.html', {'all_books': all_books})


def author_del(request):
    nid = request.GET.get('nid')
    models.Author.objects.filter(pk=nid).delete()
    return redirect('authorlist')


def author_edit(request):
    # 获得所有书籍对象
    book_obj = models.Book.objects.all()
    # get请求
    # 获得当前操作的作者的id
    nid = request.GET.get('nid')
    # 根据nid在数据库里查询作者信息对象
    author_obj = models.Author.objects.get(pk=nid)
    # post请求
    if request.method == 'POST':
        # 获得作者姓名，存入数据库
        author_name = request.POST.get('author_name')
        author_obj.name = author_name
        author_obj.save()
        # 获得代表作，重新设置关系对象
        book_ids = request.POST.getlist('book_ids')
        author_obj.books.set(book_ids)
        # 跳转到展示页面
        return redirect('authorlist')
    # 渲染增加作者页面
    return render(request, 'author_edit.html', {'author_obj': author_obj, 'book_obj': book_obj})


class Upload(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        file = request.FILES.get('upload_name')
        with open(file.name, 'wb') as f:
            for i in file:
                f.write(i)
        return render(request, 'upload.html', {'success': '上传成功'})
