from django.urls import path
from accounts.views import CustomGraphQLView

urlpatterns = [
    path("ql_schema/", CustomGraphQLView.as_view(graphiql=True), name="ql_schema"),
]