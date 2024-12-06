import random, time
from baselines import logger
import itertools
from itertools import chain

class CentralizedAgent:
    def __init__(self, num_actions, num_agents, q_init):
        self.Q = {}
        self.actions = list(itertools.product(range(num_actions), repeat=num_agents))
        self.q_init = q_init

    def get_qmax(self, s): 
        s=tuple(s)
        if s not in self.Q:
            self.Q[s] = {a: self.q_init for a in self.actions}
        return max(self.Q[s].values())

    def get_best_action(self, s):
        s=tuple(chain(*s))
        qmax = self.get_qmax(s)
        best = [a for a in self.actions if self.Q[s][a] == qmax]
        return random.choice(best)

# function stays same.
def learn(env,
          num_agents,
          network=None,
          seed=None,
          lr=0.1,
          total_timesteps=100000,
          epsilon=0.1,
          print_freq=10000,
          gamma=0.9,
          q_init=2.0,
          use_crm=False,
          use_rs=False):

    agent = CentralizedAgent(env.action_space.n, num_agents, q_init)
    reward_total = 0
    step = 0
    num_episodes = 0
    while step < total_timesteps:
        states = tuple(env.reset())
        while True:
            if random.random() < epsilon:
                actions = random.choice(agent.actions)
            else:
                actions = agent.get_best_action(states) 

            next_states, rewards, dones, infos = env.step(actions)
            next_states = tuple(next_states)
            for (s, a, r, sn, done) in zip(states, actions, infos["rewards"], next_states, infos["dones"]):
                s = tuple(s)
                if s not in agent.Q:
                    agent.Q[s] = {b: q_init for b in agent.actions}
                if done:
                    _delta = r - agent.Q[s][a]
                else:
                    print("bbb",agent.Q)
                    _delta = r + gamma * agent.get_qmax(sn) - agent.Q[s][a]
                agent.Q[s][a] += lr * _delta

            reward_total += sum(rewards)
            step += num_agents
            if step % print_freq == 0:
                logger.record_tabular("steps", step)
                logger.record_tabular("episodes", num_episodes)
                logger.record_tabular("total reward", reward_total)
                logger.dump_tabular()
                reward_total = 0
            if all(dones):
                num_episodes += 1
                break
            states = next_states