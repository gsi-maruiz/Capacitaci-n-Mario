import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ingredientsGraphql.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {'name': ["icontains"], 'ingredients': ["exact"]}
        # interfaces = (relay.Node,)
        # exclude = ("name",)  # show all fields of the model except this

    extra_field = graphene.String()  # add a new property to model

    def resolve_extra_field(self, info):
        return "hello!"


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact', 'icontains'],
        }
        # interfaces = (relay.Node,)


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        # Notice we return an instance of this mutation
        return CreateCategory(category=category)


class EditCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        try:
            category = Category.objects.get(pk=id)
            category.name = name
            category.save()
            return CreateCategory(category=category)
        except Category.DoesNotExist:
            return None


class IngredientsInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    notes = graphene.String(required=True)
    category_id = graphene.Int(required=True)


class CreateIngredient(graphene.Mutation):
    class Arguments:
        ingredientsInput = IngredientsInput(required=True)

    ingredients = graphene.Field(IngredientType)

    @classmethod
    def mutate(cls, root, info, ingredientsInput):
        category = Category.objects.get(pk=ingredientsInput.category_id)
        ingredient = Ingredient(name=ingredientsInput.name, notes=ingredientsInput.notes, category=category)
        ingredient.save()
        return CreateIngredient(ingredients=ingredient)


# using relay
class CreateCategoryRelay(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return Category(category=category)


class QueryBasic(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    all_category = graphene.List(CategoryType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

    def resolve_category_by_id(root, info, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def resolve_all_category(root, info):
        return Category.objects.all()


class QueryRelay(graphene.ObjectType):
    category = relay.Node.Field(CategoryType)
    all_categories = DjangoFilterConnectionField(CategoryType)

    ingredient = relay.Node.Field(IngredientType)
    all_ingredients = DjangoFilterConnectionField(IngredientType)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    edit_category = EditCategory.Field()
    create_ingredients = CreateIngredient.Field()
