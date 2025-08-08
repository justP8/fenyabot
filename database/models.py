from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField(pk=True)
    full_name = fields.CharField(max_length=128)
    username = fields.CharField(max_length=32, null=True)

    class Meta:
        table = 'Users'


class Const(Model):
    name = fields.CharField(max_length=30, pk=True)
    value = fields.TextField()

    class Meta:
        table = 'Consts'


class GraphPage(Model):
    alias = fields.CharField(max_length=30, pk=True)
    path = fields.CharField(max_length=50)
    url = fields.CharField(max_length=80)
    title = fields.CharField(max_length=50)
    author_name = fields.CharField(max_length=20)
    author_url = fields.CharField(max_length=35)

    class Meta:
        table = 'GraphPages'
