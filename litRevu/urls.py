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
    path("userTickets", litRevu.views.UserTicketsView.as_view(), name="user_tickets"),
    path("userReviews", litRevu.views.UserReviewsView.as_view(), name="user_reviews"),
    path("ticketModification/<slug:pk>/", litRevu.views.TicketModification.as_view(), name="ticket_modification"),
    path("reviewModification/<slug:pk>/", litRevu.views.ReviewModification.as_view(), name="review_modification"),
    path("deleteReview/<slug:pk>/", litRevu.views.DeleteReview.as_view(), name="delete_review"),
    path("deleteTicket/<slug:pk>/", litRevu.views.DeleteTicket.as_view(), name="delete_ticket")

]

htmx_urlpatterns = [
    path('subscribe_to/', litRevu.views.sub_to, name='subscribe_to'),
    path('unsubscribe_to/<str:unfollow_user>', litRevu.views.unsub_to, name='unsubscribe_to'),

]

urlpatterns += htmx_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


