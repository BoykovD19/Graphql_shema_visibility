import graphene
from graphene_django.types import DjangoObjectType
from accounts.models import User, UserInfo


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserModelInfo(DjangoObjectType):
    class Meta:
        model = UserInfo
        fields = "__all__"


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True),
                          description='Gets single User by ID')

    all_user_info = graphene.List(UserModelInfo, description='Gets info of all users')

    def resolve_user(self, info, id):
        if info.context.user.has_perm('auth.view_user'):
            return User.objects.get(pk=id)
        else:
            raise Exception("You do not have permission to access this field.")

    def resolve_all_user_info(self, info):
        return UserInfo.objects.all()


schema = graphene.Schema(query=Query)
