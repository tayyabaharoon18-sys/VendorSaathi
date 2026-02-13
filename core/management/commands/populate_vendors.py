from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import VendorProfile, Product, Review
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
import random


class Command(BaseCommand):
    help = 'Populates the database with sample vendor data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write("Clearing existing data...")
        VendorProfile.objects.all().delete()
        User.objects.filter(username__startswith='vendor').delete()
        
        # Sample vendor data
        vendors_data = [
            {
                'name': 'Rajan\'s Street Food Corner',
                'category': 'Food & Beverages',
                'location': 'Mumbai, Maharashtra',
                'story': 'Started my street food business 15 years ago with just a cart. Today, I serve the best pav bhaji and vada pav in the area. My secret? Fresh ingredients and love for what I do!',
                'products': [
                    {'name': 'Pav Bhaji', 'price': 80},
                    {'name': 'Vada Pav', 'price': 30},
                    {'name': 'Dabeli', 'price': 40},
                ],
                'reviews': [
                    {'name': 'Priya Sharma', 'rating': 5, 'comment': 'Best pav bhaji in Mumbai! The taste is authentic and the portions are generous.'},
                    {'name': 'Amit Patel', 'rating': 5, 'comment': 'Been coming here for years. Rajan bhai makes the best street food!'},
                ]
            },
            {
                'name': 'Meena\'s Handicrafts',
                'category': 'Handicrafts & Art',
                'location': 'Jaipur, Rajasthan',
                'story': 'I learned traditional Rajasthani handicraft from my grandmother. Now I create beautiful handmade items that showcase our rich cultural heritage. Each piece tells a story.',
                'products': [
                    {'name': 'Handmade Clay Pots', 'price': 250},
                    {'name': 'Embroidered Cushion Covers', 'price': 350},
                    {'name': 'Handcrafted Jewelry', 'price': 500},
                ],
                'reviews': [
                    {'name': 'Sara Khan', 'rating': 5, 'comment': 'Absolutely beautiful craftsmanship! The cushion covers are stunning.'},
                    {'name': 'Raj Malhotra', 'rating': 4, 'comment': 'Great quality products. Loved the pottery work.'},
                ]
            },
            {
                'name': 'Kumar\'s Organic Vegetables',
                'category': 'Agriculture & Produce',
                'location': 'Pune, Maharashtra',
                'story': 'A third-generation farmer committed to organic farming. I grow vegetables without chemicals, ensuring healthy produce for your family. Farm to table, fresh and pure!',
                'products': [
                    {'name': 'Organic Tomatoes (1kg)', 'price': 60},
                    {'name': 'Fresh Spinach Bundle', 'price': 30},
                    {'name': 'Organic Carrots (1kg)', 'price': 50},
                ],
                'reviews': [
                    {'name': 'Anita Deshmukh', 'rating': 5, 'comment': 'The vegetables are always fresh and last longer than market ones!'},
                    {'name': 'Sunil Kumar', 'rating': 5, 'comment': 'Truly organic! The taste difference is remarkable.'},
                ]
            },
            {
                'name': 'Fatima\'s Tailoring Studio',
                'category': 'Fashion & Tailoring',
                'location': 'Delhi, NCR',
                'story': 'Stitching dreams since 2005! I specialize in custom tailoring and alterations. From traditional wear to modern outfits, I create clothes that fit perfectly and make you feel confident.',
                'products': [
                    {'name': 'Custom Suit Stitching', 'price': 1500},
                    {'name': 'Dress Alterations', 'price': 300},
                    {'name': 'Kurti Design & Stitch', 'price': 800},
                ],
                'reviews': [
                    {'name': 'Neha Gupta', 'rating': 5, 'comment': 'Fatima ji is a master tailor! Perfect fitting every time.'},
                    {'name': 'Rahul Verma', 'rating': 5, 'comment': 'Got my wedding suit made here. Excellent work!'},
                ]
            },
            {
                'name': 'Shankar\'s Flower Shop',
                'category': 'Flowers & Gardening',
                'location': 'Bangalore, Karnataka',
                'story': 'Flowers bring joy to life! I supply fresh flowers for all occasions - weddings, festivals, or just to brighten your day. Each bouquet is crafted with care and love.',
                'products': [
                    {'name': 'Rose Bouquet (12 roses)', 'price': 400},
                    {'name': 'Jasmine Garland', 'price': 150},
                    {'name': 'Mixed Flower Arrangement', 'price': 600},
                ],
                'reviews': [
                    {'name': 'Lakshmi Iyer', 'rating': 5, 'comment': 'Always fresh flowers! Great service for my daily puja needs.'},
                    {'name': 'Karthik Reddy', 'rating': 4, 'comment': 'Good variety and reasonable prices.'},
                ]
            },
            {
                'name': 'Ahmed\'s Mobile Repair',
                'category': 'Electronics & Repair',
                'location': 'Hyderabad, Telangana',
                'story': 'Fixing phones and making smiles since 2010! I provide quick and affordable mobile repair services. No issue is too big or small. Your satisfaction is my guarantee.',
                'products': [
                    {'name': 'Screen Replacement', 'price': 2500},
                    {'name': 'Battery Replacement', 'price': 1200},
                    {'name': 'Water Damage Repair', 'price': 1800},
                ],
                'reviews': [
                    {'name': 'Vivek Sharma', 'rating': 5, 'comment': 'Fixed my phone in just 30 minutes! Great service.'},
                    {'name': 'Pooja Nair', 'rating': 5, 'comment': 'Very honest and skilled. Highly recommended!'},
                ]
            },
            {
                'name': 'Geeta\'s Homemade Pickles',
                'category': 'Food & Preserves',
                'location': 'Lucknow, Uttar Pradesh',
                'story': 'Using my grandmother\'s secret recipes, I make traditional Indian pickles that taste like home. Each jar is made with love, using the finest ingredients and traditional methods.',
                'products': [
                    {'name': 'Mango Pickle (500g)', 'price': 200},
                    {'name': 'Mixed Vegetable Pickle (500g)', 'price': 180},
                    {'name': 'Lemon Pickle (500g)', 'price': 150},
                ],
                'reviews': [
                    {'name': 'Sunita Yadav', 'rating': 5, 'comment': 'Reminds me of my grandmother\'s pickles! Absolutely delicious.'},
                    {'name': 'Manoj Singh', 'rating': 5, 'comment': 'Best pickle I\'ve ever tasted. Perfect spice level!'},
                ]
            },
            {
                'name': 'Prakash\'s Cycle Repair',
                'category': 'Transportation & Repair',
                'location': 'Chennai, Tamil Nadu',
                'story': 'Keeping cycles running smoothly for over 20 years! From simple repairs to complete overhauls, I ensure your cycle is safe and reliable. Quick service at fair prices.',
                'products': [
                    {'name': 'Puncture Repair', 'price': 50},
                    {'name': 'Brake Adjustment', 'price': 100},
                    {'name': 'Full Service & Tune-up', 'price': 400},
                ],
                'reviews': [
                    {'name': 'Arjun Kumar', 'rating': 5, 'comment': 'Very reliable and affordable. Great work!'},
                    {'name': 'Deepa Rajan', 'rating': 4, 'comment': 'Quick and efficient service.'},
                ]
            },
            {
                'name': 'Leela\'s Beauty Parlor',
                'category': 'Beauty & Wellness',
                'location': 'Kolkata, West Bengal',
                'story': 'Making women feel beautiful and confident for 10 years! I offer a range of beauty services in a comfortable, hygienic environment. Your beauty is my passion.',
                'products': [
                    {'name': 'Hair Cut & Style', 'price': 300},
                    {'name': 'Facial Treatment', 'price': 600},
                    {'name': 'Bridal Makeup', 'price': 5000},
                ],
                'reviews': [
                    {'name': 'Ritu Das', 'rating': 5, 'comment': 'Leela di is amazing! Best bridal makeup in Kolkata.'},
                    {'name': 'Shreya Banerjee', 'rating': 5, 'comment': 'Very professional and talented. Highly recommended!'},
                ]
            },
            {
                'name': 'Ramesh\'s Chai Stall',
                'category': 'Food & Beverages',
                'location': 'Varanasi, Uttar Pradesh',
                'story': 'Serving the perfect cup of chai for 25 years! Made with fresh ingredients and lots of love. A cup of my chai refreshes your body and soul. Morning starts here!',
                'products': [
                    {'name': 'Special Masala Chai', 'price': 20},
                    {'name': 'Ginger Chai', 'price': 20},
                    {'name': 'Samosa (2 pieces)', 'price': 30},
                ],
                'reviews': [
                    {'name': 'Vishal Tiwari', 'rating': 5, 'comment': 'The best chai in Varanasi! Can\'t start my day without it.'},
                    {'name': 'Anjali Mishra', 'rating': 5, 'comment': 'Perfect blend of spices. Simply the best!'},
                ]
            },
        ]

        self.stdout.write("Creating vendors with images...")

        for idx, vendor_data in enumerate(vendors_data, 1):
            # Create user
            username = f"vendor{idx}"
            user = User.objects.create_user(
                username=username,
                email=f"{username}@vendorsaathi.com",
                password="password123"
            )
            
            # Create vendor image
            vendor_img_name = f"vendor_{idx}.jpg"
            self.create_vendor_image(vendor_img_name, vendor_data['name'], vendor_data['category'])
            
            # Create vendor profile
            vendor = VendorProfile.objects.create(
                user=user,
                name=vendor_data['name'],
                category=vendor_data['category'],
                location=vendor_data['location'],
                photo=f"vendors/{vendor_img_name}",
                story=vendor_data['story']
            )
            
            # Create products
            for prod_idx, product_data in enumerate(vendor_data['products'], 1):
                product_img_name = f"product_{idx}_{prod_idx}.jpg"
                self.create_product_image(product_img_name, product_data['name'])
                
                Product.objects.create(
                    vendor=vendor,
                    name=product_data['name'],
                    price=product_data['price'],
                    image=f"products/{product_img_name}"
                )
            
            # Create reviews
            for review_data in vendor_data['reviews']:
                Review.objects.create(
                    vendor=vendor,
                    name=review_data['name'],
                    rating=review_data['rating'],
                    comment=review_data['comment']
                )
            
            self.stdout.write(self.style.SUCCESS(f"✓ Created vendor: {vendor_data['name']}"))
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Successfully created {len(vendors_data)} vendors with products and reviews!"))

    def create_vendor_image(self, filename, vendor_name, category):
        """Create a placeholder vendor image"""
        # Create a colorful image
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
        color = random.choice(colors)
        
        img = Image.new('RGB', (400, 400), color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 32)
            small_font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add text with better positioning
        initials = ''.join([word[0] for word in vendor_name.split()[:2]]).upper()
        
        # Draw circle background for initials
        draw.ellipse([100, 100, 300, 300], fill='white', outline=color, width=3)
        
        # Draw initials
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (400 - text_width) // 2
        y = (400 - text_height) // 2 - 20
        draw.text((x, y), initials, fill=color, font=font)
        
        # Draw category at bottom
        bbox = draw.textbbox((0, 0), category, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = (400 - text_width) // 2
        draw.text((x, 320), category, fill='white', font=small_font)
        
        # Save image
        vendors_dir = os.path.join(settings.MEDIA_ROOT, 'vendors')
        os.makedirs(vendors_dir, exist_ok=True)
        img_path = os.path.join(vendors_dir, filename)
        img.save(img_path)

    def create_product_image(self, filename, product_name):
        """Create a placeholder product image"""
        # Create a gradient-like image
        colors = ['#FFE5E5', '#E5F5FF', '#E5FFE5', '#FFF5E5', '#F5E5FF', '#FFFFE5']
        color = random.choice(colors)
        
        img = Image.new('RGB', (300, 300), color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except:
            font = ImageFont.load_default()
        
        # Add decorative border
        draw.rectangle([10, 10, 290, 290], outline='#666666', width=2)
        
        # Add product name (wrapped)
        words = product_name.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > 250:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center the text
        total_height = len(lines) * 25
        start_y = (300 - total_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (300 - text_width) // 2
            y = start_y + (i * 25)
            draw.text((x, y), line, fill='#333333', font=font)
        
        # Save image
        products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(products_dir, exist_ok=True)
        img_path = os.path.join(products_dir, filename)
        img.save(img_path)
