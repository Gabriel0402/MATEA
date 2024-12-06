import random, time
from baselines import logger

class Agent:
    def __init__(self, num_actions, q_init):
        self.Q = {}
        self.actions = list(range(num_actions))
        self.q_init = q_init

    def get_qmax(self, s):
        s=tuple(s)
        if s not in self.Q:
            self.Q[s] = dict([(a,self.q_init) for a in self.actions])
        return max(self.Q[s].values())

    def get_best_action(self, s):
        s =tuple(s)
        qmax = self.get_qmax(s)
        best = [a for a in self.actions if self.Q[s][a] == qmax]
        return random.choice(best)

# In the learning method
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
          use_rs=False):  # Parameters stay the same

    # Initialize agents
    agents = [Agent(env.action_space.n, q_init) for _ in range(num_agents)]

    reward_total = 0
    step = 0
    num_episodes = 0
    Q = {}
    actions = list(range(env.action_space.n)) 
    # Variable initialization stays same

    while step < total_timesteps:
        states = tuple(env.reset())
        for s, agent in zip(states, agents):
            s=tuple(s)
            if s not in agent.Q: agent.Q[s] = dict([(a, q_init) for a in agent.actions])
        while True:
            # Selecting and executing the action for each agent
            actions = [random.choice(agent.actions) if random.random() < epsilon else agent.get_best_action(s) for s, agent in zip(states, agents)]
            # env.reset()
            next_states, rewards, dones, infos = env.step(actions)
            next_states = tuple(next_states)

            # Updating the q-values for each agent
            for _s, _a, _r, _sn, _done, agent in zip(states, actions, infos["rewards"], next_states, infos["dones"], agents):
                _s = tuple(_s)
                if _s not in agent.Q: agent.Q[_s] = dict([(b, q_init) for b in agent.actions])
                if _done: _delta = _r - agent.Q[_s][_a]
                else: _delta = _r + gamma * agent.get_qmax(_sn) - agent.Q[_s][_a]
                agent.Q[_s][_a] += lr * _delta

            # Moving to the next state
            reward_total += rewards
            step += num_agents
            if step % print_freq == 0:
                logger.record_tabular("steps", step)
                logger.record_tabular("episodes", num_episodes)
                logger.record_tabular("total reward", reward_total)
                logger.dump_tabular()
                reward_total = 0
            if dones:
                num_episodes += 1
                break
            states = next_states