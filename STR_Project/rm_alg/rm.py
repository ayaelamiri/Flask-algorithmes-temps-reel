# Author: Diego PERINI
# License: Public Domain
# Rate monotonic scheduling implementation
import functools
import random

from rm_alg.prime import lcm


# A task instance
class TaskIns(object):

    # Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start = start
        self.end = end
        self.usage = 0
        self.priority = priority
        self.name = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    # Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    # Default representation
    def __repr__(self, budget_text=None):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(
            self.priority) + budget_text

    # Get name as Name#id
    def get_unique_name(self):
        return str(self.name)


# Task types (templates for periodic tasks)
class TaskType(object):

    # Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period = period
        self.release = release
        self.execution = execution
        self.deadline = deadline
        self.name = name


# Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0


# Rate monotonic comparison
def tasktype_cmp(self, other):
    if self.period < other.period:
        return -1
    if self.period > other.period:
        return 1
    return 0


if __name__ == '__main__':
        run = False
        html_color = {'Task1': '#015668', 'Task2': '#844685', 'Task3': '#a4c5c6', 'Task4': 'aqua', 'Task5': 'coral',
                      'Empty': '#faf4ff',
                      'Finish': 'black'}
        taskfile = open('tasks.txt')
        lines = taskfile.readlines()
        task_types = []
        tasks = []
        hyperperiod = []

        # Allocate task types
        for line in lines:
            line = line.split(' ')
            for i in range(0, 4):
                line[i] = int(line[i])
            if len(line) == 5:
                name = line[4]
            elif len(line) == 4:
                name = 'Task'
            else:
                raise Exception('Invalid tasks.txt file structure')
            if int(line[0]) > 0:
                task_types.append(
                    TaskType(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))

        # Calculate hyperperiod
        for task_type in task_types:
            hyperperiod.append(task_type.period)
        hyperperiod = lcm(hyperperiod)

        # Sort types rate monotonic
        task_types = sorted(task_types, key=functools.cmp_to_key(tasktype_cmp))

        # Create task instances
        for i in range(0, hyperperiod):
            for task_type in task_types:
                if (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                    start = i
                    end = start + task_type.execution
                    priority = task_type.period
                    tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))

        # Html output start
        html = ""
        html1 = "</main><div style='margin: 50px auto auto;'>"


        # Check utilization
        utilization = 0
        for task_type in task_types:
            utilization += float(task_type.execution) / float(task_type.period)
        if utilization > 1:
            print('Utilization error!')

        # Simulate clock
        clock_step = 1
        task_executed= []
        for i in range(0, hyperperiod, clock_step):
            # Fetch possible tasks that can use cpu and sort by priority
            possible = []
            for t in tasks:
                if t.start <= i:
                    possible.append(t)
            possible = sorted(possible, key=functools.cmp_to_key(priority_cmp))

            # Select task with highest priority

            if len(possible) > 0:
                on_cpu = possible[0]
                print(on_cpu.get_unique_name(), " uses the processor. "),
                task_executed.append(on_cpu.get_unique_name())
                print(task_executed)
                html += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + html_color[on_cpu.name] + ';">' + on_cpu.get_unique_name() + '<br />' + str(i) + '-' + str(i+1) + '</div>'
                if on_cpu.use(clock_step):
                    tasks.remove(on_cpu)
                    html += '<div style="float: left; text-align: center; width: 5px; height: 20px; background-color:' + \
                            html_color['Finish'] + ';">' + '<br />' + str(i + 1) + '</div>'
                    print("Finish!"),
            else:
                print('No task uses the processor. ')
                task_executed.append('empty')
                html += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                        html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
            print("\n")

        html2 = "<br /><br />"
        html3 = "<br /><br />"
        i = 0
        for y in task_executed:
            if y=='Task1':
                html1 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                        html_color[y] + ';">' + y + '<br />' + str(i) + '-' + str(
                    i + 1) + '</div>'
                html2 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                        html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
                html3 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                        html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
            elif y=='Task2':
                html2 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color[y] + ';">' + y + '<br />' + str(i) + '-' + str(
                    i + 1) + '</div>'
                html1 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
                html3 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
            elif y=='Task3':
                html3 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color[y] + ';">' + y + '<br />' + str(i) + '-' + str(
                    i + 1) + '</div>'
                html2 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
                html1 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
            else:
                html1 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
                html2 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
                html3 += '<div style="float: left; text-align: center; width: 55px; height: 20px; background-color:' + \
                         html_color['Empty'] + ';">' + '<br />' + str(i) + '-' + str(i + 1) + '</div>'
            i+=1




        # Print remaining periodic tasks
        html += "<br /><br />"
        html2 += "<br /><br />"
        html3 += "<br /><br /><br /><br />"
        html1 += "<br /><br />" + html2 + html3 + html

        for p in tasks:
            print(p.get_unique_name() + " is dropped due to overload at time: " + str(i))
            html += "<p>" + p.get_unique_name() + " is dropped due to overload at time: " + str(i) + "</p>"

        # Html output end
        html1 += "</div></div></body></html>"
        index = open('templates/index.html')
        lines = index.readlines()
        indexHtml = ""
        for line in lines:
            indexHtml += line
        output = open('templates/rm.html', 'w')
        output.write(indexHtml + html1)
        output.close()

