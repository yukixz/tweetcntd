from django.conf.urls import include, patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('tweetcntd.views.home')),
    url(r'^auth/', include('tweetcntd.views.auth')),
    url(r'^admin/', include('tweetcntd.views.admin')),
    # url(r'^backend/', include('tweetcntd.views.backend')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
