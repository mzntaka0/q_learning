import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pdb
import json


def autocreateR(dim):
    print('dim: {}'.format(dim))
    R = np.zeros(dim**2).reshape(dim, dim)
    R[:, :] = -1
    goal_node = np.random.randint(int(4*(dim-1)/5.0), dim)
    print('goal node is: {}'.format(goal_node))

    path_lists = []
    for i in range(dim):
        path_num = np.random.randint(1, int(2*dim/5.0))
        path_lists.append(
                np.random.randint(0, dim, path_num)
                )

    for i, path_list in enumerate(path_lists):
        if i == goal_node:
            R[i, i] = 100
            continue
        for path in path_list:
            if path == goal_node:
                R[i, path] = 100
                continue
            R[i, path] = 0
        else:
            R[i, i] = -1

    return R.tolist(), goal_node


if __name__ == '__main__':
    dim_list = [i for i in range(5, 101, 5)]
    print(dim_list)

    for dim in dim_list:
        R, goal_node = autocreateR(dim)
        np_R = np.array(R)
        print(np_R)


        g = nx.DiGraph()

        for i in range(np_R.shape[0]):
            for j in range(np_R.shape[1]):
                if np_R[i][j] == 0 or R[i][j] == 100:
                    g.add_edge(i, j)

        for path in nx.all_simple_paths(g, source=0, target=goal_node):
            print(path)
        print(g.edges())
        pos = nx.circular_layout(g, dim=2)
        nx.draw(g, pos)
        plt.show()





        #fig, ax = plt.subplots()
        #ax.set_xticks(np.arange(np.array(R).shape[0]) + 0.5, minor=False)
        #ax.set_yticks(np.arange(np.array(R).shape[1]) + 0.5, minor=False)
        #ax.invert_yaxis()
        #heatmap = ax.pcolor(R, cmap='GnBu')
        #plt.show()
        #with open('../../test_jsons/params_without_R.json', 'rb') as f:
        #    params_without_R = json.load(f)

        #params_without_R['R'] = R
        #params_without_R['goal'] = goal_node

        #with open('../../test_jsons/params_dim_{}.json'.format(dim), 'w') as f:
        #    json.dump(params_without_R, f)
