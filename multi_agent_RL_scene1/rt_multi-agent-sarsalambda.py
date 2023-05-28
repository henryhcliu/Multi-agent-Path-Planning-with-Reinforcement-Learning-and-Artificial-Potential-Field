"""
Sarsa is a online updating method for Reinforcement learning.
Unlike Q learning which is a offline updating method, Sarsa is updating while in the current trajectory.
You will see the sarsa is more coward when punishment is close because it cares about all behaviours,
while q learning is more brave because it only cares about maximum behaviour.
"""

from maze_env_sarsa_multi_agent_v2 import Maze
from RL_brain_sarsalambda_mul_v2 import SarsaTable
import numpy as np
import pandas as pd
import math
import os

def calcu_dis(obs):
    dis = np.zeros(3)
    dis[0] = math.sqrt((obs[0][0]-obs[1][0])**2+(obs[0][1]-obs[1][1])**2)
    dis[1] = math.sqrt((obs[0][0]-obs[2][0])**2+(obs[0][1]-obs[2][1])**2)
    dis[2] = math.sqrt((obs[1][0]-obs[2][0])**2+(obs[1][1]-obs[2][1])**2)
    return dis
    

UNIT = 40
def update():
    for episode in range(1): # Here only for test of the algorithm.
        flag_update = 0
        # initial observation
        visual = 1
        observation = env.reset(visual)
        coordinate = [[0,0],[0,0],[0,0]]
        for i in range(3):
            coordinate[i][0] = (observation[i][0]+observation[i][2])/2+20
            coordinate[i][1] = (observation[i][1]+observation[i][3])/2+20
        coordinate = np.array(coordinate) /UNIT
        observation_ = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        
        # RL choose action based on observation
        
        # Step 1: RL choose action based on observation
        action1 = RL1.choose_action(str(observation[0]), index_bot[0])
        action2 = RL2.choose_action(str(observation[1]), index_bot[1])
        action3 = RL3.choose_action(str(observation[2]), index_bot[2])
        
        # Step 2: Artifitial Potential Field (not Updated)
        # 210528 00.19
        distances = calcu_dis(coordinate)
        if np.min(distances) <= math.sqrt(5):
            place = np.array(np.where(distances == np.min(distances)))
            if place.any() == 0:
                delta_x = coordinate[0][0]-coordinate[1][0]
                delta_y = coordinate[0][1]-coordinate[1][1]
                if abs(delta_x) < abs(delta_y):
                    if delta_x>0:
                        action2 = 3
                    else:
                        action2 = 2
                else:
                    if delta_y>0:
                        action2 = 0
                    else:
                        action2 = 1
            elif place.any() == 1:
                delta_x = coordinate[0][0]-coordinate[2][0]
                delta_y = coordinate[0][1]-coordinate[2][1]
                if abs(delta_x) < abs(delta_y):
                    if delta_x > 0:
                        action3 = 3
                    else:
                        action3 = 2
                else:
                    if delta_y > 0:
                        action3 = 0
                    else:
                        action3 = 1
            elif place.any() == 2:
                delta_x = coordinate[1][0]-coordinate[2][0]
                delta_y = coordinate[1][1]-coordinate[2][1]
                if abs(delta_x) < abs(delta_y):
                    if delta_x > 0:
                        action3 = 3
                    else:
                        action3 = 2
                else:
                    if delta_y > 0:
                        action3 = 0
                    else:
                        action3 = 1
                

        # initial all zero eligibility trace
        # RL1.eligibility_trace *= 0
        # RL2.eligibility_trace *= 0
        # RL3.eligibility_trace *= 0
        
        
        #flag = 1
        while True:
            # fresh env
            visual  = 1
            env.render(visual)

            # RL take action and get next observation and reward
            # Bot 1
            observation_[0], reward1, if_index_goal = env.step(0, action1)
            if if_index_goal != 0:
                index_bot[0] = 1
                index_goal[if_index_goal-1] = 1
                if if_index_goal != 1:
                    # change the task of other robots
                    if if_index_goal == 2:
                        RL2.q_table = RL1.q_table
                    else:
                        RL3.q_table = RL1.q_table
            elif reward1 == -1:
                index_bot[0] = 1
            
            # Bot 2
            observation_[1], reward2, if_index_goal = env.step(1, action2)
            if if_index_goal != 0:
                index_bot[1] = 1
                index_goal[if_index_goal-1] = 1
                if if_index_goal != 2:
                    # change the task of other robots
                    if if_index_goal == 1:
                        RL1.q_table = RL2.q_table
                    else:
                        RL3.q_table = RL2.q_table
            elif reward2 == -1:
                index_bot[1] = 1
                        
            # Bot 3
            observation_[2], reward3, if_index_goal = env.step(2, action3)
            if if_index_goal != 0:
                index_bot[2] = 1
                index_goal[if_index_goal-1] = 1
                if if_index_goal != 3:
                    # change the task of other robots
                    if if_index_goal == 1:
                        RL1.q_table = RL3.q_table
                    else:
                        RL2.q_table = RL3.q_table
            elif reward3 == -1:
                index_bot[2] = 1
                        
                        
            # RL choose actions of bots based on next observation
            # Step 1: RL choose action based on observation
            action1_ = RL1.choose_action(str(observation_[0]), index_bot[0])
            action2_ = RL2.choose_action(str(observation_[1]), index_bot[1])
            action3_ = RL3.choose_action(str(observation_[2]), index_bot[2])
            
            # Step 2: Artifitial Potential Field(Updated)
            coordinate_ = np.array([[0,0],[0,0],[0,0]])
            for i in range(3):
                coordinate_[i][0] = (observation_[i][0]+observation_[i][2])/2+20
                coordinate_[i][1] = (observation_[i][1]+observation_[i][3])/2+20
            coordinate_ = np.array(coordinate_)/UNIT
            #observation_ = [[0,0],[0,0],[0,0]]
            distances = calcu_dis(coordinate_)
            if np.min(distances) <= math.sqrt(5):
                
                for i in range(3):
                    if distances[i] <= math.sqrt(5):
                        place = i
                        break
                if place == 0:
                    
                    delta_x = coordinate_[0][0]-coordinate_[1][0]
                    delta_y = coordinate_[0][1]-coordinate_[1][1]
                    if abs(delta_x)<abs(delta_y):
                        if delta_x>0:
                            if index_bot[1] == 0:
                                action2_ = 3
                                flag_update = 2
                            else:
                                action1_ = 2
                                flag_update = 1
                        else:
                            if index_bot[1] == 0:
                                action2_ = 2
                                flag_update = 2
                            else:
                                action1_ = 3
                                flag_update = 1
                    else:
                        if delta_y>0:
                            if index_bot[1] == 0:
                                action2_ = 0
                                flag_update = 2
                            else:
                                action1_ = 1
                                flag_update = 1
                        else:
                            if index_bot[1] == 0:
                                action2_ = 1
                                flag_update = 2
                            else:
                                action1_ = 0
                                flag_update = 1
                elif place == 1:
                    delta_x = coordinate_[0][0]-coordinate_[2][0]
                    delta_y = coordinate_[0][1]-coordinate_[2][1]
                    if abs(delta_x)<abs(delta_y):
                        if delta_x>0:
                            if index_bot[2] == 0:
                                action3_ = 3
                                flag_update = 3
                            else:
                                action1_ = 2
                                flag_update = 1
                        else:
                            if index_bot[2] == 0:
                                action3_ = 2
                                flag_update = 3
                            else:
                                action1_ = 3
                                flag_update = 1
                    else:
                        if delta_y>0:
                            if index_bot[2] == 0:
                                action3_ = 0
                                flag_update = 3
                            else:
                                action1_ = 1
                                flag_update = 1
                        else:
                            if index_bot[2] == 0:
                                action3_ = 1
                                flag_update = 3
                            else:
                                action1_ = 0
                                flag_update = 1
                elif place == 2:
                    delta_x = coordinate[1][0]-coordinate[2][0]
                    delta_y = coordinate[1][1]-coordinate[2][1]
                    if abs(delta_x) < abs(delta_y):
                        if delta_x > 0:
                            if index_bot[2] == 0:
                                action3_ = 3
                                flag_update = 3
                            else:
                                action2_ = 2
                                flag_update = 2
                        else:
                            if index_bot[2] == 0:
                                action3_ = 2
                                flag_update = 3
                            else:
                                action2_ = 3
                                flag_update = 2
                    else:
                        if delta_y > 0:
                            if index_bot[2] == 0:
                                action3_ = 0
                                flag_update = 3
                            else:
                                action2_ = 1
                                flag_update = 2
                        else:
                            if index_bot[2] == 0:
                                action3_ = 1
                                flag_update = 3
                            else:
                                action2_ = 0
                                flag_update = 2
            # 开启对智能体的撞墙检测，如果下一步动作是使智能体撞墙，则再调用贪婪算法，重新选择该智能体的动作
            if flag_update != 0:
                actions = [action1_, action2_, action3_]
                if actions[flag_update-1] == 0:   # up
                    if observation_[flag_update-1][1] <= UNIT:
                        if flag_update == 1:
                            action1_ = RL1.choose_action(str(observation_[0]), index_bot[0])
                        elif flag_update == 2:
                            action2_ = RL2.choose_action(str(observation_[1]), index_bot[1])
                        else:
                            action3_ = RL3.choose_action(str(observation_[2]), index_bot[2])
                elif actions[flag_update-1] == 1:   # down
                    if observation_[flag_update-1][1] >= (MAZE_H - 1) * UNIT:
                        if flag_update == 1:
                            action1_ = RL1.choose_action(str(observation_[0]), index_bot[0])
                        elif flag_update == 2:
                            action2_ = RL2.choose_action(str(observation_[1]), index_bot[1])
                        else:
                            action3_ = RL3.choose_action(str(observation_[2]), index_bot[2])
                    
                elif actions[flag_update-1] == 2:   # right
                    if observation_[flag_update-1][0] >= (MAZE_W - 1) * UNIT:
                        if flag_update == 1:
                            action1_ = RL1.choose_action(str(observation_[0]), index_bot[0])
                        elif flag_update == 2:
                            action2_ = RL2.choose_action(str(observation_[1]), index_bot[1])
                        else:
                            action3_ = RL3.choose_action(str(observation_[2]), index_bot[2])
                elif actions[flag_update-1] == 3:   # left
                    if observation_[flag_update-1][0] <= UNIT:
                        if flag_update == 1:
                            action1_ = RL1.choose_action(str(observation_[0]), index_bot[0])
                        elif flag_update == 2:
                            action2_ = RL2.choose_action(str(observation_[1]), index_bot[1])
                        else:
                            action3_ = RL3.choose_action(str(observation_[2]), index_bot[2])
            
            # Without Learning when performing tasks!
            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            # RL1.learn(str(observation[0]), action1, reward1, str(observation_[0]), action1_)
            # RL2.learn(str(observation[1]), action2, reward2, str(observation_[1]), action2_)
            # RL3.learn(str(observation[2]), action3, reward3, str(observation_[2]), action3_)

            # swap observation and action
            observation = observation_
            action1 = action1_
            action2 = action2_
            action3 = action3_

            # break while loop when end of this episode
            if index_goal == [1,1,1] or index_bot == [1,1,1]:
                if index_goal != [1,1,1]:
                    print('Task Failed!\nMilitary base search situation:', index_goal)
                else:
                    print('Task Succeeded!')
                break
            

    # end of game
    print('game over!')
    #RL1.q_table.to_csv('q_table_SarsLambda_after_100episodes') # save the trained model
    #env.destroy()

if __name__ == "__main__":
    env = Maze()
    index_goal = [0,0,0]
    index_bot = [0,0,0]
    MAZE_H = 10
    MAZE_W = 10
    RL1 = SarsaTable(actions=list(range(env.n_actions)))
    RL1.q_table=pd.read_csv(os.path.join(os.path.dirname(__file__), 'q_table_SarsLambda_100_1_1_9_3'),names=env.action_space) # This line for test
    RL2 = SarsaTable(actions=list(range(env.n_actions)))
    RL2.q_table=pd.read_csv(os.path.join(os.path.dirname(__file__), 'q_table_SarsLambda_100_1_4_10_6'),names=env.action_space) # This line for test
    RL3 = SarsaTable(actions=list(range(env.n_actions)))
    RL3.q_table=pd.read_csv(os.path.join(os.path.dirname(__file__), 'q_table_SarsLambda_100_1_7_6_9'),names=env.action_space) # This line for test

    env.after(10, update)
    env.mainloop()