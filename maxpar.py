# library imports
from graphviz import Digraph
# Graph visualization package'graphviz' is a way of representing structural
# information as diagrams of abstract graphs and networks.
from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import queue  # imported for using queue.Empty exception
from itertools import combinations  # imported for using combinations
import copy  # imported for using deepcopy


class Task:
    # Task class constructor
    def __init__(self, name="", run=None, reads=[], writes=[]):
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
        self._tasks_to_do = Queue()
        self._tasks_done = Queue()
        self._for_draw = tasks
        self.check_interferente()

    def __new__(cls, tasks, preferences):
        # Test if there is any duplicate task name
        if len(tasks) != len(set([item.name for item in tasks])):
            raise Exception('Duplicate Task name')
        # Test if there is any Inexistant task
        if False in (
            [item in [item.name for item in tasks] for item in preferences] + [
                _item in [item.name for item in tasks] for item in preferences
                for _item in preferences.get(item)
            ]):
            raise Exception('Inexistant Task name')
        return super().__new__(cls)

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

    # getDependencies method
    def getDependencies(self, task):
        """ 
        TaskSystem getDependencies method
        exp: ..
        """
        return self.preferences[task]

    def check_condition_task(self):
        """
        Check if any item in tasks list have condition
        """
        return True in [(len(item.get('conditions')) != 0)
                        for item in self._tasks]

    # test all of combinations and verify which is interferente
    def check_interferente(self):
        result = []
        for task in self._tasks:
            result.append({"task": task, "conditions": [], "finished": False})
        tasks_combinations = list(combinations(self._tasks, 2))
        for item in tasks_combinations:
            if self.interferente(item[0], item[1]):
                for t in result:
                    if (t.get('task') == item[1]):
                        t['conditions'] = self.getDependencies(item[1].name)
        self._tasks = result
        self._for_draw = copy.deepcopy(result)

    # run the tasks system
    def run(self):
        """ 
        TaskSystem run method
        exp: ..
        """
        while True:
            processes = []
            for index, task in enumerate(self._tasks):
                if not (task.get('conditions')):
                    if not (task.get('finished')):
                        self._tasks_to_do.put(task)
                        self._tasks[index]['finished'] = True

            # creating processes
            for w in range(len(self._tasks)):
                p = Process(target=self.do_task)
                processes.append(p)
                p.start()

                # completing process
            for p in processes:
                p.join()

            # print the output
            while not self._tasks_done.empty():
                print(self._tasks_done.get())
            if self.check_condition_task():
                for task in self._tasks:
                    if not (task.get('conditions')):
                        for index, item in enumerate(self._tasks):
                            if task.get('task').name in item.get('conditions'):
                                self._tasks[index]['conditions'].remove(
                                    task.get('task').name)
            else:
                break

    def do_task(self):
        while True:
            try:
                '''
                    try to get task from the queue. get_nowait() function will 
                    raise queue.Empty exception if the queue is empty. 
                    queue(False) function would do the same task also.
                '''
                task = self._tasks_to_do.get_nowait()
            except queue.Empty:
                break
            else:
                '''
                    if no exception has been raised, add the task completion 
                    message to task_that_are_done queue
                '''
                if task.get('conditions'):
                    for t in task.get('conditions'):
                        print(f't is {t}')
                else:
                    task.get('task').run()
                    self._tasks_done.put(
                        task.get('task').name + ' is done by ' +
                        current_process().name)

    def draw(self):
        """ 
        TaskSystem draw method
        exp: ..
        """
        print('----------- Drawing TaskSystem image start -----------')
        dot = Digraph(name="G", format="png")
        for item in self._for_draw:
            dot.node(item.get('task').name, item.get('task').name)
        for item in self._for_draw:
            for condition in item.get('conditions'):
                dot.edge(item.get('task').name, condition)
        dot.render("TaskSystem")
        print('----------- Drawing TaskSystem image done  -----------')

    def interferente(self, task1, task2):
        """
        Check if two tasks are interfering:
        Bernstein’s Conditions are the conditions applied on two statements S1 and S2 that are to be executed in the processor.
        
        Principe: The intersection between read-write set, write-read set and write-write set of S1 and S2 must be null.
        """
        return (not(list(set(task1.reads) & set(task2.writes))) and \
            not(list(set(task1.writes) & set(task2.reads)))  and\
                not(list(set(task1.writes) & set(task2.writes))))


if __name__ == "__main__":
    print("just to test")
    # print("------------ No interferente tasks ---------------")

    # def runT1():
    #     print("runT1")

    # def runT2():
    #     print("runT2")

    # def runTsomme():
    #     print("runTsomme")

    # t1 = Task()
    # t1.name = "T1"
    # t1.writes = ["X"]
    # t1.run = runT1
    # t2 = Task()
    # t2.name = "T2"
    # t2.writes = ["X"]
    # t2.run = runT2
    # tSomme = Task()
    # tSomme.name = "somme"
    # tSomme.reads = ["X", "Y"]
    # tSomme.writes = ["Z"]
    # tSomme.run = runTsomme
    # # t1.run()
    # # t2.run()
    # # tSomme.run()
    # # print(X)
    # # print(Y)
    # # print(Z)
    # taskSystem = TaskSystem([t1, t2, tSomme], {
    #     "T1": [],
    #     "T2": [],
    #     "somme": ["T1", "T2"]
    # })
    # taskSystem.run()
    # taskSystem.draw()
    print("------------ With interferente tasks ---------------")

    def runT1():
        print("runT1")

    def runT2():
        print("runT2")

    def runTsomme():
        print("runTsomme")

    t1 = Task()
    t1.name = "T1"
    t1.writes = ["A"]
    t1.reads = ["X", "Y"]
    t1.run = runT1
    t2 = Task()
    t2.name = "T2"
    t2.writes = ["B"]
    t2.reads = ["Z"]
    t2.run = runT2
    tSomme = Task()
    tSomme.name = "somme"
    tSomme.reads = ["A", "B"]
    tSomme.writes = ["C"]
    tSomme.run = runTsomme
    taskSystem = TaskSystem([t1, t2, tSomme], {
        "T1": [],
        "T2": ["T1"],
        "somme": ["T1", "T2"]
    })
    taskSystem.run()
    taskSystem.draw()
