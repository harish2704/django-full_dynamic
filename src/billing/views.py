from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.template.context import RequestContext
from django.db.models.loading import cache
import pprint
from billing.forms import *
from django.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from eav.forms import BaseDynamicEntityForm
from itertools import izip


def index(request):
    return render_to_response('billing/index.html',
                              {   'data':pprint.pformat(cache.__dict__),
                                  'request':request,},
                              RequestContext(request))

def form(request):
    data = {}
    entities = Entity.objects.all()
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        customer_form = CustomerForm(request.POST)
        ordereditem_formset = OrderedItemFormSet(request.POST,prefix='oi')
        item_formset = ItemFormSet(request.POST,prefix='i')
        # import ipdb ; ipdb.set_trace()
        if customer_form.is_valid() and order_form.is_valid() and ordereditem_formset.is_valid() and item_formset.is_valid():
            customer = customer_form.save()
            order = order_form.save(commit=False)
            order.customer = customer
            order.save()
            for ordereditem, item in izip( ordereditem_formset.save(commit=False), item_formset.save(commit=False)):
                ordereditem.order = order
                ordereditem.save()
                item.ordered_item = ordereditem
                item.save()
                data.update({'msg':'Form Saved Successfully'})
    else:
        # import ipdb ; ipdb.set_trace()
        order_form = OrderForm()
        customer_form = CustomerForm()
        ordereditem_formset = OrderedItemFormSet(prefix='oi',
                                                 queryset=OrderedItem.objects.none())
        item_formset = ItemFormSet(prefix='i',
                                   queryset=Item.objects.none())
    data.update({'entities':entities,
            'order_form':order_form,
            'customer_form':customer_form,
            'izip_forms':izip(ordereditem_formset.forms,item_formset.forms),
            'izip_managementforms':[ordereditem_formset.management_form,
                                    item_formset.management_form]})
    return render_to_response('billing/form.html',
                            RequestContext(request,data))

def ajax(request):
    if request.method == 'POST' :
        try:
            itemtype = request.POST['itemtype']
            num = request.POST['num']
        except KeyError:
            itemtype = ''
            num = 0
        # import ipdb ; ipdb.set_trace()
        entt = Entity.objects.get(id = int(itemtype))
        itemm = Item()
        itemm.entity = entt
        formm = ItemForm(instance=itemm,prefix= 'i-%s' % num)
        formm.fields['ORDER'] = IntegerField(required = False,
                                             widget = HiddenInput,
                                             label ='Order',
                                             )
        formm.fields['DELETE'] =BooleanField(label = 'Delete',
                                             required = False,
                                             widget = HiddenInput,
                                             )
        formm.fields['id'] = CharField(required = False,
                                       widget = HiddenInput,
                                       )
        return HttpResponse (formm.as_ul())

def order(request, o_id):
    data = {}
    entities = Entity.objects.all()
    order = Order.objects.get(id = o_id)
    ordered_items = order.ordereditem_set.all()
    items = Item.objects.filter(ordered_item__order=order)
    order_form = OrderForm(instance = order)
    ordereditem_formset = OrderedItemFormSet(prefix='oi',
                                             queryset=ordered_items)
    item_formset = ItemFormSet(prefix='i',
                               queryset=items)
    data.update({'entities':entities,
            'order_form':order_form,
            # 'custmer_form':customer_form,
            'izip_forms':izip(ordereditem_formset.forms,item_formset.forms),
            'izip_managementforms':[ordereditem_formset.management_form,
                                    item_formset.management_form]})
    return render_to_response('billing/form.html',
                              RequestContext(request,data))

def orders(request):
    orders = Order.objects.all()
    data = {'orders':orders}
    return render_to_response('billing/orders.html',
                              RequestContext(request,data))










# vim: set ft=python.django:
