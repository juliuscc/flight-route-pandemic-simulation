import networkx as nx

import simulation.prepare_graph as prepare_graph
import simulation.check_progress as check_progress
import simulation.iterate as iterate_graph
import simulation.select_start_range as ssr
import simulation.simulation_const as sim_const


def test_for_ranges(original_graph):
    series_for_all_ranges = list()
    exception_nodes = list()
    graph_size = len(original_graph.nodes)
    ranges = ssr.range(original_graph, elements=3, selectRange=0.1,)

    print("Testing ranges. High to low.")

    for rI, r in enumerate(ranges):
        series_for_range = list()
        print(f"Testing range ({rI+1} / {len(ranges)}): ", end='', flush=True)
        for (node, degree) in r:
            print("*", end='', flush=True)

            SEIR_convergence_series = simulate_with_starting_point(
                original_graph, node)
            # print(steps_for_current_node)
            series_for_range.append(SEIR_convergence_series)
            # try:
            # except Exception:
            #     exception_nodes.append(node)
        print("")
        series_for_all_ranges.append(series_for_range)

    if (len(exception_nodes) > 0):
        print(
            f"Nodes: {exception_nodes} did not finish. Probably not i giant component. Consider removing!"
        )

    return series_for_all_ranges


def simulate_with_starting_point(original_graph, node_id):
    # Create a copy of the graph and add the SEIR properties
    graph = original_graph.copy()

    # Add the exposed airport
    node = graph.nodes[node_id]
    node['exposed'] = int(
        sim_const.PORTION_OF_POPULATION_EXPOSED * node['susceptible']
    )
    node['infected'] = int(
        sim_const.PORTION_OF_POPULATION_INFECTED * node['susceptible']
    )
    node['susceptible'] = (
        node['susceptible'] - node['exposed'] - node['infected']
    )

    step = 0
    states = list()
    seir_state = None
    previous_state = None

    # In a loop:
    while True:
        # 1.
        # Collect the current state for all nodes in the network.
        seir_state = check_progress.collect_SEIR_state_sum(graph)

        # 1b.
        # If this state is exactly the same as previous, no change in any field
        # we should stop the simulation
        if previous_state != None and seir_state == previous_state:
            break

        # 1c.
        # If we have done too many steps (hard limit), break the simulation anyway
        if step > sim_const.MAX_STEPS_IN_SIMULATION:
            break

        # 2.
        # Append the sum of all SEIR state divided by total population
        # to the current step (sum of all output variables should be 1)
        normalized = check_progress.normalize_SEIR_data(seir_state)
        states.append(normalized)

        # 3.
        # Perform one iteration on the graph.
        iterate_graph.iterate_graph(graph)

        previous_state = seir_state
        step += 1

    return states
