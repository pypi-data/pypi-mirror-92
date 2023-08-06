from django.views.generic import View,CreateView,ListView,DetailView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse,reverse_lazy
from django.db.models import Q
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from .models import ActivityInstall, ActivityRemove, ActivityReason
from .models import Activity, Actor, OldDevice
from .forms import  ActorForm, ActorFilterForm
from .filters import ActorFilter
from .tables import ActorTable

from dcim.models import Device, DeviceRole
from utilities.views import BulkDeleteView, ObjectEditView, ObjectListView, ObjectDeleteView


#from extras.models import ChangeLoggedModel
#from rq import Worker #verificar se a para usar
#logger = logging.getLogger("rq.worker") #verificar se da para usar

'''
Version 2 : PlugConectividadeapp
'''

#view for input information on the device for get,
#input method post activity, its send to view CreateactivityView
class ListConectividadeView(LoginRequiredMixin,View):
    
    """
    List all reg in the database.
    """
 
    #tratar

    def get(self, request):
 
        rg = Activity.objects.all().order_by('-id')[:5] 
        ls = Device.objects.order_by('-id')[:10] 
        dr = DeviceRole.objects.all()

        quantity = len(ls)#verifica se tem device instalado
        
        if quantity == 0 : #se não tem manda false
            quant=False
        else:
            quant=True


        context = {
            'registro': rg,
            'devicerole': dr,
            'ls': ls,
            'quant':quant,   
        }
       
        return render(request, 'conectividadeapp/listagem.html', context)

    def post(self, request):

        
        rg = Activity.objects.all().order_by('-id')[:5] 
        dv = Device.objects.all()  
        ls = Device.objects.order_by('-id')[:30] 
        dr = DeviceRole.objects.all()
        actors= Actor.objects.all()

        quantity = len(ls)#verifica se tem device instalado
        
        if quantity == 0 : #se não tem device cadastrado nada false
            quant=False
        else:
            quant=True

        #analisar se é a melhor maneira
        if request.POST['deviceid'] :   
            deviceid  = request.POST['deviceid']
        
        else:
            print("erro deviceid")
            return redirect('plugins:conectividadeapp:list')


        if request.POST['op'] :

            op = request.POST['op']
            

            if op == "1" : 
                
                activity_reason = ActivityReason.objects.filter(type="INSTALL")

            else :
                activity_reason = ActivityReason.objects.filter(type="REMOVE")
      
        else:
            #print("erro op")
            return redirect('plugins:conectividadeapp:list')


        #testes e revisar!
        # try get object for post
        try: 
            device_obj =get_object_or_404(Device.objects.filter(id=deviceid)) # cria instancia do device
        #erro
        except MultiValueDictKeyError :

            return redirect('plugins:conectividadeapp:list')
    
        else:
            
            if deviceid :
                device_obj = Device.objects.get(id=deviceid) # cria instancia do device
  
                context = {
                        'registro': rg,
                        'devicerole': dr,
                        'ls': ls,
                        'op': op,
                        'deviceid':deviceid,
                        'device_obj':device_obj, 
                        'actors':actors,   
                        'quant':quant,    
                        'activity_reason':activity_reason,
                                     

                    }
                return render(request, 'conectividadeapp/listagem.html', context)
            else:
                
                return redirect('plugins:conectividadeapp:list')
    


        # Context dictionary for rendering
        context = {
                    'registro': rg,
                    'devicerole': dr,
                    'ls': ls,
                    'op': op,
                    'actors': actors,  
                    'quant': quant,
                    'activity_reason': activity_reason, 
                }
        
        return render(request, 'conectividadeapp/listagem.html', context)

#view to save activity and olddevice. 
# Save  automaticy olddevice made in activity. 
# its dependency to save activity.
class CreateactivityView(LoginRequiredMixin,View):
    def get(self, request):
        
       
        return render(request, 'conectividadeapp/activity_op.html')


    def post(self, request):

        data = {}
        
        op = request.POST['op']
                    
        # opção de remoção ou instalação para um determinado device
        #removal or installation option for a given device
        if op=="1" or op == "0":
        

            data['registro'] = Activity.objects.all().order_by('-id')[:5] 

            deviceobj=request.POST['device_obj_id']
            actorlist=request.POST.getlist('actorss')
            reasonobj=request.POST['reason']
            #fks:
            dev_ob = Device.objects.get(id=deviceobj)
            res_ob = ActivityReason.objects.get(id=reasonobj)
            #onetoone
            gravadevice = OldDevice.objects.create(
                    name = request.POST['device_name'], 
                    ipv4 = request.POST['ip'],
                    ipv6 = request.POST['ipv6'],
                    site = request.POST['site'], 
                    rack = request.POST['rack']
                    )
            res_old =OldDevice.objects.get(id=gravadevice.pk)
            
            if op == "1": #entra aqui se for install
                activity_op =ActivityInstall.objects.create(device= dev_ob,olddevice=res_old,reason=res_ob,when=request.POST['year_month_day'],description=request.POST['description'])
            else: #entra aqui se for remov 
                activity_op =ActivityRemove.objects.create(device= dev_ob,olddevice=res_old,reason=res_ob,when=request.POST['year_month_day'],description=request.POST['description'])


            for k in actorlist: #add list
                activity_op.actor.add(k)

            activity_op.is_active=False
            activity_op.save()
            
            
            atv=Activity.objects.last()
            data['id_activit'] = atv.pk

            return render(request, 'conectividadeapp/activity_success.html', data)
        

        # imput multiple devices /insere varios devices para uma atividade
        if op=="3" or op == "4":

            devices_multlist=request.POST.getlist('devices_mult')
            tam=len(devices_multlist)
           
            data['registro'] = Activity.objects.all().order_by('-id')[:tam] 

           
            for j in devices_multlist:
              
                
                actorlist=request.POST.getlist('actorss')
                reasonobj=request.POST['reason']


                #fks/ create to objects device and activity reason:
                dev_ob = Device.objects.get(id=j)
                res_ob = ActivityReason.objects.get(id=reasonobj)

                # tratamento de atributos do objeto selecionado / object attributes processing for olddevice:
                
                if dev_ob.name == None :
                    dev_ob.name = ""
                if dev_ob.primary_ip4 == None :
                    dev_ob.primary_ip4 = None
                if dev_ob.primary_ip6 == None :
                    dev_ob.primary_ip6 = None
                if dev_ob.site == None :
                    dev_ob.site = ""

                if dev_ob.rack == None :
                    rack = None
                else :
                    rack = dev_ob.rack.name
                '''
                print(dev_ob.name)
                print(dev_ob.primary_ip4)
                print(dev_ob.primary_ip6)
                print(dev_ob.site)
                print(dev_ob.rack.name)
                '''
                #onetoone
                gravadevice = OldDevice.objects.create(
                        name = dev_ob.name, 
                        ipv4 = dev_ob.primary_ip4,
                        ipv6 = dev_ob.primary_ip6,
                        site = dev_ob.site, 
                        rack = rack
                        )
                res_old =OldDevice.objects.get(id=gravadevice.pk)
                
                if op == "3": #entra aqui se for atividade de instalação/into install activity
                    activity_op =ActivityInstall.objects.create(device= dev_ob,olddevice=res_old,reason=res_ob,when=request.POST['year_month_day'],description=request.POST['description'])
                else: #entra aqui se for atividade de remoção / into remove activity
                    activity_op =ActivityRemove.objects.create(device= dev_ob,olddevice=res_old,reason=res_ob,when=request.POST['year_month_day'],description=request.POST['description'])


                for k in actorlist: # adiciona lista de atores /add  actores list
                    activity_op.actor.add(k)

                activity_op.is_active=False #mecanismo de status da atividade, tratado no signals django
                activity_op.save() #save is active / salvo atributo "is_active"
            
            
            #get id in object for demonstration in template/ pega objeto para demotrar no template
            atv=Activity.objects.last() 
            data['id_activit'] = atv.pk
            
            return render(request, 'conectividadeapp/activity_success.html', data)
        
'''
Activity Filter Views
'''

# All activities
# Activity List Views

class ActivityopListView(LoginRequiredMixin, View):

    def get(self, request):


        return render(request, 'conectividadeapp/activity_op.html')

class ActivityListView(LoginRequiredMixin, View):

    def get(self, request, type):

        # Current year
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day

        # Template to be rendered
        template_name = 'conectividadeapp/activity_list.html'

        # Search and Filters setup
        r = request.GET

        search = None
        year_month_day_researched = None
        year_month_researched = None
        year_researched = None

        first_activity = Activity.objects.all().order_by('when')[0]

        if 'btn-search-research' in r:
            if r.get('search') is not None:
                search = r.get('search')

                activity_list = (
                    Activity.objects.filter(type__icontains=search)
                    | Activity.objects.filter(actor__name__icontains=search)
                    | Activity.objects.filter(description__icontains=search)
                ).order_by('-when')

        elif 'btn-year-month-day-research' in r:
            if r.get('year_month_day') is not None:
                year_month_day_researched = datetime.datetime.strptime(r.get('year_month_day'), '%Y-%m-%d')

                activity_list = Activity.objects.filter(
                    when__year=year_month_day_researched.year,
                    when__month=year_month_day_researched.month,
                    when__day=year_month_day_researched.day,
                ).order_by('-when')

        elif 'btn-year-month-research' in r:
            if r.get('year_month') is not None:
                year_month_researched = datetime.datetime.strptime(r.get('year_month'), '%Y-%m')

                activity_list = Activity.objects.filter(
                    when__year=year_month_researched.year,
                    when__month=year_month_researched.month,
                ).order_by('-when')

        elif 'btn-year-research' in r:
            if r.get('year') is not None:
                year_researched = datetime.datetime.strptime(r.get('year'), '%Y')

                activity_list = Activity.objects.filter(
                    when__year=year_researched.year,
                ).order_by('-when')

        else:
            activity_list = Activity.objects.all().order_by('-when')

        if type == 'INSTALL' or type == 'REMOVE':
            activity_list = activity_list.filter(type=type)

        # Limits listing of only active activities
        activity_list = activity_list.filter(is_active=True)
        
        # Quantity of activities after the filter
        quantity = len(activity_list)

        # Context dictionary for rendering
        context = {
            'current_year': current_year,
            'current_month': current_month,
            'current_day': current_day,
            'activity_list': activity_list,
            'quantity': quantity,
            'first_activity': first_activity,
            'year_month_researched': year_month_researched,
            'year_month_day_researched': year_month_day_researched,
            'year_researched': year_researched,
        }

        return render(request, template_name, context)




'''
Activity details (DetailView) and update
'''

#detalhes da atividade
class ActivityDetailsView(LoginRequiredMixin,DetailView):
    model = Activity
    template_name = 'conectividadeapp/activity_details.html'

#update atividade (ActivityUpdateView)
#class ActivityUpdateView(PermissionRequiredMixin,LoginRequiredMixin,View):
class ActivityUpdateView(LoginRequiredMixin,View):

    def get(self, request, pk):
        pass

    def post(self, request, atv):

        if request.POST['status'] :

            status =  request.POST['status'] 
            print(status)

            if status == "True" :
                Activity.objects.filter(pk=atv).update(is_active=False)

            else :
                Activity.objects.filter(pk=atv).update(is_active=True)

        else:

            return redirect('plugins:conectividadeapp:list')
       
       
        activity= get_object_or_404(Activity.objects.filter(id = atv))
        
        return render(request, 'conectividadeapp/activity_details.html', {
            'activity' : activity 
        } )

'''
 Device history

'''

class DeviceHistoryView(LoginRequiredMixin,View):
    def get(self, request, pk):
        device = get_object_or_404(Device.objects.filter(id=pk))
        o = Device.objects.get(id=pk)    # pega o objeto da atividade
        activitys = o.activity_set.all()
        return render(request, 'conectividadeapp/device_history.html',  {
            'device': device,
            'activitys': activitys,
        })

    def post(self, request):
        
        actors=Actor.objects.all()


         #analisar se é a melhor maneira
        if request.POST['device_obj_id'] :   
            deviceid  = request.POST['device_obj_id']
            device_obj = Device.objects.get(id=deviceid) # cria instancia do device

        else:
            print("erro device_obj_id")
            return redirect('plugins:conectividadeapp:list')


        if request.POST['op'] :

            op = request.POST['op']
            

            if op == "1" : 
                
                activity_reason = ActivityReason.objects.filter(type="INSTALL")

            else :
                activity_reason = ActivityReason.objects.filter(type="REMOVE")
      
        else:
            print("erro op")
            return redirect('plugins:conectividadeapp:list')

        context = {      
                        'op': op,
                        'actors': actors,  
                        'activity_reason': activity_reason, 
                        'device_obj':device_obj
                    }

        return render(request, 'conectividadeapp/activity_form_device.html', context)


'''
    Multiple Device
'''

  
class SelectMultipleView(LoginRequiredMixin,View):

  
    def post(self, request): #metodo para achamada form
        
        
        device_obj= True
        actors= Actor.objects.all()

        
        if request.POST.getlist('devices_mult') : 
                
            devices_mult=request.POST.getlist('devices_mult')

            quantity = len(devices_mult)#verifica quantos tem na lista
            
            #print(devices_mult)
            #print(quantity)
            #print("----")
          
            if quantity == 1 or quantity == 2  :
                #print("a")
                #print(devices_mult)
                #print(quantity)
                return redirect('plugins:conectividadeapp:searchdevice')
            
            else :
                # se mais de um device é selecionado ok!
                del devices_mult[0] #deleta o primeiro elemento (elemento de controle)
                #cria os objetos

                #https://docs.djangoproject.com/en/dev/topics/db/queries/#the-pk-lookup-shortcut

                #obj = Device.objects.in_bulk(devices_mult, field_name='pk')
                obj = Device.objects.filter(pk__in=devices_mult)
        else :
            print("b")

            return redirect('plugins:conectividadeapp:searchdevice')
   

        if request.POST['op'] :
        
            op = request.POST['op']
            
            if op == "3" : 

                activity_reason  = ActivityReason.objects.filter(type="INSTALL")

            else :
                
                activity_reason = ActivityReason.objects.filter(type="REMOVE")
       
        else :
            
            #print("c")

            return redirect('plugins:conectividadeapp:searchdevice')

        
        
        return render(request, 'conectividadeapp/activity_form_select_multipledevice.html', { 
                
                'devices_mult':devices_mult,
                'obj':obj,
                'device_obj':device_obj,
                'activity_reason':activity_reason,
                'op':op,
                'actors':actors,
            }
            )
 
'''
CRUD actor
'''

class ActorView(LoginRequiredMixin,View):
    def get(self, request, pk):
        actor = get_object_or_404(Actor.objects.filter(id=pk))
        o=Actor.objects.get(id=pk) #pega o objeto da atividade
        activitys=o.activity_set.all()
        return render(request, 'conectividadeapp/actor.html',  {
            'actor': actor,
            'activitys': activitys,
        })

class CreateActor(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'conectividadeapp.add_actor'
    model = Actor
    queryset = Actor.objects.all()
    model_form =  ActorForm
    template_name = 'conectividadeapp/actor_edit.html'
    default_return_url = 'plugins:conectividadeapp:actor_list'

class EditActor(LoginRequiredMixin,CreateActor):
    permission_required = 'conectividadeapp.change_actor'

class ActorListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'conectividadeapp.view_actor'
    queryset = Actor.objects.all()
    filterset = ActorFilter
    filterset_form = ActorFilterForm
    table = ActorTable
    template_name = 'conectividadeapp/actor_list.html'

class DeleteActor(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'conectividadeapp.delete_actor'
    model = Actor
    default_return_url = 'plugins:conectividadeapp:actor_list'

class BulkDeleteActor(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'conectividadeapp.delete_actor'
    queryset = Actor.objects.filter()
    table = ActorTable
    default_return_url = 'plugins:conectividadeapp:actor_list'
'''
Search Devices Views
'''
class ListDeviceView(LoginRequiredMixin,ListView):
    model = Device
    template_name = 'conectividadeapp/searchdevice.html'

class SearchDeviceView(LoginRequiredMixin,ListView):
    model = Device
    template_name = 'conectividadeapp/searchdeviceresult.html'

    def get_queryset(self):

        query = self.request.GET.get('q')
        object_list = Device.objects.filter(
            Q(asset_tag__icontains=query)
            | Q(name__icontains=query)
        )
        return object_list
