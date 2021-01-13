class GraphMeta(type):
    def __instancecheck__(self, instance):
        return self.__subclasscheck__(type(instance))
    def __subclasscheck__(self, subclass):
        return ( hasattr(subclass,'v_size') and callable(subclass.v_size)
                 and hasattr(subclass,'e_size') and callable(subclass.e_size)
                 and hasattr(subclass,'get_all_v') and callable(subclass.get_all_v)
                 and hasattr(subclass,'all_in_edges_of_node') and callable(subclass.all_in_edges_of_node)
                 and hasattr(subclass,'all_out_edges_of_node') and callable(subclass.all_out_edges_of_node)
                 and hasattr(subclass, 'get_mc') and callable(subclass.get_mc)
                 and hasattr(subclass, 'add_edge') and callable(subclass.add_edge)
                 and hasattr(subclass, 'add_node') and callable(subclass.add_node)
                 and hasattr(subclass, 'remove_node') and callable(subclass.remove_node)
                 and hasattr(subclass, 'remove_edge') and callable(subclass.remove_edge)
                 )
class updateInFormalGraphInterface(metaclass=GraphMeta):
    pass