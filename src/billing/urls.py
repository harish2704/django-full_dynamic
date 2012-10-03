from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^$','billing.views.index'),
    (r'^form/','billing.views.form'),
    (r'^ajax/','billing.views.ajax'),
    (r'^orders/','billing.views.orders'),
    (r'^order/(?P<o_id>\d+)/$','billing.views.order'),

)









# vim: set ft=python.django:
