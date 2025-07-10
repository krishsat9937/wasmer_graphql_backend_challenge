# core/views.py
from strawberry.django.views import AsyncGraphQLView
from core.loaders import AppsByUserLoader
from strawberry.django.views import StrawberryDjangoContext

class CustomGraphQLContext(StrawberryDjangoContext):
    def __init__(self, request, response):
        super().__init__(request, response)
        # add your loaders as an attribute
        self.loaders = {
            "apps_by_user": AppsByUserLoader(),
        }

class CustomGraphQLView(AsyncGraphQLView):
    async def get_context(self, request, response):
        # completely ignore the parent’s context and return yours
        return CustomGraphQLContext(request, response)
