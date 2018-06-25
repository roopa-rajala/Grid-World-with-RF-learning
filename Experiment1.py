import random
noOfOperatorsApplied = 0
Width = 80
reached = 0
score =0
episode =0
flag =0
player = (4, 0)
(x, y) = (5, 5)
walk_reward = -1
w=12
gamma=0.5
alpha=0.3
hasblock=0
actions=[0,1,2,3]
pickup = [0,1,2,3,4]
dropoff=[0,1,2,3,5]
a=[4,4,4,4,0,0]
q={}
for i in range(5):
    for j in range(5):
        for m in range(2):
            for k in range(6):
                q[(i,j,m,k)]=0
pickDrop = [(0,0, 0, "red", 4, 12), (1,0, 3, "red", 4, 12), (2,2, 2, "red", 4, 12), (3,4, 4, "red", 4, 12),
                    (4,3, 3, "green", 0, 12), (5,0, 4, "green", 0, 12)]

class Experiment:
    root = None
    board = None
    def __init__(self,root,board):
        self.root = root
        self.board = board
    # create the grid
    def grid(self):
        global text, me, episode, hasblock
        self.board.grid(row=0, column=0)
        for i in range(x):
            for j in range(y):
                self.board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="white",
                                            width=1)
        #
        for (pos, i, j, c, d, w) in pickDrop:
            self.board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill=c, width=1)
        val = round(q.get((player[0], player[1], hasblock, 0)), 2)
        self.board.create_text(player[0] * Width + Width * 5 / 10, player[1] * Width + Width * 1 / 10, text=val)
        val = round(q.get((player[0], player[1], hasblock, 3)), 2)
        self.board.create_text(player[0] * Width + Width * 1 / 10, player[1] * Width + Width * 5 / 10, text=val)
        val = round(q.get((player[0], player[1], hasblock, 1)), 2)
        self.board.create_text(player[0] * Width + Width * 5 / 10, player[1] * Width + Width * 9 / 10, text=val)
        val = round(q.get((player[0], player[1], hasblock, 2)), 2)
        self.board.create_text(player[0] * Width + Width * 9 / 10, player[1] * Width + Width * 5 / 10, text=val)
        #agent
        if hasblock == 0:
            me = self.board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                                             player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10,
                                             fill="orange",
                                             width=1, tag="me")

        else:
            me = self.board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                                             player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10,
                                             fill="pink",
                                             width=1, tag="me")

    def PRandom(self):

        global text,  me, episode, hasblock
        if episode > 3000:
            self.printqtable()
            self.PGreedy()
            return
        self.grid()
        direction = random.randint(0, 3)
        self.checkApplicableOperator()
        self.move_random(direction)
        episode += 1
        self.root.after(1, self.PRandom)

    def PGreedy(self):
        global text,  me, episode, hasblock
        if episode > 6000:
            self.printqtable()
            return
        self.grid()
        self.checkApplicableOperator()
        self.chooseAction()
        episode += 1
        self.root.after(1, self.PGreedy)
    def checkApplicableOperator(self):
        global player,hasblock,pickDrop,score,episode,noOfOperatorsApplied
        for (pos, i, j, c, d, w) in pickDrop:
            if player[0] == i and player[1] == j:

                if c == "red" and hasblock == 0 and d > 0:
                    score += 12
                    hasblock = 1
                    lst = list(pickDrop[pos])
                    lst[4] = lst[4] - 1
                    a[pos] = a[pos] - 1
                    pickDrop[pos] = tuple(lst)
                    self.learn(player[0], player[1], 4, 12, player[0], player[1], hasblock)
                    episode+=1
                    noOfOperatorsApplied+=1
                elif c == "green" and hasblock == 1 and d < 8:
                    score += 12
                    hasblock = 0
                    lst = list(pickDrop[pos])
                    lst[4] = lst[4] + 1
                    a[pos] = a[pos] + 1
                    # if lst[4]==8:
                    #     print("first dropoff:",episode)
                    pickDrop[pos] = tuple(lst)
                    self.learn(player[0], player[1], 5, 12, player[0], player[1], hasblock)
                    episode+=1
                    noOfOperatorsApplied += 1
    def chooseAction(self):

        qvalues = [self.getQ(player[0], player[1], hasblock, direct) for direct in actions]
        maxQ  =max(qvalues)
        m=[]
        for index in range(4):
            if qvalues[index] == maxQ:
                m.append(index)
        if len(m)>1:
             moveTo = random.randint(0, len(m))

        else:
            moveTo = m[0]
        self.move_random(moveTo)

    def move_random(self,direction):
        global noOfOperatorsApplied
        if direction == 0:
            noOfOperatorsApplied += 1
            self.call_up()

        elif direction == 1:
            noOfOperatorsApplied += 1
            self.call_down()
        elif direction == 2:
            noOfOperatorsApplied += 1
            self.call_right()
        else:
            noOfOperatorsApplied += 1
            self.call_left()

    def call_up(self):
        self.try_move(0, -1, 0)

    def call_left(self):
        self.try_move(-1, 0, 3)

    def call_right(self):
        self.try_move(1, 0, 2)

    def call_down(self):
        self.try_move(0, 1, 1)

    def reset(self):
        global a
        new_x = 4
        new_y = 0
        a = [4, 4, 4, 4, 0, 0]
        for (pos, i, j, c, d, w) in pickDrop:
                if c == "red":
                    lst = list(pickDrop[pos])
                    lst[4] = 4
                    pickDrop[pos] = tuple(lst)
                elif c == "green":
                    lst = list(pickDrop[pos])
                    lst[4] = 0
                    pickDrop[pos] = tuple(lst)

    def try_move(self,dx, dy, direct):
        global player, x, y, score, walk_reward, restart, me, hasblock, reached, flag,episode,a,noOfOperatorsApplied
        new_x = player[0] + dx
        new_y = player[1] + dy
        if a[0] == 0 and a[1] == 0 and a[2] == 0 and a[3] == 0 and a[4] == 8 and a[5] == 8:
            print("Terminated after",episode,"steps with",noOfOperatorsApplied)
            noOfOperatorsApplied = 0
            self.reset()

        self.checkedges(player[0], player[1])
        if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y):

            self.board.coords(me, new_x * Width + Width * 2 / 10, new_y * Width + Width * 2 / 10,
                         new_x * Width + Width * 8 / 10, new_y * Width + Width * 8 / 10)

            score += -1

            for (pos, i, j, c, d, w) in pickDrop:
                if new_x == i and new_y == j:
                    if c == "red" and hasblock==0 and d>0:
                        flag=1

                    elif c == "green" and hasblock==1 and d<8:
                        flag = 2
            self.learn(player[0], player[1], direct, -1, new_x, new_y, hasblock)
            player = (new_x, new_y)
            if episode==100 or episode==500 or episode ==1500 or episode ==3000 or episode==3500 or episode ==4500 or episode==5000 or episode==6000 or episode==5500 :
                print(episode,score)
            flag = 0

    def checkedges(self,new_x,new_y):
        if (new_x == 0 and new_y>0 and new_y<4):
            self.learn(player[0], player[1],3, -1, new_x, new_y, hasblock)
        elif(new_x == 4 and new_y>0 and new_y<4):
            self.learn(player[0], player[1], 2, -1, new_x, new_y, hasblock)
        elif(new_y == 0 and new_x>0 and new_x<4):
            self.learn(player[0], player[1],0 , -1, new_x, new_y, hasblock)
        elif(new_y == 4 and new_x>0 and new_x<4):
            self.learn(player[0], player[1], 1, -1, new_x, new_y, hasblock)
        elif(new_x==0 and new_y==0):
            self.learn(player[0], player[1], 0, -1, new_x, new_y, hasblock)
            self.learn(player[0], player[1], 3, -1, new_x, new_y, hasblock)
        elif (new_x == 4 and new_y == 0):
            self.learn(player[0], player[1], 0, -1, new_x, new_y, hasblock)
            self.learn(player[0], player[1], 2, -1, new_x, new_y, hasblock)
        elif (new_x == 0 and new_y == 4):
            self.learn(player[0], player[1], 3, -1, new_x, new_y, hasblock)
            self.learn(player[0], player[1], 1, -1, new_x, new_y, hasblock)
        elif (new_x == 4 and new_y == 4):
            self.learn(player[0], player[1], 2, -1, new_x, new_y, hasblock)
            self.learn(player[0], player[1], 1, -1, new_x, new_y, hasblock)

    def getQ(self,statex, statey, hasblock, action):
        return q.get((statex, statey, hasblock, action))

    def learn(self,statex1, statey1, direct, reward, statex2, statey2, hasblock):
        if flag == 0:
            maxqnew = max([self.getQ(statex2, statey2, hasblock, direct) for direct in actions])
        elif flag == 1:
            maxqnew = max([self.getQ(statex2, statey2, hasblock, direct) for direct in pickup])
        elif flag == 2:
            maxqnew = max([self.getQ(statex2, statey2, hasblock, direct) for direct in dropoff])

        self.learnQ(statex1, statey1, direct, reward, reward + gamma * maxqnew, hasblock)

    def learnQ(self,statex, statey, action, reward, value, hasblock):
        '''
        Q-learning:
            Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))
        '''
        oldv = q.get((statex, statey, hasblock, action), None)
        if oldv is None:
            q[(statex, statey, hasblock, action)] = reward
        else:
            q[(statex, statey, hasblock, action)] = (1 - alpha) * oldv + alpha * value
            # q[(statex, statey,hasblock, action)] = oldv + alpha * (value - oldv)

    def printqtable(self):
        print("Q table for agent does not have block")
        print("X Y N S E W")
        for row in range(5):
            for column in range(5):
                    print(row,column,q.get((row,column,0,0)),q.get((row,column,0,1)),q.get((row,column,0,2)),q.get((row,column,0,3)))
        print("Q table for have block")
        print("X Y N S E W")
        for row in range(5):
            for column in range(5):
                    print(row,column,q.get((row,column,1,0)),q.get((row,column,1,1)),q.get((row,column,1,2)),q.get((row,column,1,3)))