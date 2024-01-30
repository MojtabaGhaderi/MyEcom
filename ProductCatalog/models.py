from django.db import models
from django.db.models import Q


class CategoryModel(models.Model):
    name = models.CharField(unique=True, max_length=100)
    lft = models.PositiveIntegerField()
    rgt = models.PositiveIntegerField()

    @classmethod
    def create_root_category(cls, name):
        root = cls(name=name, lft=1, rgt=2)
        root.save()
        return root

    def add_child(self, name):
        # here we should receive child
        parent_right = self.rgt
        CategoryModel.objects.filter(rgt__gte=parent_right).update(rgt=models.F('rgt') + 2)
        CategoryModel.objects.filter(lft__gt=parent_right).update(lft=models.F('lft') + 2)

        child = CategoryModel(name=name, lft=parent_right, rgt=parent_right+1)
        child.save()
        print("we are in the add_child. child is:", child, child.name)
        return child
        # for child in children:
        #     child.lft = cache
        #     child.rgt = cache + 1
        #
        #     child.save()

    def delete(self):
        deleting_nodes = self.get_descendants()
        if deleting_nodes:
            # nodn = number of deleting nodes

            nodn = deleting_nodes.count() + 1
            deleting_nodes.delete()
        else:
            nodn = 1


        CategoryModel.objects.filter(rgt__gt=self.rgt).update(rgt=models.F('rgt') - nodn*2)
        CategoryModel.objects.filter(lft__gt=self.rgt).update(lft=models.F('lft') - nodn*2)
        super() .delete()

    def get_descendants(self):
        descendants = CategoryModel.objects.filter(Q(rgt__lt=self.rgt) & Q(lft__gt=self.lft)).order_by('lft')
        return descendants

    def get_ancestors(self):
        ancestors = CategoryModel.objects.filter(Q(rgt__gt=self.rgt) & Q(lft__lt=self.lft)).order_by('-lft')
        return ancestors

    def move(self, destination_id):
        destination = CategoryModel.objects.get(pk=destination_id)

        root = self
        root.name += 'm'
        root.save()
        moved_root_name = root.name[:-1]

        destination.add_child(moved_root_name)
        root.refresh_from_db()

        branch = list(root.get_descendants())

        for node in branch:
            node.name += 'm'
            node.save()

        for node in branch:
            ancestor = node.get_ancestors().first()
            ancestor = CategoryModel.objects.get(name=ancestor.name[:-1])
            ancestor.add_child(node.name[:-1])
        root.refresh_from_db()

        root.delete()

    def edit_name(self, name):
        category = CategoryModel.objects.get(pk=self.pk)
        category.name = name
        category.save()









class ProductModel(models.Model):
    pass
