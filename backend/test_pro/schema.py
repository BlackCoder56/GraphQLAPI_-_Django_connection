import graphene
import test_app.schema


class Query(test_app.schema.Query, graphene.ObjectType):
    pass

class Mutation(test_app.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

# schema = graphene.Schema(query=Query)