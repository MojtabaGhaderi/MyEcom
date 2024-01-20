from django.db import models
from django.db.models import Q


class CategoryModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    lft = models.PositiveIntegerField()
    rgt = models.PositiveIntegerField()

    def add_child(self, children):
        # here we should receive child
        cache = self.rgt
        CategoryModel.objects.filter(rgt__gte=self.rgt).update(rgt=models.F('rgt') + 2)
        CategoryModel.objects.filter(lft__gt=self.lft).update(lft=models.F('lft') + 2)

        for child in children:
            child.lft = cache
            child.rgt = cache + 1

            child.save()

    def delete(self):
        deleting_nodes = self.get_descendants()
        if deleting_nodes:
            # nodn = number of deleting nodes

            nodn = deleting_nodes.count() + 1
        else:
            nodn = 1

        CategoryModel.objects.filter(rgt__gt=self.rgt).update(rgt=models.F('rgt') - nodn*2)
        CategoryModel.objects.filter(lft__gt=self.rgt).update(lft=models.F('lft') - nodn*2)

        deleting_nodes.delete()

    def get_descendants(self):
        descendants = CategoryModel.objects.filter(Q(rgt__lt=self.rgt) & Q(lft__gt=self.lft)).order_by('lft')
        return descendants

    def get_ancestors(self):
        ancestors = CategoryModel.objects.filter(Q(rgt__gt=self.rgt) & Q(lft__lt=self.lft)).order_by('-lft')
        return ancestors

    def move(self, destination):
        branch = self.get_descendants()
        self.delete()
        destination.add_child(list(branch))



class ProductModel(models.Model):
    pass
