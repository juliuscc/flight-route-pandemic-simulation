import networkx as nx
import random
import numpy as np

import lib.simulation.simulation_const as simConst

recover_probability = 0.01


def iterate_graph(graph):
    """Do one iteration over the graph with external and internal factors"""
    # This buffer is used to send messages between neighbors in an efficient way.
    message_buffer = dict()

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
            node_data['infected'],
            node_data['recovered']]
        )

        # 2.
        # Weight the outgoing value xi from x going to each neighbor by that neighbors
        # initial population. The outgoing value xi should be a vector on the format
        # xi = [S, E, I, R]
        for neighbourID in graph.adj[node_id]:
            if neighbourID not in message_buffer:
                message_buffer[neighbourID] = list()

            neighbour_weight = (
                # Population for this neighbour
                graph.nodes[neighbourID]['population'] /
                # Total population for current node
                node_data['sum_neighbour_weights']
            )

            # 3.
            # Append the value from this node on the end of the queue in message_buffer
            # for the neighboring node to consume.
            message_buffer[neighbourID].append(
                node_seir_state * neighbour_weight
            )

    return


def _do_external_gather(graph, message_buffer):
    """Read the message queue from all neighbors and update internal state"""

    for node_id in graph.nodes:
        node_data = graph.nodes[node_id]

        local_seir_state = np.array([
            node_data['susceptible'],
            node_data['exposed'],
            node_data['infected'],
            node_data['recovered']
        ])

        incoming_seir_state = np.array([0, 0, 0, 0])

        # 1.
        # Acquire the list of all neighbors messages and sum the incoming population
        # for each of SEIR.
        for incoming_state in message_buffer[node_id]:
            incoming_seir_state += incoming_state

        message_buffer[node_id].clear()

        # 3.
        # Normalize the sum of all incoming populations to be
        # equal to the initial_population
        seir_sum = sum(incoming_seir_state)
        frac = node_data['population'] / seir_sum
        incoming_seir_state *= frac

        # 4.
        # Update local state where the fraction beta = [0, 1] of the new populations
        # come from external sources and the rest is kept from the previous state.
        new_state = (
            local_seir_state * simConst.BETA_KEEP_LOCAL_STATE_FRACTION +
            incoming_seir_state * (1 - simConst.BETA_KEEP_LOCAL_STATE_FRACTION)
        )

        node_data['susceptible'] = new_state[0]
        node_data['exposed'] = new_state[1]
        node_data['infected'] = new_state[2]
        node_data['recovered'] = new_state[3]
    return


def _do_internal_update(graph):

    # 1. Perform all the quations for the SEIR model and update the local state.
    # TODO: What are these anyway?
    for node_id in graph.nodes:
        node_data = graph.nodes[node_id]

        node_data['susceptible'] = node_data['susceptible']
        node_data['exposed'] = node_data['exposed']
        node_data['infected'] = node_data['infected']
        node_data['recovered'] = node_data['recovered']

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
