# -*- coding: utf-8 -*-

class Graph:
    
    def __init__(self,):
        
        self.nodes = []  # assume [(node name, node type)]
        self.edges = []   # assume [(node1, node2)] where node1(src)->node2(dest)
    
    #
    # return the local graph of this description only
    #
    def addDescription(self, description):
        
        terms = description.strip('.\n\t').split(' ')  # assume the description is separate by space
        des_nodes = []  # the nodes in this description
        des_edges = []  # the edges in this description
        
        # extract all the process objects (nodes)
        for aterm in terms:
            if aterm.startswith('@'):
                des_nodes.append((aterm[1:], 'Actor'))
            elif aterm.startswith('$'):
                des_nodes.append((aterm[1:], 'Message'))
            elif aterm.startswith('*'):
                des_nodes.append((aterm[1:], 'System'))
                
        # build the edge
        if len(des_nodes) < 2:  # which means there is 0 or 1 node only
            pass
        else:
            for i in range(0, len(des_nodes)-1):  # build by occurance sequence in this setence
                des_edges.append((des_nodes[i], des_nodes[i+1]))
                
        # add the nodes and edges to the global graph
        self.nodes = list(set(self.nodes + des_nodes))  # the order will be broken
        self.edges = list(set(self.edges + des_edges))  # the order will be broken
        
        return des_nodes, des_edges
    
    def currentGraph(self,):
        
        return self.nodes, self.edges
    

class AMSGraph(Graph):
    
    #
    # return the local graph of this description only
    #
    def addDescription(self, description):
        
        terms = description.strip('.\n\t').split(' ')  # assume the description is separate by space
        des_nodes = []  # the nodes in this description
        des_edges = []  # the edges in this description
        actor_nodes = []
        message_nodes = []
        system_nodes = []

        # extract all the process objects (nodes)
        for aterm in terms:
            if aterm.startswith('@'):
                des_nodes.append((aterm[1:], 'Actor'))
                actor_nodes.append(aterm[1:])
            elif aterm.startswith('$'):
                des_nodes.append((aterm[1:], 'Message'))
                message_nodes.append(aterm[1:])
            elif aterm.startswith('*'):
                des_nodes.append((aterm[1:], 'System'))
                system_nodes.append(aterm[1:])
        
        # build the edge
        if len(des_nodes) < 2:  # which means there is 0 or 1 node only
            pass
        else:
            # build the actor->message edges
            for actor in actor_nodes:
                for message in message_nodes:
                    des_edges.append(((actor, 'Actor'), (message, 'Message')))
            # build the message->system edges
            for message in message_nodes:
                for system in system_nodes:
                    des_edges.append(((message, 'Message'), (system, 'System')))
        
        # add the nodes and edges to the global graph
        self.nodes = list(set(self.nodes + des_nodes))  # the order will be broken
        #self.edges = list(set(self.edges + des_edges))  # the order will be broken
        self.edges = self.edges + des_edges  # allow the duplicate edges
        
        return des_nodes, des_edges
        