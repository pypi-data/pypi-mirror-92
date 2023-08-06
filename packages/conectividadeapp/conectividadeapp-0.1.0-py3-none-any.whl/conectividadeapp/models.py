from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE, PROTECT
from dcim.models import Device


from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE

from dcim.models import Device


class ActorCategory(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Name',
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Complete Name',
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='E-mail',
    )
    category = models.ForeignKey(
        ActorCategory,
        on_delete=models.PROTECT,
        verbose_name='Category',
    )
    cellphone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Cellphone',
    )
    telephone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Telephone',
    )

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

    def __str__(self):
        return self.name

    @property
    def first_name(self):
        return self.name.split()[0]

class OldDevice(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    rack = models.CharField(max_length=100, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    ipv4 = models.CharField(max_length=40, null=True, blank=True)
    ipv6 = models.CharField(max_length=70, null=True, blank=True)

class ActivityAbstract(models.Model):

    device = models.ForeignKey(
        Device,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    olddevice = models.OneToOneField(
        OldDevice, 
        on_delete=CASCADE, 
        null=True,
        blank=True,
    )
    actor = models.ManyToManyField(
        Actor,
    )

    when = models.DateField(
        default=date.today,
    )

    description = models.TextField(
        max_length=255,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default = True,
    )

    def __str__(self):
        return f'{self.id}'

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    class Meta:
        abstract = True

class ActivityReason(models.Model):
    CHOICES = [
        ('INSTALL', 'Instalação'),
        ('REMOVE', 'Remoção'),
    ]

    name = models.CharField(
        max_length=256,
    )

    type = models.CharField(
        max_length=7,
        choices=CHOICES,
        default='INSTALL',
    )

    def __str__(self):
        return f'{self.name}'


class Activity(ActivityAbstract):
        reason = models.ForeignKey(
            'ActivityReason',
            on_delete=models.CASCADE,
            null=True,
            blank=True,
        )

        type = models.CharField(
            max_length=7,
            default='INSTALL',
        )

class ActivityInstall(ActivityAbstract):
    reason = models.ForeignKey(
        ActivityReason,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'INSTALL'}
    )

    type = models.CharField(
        max_length=7,
        default='INSTALL'
    )

    main_activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

class ActivityRemove(ActivityAbstract):
    reason = models.ForeignKey(
        ActivityReason,
        on_delete=models.CASCADE,
        limit_choices_to={'type': 'REMOVE'}
    )

    type = models.CharField(
        max_length=7,
        default='REMOVE'
    )

    main_activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True, blank=True
    )


'''
DJANGO SIGNALS FOR ACTIVITY MANAGEMENT
'''

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

@receiver(post_save, sender=ActivityInstall or ActivityRemove)
def create_new_activity(sender, instance, created, **kwargs):
    if created:
        activity = Activity.objects.create(
            device=instance.device,
            olddevice=instance.olddevice,
            when=instance.when,
            description=instance.description,
            reason=instance.reason,
            type=instance.type,
            is_active=instance.is_active,
        )
        instance.main_activity = activity
        instance.save()
    else:
        if not instance.is_active:
            instance.delete()
            
post_save.connect(create_new_activity, sender=ActivityInstall)
post_save.connect(create_new_activity, sender=ActivityRemove)

@receiver(m2m_changed, sender=ActivityInstall.actor.through or ActivityRemove.actor.through)
def add_actors_to_activity(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        main_activity = instance.main_activity
        actors = model.objects.filter(pk__in=pk_set)
        for actor in actors:
            main_activity.actor.add(actor.pk)
        main_activity.save()
       

m2m_changed.connect(add_actors_to_activity, sender=ActivityInstall.actor.through)
m2m_changed.connect(add_actors_to_activity, sender=ActivityRemove.actor.through)