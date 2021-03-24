from graphviz import Digraph

# define Task class
class Task:
    def __init__(self, name="", run=None ,reads=[], writes=[]):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

def inter(task1, task2):
    return  (not(list(set(task1.reads) & set(task2.writes))) and \
         not(list(set(task1.writes) & set(task2.reads)))  and\
             not(list(set(task1.writes) & set(task2.writes))))

class TaskSystem:
    def __init__(self, tasks=[], preferences={}):
        """ 
        TaskSystem constructor
        """
        self.tasks = tasks
        self.preferences = preferences

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
    
    def draw(self):
        """ 
        TaskSystem draw method
        exp: ..
        """
        dot = Digraph()
        for item in self.preferences:
            dot.node(item, item)
        # dot.edges(['AB', 'AB', 'AB', 'BC', 'BA', 'CB'])

        # print(dot.source)
        # dot.render("file_name", view=True)

if __name__ == "__main__":
    print("just to test")
    X = None
    Y = None
    Z = None
    def runT1():
        global X
        X = 1
        print("t1")

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
    print(X)
    print(Y)
    print(Z)
