import networkx as nx
from simulation.prepare_graph import prepare_graph
from simulation.check_progress import check_progress
from simulation.iterate import iterate_graph


def steps_for_node(original_graph, node_id):
    graph = original_graph.copy()
    prepare_graph(graph)

    # print(graph.nodes())
    # print(graph.edges())
    # print(graph.adj['2618'])

    graph.add_node(
        node_id,
        contaminated=True,
        contaminated_step=0
    )

    steps = 0
    coverage = 0

    while(coverage < 0.95):
        print(f"Coverage is {coverage} on step {steps}")
        iterate_graph(graph, steps)
        coverage = check_progress(graph)
        steps += 1

    print(
        f"It takes {steps} for 95% of the world to be contaminated when beginning from node {node_id}")
