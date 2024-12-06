import gym, random
from gym import spaces
import numpy as np
from reward_machines.rm_environment import RewardMachineEnv, MARewardMachineEnv
from envs.grids.craft_world import CraftWorld
from envs.grids.macraft_world import MACraftWorld
from envs.grids.value_iteration import value_iteration

class GridEnv(gym.Env):
    def __init__(self, env):
        self.env = env
        N,M      = self.env.map_height, self.env.map_width
        self.action_space = spaces.Discrete(4) # up, right, down, left
        self.observation_space = spaces.Box(low=0, high=max([N,M]), shape=(2,), dtype=np.uint8)

    def get_events(self):
        return self.env.get_true_propositions()

    def step(self, action):
        self.env.execute_action(action)
        obs = self.env.get_features()
        reward = 0 # all the reward comes from the RM
        done = False
        info = {}
        return obs, reward, done, info

    def reset(self):
        self.env.reset()
        return self.env.get_features()

    def show(self):
        self.env.show()

    def get_model(self):
        return self.env.get_model()

class MAGridEnv(gym.Env):
    def __init__(self, env, num_agents):
        self.env = env
        self.num_agents = num_agents

        # Set the action and observation spaces based on the environment
        N, M = self.env.map_height, self.env.map_width
        self.action_space = spaces.Discrete(5)  # up, right, down, left, stay
        self.observation_space = spaces.Box(low=0, high=max([N, M]), shape=(num_agents,), dtype=np.uint8)

    def get_events(self):
        return self.env.get_true_propositions()

    def step(self, actions):
        assert len(actions) == self.num_agents, "Number of actions must match the number of agents."

        self.env.execute_action(actions)

        # for agent_id, action in enumerate(actions):
        #     self.env.execute_action(action)

        obs = self.env.get_features()
        reward = np.zeros(self.num_agents)  # all the reward comes from the RM
        done = [False] * self.num_agents
        info = {}
        
        return obs, reward, done, info

    def reset(self):
        self.env.reset()

        obs = self.env.get_features()
        return obs

    def show(self):
        self.env.show()

    def get_model(self):
        return self.env.get_model()

class GridRMEnv(RewardMachineEnv):
    def __init__(self, env, rm_files):
        super().__init__(env, rm_files)

    def render(self, mode='human'):
        if mode == 'human':
            # commands
            str_to_action = {"w":0,"d":1,"s":2,"a":3,"x":4}

            # play the game!
            done = True
            while True:
                if done:
                    print("New episode --------------------------------")
                    obs = self.reset()
                    print("Current task:", self.rm_files[self.current_rm_id])
                    self.env.show()
                    print("Features:", obs)
                    print("RM state:", self.current_u_id)
                    print("Events:", self.env.get_events())

                print("\nAction? (WASD keys or q to quite) ", end="")
                a = input()
                print()
                if a == 'q':
                    break
                # Executing action
                if a in str_to_action:
                    obs, rew, done, _ = self.step(str_to_action[a])
                    self.env.show()
                    print("Features:", obs)
                    print("Reward:", rew)
                    print("RM state:", self.current_u_id)
                    print("Events:", self.env.get_events())
                else:
                    print("Forbidden action")
        else:
            raise NotImplementedError

    def test_optimal_policies(self, num_episodes, epsilon, gamma):
        """
        This code computes optimal policies for each reward machine and evaluates them using epsilon-greedy exploration

        PARAMS
        ----------
        num_episodes(int): Number of evaluation episodes
        epsilon(float):    Epsilon constant for exploring the environment
        gamma(float):      Discount factor

        RETURNS
        ----------
        List with the optimal average-reward-per-step per reward machine
        """
        S,A,L,T = self.env.get_model()
        print("\nComputing optimal policies... ", end='', flush=True)
        optimal_policies = [value_iteration(S,A,L,T,rm,gamma) for rm in self.reward_machines]
        print("Done!")
        optimal_ARPS = [[] for _ in range(len(optimal_policies))]
        print("\nEvaluating optimal policies.")
        for ep in range(num_episodes):
            if ep % 100 == 0 and ep > 0:
                print("%d/%d"%(ep,num_episodes))
            self.reset()
            s = tuple(self.obs)
            u = self.current_u_id
            rm_id = self.current_rm_id
            rewards = []
            done = False
            while not done:
                a = random.choice(A) if random.random() < epsilon else optimal_policies[rm_id][(s,u)]
                _, r, done, _ = self.step(a)
                rewards.append(r)
                s = tuple(self.obs)
                u = self.current_u_id
            optimal_ARPS[rm_id].append(sum(rewards)/len(rewards))
        print("Done!\n")

        return [sum(arps)/len(arps) for arps in optimal_ARPS]

class MAGridRMEnv(MARewardMachineEnv):
    def __init__(self, env, rm_files,num_agents):
        super().__init__(env, rm_files,num_agents)

    def render(self, mode='human'):
        if mode == 'human':
            # commands
            str_to_action = {"w":0,"d":1,"s":2,"a":3}

            # play the game!
            done = True
            while True:
                if done:
                    print("New episode --------------------------------")
                    obs = self.reset()
                    print("Current task:", [self.rm_files_list[i] for i in range(self.num_agents)])
                    self.env.show()
                    print("Features:", obs)
                    print("RM state:", [self.current_rm_ids[i] for i in range(self.num_agents)])
                    print("Events:", self.env.get_events())

                actions = []
                for i in range(self.num_agents):         
                    print("\nAction? (WASD keys or q to quite) ", end="")
                    a = input()
                    if a == 'q':
                        break
                    if a in str_to_action:
                        actions.append(str_to_action[a])
                    else:
                        print("Forbidden action")
                    # Executing action
                print()
                obs, rew, done, _ = self.step(actions)
                self.env.show()
                print("Features:", obs)
                print("Reward:", rew)
                print("RM state:", [self.current_rm_ids[i] for i in range(self.num_agents)])
                print("Events:", self.env.get_events())
                        
        else:
            raise NotImplementedError

  
# ----------------------------------------------- MULTI-Agent Task
class MACraftRMEnv3(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/craft/mat1.txt"],["./envs/grids/reward_machines/craft/mat2.txt"],["./envs/grids/reward_machines/craft/mat3.txt"]]
        env = MACraftWorld(file_map,3)
        super().__init__(MAGridEnv(env,3), rm_files,3)

class MACraftRMEnv2Dcent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/2agent/mat1.txt"],["./envs/grids/reward_machines/2agent/mat2.txt"]]
        env = MACraftWorld(file_map,2)
        super().__init__(MAGridEnv(env,2), rm_files,2)

class MACraftRMEnv2Cent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/2agent/cent.txt"],["./envs/grids/reward_machines/2agent/cent.txt"]]
        env = MACraftWorld(file_map,2)
        super().__init__(MAGridEnv(env,2), rm_files,2)

class MACraftRMEnv3Dcent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/3agent/mat1.txt"],["./envs/grids/reward_machines/3agent/mat2.txt"],["./envs/grids/reward_machines/3agent/mat3.txt"]]
        env = MACraftWorld(file_map,3)
        super().__init__(MAGridEnv(env,3), rm_files,3)

class MACraftRMEnv3Cent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/3agent/cent.txt"],["./envs/grids/reward_machines/3agent/cent.txt"],["./envs/grids/reward_machines/3agent/cent.txt"]]
        env = MACraftWorld(file_map,3)
        super().__init__(MAGridEnv(env,3), rm_files,3)

class MACraftRMEnv5Dcent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/5agent/mat1.txt"],["./envs/grids/reward_machines/5agent/mat2.txt"],["./envs/grids/reward_machines/5agent/mat3.txt"],["./envs/grids/reward_machines/5agent/mat4.txt"],["./envs/grids/reward_machines/5agent/mat5.txt"]]
        env = MACraftWorld(file_map,5)
        super().__init__(MAGridEnv(env,5), rm_files,5)

class MACraftRMEnv5Cent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/5agent/cent.txt"],["./envs/grids/reward_machines/5agent/cent.txt"],["./envs/grids/reward_machines/5agent/cent.txt"],["./envs/grids/reward_machines/5agent/cent.txt"],["./envs/grids/reward_machines/5agent/cent.txt"]]
        env = MACraftWorld(file_map,5)
        super().__init__(MAGridEnv(env,5), rm_files,5)
        
class MACraftRMEnvCent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/craft/mat1_a.txt"],["./envs/grids/reward_machines/craft/mat2_a.txt"],["./envs/grids/reward_machines/craft/mat3_a.txt"]]
        env = MACraftWorld(file_map,3)
        super().__init__(MAGridEnv(env,3), rm_files,3)
        
class MACraftRMEnvDcent(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/craft/mat1_s.txt"],["./envs/grids/reward_machines/craft/mat2_s.txt"],["./envs/grids/reward_machines/craft/mat3_s.txt"]]
        env = MACraftWorld(file_map,3)
        super().__init__(MAGridEnv(env,3), rm_files,3)
    
class MACraftRMEnvDcent1(MAGridRMEnv):
    def __init__(self, file_map):
        rm_files = [["./envs/grids/reward_machines/craft/mat1_bg.txt"],["./envs/grids/reward_machines/craft/mat2_bg.txt"],["./envs/grids/reward_machines/craft/mat3_bg.txt"]]
        env = MACraftWorld(file_map,3)
        super().__init__(MAGridEnv(env,3), rm_files,3)
        
class MACraftRMEnv3M0(MACraftRMEnv3):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        super().__init__(file_map)

class MACraftRMEnv3M1(MACraftRMEnv3):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap1.txt"
        super().__init__(file_map)

class MACraftRMEnv3M2(MACraftRMEnv3):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap2.txt"
        super().__init__(file_map)
        
class MACraftRMEnv3M3(MACraftRMEnv3):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap3.txt"
        super().__init__(file_map)
        
class MACraftRMEnv3M10Cent(MACraftRMEnvCent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        super().__init__(file_map)

class MACraftRMEnv3M10Dcent(MACraftRMEnvDcent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        super().__init__(file_map)

class MACraftRMEnv3M10Dcent1(MACraftRMEnvDcent1):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        super().__init__(file_map)

class MACraftRMEnv2M0Dcent(MACraftRMEnv2Dcent):
    def __init__(self):
        file_map = "./envs/grids/maps/2agentmap.txt"
        super().__init__(file_map)

class MACraftRMEnv2M0Cent(MACraftRMEnv2Cent):
    def __init__(self):
        file_map = "./envs/grids/maps/2agentmap.txt"
        super().__init__(file_map)

class MACraftRMEnv5M0Dcent(MACraftRMEnv5Dcent):
    def __init__(self):
        file_map = "./envs/grids/maps/5agentmap.txt"
        super().__init__(file_map)

class MACraftRMEnv5M0Cent(MACraftRMEnv5Cent):
    def __init__(self):
        file_map = "./envs/grids/maps/5agentmap.txt"
        super().__init__(file_map)

class MACraftOriginalEnv(MAGridEnv):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        env = MACraftWorld(file_map,3)
        super().__init__(env,3)

class MACraftRMEnv3M0Dcent(MACraftRMEnv3Dcent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        super().__init__(file_map)

class MACraftRMEnv3M0Cent(MACraftRMEnv3Cent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap0.txt"
        super().__init__(file_map)

class MACraftRMEnv3M1Dcent(MACraftRMEnv3Dcent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap1.txt"
        super().__init__(file_map)

class MACraftRMEnv3M1Cent(MACraftRMEnv3Cent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap1.txt"
        super().__init__(file_map)

class MACraftRMEnv3M2Dcent(MACraftRMEnv3Dcent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap2.txt"
        super().__init__(file_map)

class MACraftRMEnv3M2Cent(MACraftRMEnv3Cent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap2.txt"
        super().__init__(file_map)

class MACraftRMEnv3M3Dcent(MACraftRMEnv3Dcent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap3.txt"
        super().__init__(file_map)

class MACraftRMEnv3M3Cent(MACraftRMEnv3Cent):
    def __init__(self):
        file_map = "./envs/grids/maps/mamap3.txt"
        super().__init__(file_map)