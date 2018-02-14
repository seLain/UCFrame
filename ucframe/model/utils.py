
from Manager.TaskCaseManager.taskCaseManager import TaskCaseManager
from Manager.TaskCaseManager.taskCase import TaskCase

def get_pure_graph():
    
    graph_nodes, graph_edges = get_no_redundant_graph()
    
    pure_nodes = []
    pure_edges = []
    
    for anode in graph_nodes:
        pure_nodes.append((anode['text'], anode['type']))
        
    for aedge in graph_edges:
        
        source_node = None;
        target_node = None;
        
        for anode in pure_nodes:
            if anode[0] == graph_nodes[aedge['source-index']]['text'] and anode[1] == graph_nodes[aedge['source-index']]['type']:
                source_node = anode
            if anode[0] == graph_nodes[aedge['target-index']]['text'] and anode[1] == graph_nodes[aedge['target-index']]['type']:
                target_node = anode
                
        pure_edges.append((source_node, target_node))

    return pure_nodes, pure_edges
        
def get_no_redundant_graph():

    RepoLocationList = ['ucframe', 'model', 'TaskCaseRepository']
    taskManager = TaskCaseManager(RepoLocationList)
    taskmodels = taskManager.all_task_models()
    
    export_nodes_data = []
    export_nodes_data_id = 1
    no_redundant_edges = []
    export_edges_data = []
    for id in taskmodels.keys():
        graph = taskmodels[id]
        nodes, edges = graph.currentGraph()
        # remove the duplicate noes. there are duplicated node because of task integration
        duplicated_nodes = []
        for anode in nodes:
            for n in export_nodes_data:
                if anode[0] == n['text'] and anode[1] == n['type']:
                    duplicated_nodes.append(anode)
                    break
        # prepare the nodes
        for anode in nodes:
            if anode not in duplicated_nodes:  # check if the node is duplicated
                export_nodes_data.append({'id': export_nodes_data_id, 
                                          'reflexive': 'false',
                                          'text': anode[0],
                                          'type': anode[1]})
                export_nodes_data_id += 1
        # prepare the edges
        for aedge in edges:
            source_index = -1
            target_index = -1
            for anode in export_nodes_data:
                if aedge[0][0] == anode['text']:
                    source_index = export_nodes_data.index(anode)
                if aedge[1][0] == anode['text']:
                    target_index = export_nodes_data.index(anode)
            export_edge = {'source-index': source_index, 'target-index': target_index}
            if export_edge in no_redundant_edges:
                for element in export_edges_data:
                    if element['source-index'] == export_edge['source-index'] and element['target-index'] == export_edge['target-index']:
                        element['count'] += 1
                        break
            else:
                no_redundant_edges.append(export_edge)
                export_edges_data.append({'source-index': source_index,
                                          'target-index': target_index,
                                          'count': 1})
    
    return export_nodes_data, export_edges_data

# calcualte the number of occurence 
def term_occurence_count(term_type, term_text):

    occur_count = {'owner_count': 0,
                   'cuc_count': 0,
                   'occur_count': 0 }

    RepoLocationList = ['ucframe', 'model', 'TaskCaseRepository']
    taskManager = TaskCaseManager(RepoLocationList)
    all_task_cases = taskManager.taskCase
    taskmodels = taskManager.all_task_models()

    owner_list = []
    cuc_list = []

    for id in taskmodels.keys():
        #print 'check task id:', id
        graph = taskmodels[id]
        nodes, edges = graph.currentGraph()
        for anode in nodes:
            if term_type == anode[1] and term_text == anode[0]:
                occur_count['occur_count'] += 1
                #print '[term_occurence_count]:', all_task_cases[id]
                owner = all_task_cases[id]['Task-Meta']['Member']
                if owner not in owner_list:
                    owner_list.append(owner)
                if id not in cuc_list:  # add to the cuc_list
                    cuc_list.append(id)

    occur_count['owner_count'] = len(owner_list)
    occur_count['cuc_count'] = len(cuc_list)

    return occur_count

