**This package provides an abstract django model, that allows you to transparently retrieve or delete your objects, without having them deleted from your database.**

### Example of usage

#### imports
```python
from django_soft_delete.models import SoftDeletionModel

```

#### Create a new model class derived from SoftDeletionModel.
```python
class User(SoftDeletionModel):
    name = models.CharField(max_length=100)
```


#### And just invoke delete method, that's all.

```python
user = User(name='test')
user.save()
user.delete()
```
##### You can use all functionalities with queryset as well.

```python
users = User.objects.filter(name='test')
users.delete()
```

##### This user will be masked, but not deleted from the database.

```python
User.object.filter(name='test') #returns empty query string.

User.all_objects.filter(name='test) #returns deleted user instance which has non empty deleted_at field.
```



##### In order to create model deletion relations, you have to import deletion.py and use the related on_delete functions like CASCADE, PROTECT, etc.
```python
from django_soft_delete.deletion import CASCADE
from django_soft_delete.models import SoftDeletionModel

class User(SoftDeletionModel):
    name = models.CharField(max_length=100)
    
    
class Profile(SoftDeletionModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=CASCADE,
                             verbose_name=_('User'), null=True,
                             blank=True)
```
##### In order to revive your soft-deleted records, you can use undelete method.
```python
user = User(name='test')
user.save()
user.delete()
user.undelete()
```

##### In order to delete your instance permanently from your database, you can use hard_delete method.

```python
user = User(name='test')
user.save()
user.hard_delete()
```

## Installation
- pip install soft-django-delete

##### Add 'django_soft_delete' in your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django_soft_delete',
    [...]
]
```