from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField, CASCADE, BooleanField


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    content = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField())


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
