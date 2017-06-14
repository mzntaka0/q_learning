import numpy as np
import matplotlib.pyplot as plt


class Agent:
    """
    [For Reinforcement Learning]
    This class yield Agent which explore and exploit the Environment.
    And find the optimized way of there

    parameter
    ----------
    R[ndarray]: reward matrix
    goal[int]: the goal of environment
    alpha[0.0~1.0]: learning rate
    gamma[0.0~1.0]: discount rate
    """
    # todo: will make Environment Class
    Q = None

    def __init__(self, R, goal, alpha=None, gamma=0.8, epsilon=0.7):
        self.R = R
        self.state = self._get_initial_state()  # int
        self.next_state = None
        self.goal = goal  # int
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        if Agent.Q == None:
            Agent.Q = np.zeros_like(self.R)
        

    def _get_initial_state(self):
        return np.random.random_integers(self.R.shape[0] - 1)


    def recognize_possible_action(self, state):
        """ tell which you can take action in the state """ 
        return np.where(R[state, :] != -1)[0]


    # todo: if all Q value is same, then entirely choose next state randomly
    def _soft_epsilon_greedy(self):
        """
        make aciton probability list

        return
        ----------
        """
        q_list = []
        q_soft = []
        # todo: add condition depending on the possible actions -> soft epsilon-greedy
        print('state{}'.format(self.state))
        possible_actions = self.recognize_possible_action(self.state)
        print('possible_actions: {}'.format(possible_actions))
        for i in possible_actions:
            q_list.append(Agent.Q[self.state, i])
        q_list_np = np.array(q_list)
        exp_max = np.max(q_list_np)
        exp_q = np.exp(q_list_np - exp_max)
        exp_q_sum = np.sum(exp_q)
        print('exp_q: {}, exp_q_sum: {}'.format(exp_q, exp_q_sum))

        for i in exp_q:
            q_soft.append(i / exp_q_sum)

        print('q_soft: {}'.format(q_soft))

        return q_soft


#        action_select_probability = np.zeros(len(possible_actions)-1, dtype=np.float)
#        if len(possible_actions) > 2:
#            action_select_probability[:] = (1.0 - self.epsilon) / (float(len(possible_actions) - 1.0))
#        else:
#            action_select_probability[:] = 1.0 - self.epsilon
#        action_select_probability[np.argmax(Agent.Q[self.state, :])] = self.epsilon
#
#        return action_select_probability


    def select_action(self, state):
        """
        select action using epsilon_greedy

        input
        ----------

        return
        ---------- 
        selected action[tuple]
        """
        print(self.recognize_possible_action(self.state))
        self.next_state = np.random.choice(self.recognize_possible_action(self.state), p=self._soft_epsilon_greedy())

        return (self.state, self.next_state)


    def _next_state_Q_values(self):
        next_Q_action = self.recognize_possible_action(self.next_state)

        return [i for i in Agent.Q[self.next_state, :]]


    def calc_Q_value(self):
        Agent.Q[self.select_action(self.state)] = self.R[self.select_action(self.state)] \
                                                  + self.gamma * np.max(self._next_state_Q_values())


    def set_next_state_as_state(self):
        self.state = self.next_state

        return

    def is_goal(self):
        if self.state == self.goal:
            return True
        else:
            return False


    def select_optimized_strategy(self):
        return


    def start_learning(self):
        print(Agent.Q)
        while not self.is_goal():
            self.select_action(self.state)
            self.calc_Q_value()
            self.set_next_state_as_state()
            print("===Q value===\n {}".format(Agent.Q))

        return




def q_learn(iter_num, R, goal, gamma, alpha=None):
    Agent_dic = {}

    # episode iteration
    for i in range(iter_num):
        print('''
                ##########
                #Agent_{}
                #########
                '''.format(i))
        Agent_dic['agent{}'.format(i)] = Agent(R=R, goal=4, alpha=alpha, gamma=gamma)
        Agent_dic['agent{}'.format(i)].start_learning()

        print(Agent_dic)

    return


if __name__ == '__main__':
    ########################
    # make the Reward Matrix
    ########################
    R = np.zeros(25).reshape(5, 5)
    R[:, :] = -1
    R_exist_path_dic = {
            (0, 1): 0, (0, 2): 0, (0, 3): 0,   # 0
            (1, 2): 0, (1, 4): 100,            # 1
            (2, 0): 0, (2, 3): 0,              # 2
            (3, 0): 0, (3, 4): 100,            # 3
            (4, 4): 100,                       # 4
            }

    for edge, value in R_exist_path_dic.iteritems():
        R[edge] = value

    print(R)


    #########################
    # Q Learning Training
    #########################
    q_learn(iter_num=50, R=R, goal=4, gamma=0.8)
