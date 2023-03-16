from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Bulletin)
admin.site.register(models.Guest)
admin.site.register(models.Department)
admin.site.register(models.EveningTask)
admin.site.register(models.MorningTask)
admin.site.register(models.Asset)
admin.site.register(models.Audit)
admin.site.register(models.RenewedAsset)

admin.site.site_header = "MIS Log System"
admin.site.site_title = "MIS Log System"