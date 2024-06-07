from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


import litRevu.views

urlpatterns = [
    path("ticketCreation", litRevu.views.TicketCreationView.as_view(), name="ticket_creation"),
    path("ticket&reviewCreation", litRevu.views.TicketReviewCreationView.as_view(), name="ticket_review_creation"),
    path("reviewCreation", litRevu.views.ReviewCreationView.as_view(), name="review_creation"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

