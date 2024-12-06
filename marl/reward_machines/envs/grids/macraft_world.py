from envs.grids.game_objects import *
import random, math, os
import numpy as np

class MACraftWorld:

    def __init__(self, file_map, num_agents):
        self.num_agents = num_agents
        self.agents = []
        self._load_map(file_map)
        self.env_game_over = False

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def execute_action(self, actions):
        for agent, action in zip(self.agents, actions):
            ni, nj = agent.i, agent.j

            # Getting new position after executing action
            ni, nj = self._get_next_position(ni, nj, action)

            # Interacting with the objects that is in the next position (this doesn't include monsters)
            action_succeeded = self.map_array[ni][nj].interact(agent)

            # So far, an action can only fail if the new position is a wall
            if action_succeeded:
                agent.change_position(ni, nj)

    def _get_next_position(self, ni, nj, action):
        """
        Returns the position where the agent would be if we execute action
        """
        action = Actions(action)

        # OBS: Invalid actions behave as NO-OP
        if action == Actions.up   : ni-=1
        if action == Actions.down : ni+=1
        if action == Actions.left : nj-=1
        if action == Actions.right: nj+=1

        return ni, nj

    def get_true_propositions(self):
        """
        Returns a list of strings with the propositions that are True for each agent
        """
        ret = []
        for agent in self.agents:
            prop = str(self.map_array[agent.i][agent.j]).strip()
            ret.append(prop)
        return ret

    def get_features(self):
        """
        Returns a list of arrays, each array representing the features of each agent
        """
        ret = []
        for agent in self.agents:
            features = np.array([agent.i, agent.j])
            ret.append(features)
        return ret

    def show(self):    
        """
        Prints the current map with all the agents
        """
        r = ""
        for i in range(self.map_height):
            s = ""
            for j in range(self.map_width):
                agents_at_position = []
                for agent in self.agents:
                    if agent.idem_position(i, j):
                        agents_at_position.append(str(agent))
                if len(agents_at_position) > 0:
                    s += " ".join(agents_at_position)
                else:
                    s += str(self.map_array[i][j])
            if i > 0:
                r += "\n"
            r += s
        print(r)

    def get_model(self):
        """
        This method returns a model of the environment. 
        We use the model to compute optimal policies using value iteration.
        The optimal policies are used to set the average reward per step of each task to 1.
        """
        S = [(x, y) for x in range(1, 40) for y in range(1, 40)] # States
        A = self.actions.copy() # Actions
        L = dict([((x, y), str(self.map_array[x][y]).strip()) for x, y in S]) # Labeling function
        T = {} # Transitions (s, a) -> s' (they are deterministic)
        for s in S:
            x, y = s
            for a in A:
                x2, y2 = self._get_next_position(x, y, a)
                T[(s, a)] = s if str(self.map_array[x2][y2]) == "X" else (x2, y2)
        return S, A, L, T # SALT xD

    def _load_map(self, file_map):
        """
        This method adds the following attributes to the game:
            - self.map_array: array containing all the static objects in the map (no monsters and no agent)
                - e.g. self.map_array[i][j]: contains the object located on row 'i' and column 'j'
            - self.agents: list of agents present in the environment
            - self.map_height: number of rows in every room 
            - self.map_width: number of columns in every room
        The inputs:
            - file_map: path to the map file
        """
        # contains all the actions that the agent can perform
        self.actions = [Actions.up.value, Actions.right.value, Actions.down.value, Actions.left.value]

        # loading the map
        self.map_array = []
        self.class_ids = {} # I use the lower case letters to define the features
        f = open(file_map)
        i, j = 0, 0
        for l in f:
            # I don't consider empty lines!
            if len(l.rstrip()) == 0:
                continue

            # this is not an empty line!
            row = []
            j = 0
            for e in l.rstrip():
                if e in "abcdefghijklmnopqrstuvwxyzH":
                    entity = Empty(i, j, label=e)
                    if e not in self.class_ids:
                        self.class_ids[e] = len(self.class_ids)
                    # if e == "H":
                    #     self.agents.append(entity) # Add agent to the list of agents
                if e in " A" or e in " B" or e in " C" or e in "D" or e in "E":
                    entity = Empty(i, j)
                if e == "X":
                    entity = Obstacle(i, j)
                if self.num_agents == 2:
                    if e == "A" or e == "B":
                        self.agents.append(Agent(e,i,j,self.actions))
                elif self.num_agents == 3:
                    if e == "A" or e == "B" or e == "C":
                        self.agents.append(Agent(e,i,j,self.actions))
                elif self.num_agents == 5:
                    if e == "A" or e == "B" or e == "C" or e == "D" or e == "E":
                        self.agents.append(Agent(e,i,j,self.actions))
                self.agents=sorted(self.agents, key=lambda x: x.c)
                row.append(entity)
                j += 1
            self.map_array.append(row)
            i += 1
        f.close()
        # height width
        self.map_height, self.map_width = len(self.map_array), len(self.map_array[0])