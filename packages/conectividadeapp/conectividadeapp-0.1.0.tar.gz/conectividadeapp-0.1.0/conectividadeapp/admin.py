from django.contrib import admin
from .models import Activity
from .models import Actor
from .models import OldDevice
from .models import ActivityInstall, ActivityRemove, ActivityReason
from .models import ActorCategory



@admin.register(ActorCategory)
class ActorCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'type']


@admin.register(OldDevice)
class OldDevice(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
   list_display = ('id','name')


@admin.register(ActivityInstall)
class ActivityInstallAdmin(admin.ModelAdmin):
    list_display = ['id', 'when', 'description', 'reason', 'type']

@admin.register(ActivityRemove)
class ActivityRemoveAdmin(admin.ModelAdmin):
    list_display = ['id', 'when', 'description', 'reason', 'type']

@admin.register(ActivityReason)
class ActivityReason(admin.ModelAdmin):
    list_display = ['name', 'type']

 
#admin.site.register(Categoria)
#admin.site.register(Registroo)

#admin.site.register()

# Register your models here.