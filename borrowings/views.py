from rest_framework.viewsets import ModelViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingListSerializer, BorrowingDetailSerializer


class BorrowingsViewSet(ModelViewSet):

    serializer_class = BorrowingSerializer
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BorrowingListSerializer
        if self.action == 'retrieve':
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
