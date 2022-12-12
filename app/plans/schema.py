import graphene

from investments.schema import UpdatePortfolio, PortfoliosQuery


class Query(PortfoliosQuery, graphene.ObjectType):
    pass


class Mutation(UpdatePortfolio, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
