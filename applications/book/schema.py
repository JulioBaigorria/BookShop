import graphene
from graphene_django import DjangoObjectType
from .models import Book, Author, Category


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ('id', 'title', 'excerpt', 'category', 'author', 'date_created',)


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ('id', 'name',)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book_by_name = graphene.Field(BookType)

    all_authors = graphene.List(AuthorType)
    author_by_name = graphene.Field(AuthorType)

    all_categories = graphene.List(CategoryType)
    category_by_name = graphene.Field(CategoryType)

    ''' get -> field
        filter -> list
        all -> list '''

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_book_by_name(root, info):
        return Book.objects.get(title="Gone Girl")

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


class Mutation(graphene.ObjectType):

    create_book = CreateBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
