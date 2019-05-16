import networkx as nx
import random
import numpy as np
import numpy.linalg as npl

import simulation.simulation_const as simConst

recover_probability = 0.01

# This buffer is used to send messages between neighbors in an efficient way.
message_buffer = dict()


def iterate_graph(graph):
    """Do one iteration over the graph with external and internal factors"""

    _do_external_scatter(graph, message_buffer)
    _do_external_gather(graph, message_buffer)

    _do_internal_update(graph)


def _do_external_scatter(graph, message_buffer):
    """From each node, send information to all neighboring nodes
    about the influence it has on them"""

    for node_id in graph.nodes:
        # 1.
        # Collect the current state (SEIR) of this node in vector.
        node_data = graph.nodes[node_id]
        node_seir_state = np.array([
            node_data['susceptible'],
            node_data['exposed'],
            node_data['infectious'],
            node_data['recovered']]
        )

        # 2.
        # Weight the outgoing value xi from x going to each neighbor by that neighbors
        # initial population. The outgoing value xi should be a vector on the format
        # xi = [S, E, I, R]
        for neighbourID in graph.adj[node_id]:
            if neighbourID not in message_buffer:
                message_buffer[neighbourID] = list()

            f = ((graph.nodes[neighbourID]['population'] *
                  (1 - simConst.BETA_KEEP_LOCAL_STATE_FRACTION))
                 /
                 graph.nodes[neighbourID]['sum_neighbour_weights']
                 )

            # 3.
            # Append the value from this node on the end of the queue in message_buffer
            # for the neighboring node to consume.
            message_buffer[neighbourID].append(
                node_seir_state * f
            )

    return


def _do_external_gather(graph, message_buffer):
    """Read the message queue from all neighbors and update internal state"""

    for node_id in graph.nodes:
        node_data = graph.nodes[node_id]

        local_seir_state = np.array([
            node_data['susceptible'],
            node_data['exposed'],
            node_data['infectious'],
            node_data['recovered']
        ])

        incoming_seir_state = np.array([0., 0., 0., 0.])

        # 1.
        # Acquire the list of all neighbors messages and sum the incoming population
        # for each of SEIR.
        for incoming_state in message_buffer[node_id]:
            incoming_seir_state += incoming_state

        message_buffer[node_id].clear()

        # Normalizing should no longer be needed here.
        # # 3.
        # # Normalize the sum of all incoming populations to be
        # # equal to the initial_population
        # seir_sum = sum(incoming_seir_state)
        # frac = node_data['population'] / seir_sum
        # incoming_seir_state *= frac

        # 4.
        # Update local state where the fraction beta = [0, 1] of the new populations
        # come from external sources and the rest is kept from the previous state.
        new_state = (
            local_seir_state * simConst.BETA_KEEP_LOCAL_STATE_FRACTION +
            # NO NORMALIZING JUST ADD IT! * (1 - simConst.BETA_KEEP_LOCAL_STATE_FRACTION)
            incoming_seir_state
        )

        # To compensate for rounding errors we normalize here
        # this is not really necessary if we don't want the number to
        # be exactly constant.
        seir_sum = sum(new_state)
        frac = node_data['population'] / seir_sum
        new_state *= frac

        node_data['susceptible'] = new_state[0]
        node_data['exposed'] = new_state[1]
        node_data['infectious'] = new_state[2]
        node_data['recovered'] = new_state[3]
    return


def _do_internal_update(graph):
    for node_id in graph.nodes:
        node_data = graph.nodes[node_id]

        x_old = np.array([
            node_data['susceptible'],
            node_data['exposed'],
            node_data['infectious'],
            node_data['recovered']
        ])

        # Getting parameters
        omega = simConst.SEIR_RATE_RECOVERY
        mu = simConst.SEIR_RATE_NATURAL_DEATH
        nu = simConst.SEIR_RATE_NATURAL_BIRTH
        sigma = simConst.SEIR_PERIOD_LATENT
        gamma = simConst.SEIR_INFECTED_PERIOD
        beta = simConst.SEIR_TRANSMISSION_COEFFICIENT
        h = simConst.SEIR_TIME_STEP

        # Setting up M_x parameters
        A = 1 + mu * h + (beta * h * x_old[2]) / node_data['population']
        B = omega * h
        C = 1 + (mu + sigma) * h
        D = 1 + (mu + gamma) * h
        G = sigma * h
        H = (beta * h * x_old[2]) / node_data['population']
        J = 1 + (mu + omega) * h
        F = gamma * h

        # Creating matrices Mx and D
        M_x = np.array([[A, 0., 0., -B],
                        [-H, C, 0., 0.],
                        [0., -G, D, 0.],
                        [0., 0., -F, J]])

        D = (np.identity(4)
             + ((nu * h) / 1 + (mu - nu) * h)
             * np.array([[1., 1., 1., 1.],
                         [0., 0., 0., 0.],
                         [0., 0., 0., 0.],
                         [0., 0., 0., 0.]]))

        # Creating the new state
        x_new = np.matmul(npl.inv(M_x), D).dot(x_old)

        # Save state
        node_data['susceptible'] = x_new[0]
        node_data['exposed'] = x_new[1]
        node_data['infectious'] = x_new[2]
        node_data['recovered'] = x_new[3]

        # Just convert all infected to susceptible.
        if 'blocked' in node_data:
            node_data['susceptible'] += node_data['infectious']
            node_data['infectious'] = 0

    return

#
#
#
#
#
#
#
#
#
#
###########################################################
# Old functions that should probably be removed soon!!    #
###########################################################


def _infect_node(graph, node_id, step=0):
    attributes = graph.nodes.data()[node_id]
    attributes['contaminated'] = True
    attributes['contaminated_step'] = step

    graph.add_node(
        node_id,
        **attributes
    )


def _heal_node(graph, node_id, step=0):
    attributes = graph.nodes.data()[node_id]
    attributes['contaminated'] = False
    attributes['contaminated_step'] = step

    graph.add_node(
        node_id,
        **attributes
    )


def _iterate_graph_old(graph, step):
    # Get all infected nodes
    infected_nodes = filter(
        lambda node: node[1]['contaminated'],
        graph.nodes.data()
    )

    # Iterate over every infected node
    for infected in infected_nodes:
        infected_id = infected[0]
        infection_probability = infected[1]['importance']

        # Get all healthy neighbours of the infected node
        neighbours = graph.adj[infected_id]
        healthy_neighbours = [neighbour for neighbour in neighbours if not graph.nodes.data()[
            neighbour]['contaminated']]

# TODO: This should be updated to consider the external factor

        # Do a coin flip for every healthy neighbour and infect
        for neighbour in healthy_neighbours:
            if random.random() < infection_probability:
                infect_node(graph, neighbour)

    # 2. Recover step

    # Get all infected nodes
    infected_nodes = filter(
        lambda node: node[1]['contaminated'],
        graph.nodes.data()
    )

    # Iterate over every infected node
    for infected in infected_nodes:
        infected_id = infected[0]

        if random.random() < recover_probability:
            heal_node(graph, infected_id)
