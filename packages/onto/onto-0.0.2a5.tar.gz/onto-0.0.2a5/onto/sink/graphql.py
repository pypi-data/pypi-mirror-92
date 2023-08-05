import weakref
from collections import defaultdict, OrderedDict
from inspect import Parameter
from typing import Type

from onto.source.protocol import Protocol
from onto.view_model import ViewModel

from onto.sink.base import Sink


from collections import namedtuple

graph_schema = namedtuple('graph_schema', ['op_type', 'name', 'graphql_object_type', 'args'])
import graphql


class GraphQLSink(Sink):

    _protocol_cls = Protocol

    def __set_name__(self, owner, name):
        """ Keeps mediator as a weakref to protect garbage collection
        Note: mediator may be destructed if not maintained or referenced
            by another variable. Mediator needs to be explicitly kept alive.

        TODO: note that parent and sink_name are not initialized

        :param owner:
        :param name:
        :return:
        """
        self.parent = weakref.ref(owner)
        self._name = name

    @property
    def sink_name(self):
        name = self._name
        if self._camelize:
            from onto.utils import camel
            name = camel(name)
        return name

    @property
    def triggers(self):
        return self.protocol

    @property
    def mediator_instance(self):
        return self.parent()()

    def _maybe_deserialize(self, val, annotated_type):
        from onto.models.base import BaseRegisteredModel
        if issubclass(annotated_type, BaseRegisteredModel):
            return annotated_type.from_dict(val)
        else:
            return val

    def _f_of_rule(self, func_name):
        fname = self.protocol.fname_of(func_name)
        if fname is None:
            raise ValueError(
                f"fail to locate {func_name}"
                f" for {self.mediator_instance.__class__.__name__}"
            )
        f = getattr(self.mediator_instance, fname)
        return f

    def _invoke_mediator(self, *args, func_name, **kwargs):
        f = self._f_of_rule(func_name=func_name)

        annotation_d = {
            k: v
            for k, v in self._parameters_for(f)
        }

        new_kwargs = {
            k:self._maybe_deserialize(val=v, annotated_type=annotation_d[k])
            for k, v in kwargs.items()
        }

        return f(*args, **new_kwargs)

    def __init__(self, view_model_cls: Type[ViewModel], camelize=True, many=False):
        """

        :param view_model_cls:
        :param camelize:
        """
        self.protocol = self._protocol_cls()
        self.view_model_cls = view_model_cls
        import asyncio
        loop = asyncio.get_event_loop()
        from functools import partial
        cons = partial(asyncio.Queue, loop=loop)
        self.qs = defaultdict(cons)
        self.loop = loop
        self._camelize = camelize
        self.many = many
        super().__init__()

    def _param_to_graphql_arg(self, annotated_type):
        from onto.models.utils import _graphql_type_from_py
        from graphql import GraphQLArgument, GraphQLInputObjectType
        # TODO: add notes about `typing.*` not supported
        gql_field_cls = _graphql_type_from_py(annotated_type, input=True)
        arg = GraphQLArgument(gql_field_cls)  # TODO: set default_value
        return arg

    @staticmethod
    def _parameters_for(f):

        def _annotation_type_of(param):
            annotation = param.annotation
            import inspect
            if annotation is inspect._empty:
                raise ValueError(f'parameter {param} is not annotated'
                                 'for conversion to graphql argument')
            return annotation

        from inspect import signature
        sig = signature(f)
        param_d = OrderedDict(sig.parameters.items())
        # param_d.popitem(last=False)  # Pop self argument
        # NOTE: param_d.popitem(last=False) may not always pop self argument
        for name, param in param_d.items():
            yield name, _annotation_type_of(param)

    def _args_of_f(self, f):
        for name, annotated_type in self._parameters_for(f):
            yield name, self._param_to_graphql_arg(annotated_type=annotated_type)

    def _args_of(self, rule):
        f = self._f_of_rule(func_name=rule)
        return self._args_of_f(f=f)

    op_type = None

    def _as_graphql_schema(self):
        from onto.models.utils import \
            _graphql_object_type_from_attributed_class
        attributed = self.view_model_cls

        ot = _graphql_object_type_from_attributed_class(attributed)
        if self.many:
            ot = graphql.GraphQLList(type_=ot)

        name, args = self._register_op()

        return graph_schema(
            op_type=self.op_type,
            name=name,
            graphql_object_type=ot,
            args=args
        )


    def start(self):
        subscription_schema = self._as_graphql_schema()
        return subscription_schema


class GraphQLSubscriptionSink(GraphQLSink):

    op_type = 'Subscription'

    def _register_op(self):
        from gql import subscribe
        async def f(parent, info, **kwargs):
            # Register topic
            topic_name = self._invoke_mediator(func_name='add_topic', **kwargs)
            # Listen to topic
            q = self.qs[topic_name]

            while True:
                event = await q.get()
                yield {
                    self.sink_name:
                        self._invoke_mediator(func_name='on_event',
                                              event=event)
                }

        # name = self.parent().__name__
        # f.__name__ = name
        name = self.sink_name
        f.__name__ = name
        subscribe(f)
        args = dict(self._args_of('add_topic'))

        return name, args


class GraphQLQuerySink(GraphQLSink):

    op_type = 'Query'

    def _register_op(self):
        from gql import query

        async def f(parent, info, **kwargs):
            res = self._invoke_mediator(func_name='query', **kwargs)
            return res

        name = self.sink_name
        f.__name__ = name
        query(f)
        args = dict(self._args_of('query'))
        return name, args


class GraphQLMutationSink(GraphQLSink):

    op_type = 'Mutation'

    def _register_op(self):
        from gql import mutate

        async def f(parent, info, **kwargs):
            res = self._invoke_mediator(func_name='mutate', **kwargs)
            return res

        name = self.sink_name
        f.__name__ = name
        mutate(f)
        args = dict(self._args_of('mutate'))
        return name, args


def op_schema(op_type, schema_all):
    ot = graphql.GraphQLObjectType(
        name=op_type,
        fields={
            schema.name:
                graphql.GraphQLField(
                    schema.graphql_object_type,
                    args=schema.args)
            for schema in schema_all
            if schema.op_type == op_type
        }
    )
    return ot


query = GraphQLQuerySink
mutation = GraphQLMutationSink
subscription = GraphQLSubscriptionSink
