import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import VendorProfile, Product, Review
from .forms import UserRegistrationForm, VendorProfileForm


FALLBACK_VENDOR_IMAGES = {
    "food": [
        "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1552332386-f8dd00dc2f85?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?auto=format&fit=crop&w=800&q=80",
    ],
    "handicraft": [
        "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
    ],
    "agriculture": [
        "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1506807803488-8eafc15316c9?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?auto=format&fit=crop&w=800&q=80",
    ],
    "fashion": [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1536148935331-408321065b18?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80",
    ],
    "electronics": [
        "https://images.unsplash.com/photo-1517430816045-df4b7de11d1d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80",
    ],
    "beauty": [
        "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1522335789203-08eadf2f183d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80",
    ],
}

FALLBACK_VENDOR_DEFAULTS = [
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=800&q=80",
]

FALLBACK_PRODUCT_IMAGES = {
    "food": [
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1447078806655-40579c2520d6?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1552332386-f8dd00dc2f85?auto=format&fit=crop&w=800&q=80",
    ],
    "handicraft": [
        "https://images.unsplash.com/photo-1543165365-c00adfab93c9?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&w=800&q=80",
    ],
    "agriculture": [
        "https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1524593119774-35f74f015d2a?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=800&q=80",
    ],
    "fashion": [
        "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=800&q=80",
    ],
    "electronics": [
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1581092795360-f9b67f7cc9d3?auto=format&fit=crop&w=800&q=80",
    ],
    "beauty": [
        "https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1556228578-8c89e6adf3c1?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1556228578-0ae5edf055c0?auto=format&fit=crop&w=800&q=80",
    ],
}

FALLBACK_PRODUCT_DEFAULTS = [
    "https://images.unsplash.com/photo-1505740106531-4243f3831c78?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
]


def _get_fallback_image(category, mapping, defaults):
    category_lower = (category or "").lower()
    for key, urls in mapping.items():
        if key in category_lower:
            return random.choice(urls)
    return random.choice(defaults)


def home(request):
    """Homepage view with statistics"""
    vendor_count = VendorProfile.objects.count()
    product_count = Product.objects.count()
    review_count = Review.objects.count()
    
    # Count unique cities
    city_count = VendorProfile.objects.values('location').distinct().count()
    
    context = {
        'vendor_count': vendor_count,
        'product_count': product_count,
        'review_count': review_count,
        'city_count': city_count,
    }
    
    return render(request, "core/home.html", context)


def vendors(request):
    """Vendors listing page with optional category filter"""
    category = request.GET.get('category', None)
    
    if category:
        # Case-insensitive exact match first, then try partial match
        vendors_list = VendorProfile.objects.filter(category__iexact=category)
        if not vendors_list.exists():
            # If no exact match, try case-insensitive partial match
            vendors_list = VendorProfile.objects.filter(category__icontains=category)
    else:
        vendors_list = VendorProfile.objects.all()

    vendors_list = list(vendors_list)

    for vendor in vendors_list:
        fallback_url = _get_fallback_image(vendor.category, FALLBACK_VENDOR_IMAGES, FALLBACK_VENDOR_DEFAULTS)
        photo_field = getattr(vendor, "photo", None)

        vendor.display_photo = fallback_url

        if photo_field and getattr(photo_field, "name", ""):
            try:
                # Check if file actually exists
                if photo_field.storage.exists(photo_field.name):
                    vendor.display_photo = photo_field.url
                else:
                    vendor.display_photo = fallback_url
            except (ValueError, Exception):
                vendor.display_photo = fallback_url
    
    context = {
        'vendors': vendors_list,
        'category': category,
    }
    
    return render(request, "core/vendors.html", context)


def vendor_detail(request, id):
    """Individual vendor profile page"""
    vendor = get_object_or_404(VendorProfile, id=id)
    products = list(Product.objects.filter(vendor=vendor))
    reviews = Review.objects.filter(vendor=vendor)

    vendor_fallback = _get_fallback_image(vendor.category, FALLBACK_VENDOR_IMAGES, FALLBACK_VENDOR_DEFAULTS)
    photo_field = getattr(vendor, "photo", None)
    vendor.display_photo = vendor_fallback

    if photo_field and getattr(photo_field, "name", ""):
        try:
            # Check if file actually exists
            if photo_field.storage.exists(photo_field.name):
                vendor.display_photo = photo_field.url
            else:
                vendor.display_photo = vendor_fallback
        except (ValueError, Exception):
            vendor.display_photo = vendor_fallback

    for product in products:
        product_fallback = _get_fallback_image(vendor.category, FALLBACK_PRODUCT_IMAGES, FALLBACK_PRODUCT_DEFAULTS)
        image_field = getattr(product, "image", None)
        product.display_image = product_fallback

        if image_field and getattr(image_field, "name", ""):
            try:
                # Check if file actually exists
                if image_field.storage.exists(image_field.name):
                    product.display_image = image_field.url
                else:
                    product.display_image = product_fallback
            except (ValueError, Exception):
                product.display_image = product_fallback

    context = {
        "vendor": vendor,
        "products": products,
        "reviews": reviews
    }
    
    return render(request, "vendor_detail.html", context)


def awareness(request):
    """Awareness page for vendors"""
    return render(request, "core/awareness.html")


def about(request):
    """About Us page"""
    return render(request, "core/about.html")


# ===== Authentication Views =====

def register_view(request):
    """Vendor registration view"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = VendorProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create user
            user = user_form.save()
            
            # Create vendor profile
            vendor_profile = profile_form.save(commit=False)
            vendor_profile.user = user
            vendor_profile.save()
            
            # Log the user in
            login(request, user)
            
            messages.success(request, f'Welcome {user.username}! Your vendor account has been created successfully.')
            return redirect('profile')
    else:
        user_form = UserRegistrationForm()
        profile_form = VendorProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'auth/register.html', context)


def login_view(request):
    """Vendor login view"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next page or profile
            next_page = request.GET.get('next', 'profile')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    """Vendor logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    """Vendor profile dashboard view"""
    try:
        vendor_profile = request.user.vendorprofile
    except VendorProfile.DoesNotExist:
        messages.warning(request, 'Please complete your vendor profile.')
        return redirect('edit_profile')
    
    # Get fallback image
    vendor_fallback = _get_fallback_image(vendor_profile.category, FALLBACK_VENDOR_IMAGES, FALLBACK_VENDOR_DEFAULTS)
    photo_field = getattr(vendor_profile, "photo", None)
    vendor_profile.display_photo = vendor_fallback

    if photo_field and getattr(photo_field, "name", ""):
        try:
            vendor_profile.display_photo = photo_field.url
        except ValueError:
            vendor_profile.display_photo = vendor_fallback
    
    # Get vendor's products and reviews
    products = Product.objects.filter(vendor=vendor_profile)
    reviews = Review.objects.filter(vendor=vendor_profile)
    
    context = {
        'vendor': vendor_profile,
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'auth/profile.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    """Edit vendor profile view"""
    try:
        vendor_profile = request.user.vendorprofile
    except VendorProfile.DoesNotExist:
        vendor_profile = None
    
    if request.method == 'POST':
        if vendor_profile:
            profile_form = VendorProfileForm(request.POST, request.FILES, instance=vendor_profile)
        else:
            profile_form = VendorProfileForm(request.POST, request.FILES)
        
        if profile_form.is_valid():
            vendor_profile = profile_form.save(commit=False)
            vendor_profile.user = request.user
            vendor_profile.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        if vendor_profile:
            profile_form = VendorProfileForm(instance=vendor_profile)
        else:
            profile_form = VendorProfileForm()
    
    context = {
        'profile_form': profile_form,
        'vendor': vendor_profile,
    }
    return render(request, 'auth/edit_profile.html', context)



