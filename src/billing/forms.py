from billing.models import *
from eav.forms import BaseDynamicEntityForm
from django.forms import *
from django.forms.models import modelform_factory, modelformset_factory, formset_factory, BaseModelFormSet, ModelForm
from django.forms.util import ErrorList


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])


class CusModelForm(ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=DivErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        super(CusModelForm,self).__init__(data, files, auto_id,
                                          prefix, initial, error_class,
                                          label_suffix, empty_permitted,
                                          instance)


CustomerForm = modelform_factory(Customer,
                                 form=CusModelForm)

OrderForm = modelform_factory(Order,
                              exclude=('customer'),
                              form=CusModelForm)

OrderedItemForm = modelform_factory(OrderedItem,
                                    exclude=('order'),
                                    form=CusModelForm)

class ItemForm(BaseDynamicEntityForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        opts = self._meta
        if instance is None:
            if opts.model is None:
                raise ValueError('ModelForm has no model class specified.')
            # if we didn't get an instance, instantiate a new one
            e_id = ''
            if data is not None:
                try:
                    e_id = data[prefix + '-entity']
                except KeyError:
                    pass
            self.instance = opts.model(entity_id=e_id)
            object_data = {}
        else:
            self.instance = instance
            object_data = model_to_dict(instance, opts.fields, opts.exclude)
        # if initial was provided, it should override the values from instance
        if initial is not None:
            object_data.update(initial)
        # self._validate_unique will be set to True by BaseModelForm.clean().
        # It is False by default so overriding self.clean() and failing to call
        # super will stop validate_unique from being called.
        self._validate_unique = False
        super(BaseModelForm, self).__init__(data, files, auto_id, prefix, object_data,
                                            error_class, label_suffix, empty_permitted)
        self._build_dynamic_fields()
    class Meta:
        model = Item
        exclude = ('ordered_item')
        widgets = {
            # 'entity': HiddenInput,
        }


class MyBaseFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(MyBaseFormSet, self).add_fields(form, index)
        form.fields['ORDER'].widget = HiddenInput()
        form.fields['DELETE'].widget = HiddenInput()


OrderFormSet = modelformset_factory(Order,
                                    exclude=('customer'),
                                    form=CusModelForm,
                                    )

OrderedItemFormSet = modelformset_factory(OrderedItem,
                                          exclude=('order'),
                                          form=CusModelForm,
                                          can_delete=True,
                                          can_order=True,
                                          formset = MyBaseFormSet,)

ItemFormSet = modelformset_factory(Item,
                                   exclude=('ordered_item'),
                                   form=ItemForm,
                                   can_delete=True,
                                   can_order=True,
                                   formset = MyBaseFormSet,)



# vim: set ft=python.django:
