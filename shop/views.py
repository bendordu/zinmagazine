from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required
from .models import Category, Product, Comment, PriceType, TypePr
from .forms import ProductCreateForm
from uuslug import slugify
from django.db.models import Q
from django.contrib.auth.models import User
import os
import shutil
from django.conf import settings


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
        except:
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
    comments = product.comments.filter(active=True)
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
                    directory = 'products/' + str(new_pr.name)
                    parent_dir = settings.MEDIA_ROOT 
                    path = os.path.join(parent_dir, directory)
                    os.makedirs(path)
                except OSError as error:
                    pass

                start_path = 'products/'+str(new_pr.name)+'/'+str(new_pr.name)
                files = ["image", "image_dop1", "image_dop2", "file_product"]
                for f in files:
                    if eval(f"new_pr.{f}"):
                        new_pr_file = eval(f"new_pr.{f}")
                        initial_path = new_pr_file.path
                        new_pr_file.name = start_path + f'_{f}.jpg'
                        new_path = settings.MEDIA_ROOT + new_pr_file.name
                        os.rename(initial_path, new_path)

                new_pr.save()
            return redirect('shop:product_list')
    else:
        form = ProductCreateForm
    return render(request, 'shop/product/create_product.html', {'form': form})


def delete_product(request, id):
    product = Product.objects.get(id=id)
    try:
        path = settings.MEDIA_ROOT + 'products/' + str(product.name)
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
                    directory = 'products/' + str(product.name)
                    parent_dir = settings.MEDIA_ROOT 
                    path = os.path.join(parent_dir, directory)
                    os.makedirs(path)
                except OSError as error:
                    pass

                start_path = 'products/'+str(product.name)+'/'+str(product.name)
                files = ["image", "image_dop1", "image_dop2", "file_product"]
                for f in files:
                    if eval(f"product.{f}"):
                        try:
                            product_file = eval(f"product.{f}")
                            initial_path = product_file.path
                            product_file.name = start_path + f'_{f}.jpg'
                            new_path = settings.MEDIA_ROOT + product_file.name
                            os.rename(initial_path, new_path)
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
    if request.POST.get('action'):
        body = request.POST.get('body')
        comment = get_object_or_404(Comment, body=body, author=author, product=product)
        if request.POST.get('action') == 'remove':
            comment.delete()
        if request.POST.get('action') == 'edit':
            new_body = request.POST.get('new_body')
            comment.body = new_body
            comment.author = author
            comment.product = product
            comment.save()
    else:
        image = request.POST.get('image')
        data = request.POST.get('data')
        comment = Comment(body=data, author = author, product=product, image=image)
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







                          