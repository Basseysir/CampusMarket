from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm
# Create your views here.


# Features 2 & 6: Home Feed, Category Filter, Search
def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    products = Product.objects.filter(is_sold=False).order_by('-created_at')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'listings/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    })

# Features 7 & 8: View Product Details & Contact Seller
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Generate direct WhatsApp link if phone exists
    whatsapp_number = product.seller.phone_number.replace('+', '').replace(' ', '')
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text=Hi%20{product.seller.username},%20I'm%20interested%20in%20your%20listing:%20{product.title}"
    
    return render(request, 'listings/product_detail.html', {
        'product': product,
        'whatsapp_url': whatsapp_url
    })

# Features 3, 4, 5: Create Listing
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'listings/product_form.html', {'form': form, 'title': 'List an Item'})

# Feature 9: Seller Dashboard (Edit / Remove)
@login_required
def seller_dashboard(request):
    user_products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'listings/dashboard.html', {'products': user_products})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'listings/product_form.html', {'form': form, 'title': 'Edit Listing'})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_dashboard')
    return render(request, 'listings/confirm_delete.html', {'product': product})