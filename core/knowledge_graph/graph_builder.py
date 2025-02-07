from py2neo import Graph, Node, Relationship

class EnterpriseKnowledgeGraph:
    def __init__(self, uri: str, user: str, password: str):
        self.graph = Graph(uri, auth=(user, password))
        
    def create_node(self, label: str, properties: dict):
        node = Node(label, **properties)
        self.graph.create(node)
        return node
    
    def create_relationship(self, from_node: Node, to_node: Node, rel_type: str):
        rel = Relationship(from_node, rel_type, to_node)
        self.graph.create(rel)
        return rel
    
    def query_subgraph(self, entity_name: str, depth: int = 2):
        query = f"""
        MATCH (e)-[*1..{depth}]-(related)
        WHERE e.name = '{entity_name}'
        RETURN e, related
        """
        return self.graph.run(query).data()
