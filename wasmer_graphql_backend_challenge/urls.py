from django.contrib import admin
from django.urls import path
from core.views import CustomGraphQLView
from core.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "graphql/",
        CustomGraphQLView.as_view(
            schema=schema,
            graphiql=True,    # enable GraphiQL
        ),
        name="graphql",
    ),
]
