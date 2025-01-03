from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingReadSerializer, BorrowingCreateSerializer, BorrowingReturnSerializer


class BorrowingsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = BorrowingReadSerializer
    queryset = Borrowing.objects.all().select_related('user', "book")

    def get_serializer_class(self):
        if self.action == 'create':
            return BorrowingCreateSerializer
        else:
            return BorrowingReadSerializer

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id')
        is_active = self.request.query_params.get('is_active')

        if self.request.user.is_superuser and user_id:
            user_id = int(user_id)
            queryset = queryset.filter(user_id=user_id)

        if self.request.user.is_superuser and is_active:
            is_active = True if is_active.lower() == 'true' else False
            queryset = queryset.filter(is_active=is_active)

        elif not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class BorrowingReturnAPIView(
    generics.CreateAPIView,
):
    serializer_class = BorrowingReturnSerializer
    queryset = Borrowing.objects.all()

    def post(self, request, pk=None):
        borrowing = self.get_object()
        serializer = self.get_serializer(
            borrowing,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
