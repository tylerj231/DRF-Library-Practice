from django.urls import path, include
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingsViewSet, BorrowingReturnAPIView

app_name = 'borrowings'
router = DefaultRouter()
router.register('borrowings', BorrowingsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("borrowings/<int:pk>/return/",BorrowingReturnAPIView.as_view(), name='return'),
]