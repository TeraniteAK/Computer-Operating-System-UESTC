# 再加个sortqueue和修改statues就差不多了
# rel和de加个修改队列内容的
global r_list      # 全局的一个r_list   0~3 : r1~r4   内容int  当前资源剩余可分配的
r_list = []

for i in range(4):
    r_list.append(i + 1)


class process:
    def __init__(self):
        self.name = ''
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r4 = 0
        self.status = ''     #  running blocked ready
        self.priority = 0    # 1<2<3


global p_list     # 全局的p_list  状态表 内容：class process
p_list = []

global ready_queue
ready_queue = []   # 就绪队列   内容：class process
global block_queue
block_queue = []   # 阻塞队列   内容：class process
global running
running = 'null'   # 正在运行   内容：class process.name


def print_status():
    global ready_queue
    global block_queue
    global running
    print("ready_queue: ", end='')
    for item in ready_queue:
        print(item.__dict__)
    if (ready_queue == []):
        print()
    print("block_queue: ", end='')
    for item in block_queue:
        print(item.__dict__)
    if(block_queue == []):
        print()
    print("running: " + running)


def create_process(pname, priority):
    global p_list
    global running
    global block_queue
    global ready_queue
    a = process()
    a.name = pname
    a.priority = priority
    for item in p_list:
        if item.name == pname:
            print("Error: duplication of name")
            return
    if ready_queue == []:
        if running == 'null':
            running = a.name
            a.status = 'running'
        else:
            ready_queue.append(a)
            a.status = 'ready'
    else:
        ready_queue.append(a)
        a.status = 'ready'

    p_list.append(a)
    sort_blocked_queue()
    sort_ready_queue()


def release_process_all(pname):
    global p_list
    global r_list
    global running
    global block_queue
    global ready_queue
    for item in p_list:
        if item.name == pname:
            r_list[0] += item.r1
            item.r1 = 0
            r_list[1] += item.r2
            item.r2 = 0
            r_list[2] += item.r3
            item.r3 = 0
            r_list[3] += item.r4
            item.r4 = 0

    for i in range(len(block_queue)):
        if block_queue[i].name == pname:
            del(block_queue[i])

    for i in range(len(ready_queue)):
        if ready_queue[i].name == pname:
            del(ready_queue[i])

    if(running == pname):
        running = ''

    sort_blocked_queue()
    sort_ready_queue()


def delete_process(pname):
    global p_list
    global running
    global block_queue
    global ready_queue
    for item in p_list:
        if item.name == pname:
            release_process_all(pname)
            p_list.remove(item)


def show_process():
    global p_list
    for item in p_list:
        print(item.__dict__)


def request_resouce(rname, num):
    global running
    global ready_queue
    global block_queue
    global r_list
    global p_list
    num = int(num)
    if(running == 'null'):
        print("Error: no processing running")
        return
    if(rname == 'R1'):
        if(r_list[0]-num < 0):
            print("Error: insufficient resources")
            for item in p_list:
                if(item.name) == running:
                    temp = item
            temp.priority = 'blocked'
            block_queue.append(temp)   # 将running的进程放入阻塞队列 之后只要有资源出来 马上就给他
            running = ready_queue[0].name
            ready_queue.pop(0)
        else:
            for item in p_list:    # 正常分配资源
                if item.name == running:
                    item.r1 += num
                    r_list[0] -= num

    if (rname == 'R2'):
        if (r_list[1] - num < 0):
            print("Error: insufficient resources")
            for item in p_list:
                if (item.name) == running:
                    temp = item
            temp.priority = 'blocked'
            block_queue.append(temp)  # 将running的进程放入阻塞队列 之后只要有资源出来 马上就给他
            if ready_queue == []:
                return
            else:
                running = ready_queue[0].name
                ready_queue.pop(0)
        else:
            for item in p_list:  # 正常分配资源
                if item.name == running:
                    item.r1 += num
                    r_list[1] -= num

    if (rname == 'R3'):
        if (r_list[2] - num < 0):
            print("Error: insufficient resources")
            for item in p_list:
                if (item.name) == running:
                    temp = item
            temp.priority = 'blocked'
            block_queue.append(temp)  # 将running的进程放入阻塞队列 之后只要有资源出来 马上就给他
            if ready_queue == []:
                return
            else:
                running = ready_queue[0].name
                ready_queue.pop(0)
        else:
            for item in p_list:  # 正常分配资源
                if item.name == running:
                    item.r1 += num
                    r_list[2] -= num

    if (rname == 'R4'):
        if (r_list[3] - num < 0):
            print("Error: insufficient resources")
            for item in p_list:
                if (item.name) == running:
                    temp = item
            temp.priority = 'blocked'
            block_queue.append(temp)  # 将running的进程放入阻塞队列 之后只要有资源出来 马上就给他
            if ready_queue == []:
                return
            else:
                running = ready_queue[0].name
                ready_queue.pop(0)
        else:
            for item in p_list:  # 正常分配资源
                if item.name == running:
                    item.r1 += num
                    r_list[3] -= num

    sort_blocked_queue()


def print_resource():
    print(r_list)


def time_out():
    global r_list
    global ready_queue
    global running
    for item in p_list:
        if item.name == running:
            temp = item
    ready_queue.append(temp)
    running = ready_queue[0].name
    ready_queue.pop(0)

    sort_blocked_queue()
    sort_ready_queue()


def sort_ready_queue():   # 实现优先级队列排序
    temp = []
    for item in ready_queue:
        if(item.priority == 3):
            temp.append(item)

    for item in ready_queue:
        if(item.priority == 2):
            temp.append(item)

    for item in ready_queue:
        if(item.priority == 1):
            temp.append(item)


def sort_blocked_queue():   # 实现优先级队列排序
    temp = []
    for item in block_queue:
        if(item.priority == 3):
            temp.append(item)

    for item in block_queue:
        if(item.priority == 2):
            temp.append(item)

    for item in block_queue:
        if(item.priority == 1):
            temp.append(item)



if __name__ == '__main__':
    while(1):
        print("shell>", end='')
        command = []
        command = input().split()
        if(command[0] == 'cr'):
            create_process(command[1], command[2])
        elif(command[0] == 'de'):
            delete_process(command[1])
        elif(command[0] == 'pp'):
            show_process()
        elif(command[0] == 'rel'):
            release_process_all(command[1])
        elif(command[0] == 'ps'):
            print_status()
        elif(command[0] == 'req'):
            request_resouce(command[1], command[2])
        elif(command[0] == 'pr'):
            print_resource()
        elif (command[0] == 'to'):
            time_out()




