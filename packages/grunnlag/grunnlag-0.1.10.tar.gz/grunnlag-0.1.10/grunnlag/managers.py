from bergen.types.manager import  ModelManager

class RepresentationManager(ModelManager):

    def from_xarray(self, array, compute=True, **kwargs):
        instance = self.create(**kwargs)
        instance.save_array(array, compute=compute)
        print(instance)
        instance = self.update(id=instance.id, **kwargs)
        return instance