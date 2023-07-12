from django.contrib import admin
from app.models import User,Product,Complaint,SpecialOffer,Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Complaint)
admin.site.register(SpecialOffer)
admin.site.register(Cart)