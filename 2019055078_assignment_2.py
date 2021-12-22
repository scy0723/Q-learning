import random

f = open("input.txt", 'r')
lines = f.readlines()
N = sum(1 for line in open('input.txt'))
states = [[0]*N ]*N

#input
i=0
for line in lines:
    states[i]=list(line.rstrip())
    i=i+1
f.close()

# rewards
rewards = {
    'S': 0, #start point
    'G': +100,  #goal point
    'T': +1,  #bonus point
    #'T': +10,  #bonus point
    #'T': +20,  #bonus point
    'B': -100, #bomb
    'P': 0  #normal path
}

# possible actions
actions = {
    'UP': (-1, 0),
    'DOWN': (+1, 0),
    'RIGHT': (0, +1),
    'LEFT': (0, -1),
}

#gamma
gamma = 0.9

# initial
for i in range (N):
    for j in range (N):
        if (states[i][j]=='S'):
            start_position_i = i
            start_position_j = j
            break
        
q = {}
current_state_i, current_state_j = start_position_i, start_position_j
goal=0

##################Functions########################

# i,j에서 이동할 수 있는 방향
def possible_actions(i, j):
    act=[]
    for action in actions.items():
        _i, _j = i + action[1][0], j + action[1][1]
        if 0 <= _i < len(states) and 0 <= _j < len(states[i]):
            act.append(action[0])
    return act

# Q표 초기화
def initialize_q():
    for i in range(0, len(states)):
        for j in range(0, len(states[i])):
            for action in possible_actions(i,j):
                q[i,j,action]=0
            
# reward
def compute_reward(i, j): #next i,j
    return rewards[states[i][j]]

# Q값이 가장 큰 방향 선정
def best_action_policy(ii, jj):
    return max( possible_actions(ii,jj), key = lambda possible_action: q[(ii, jj, possible_action)])


#정한 방향으로 칸 움직임
def take_action(i, j, action):
    return i+actions[action][0],j+actions[action][1]

#Q update
def q_update(i, j, action, next_i, next_j):
    if (states[next_i][next_j]=='G'):
        return 100
    if (states[next_i][next_j]=='B'):
        return -100
    reward = compute_reward(next_i, next_j)
    return  reward + gamma * q[(next_i, next_j, best_action_policy(next_i, next_j))]
 
# q-learning
def q_learning(i, j):
    for act in possible_actions(i, j):
        ii, jj = take_action(i, j, act)
        q[(i, j, act)] = q_update(i, j, act, ii, jj)
    random_act = random.choice(possible_actions(i,j))
    ii, jj = take_action(i, j, random_act)

    return ii, jj

def game():
    global current_state_i, current_state_j, q
    current_state_i, current_state_j = q_learning(current_state_i, current_state_j)

#경로찾기
def print_answer(i, j):
    global goal
    ii, jj = take_action(i, j, best_action_policy(i, j) )
    
    #print(str(i*len(states)+j)+' ')  
    fw.write(str(i*len(states)+j)+' ')  
    if (states[ii][jj]=='G'):
        goal=1
        fw.write(str(ii*len(states)+jj)+' ')  
    return ii, jj

def start():
    global current_state_i, current_state_j, q
    current_state_i, current_state_j = print_answer(current_state_i, current_state_j)
      

# initialize Q function
initialize_q()
cnt=100000
fw = open("output.txt","w")
while(cnt>0):
    cnt=cnt-1
    game()


current_state_i=0
current_state_j=0
'''
for i in range (len(states)):
    for j in range (len(states)):
        for act in possible_actions(i,j):
            print(i,' ',j,' ',act,' ',q[i,j,act])
    print('\n')
print('_________________________')
'''
while (goal==0):
    start()


fw.write('\n')
fw.write(str(max(q[0,0,'RIGHT'],q[0,0,'DOWN'])))
fw.close()
    



