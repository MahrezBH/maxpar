# library imports
#
from graphviz import Digraph
# Graph visualization package'graphviz' is a way of representing structural 
# information as diagrams of abstract graphs and networks.

class Task:
    # Task class constructor
    def __init__(self, name="", run=None ,reads=[], writes=[]):
        self._name = name
        self._reads = reads
        self._writes = writes
        self._run = run
    
    # name getter
    @property
    def name(self):
        return self._name
    
    # name setter
    @name.setter
    def name(self, value):
        self._name = value
    
    # name deleter
    @name.deleter
    def name(self):
        del self._name

    # reads getter
    @property
    def reads(self):
        return self._reads
    
    # reads setter
    @reads.setter
    def reads(self, value):
        self._reads = value

    # reads deleter
    @reads.deleter
    def reads(self):
        del self._reads

    # writes getter
    @property
    def writes(self):
        return self._writes

    # writes setter
    @writes.setter
    def writes(self, value):
        self._writes = value

    # writes deleter
    @writes.deleter
    def writes(self):
        del self._writes

    # run getter    
    @property
    def run(self):
        return self._run
    
    # run setter
    @run.setter
    def run(self, value):
        self._run = value
    
    # run deleter
    @run.deleter
    def run(self):
        del self._run

class TaskSystem:
    def __init__(self, tasks=[], preferences={}):
        """ 
        TaskSystem constructor
        """
        self._tasks = tasks
        self._preferences = preferences

    # def __new__(cls, t,p):
    #     print(f' from new {cls.tasks}')

    # tasks getter
    @property
    def tasks(self):
        return self._tasks
    
    # tasks setter
    @tasks.setter
    def tasks(self, value):
        self._tasks = value
    
    # tasks deleter
    @tasks.deleter
    def tasks(self):
        del self._tasks

    # preferences getter
    @property
    def preferences(self):
        return self._preferences
    
    # preferences setter
    @preferences.setter
    def preferences(self, value):
        self._preferences = value
    
    # preferences deleter
    @preferences.deleter
    def preferences(self):
        del self._preferences

    # 
    def getDependencies(self,task):
        """ 
        TaskSystem getDependencies method
        exp: ..
        """
        return self.preferences[task]
    
    def run(self):
        """ 
        TaskSystem run method
        exp: ..
        """
        pass
    
    def draw(self, items, relations):
        """ 
        TaskSystem draw method
        exp: ..
        """
        dot = Digraph(name="G",format="png")
        for item in items:
            dot.node(item, item)
        dot.edges(relations)
        dot.render("TaskSystem")


    def interferente(self,task1, task2):
        return (not(list(set(task1.reads) & set(task2.writes))) and \
            not(list(set(task1.writes) & set(task2.reads)))  and\
                not(list(set(task1.writes) & set(task2.writes))))

if __name__ == "__main__":
    print("just to test")
    X = None
    Y = None
    Z = None
    def runT1():
        global X
        X = 1

    def runT2():
        global Y
        Y = 2

    def runTsomme():
        global X, Y, Z
        Z = X + Y

    t1 = Task()
    t1.name = "T1"
    t1.writes = ["X"]
    t1.run = runT1
    t2 = Task()
    t2.name = "T2"
    t2.writes = ["X"]
    t2.run = runT2
    tSomme = Task()
    tSomme.name = "somme"
    tSomme.reads = ["X", "Y"]
    tSomme.writes = ["Z"]
    tSomme.run = runTsomme
    t1.run()
    t2.run()
    tSomme.run()
    # print(X)
    # print(Y)
    # print(Z)
    taskSystem = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
