import numpy as np
import matplotlib.pyplot as plt
import pdb




class Agent:
    """
    [For Reinforcement Learning]
    This class yield Agent which explore and exploit the Environment.
    And find the optimized way of there

    parameter
    ----------
    R[ndarray]: reward matrix
    goal[int]: the goal of environment
    alpha[0.0_1.0]: learning rate
    gamma[0.0_1.0]: discount rate
    epsilon[0.0_1.0]: epsilon greedy parameter
    """
    # todo: will make Environment Class
    Q = None

    def __init__(self, R, goal, alpha=0.8, gamma=0.8, epsilon=0.7):
        self.R = R
        self.state = 0  # int
        self.next_state = None
        self.goal = goal  # int
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.selected_action = None
        if Agent.Q is None:
            Agent.Q = np.zeros_like(self.R)
        

    def _get_initial_state(self):
        return np.random.random_integers(self.R.shape[0] - 1)


    def recognize_possible_action(self, state):
        """ tell which you can take action in the state """ 
        return np.where(R[state, :] != -1)[0]


    # todo: if all Q value is same, then entirely choose next state randomly
    def _soft_epsilon_greedy(self, tau):
        """
        make aciton probability list

        return
        ----------
        """
        q_list = []
        q_soft = []
        possible_actions = self.recognize_possible_action(self.state)
        for i in possible_actions:
            q_list.append(Agent.Q[self.state, i])
        q_list_np = np.array(q_list) / tau
        exp_max = np.max(q_list_np)
        exp_q = np.exp(q_list_np - exp_max)
        exp_q_sum = np.sum(exp_q)

        for i in exp_q:
            q_soft.append(i / exp_q_sum)

        return q_soft


    def select_action(self, state):
        """
        select action using epsilon_greedy

        input
        ----------

        return
        ---------- 
        selected action[tuple]
        """
        self.next_state = np.random.choice(self.recognize_possible_action(self.state), p=self._soft_epsilon_greedy(tau=200.0))
        self.selected_action = (self.state, self.next_state)


    def _next_state_Q_values(self):
        return Agent.Q[self.next_state]


    def calc_Q_value(self):
        Agent.Q[self.selected_action] = (1.0 - self.alpha) * Agent.Q[self.selected_action] \
                + self.alpha * (self.R[self.selected_action] \
                + self.gamma * np.max(self._next_state_Q_values()))


    def set_next_state_as_state(self):
        self.state = self.next_state

        return


    def is_goal(self):
        if self.state == self.goal:
            print('STOP')
            return True
        else:
            print('CONTINUE')
            return False


    def start_learning(self):
        while not self.is_goal():
            self.select_action(self.state)
            self.calc_Q_value()
            self.set_next_state_as_state()
            print("""===Q value===\n
                 ------------------
                 |  s1, a12 | {}  |   
                  ----------|----   |
                 |  s1, a14 | {}  |
                  ----------|----   |
                 |  s2, a21 | {}  |
                  ----------|----   |
                 |  s2, a23 | {}  |
                  ----------|----   |
                 |  s2, a25 | {}  |
                  ----------|----   |
                 |  s3, a32 | {}  |
                  ----------|----   |
                 |  s3, a36 | {}  |
                  ----------|----   |
                 |  s4, a41 | {}  |
                  ----------|----   |
                 |  s4, a45 | {}  |
                  ----------|----   |
                 |  s5, a54 | {}  |
                  ----------|----   |
                 |  s5, a52 | {}  |
                  ----------|----   |
                 |  s5, a56 | {}  |
                 | --------------   |
                 | --------------   |
    (optional)  (|  s6, a66 | {}  |)
                   """ .format(
                       Agent.Q[0, 1], Agent.Q[0, 3],
                       Agent.Q[1, 0], Agent.Q[1, 2], Agent.Q[1, 4],
                       Agent.Q[2, 1], Agent.Q[2, 5],
                       Agent.Q[3, 0], Agent.Q[3, 4],
                       Agent.Q[4, 1], Agent.Q[4, 3], Agent.Q[4, 5],
                       Agent.Q[5, 5]
                       ))


        return




def q_learn(iter_num, R, goal, gamma, alpha):
    Agent_dic = {}

    # episode iteration
    for i in range(iter_num):
        print('''
                ##########
                #Agent_{}
                ##########
                '''.format(i))
        Agent_dic['agent{}'.format(i)] = Agent(R, goal, alpha=alpha, gamma=gamma)
        Agent_dic['agent{}'.format(i)].start_learning()

    return


if __name__ == '__main__':
    ########################
    # make the Reward Matrix
    ########################
    R = np.zeros(36).reshape(6, 6)
    R[:, :] = -1
    R_exist_path_dic = {
            (0, 1): 0, (0, 3): 0,              # 0
            (1, 0): 0, (1, 2): 0, (1, 4): 0,   # 1
            (2, 1): 0, (2, 5): 100,            # 2
            (3, 0): 0, (3, 4): 0,              # 3
            (4, 1): 0, (4, 3): 0, (4, 5): 100, # 4
            (5, 5): 100
            }

    for edge, value in R_exist_path_dic.iteritems():
        R[edge] = value

    print("""
            === R ===\n{}
            """.format(R))


    #########################
    # Q Learning Training
    #########################
    q_learn(iter_num=100, R=R, goal=5, gamma=0.5, alpha=0.8)
