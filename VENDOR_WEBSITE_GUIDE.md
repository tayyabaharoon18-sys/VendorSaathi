# Vendor Website & Contact Integration Guide

## Overview
Vendors can now have their own external websites/profiles, and customers can directly visit them when browsing by category.

## New Features Added

### 1. **Vendor Contact Information**
Each vendor profile now includes:
- ✅ **Website URL** - Link to vendor's external website or social media profile
- ✅ **Phone Number** - Direct calling capability
- ✅ **Email Address** - Contact email

### 2. **Vendor Cards Enhancement**
On the vendors listing page (`/vendors/`):
- Vendors with websites show a "Visit Website" link
- Quick access button to open vendor's external site in new tab
- "View Profile" button to see full VendorSaathi profile

### 3. **Vendor Detail Page**
On individual vendor pages:
- Contact information section with phone, email, and website
- "Call Vendor" button (if phone provided)
- "Visit Website" button (if website provided)
- All links open in new tabs for external sites

## How to Add Vendor Websites

### Via Django Admin Panel

1. **Login to Admin**
   - Visit: `http://127.0.0.1:8000/admin/`
   - Login with your credentials

2. **Edit Vendor Profile**
   - Go to "Vendor Profiles"
   - Click on a vendor or "Add Vendor Profile"

3. **Add Contact Information**
   - **Website**: Full URL (e.g., `https://example.com` or `https://instagram.com/vendorname`)
   - **Phone**: Contact number (e.g., `+91-9876543210`)
   - **Email**: Contact email (e.g., `vendor@example.com`)

4. **Save**
   - Click "Save" to update the vendor profile

## Customer Experience

### When Browsing by Category:

1. Customer visits `/vendors/` or filters by category (e.g., Food & Beverages)
2. Each vendor card shows:
   - Vendor photo
   - Name and location
   - Rating and reviews
   - Brief story
   - **"Visit Website" link** (if available)
   - **"View Profile" button**

3. Customer can:
   - Click "Visit Website" → Opens vendor's external site in new tab
   - Click "View Profile" → See full VendorSaathi profile with products

### On Vendor Detail Page:

- Contact information displayed prominently
- Direct action buttons:
  - "Call Vendor" → Opens phone dialer
  - "Visit Website" → Opens external website
  - "Share Profile" → Share VendorSaathi profile

## Example Websites You Can Add

- **Official Website**: `https://vendorname.com`
- **Instagram**: `https://instagram.com/vendorname`
- **Facebook**: `https://facebook.com/vendorname`
- **WhatsApp Business**: `https://wa.me/919876543210`
- **Google Maps**: `https://maps.google.com/?q=Business+Name`
- **LinkedIn**: `https://linkedin.com/company/vendorname`

## Benefits

### For Vendors:
✅ Drive traffic to their own websites/social media
✅ Multiple touchpoints with customers
✅ Better business visibility
✅ Professional presentation

### For Customers:
✅ Easy access to vendor's full offerings
✅ Multiple ways to contact vendors
✅ Seamless browsing experience
✅ Quick navigation between VendorSaathi and external sites

## Database Changes

New fields added to `VendorProfile` model:
```python
website = models.URLField()      # Vendor's website URL
phone = models.CharField()       # Contact phone
email = models.EmailField()      # Contact email
```

All fields are optional (blank=True, null=True), so existing vendors won't break.

## Testing

1. **Create a Test Vendor with Website**
   ```
   - Login to admin
   - Add new vendor
   - Fill in name, category, location
   - Add website: https://example.com
   - Add phone: +91-1234567890
   - Save
   ```

2. **Browse Vendors**
   - Visit: http://127.0.0.1:8000/vendors/
   - Filter by category
   - See "Visit Website" button on vendor card

3. **View Vendor Detail**
   - Click "View Profile"
   - See contact information section
   - Click "Visit Website" button
   - Verify it opens in new tab

## Technical Implementation

### Files Modified:
1. ✅ `core/models.py` - Added website, phone, email fields
2. ✅ `core/admin.py` - Enhanced admin interface
3. ✅ `core/templates/vendor_detail.html` - Contact info & website buttons
4. ✅ `core/templates/core/vendors.html` - Website links on cards
5. ✅ `main/static/css/style.css` - Styling for contact info
6. ✅ Database migration created and applied

### Security Features:
- ✅ External links open in new tab (`target="_blank"`)
- ✅ `rel="noopener"` prevents reverse tabnabbing
- ✅ URL validation in model field
- ✅ Safe rendering in templates

## Next Steps

1. **Add Vendors**: Login to admin and add website URLs to existing vendors
2. **Test Flow**: Browse by category → Click "Visit Website"
3. **Share with Users**: Vendors can now provide their complete web presence

---

**Need Help?**
- Check Django admin for easy vendor management
- All fields are optional - add what you have
- Test with real URLs to ensure links work correctly
