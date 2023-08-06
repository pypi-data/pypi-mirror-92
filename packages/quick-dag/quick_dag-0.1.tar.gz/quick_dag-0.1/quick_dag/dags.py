import daft
from causalgraphicalmodels import CausalGraphicalModel
import matplotlib.pyplot as plt

class dag_class:
    class create_dag:
        def __init__(self):
            self.nodes = set()
            self.edges = set()
            self.coordinates= {}
    
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, node_abbreviation, node_full_name, edges, coordinate):
        """
        add node to graph
        
        Params:
        -------
        node_abbreviation: str, abbreviation of node that will be displayd in graph, e.g. e
        node_full_name: str, full name of node to be added with edges, e.g. experience
        edges: arr, array of all edges that will be displayed, e.g. e->g, e->f
        """
        
        self.nodes[node_abbreviation] = {'full_name':node_full_name, 'edges':edges, 'coordinate':coordinate}


    def show(self):
        self.dag = self.create_dag()
        for node_key, node_items in self.nodes.items():
            self.dag.nodes.add(node_key)
            for e in node_items['edges']:
                self.dag.edges.add((node_key, e))
            self.dag.coordinates[node_key] = (node_items['coordinate'])
        
        self.dag.gm = CausalGraphicalModel(nodes=self.dag.nodes, edges=self.dag.edges)
        self.dag.pgm = daft.PGM()
    
        
        pgm = daft.PGM()
        for node in self.dag.gm.dag.nodes:
            pgm.add_node(node, node, *self.dag.coordinates[node])
        for edge in self.dag.gm.dag.edges:
            pgm.add_edge(*edge)
        pgm.render()
        plt.gca() #.invert_yaxis()
        
        
    def get_all_backdoor_adjustment_sets(self, node1, node2):
        all_adjustment_sets = self.dag.gm.get_all_backdoor_adjustment_sets(node1, node2)
        for s in all_adjustment_sets:
            if all(not t.issubset(s) for t in all_adjustment_sets if t != s):
                print(s)
                
    def get_all_independence_relationships(self, max_printouts=99999, filter_on_node=False):
        all_independencies = self.dag.gm.get_all_independence_relationships()
        counter = 0
        for s in all_independencies:
            if counter >= max_printouts:
                print('stopped at defined max: {}'.format(max_printouts))
                break
            if all(
                t[0] != s[0] or t[1] != s[1] or not t[2].issubset(s[2])
                for t in all_independencies
                if t != s
                ):
                if filter_on_node != False:
                    if (filter_on_node in s):
                        print(s)
                        counter += 1
                else:
                    print(s)
                    counter += 1

        