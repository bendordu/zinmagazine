import os
import shutil
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.dateformat import DateFormat
from django.utils.datastructures import MultiValueDictKeyError
from uuslug import slugify
from cart.models import CartItem
from .models import Category, Product, Comment, PriceType, TypePr
from .forms import ProductCreateForm
from likes.decorators import ajax_required


def change_product_path(product, file_name, start_path):
    """Перемещает файл товара после создания или изменения экземпляра модели продукта.
    product это экземпляр модели продукта,
    file_name это название файла продукта, 
    start_path это общее начало пути"""
    product_file = eval(f"product.{file_name}")
    initial_path = product_file.path
    product_file.name = start_path + f'_{file_name}.jpg'
    new_path = settings.MEDIA_ROOT + product_file.name
    os.rename(initial_path, new_path)



def product_list(request, category_slug=None, price_type_slug=None, type_pr_slug=None):
    category = None
    price_type = None
    type_pr = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    price_types = PriceType.objects.all()
    type_prs = TypePr.objects.all()
    if request.method == 'POST':
        search = request.POST.get('s')
        products = products.filter(Q(name__icontains=search)|Q(description__icontains=search))
        try:
            user = User.objects.get(username=search)
            products = Product.objects.filter(user=user, available=True)
        except ObjectDoesNotExist:
            pass
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if price_type_slug:
        price_type = get_object_or_404(PriceType, slug=price_type_slug)
        products = products.filter(price_type=price_type)
    if type_pr_slug:
        type_pr = get_object_or_404(TypePr, slug=type_pr_slug)
        products = products.filter(type_pr=type_pr)
    return render(request, 'shop/product/list.html',{'category': category,
                                                    'categories': categories,
                                                    'products': products,
                                                    'price_type': price_type,
                                                    'type_pr': type_pr,
                                                    'price_types': price_types,
                                                    'type_prs': type_prs})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    comments = product.comments.filter(active=True).order_by('-comment_likes', '-image0')
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'comments': comments}) 


def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_pr = form.save(commit=False)
            new_pr.slug = slugify(form.cleaned_data['name'])
            new_pr.save()
            new_pr.user.add(request.user)
            for category in form.cleaned_data['category']:
                new_pr.category.add(category)

            if new_pr.image or new_pr.image_dop1 or new_pr.image_dop2 or new_pr.file_product:
                try:
                    directory = f'products/{new_pr.name}'
                    parent_dir = settings.MEDIA_ROOT 
                    path = os.path.join(parent_dir, directory)
                    os.makedirs(path)
                except OSError as error:
                    pass

                start_path = f'products/{new_pr.name}/{new_pr.name}'
                files = ["image", "image_dop1", "image_dop2", "file_product"]
                for f in files:
                    if eval(f"new_pr.{f}"):
                        change_product_path(product=new_pr, file_name=f, start_path=start_path)


                new_pr.save()
            return redirect('shop:product_list')
    else:
        form = ProductCreateForm
    return render(request, 'shop/product/create_product.html', {'form': form})


def delete_product(request, id):
    product = Product.objects.get(id=id)  
    try:
        path = settings.MEDIA_ROOT + f'products/{product.name}'
        shutil.rmtree(path, ignore_errors=False, onerror=None)
    except:
        pass
    product.delete()
    return redirect('dashboard')


def edit_product(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        form = ProductCreateForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            for category in form.cleaned_data['category']:
                product.category.add(category)

            if product.image or product.image_dop1 or product.image_dop2 or product.file_product:
                try:
                    directory = f'products/{product.name}'
                    parent_dir = settings.MEDIA_ROOT 
                    path = os.path.join(parent_dir, directory)
                    os.makedirs(path)
                except OSError as error:
                    pass

                start_path = f'products/{product.name}/{product.name}'
                files = ["image", "image_dop1", "image_dop2", "file_product"]
                for f in files:
                    if eval(f"product.{f}"):
                        try:
                            change_product_path(product=product, file_name=f, start_path=start_path)
                        except OSError as error:
                            pass
                product.save()
            return redirect('shop:product_list')
    else:
        product = Product.objects.get(id=id)
        form = ProductCreateForm(instance=product)
    return render(request, 'shop/product/edit_product.html', {'form': form})


@ajax_required
@login_required
@require_POST
def hide_product(request):
    product = Product.objects.get(id=request.POST.get('id'))
    if request.POST.get('action') == 'hide':
        product.available = False
    else:
        product.available = True
    product.save()
    return JsonResponse({'status':'ok'})


@ajax_required
@login_required
@require_POST
def product_add_comment(request):
    product_id = request.POST.get('id')
    author = request.user
    product = Product.objects.get(id=product_id)
    body = request.POST.get('data')
    d = {'image0':None, 'image1':None, 'image2':None}
    for i in d.keys():
        try:
            d[i] = request.FILES[i]
        except MultiValueDictKeyError:
            continue
    comment = Comment(body=body, author = author, product=product, **d)
    comment.save()

    if comment.image0 or comment.image1 or comment.image2:
        parent_dir = settings.MEDIA_ROOT 
        try:
            directory = f'products/{product.name}'
            path = os.path.join(parent_dir, directory)
            os.makedirs(path)
        except OSError as error:
            pass

        files = ["image0", "image1", "image2"]
        for f in files:
            if eval(f"comment.{f}"):
                try:
                    comment_file = eval(f"comment.{f}")
                    initial_path = comment_file.path
                    created = DateFormat(comment.created).format('d-m-Y-H-i')
                    comment_file.name = f'products/{product.name}/{product.name}_comment_{comment.id}_{comment.author}_{created}_{f}.jpg'
                    new_path = os.path.normpath(os.path.join(parent_dir, comment_file.name))
                    os.rename(initial_path, new_path) 
                    comment.save()
                except OSError:
                    pass
    return JsonResponse({'status':'ok'})

@ajax_required 
@login_required
@require_POST
def product_remove_comment(request):
    comment_id = request.POST.get('id')
    comment = get_object_or_404(Comment, id=comment_id)
    if request.POST.get('action') == 'remove':
        for image in [comment.image0, comment.image1, comment.image2]:
            image.delete()
        comment.delete()
    if request.POST.get('action') == 'edit':
        body = request.POST.get('body')
        comment.body = body
        comment.save()
    return JsonResponse({'status':'ok'})

@ajax_required
@login_required
@require_POST
def product_bye_paper(request):
    product_id = request.POST.get('id')
    product = Product.objects.get(id=product_id)
    action = request.POST.get('action')
    if action == 'bye_paper':
        product.bye_paper.add(request.user)
    else:
        product.bye_paper.remove(request.user)
    return JsonResponse({'status':'ok'})

@ajax_required
@require_POST
def product_s(request):
    search = request.POST.get('s')
    prs = Product.objects.filter(available=True)
    authors = []
    for p in prs:
        for u in p.user.all():
            if search.lower() in u.username:
                if u.username not in authors:
                    authors += [u.username]
    products_ = Product.objects.filter(Q(name__icontains=search)|Q(description__icontains=search)).values('name')
    products = []
    for p in products_:
        product = p['name']
        products += [product]
    return JsonResponse({'status':'ok', 'products': products, 'authors': authors})
    

@ajax_required
@login_required
@require_POST
def product_comment_like(request):
    comment_id = request.POST.get('id')
    comment = Comment.objects.get(id=comment_id)
    if request.POST.get('action') == 'like':
        comment.comment_likes.add(request.user)
    else:
        comment.comment_likes.remove(request.user)
    return JsonResponse({'status':'ok'})

def bas(request):
    return render(request,'shop/bas.html')







                          