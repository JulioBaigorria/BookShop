import graphene
from graphql_auth import mutations
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery

from .models import Book, Author, Category

# print(graphene.__all__)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    update_account = mutations.UpdateAccount.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class Query(UserQuery, MeQuery, graphene.ObjectType):

    book = graphene.Field(BookType, id=graphene.Int())
    all_books = graphene.List(BookType)
    book_by_name = graphene.Field(BookType, title=graphene.String())

    all_authors = graphene.List(AuthorType)
    author_by_name = graphene.Field(AuthorType)

    all_categories = graphene.List(CategoryType)
    category_by_name = graphene.Field(CategoryType)

    ''' get -> field
        filter -> list
        all -> list '''
    def resolve_book(root, info, id):
        return Book.objects.select_related().get(id=id)

    def resolve_all_books(root, info):
        return Book.objects.select_related().all()

    def resolve_book_by_name(root, info, title):
        return Book.objects.get(title=title)

    def resolve_all_authors(root, info):
        return Author.objects.all()

    def resolve_author_by_name(root, info):
        return Author.objects.get(name='Lauren Groff')

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_category_by_name(root, info):
        return Category.objects.get(name='Horror')


class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        excerpt = graphene.String()
        category = graphene.String()
        author = graphene.String()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, title, excerpt, category, author):
        category = Category.objects.get(name=category)
        author = Author.objects.get(name=author)
        book = Book(title=title, excerpt=excerpt, category=category, author=author)
        book.save()
        return CreateBookMutation(book=book)


class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        excerpt = graphene.String()
        category = graphene.String()
        author = graphene.String()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, id, title, excerpt, category, author):
        book = Book.objects.get(id=id)
        getcategory = Category.objects.get(name=category)
        getauthor = Author.objects.get(name=author)

        book.title = title
        book.excerpt = excerpt
        book.category = getcategory
        book.author = getauthor

        book.save()
        return CreateBookMutation(book=book)


class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, id):
        book = Book.objects.get(id=id)
        book.delete()
        return CreateBookMutation(book=book)


class Mutation(AuthMutation, graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
