# core/schema.py

import typing
import strawberry
import strawberry.exceptions
import strawberry_django
from strawberry.schema.config import StrawberryConfig
from strawberry import auto, ID
from strawberry.relay import Node
from core.models import User as UserModel, DeployedApp as AppModel
from asgiref.sync import sync_to_async


@strawberry.interface
class NodeInterface:
    id: ID

@strawberry_django.type(model=AppModel, name="App")
class AppType(NodeInterface):
    active: auto


@strawberry_django.type(model=UserModel, name="User")
class UserType(NodeInterface):
    username: auto
    plan: auto

    @strawberry.field
    async def apps(self, info) -> list[AppType]:
        try:
            loader = info.context.loaders["apps_by_user"]
            return await loader.load(self.id)
        except Exception as e:
            # This will ensure GraphQL serializes it properly
            raise e


@strawberry.type
class Mutation:
    @strawberry_django.mutation
    async def upgrade_account(self, user_id: str) -> UserType:
        user = await UserModel.objects.aget(id=user_id)
        user.plan = "PRO"
        await user.asave()
        return user

    @strawberry_django.mutation
    async def downgrade_account(self, user_id: str) -> UserType:
        user = await UserModel.objects.aget(id=user_id)
        user.plan = "HOBBY"
        await user.asave()
        return user


@strawberry.type
class Query:
    @strawberry.field
    async def node(self, info, id: str) -> typing.Optional[NodeInterface]:
        # raw-ID dispatch:
        if id.startswith("u_"):
            try:
                return await UserModel.objects.aget(id=id)
            except UserModel.DoesNotExist:
                raise strawberry.exceptions.StrawberryException(
                    message=f"User ID: {id} not found"
                )
        if id.startswith("app_"):
            try:
                # This will raise an error if the app does not exist
                return await AppModel.objects.aget(id=id)
            except AppModel.DoesNotExist:
                raise strawberry.exceptions.StrawberryException(                    
                    message=f"App ID: {id} not found"
                )
        raise strawberry.exceptions.StrawberryException(
            message=f"Invalid ID format: {id}"
        )

    @strawberry_django.field
    async def user(self, id: str) -> UserType:
        return await UserModel.objects.aget(id=id)

    @strawberry_django.field
    async def deployed_apps(self, user_id: str) -> list[AppType]:
        qs = AppModel.objects.filter(owner_id=user_id)
        apps = await sync_to_async(list)(qs)
        return apps

    @strawberry_django.field
    async def all_users(self) -> list[UserType]:
        qs =  UserModel.objects.all()
        users = await sync_to_async(list)(qs)
        return users


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    types=[UserType, AppType]
)