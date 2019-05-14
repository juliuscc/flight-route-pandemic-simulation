import networkx as nx
from simulation.prepare_graph import prepare_graph
from simulation.check_progress import check_progress
from simulation.iterate import iterate_graph

import simulation.select_start_range as ssr


def test_all_nodes(original_graph):
    steps_for_all_nodes = list()

    graph_size = len(original_graph.nodes)
    index = 0

    for node in original_graph.nodes:

        index += 1
        if index % 5 == 0:
            print(f"Tested {(index / graph_size) * 100}% of the graph")
        try:
            steps_for_current_node = steps_for_node(original_graph, node)
            # print(steps_for_current_node)
            steps_for_all_nodes.append(steps_for_current_node)
        except Exception:
            print(
                f"Node {node} is probably not connected to the giant connected component of the graph. Consider removing {node} from dataset."
            )

    return steps_for_all_nodes


def test_for_ranges(original_graph):
    steps_for_all_nodes = list()
    exception_nodes = list()
    graph_size = len(original_graph.nodes)
    ranges = ssr.range(original_graph)

    print("Testing ranges. High to low.")

    for rI, r in enumerate(ranges):
        steps_int = list()
        print(f"Testing range ({rI+1} / {len(ranges)}): ", end='', flush=True)
        for (node, degree) in r:
            print("*", end='', flush=True)

            try:
                steps_for_current_node = steps_for_node(original_graph, node)
                # print(steps_for_current_node)
                steps_int.append(steps_for_current_node)
            except Exception:
                exception_nodes.append(node)
        print("")
        steps_for_all_nodes.append(steps_int)

    if (len(exception_nodes) > 0):
        print(
            f"Nodes: {exception_nodes} probably not i giant component. Consider removing!"
        )

    return steps_for_all_nodes


def steps_for_node(original_graph, node_id):
    graph = original_graph.copy()
    prepare_graph(graph)

    attributes = graph.nodes.data()[node_id]
    attributes['contaminated'] = True
    attributes['contaminated_step'] = 0

    graph.add_node(
        node_id,
        **attributes
    )

    steps = 0
    coverage = 0

    while(coverage < 0.95):
        iterate_graph(graph, steps)
        coverage = check_progress(graph)
        steps += 1

        if steps > 100:
            raise Exception('Stuck in loop')

    return steps
