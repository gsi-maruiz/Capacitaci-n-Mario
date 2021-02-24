import graphene

import ingredientsGraphql.schema


class QueryRelay(ingredientsGraphql.schema.QueryRelay, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class QueryBasic(ingredientsGraphql.schema.QueryBasic, graphene.ObjectType):
    pass


class Mutation(ingredientsGraphql.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=QueryBasic, mutation=Mutation)
