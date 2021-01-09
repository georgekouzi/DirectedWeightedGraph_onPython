class Node:
    def __init__(self, new_id, pos : tuple =None):
        self.__id = new_id
        self.__count_edge_in = 0
        self.__count_edge_out = 0
        self.__pos = pos

    def get_id(self):
        return self.__id

    def c_edge_out(self, count=1):
        self.__count_edge_out = self.__count_edge_out + count

    def c_edge_in(self, count=1):
        self.__count_edge_in = self.__count_edge_in + count

    def get_pos(self):
        return self.__pos

    def set_pos(self,new_pos:tuple):
        self.__pos=new_pos

    def __repr__(self):
        return f"{self.__id}: |edges out| {self.__count_edge_out} |edges in| {self.__count_edge_in}"
