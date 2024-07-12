from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


import litRevu.views

urlpatterns = [
    path("ticketCreation", litRevu.views.TicketCreationView.as_view(), name="ticket_creation"),
    path("ticket&reviewCreation", litRevu.views.TicketReviewCreationView.as_view(), name="ticket_review_creation"),
    path("reviewCreation/<int:id>", litRevu.views.ReviewCreationView.as_view(), name="review_creation"),
    path("subPage", litRevu.views.SubCreationView.as_view(), name="sub_page"),
    path("userPosts", litRevu.views.UserPostsView.as_view(), name="user_posts"),
    path("ticketModification/<int:id>", litRevu.views.TicketModification.as_view(), name="ticket_modification")

]

htmx_urlpatterns = [
    path('subscribe_to/', litRevu.views.sub_to, name='subscribe_to'),
    path('unsubscribe_to/<str:unfollow_user>', litRevu.views.unsub_to, name='unsubscribe_to'),

]

urlpatterns += htmx_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


