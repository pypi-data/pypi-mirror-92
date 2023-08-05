import uvicorn as uvicorn
from examples.meeting_room.domain_models import User

from examples.meeting_room.view_models import UserView
from onto import view_model, attrs
from onto.view import Mediator


class UserGraphQLMediator(Mediator):

    from onto.source import domain_model
    from onto.sink.graphql import subscription

    src = domain_model(domain_model_cls=User)
    subscribe_user_view = subscription(view_model_cls=UserView)

    @subscribe_user_view.triggers.add_topic
    def add_topic(self, user_id: str):
        return user_id

    @subscribe_user_view.triggers.on_event
    def on_event(self, event: dict):
        return event

    @src.triggers.on_create
    @src.triggers.on_update
    def user_updated(self, obj: User):
        v = UserView.get(user_id=obj.doc_id)
        d = v.to_dict()
        q = self.subscribe_user_view.qs[obj.doc_id]

        import asyncio
        # tell asyncio to enqueue the result
        fut = asyncio.run_coroutine_threadsafe(
            q.put(d), loop=self.subscribe_user_view.loop
        )
        # wait for the result to be enqueued
        _ = fut.result()

    @classmethod
    def start(cls):
        cls.src.start()
        s = cls.subscribe_user_view.start()
        from onto.sink.graphql import graph_schema
        import graphql
        liveness = graph_schema(
            op_type='Query',
            name='liveness',
            graphql_object_type=graphql.GraphQLObjectType(
                name='Liveness',
                fields={
                    'alive': graphql.GraphQLField(
                        graphql.GraphQLBoolean,
                        resolve=lambda *args, **kwargs: True),
                }
            ),
            args=dict()
        )

        return [s, liveness]



class LoginForm(view_model.ViewModel):
    phone_number = attrs.bproperty(type_cls=str)
    verification_code = attrs.bproperty(type_cls=str)


class LoginRes(view_model.ViewModel):
    token = attrs.bproperty(type_cls=str)


class UserLoginMediator(Mediator):

    from onto.sink.graphql import mutation

    login_user_view = mutation(view_model_cls=LoginRes)

    @login_user_view.triggers.mutate
    def login(self, form: LoginForm):
        print(form)

    @classmethod
    def start(cls):
        s = cls.login_user_view.start()
        return [s]


