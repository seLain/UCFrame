# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from ucframe import model
from ucframe.controllers.secure import SecureController
from ucframe.model import DBSession, metadata
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from ucframe.lib.base import BaseController
from ucframe.controllers.error import ErrorController

from Manager.TaskCaseManager.taskCaseManager import TaskCaseManager
from ucframe.model import utils

import os
from configobj import ConfigObj

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the ucframe application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    RepoLocationList = ['ucframe', 'model', 'TaskCaseRepository']
    taskManager = TaskCaseManager(RepoLocationList)
    
    def _before(self, *args, **kw):
        tmpl_context.project_name = "ucframe"

    @expose('ucframe.templates.index')
    def index(self):
        """Handle the front-page."""
        self.create_tagtable()
        return dict(page='index')

    @expose('ucframe.templates.contribute')
    def contribute(self, **kw):
        
        other_input = {}
        self_input = {}
        self_parameters=["taskName", "Member", "Project"]
        remove_key = []
        for i in kw:
            if kw[i] == '':
                remove_key.append(i)  
            elif i in self_parameters:
                self_input[i] = kw[i]
            else:
                other_input[i] = kw[i]
                
        return {'parameters': other_input, 'self_input': self_input}
    
    @expose('ucframe.templates.contribute_pre')
    def contribute_pre(self, **kw):
        
        other_input = {}
        self_input = {}
        self_parameters_name = ["PreCondition-Status-", "PreCondition-Condition-"]
        self_parameters=[]
        for i in range(1,10):           #[seLain] TOFIX: No better way to do this ?
            for parameters_name in self_parameters_name:
                key =  parameters_name + str(i)
                if key not in self_parameters:
                    self_parameters.append(key)
        remove_key = []                 #[seLain] TOFIX: Unknown function code
        for i in kw:
            if kw[i] == '':             
                remove_key.append(i)    #[seLain] TOFIX: Unknown function code
            elif i in self_parameters:  #[seLain] TOFIX: Unknown function code
                self_input[i] = kw[i]
            else:                       #[seLain] this code seems to be passed
                other_input[i] = kw[i]  # to the next page, for params accumulation
        
        # for embedded view test
        export_nodes_data, export_edges_data =  utils.get_no_redundant_graph()
     
        #return {'parameters':other_input, 'self_input': self_input}
        return {'parameters':other_input, 'self_input':self_input, 'nodes':export_nodes_data, 'edges':export_edges_data}
    
    @expose('ucframe.templates.contribute')  #[seLain] Does this expose necessary ?
    def redirect_page(self, **kw):
        
        if kw['redirectPage'] == "Pre-Condition-Edit":
            redirect('/contribute_pre', kw)
        elif kw['redirectPage'] == "Post-Condition-Edit":
            redirect('/contribute_post', kw)
        elif kw['redirectPage'] == "Event-Flow-Edit":
            redirect('/contribute_event', kw)
        elif kw['redirectPage'] == "Task-Meta-Edit":
            redirect('/contribute', kw)
        elif kw['redirectPage'] == "View-Task-Edit":
            redirect('/contribute_view', kw)
        elif kw['redirectPage'] == "Save-Data":
            redirect('/contribute_save', kw)
        redirect('/contribute')
    
    @expose('ucframe.templates.contribute_event')
    def contribute_event(self, **kw):
        other_input = {}
        self_input = {}
        self_parameters_name = ["EventFlow-"]
        self_parameters=[]
        for i in range(1,10):
            for parameters_name in self_parameters_name:
                key =  parameters_name + str(i)
                if key not in self_parameters:
                    self_parameters.append(key)
        remove_key = []
        for i in kw:
            if kw[i] == '':
                remove_key.append(i)  
            elif i in self_parameters:
                self_input[i] = kw[i]
            else:
                other_input[i] = kw[i]
        return {'parameters':other_input, 'self_input': self_input}
    
    @expose('ucframe.templates.contribute_post')
    def contribute_post(self, **kw):
        other_input = {}
        self_input = {}
        self_parameters_name = ["PostCondition-Status-", "PostCondition-Condition-"]
        self_parameters=[]
        for i in range(1,10):
            for parameters_name in self_parameters_name:
                key =  parameters_name + str(i)
                if key not in self_parameters:
                    self_parameters.append(key)
        remove_key = []
        for i in kw:
            if kw[i] == '':
                remove_key.append(i)  
            elif i in self_parameters:
                self_input[i] = kw[i]
            else:
                other_input[i] = kw[i]
        return {'parameters':other_input, 'self_input': self_input}
    
    @expose('ucframe.templates.contribute_view')
    def contribute_view(self, **kw):
        other_input = {}
        self_input = {}
        pre_condition_name = ["PreCondition-Status-", "PreCondition-Condition-"]
        pre_condition=[]
        post_condition_name = ["PostCondition-Status-", "PostCondition-Condition-"]
        post_condition=[]
        event_flow_name = ["EventFlow-"]
        event_flow=[]
        meta_task=["taskName", "Member", "Project"]
        for i in range(1,10):
            for parameters_name in pre_condition_name:
                key =  parameters_name + str(i)
                if key not in pre_condition:
                    pre_condition.append(key)
            for parameters_name in post_condition_name:
                key =  parameters_name + str(i)
                if key not in post_condition:
                    post_condition.append(key)
            for parameters_name in event_flow_name:
                key =  parameters_name + str(i)
                if key not in event_flow:
                    event_flow.append(key)    
                    
                    
        pre_condition_input={}
        post_condition_input={}
        event_flow_input={}    
        task_meta_input={}    
                    
        remove_key = []
        for i in kw:
            if kw[i] == '':
                remove_key.append(i)  
            elif i in pre_condition:
                pre_condition_input[i] = kw[i]
            elif i in post_condition:
                post_condition_input[i] = kw[i]
            elif i in event_flow:
                event_flow_input[i] = kw[i]
            elif i in event_flow:
                event_flow_input[i] = kw[i]
            elif i in meta_task:
                task_meta_input[i] = kw[i]
        
        # get similar CUCs
        event_list = pre_condition_input.values() + event_flow_input.values() + post_condition_input.values()
        #print 'event_list in contribute_view:', event_list
        cuc_collecction = self.similar_cucs(event_list)['cucs']
        #print 'cuc_collecction:', cuc_collecction

        return {'pre_condition':pre_condition_input, 
                'post_condition': post_condition_input, 
                'event_flow': event_flow_input, 
                'task_meta': task_meta_input,
                'similar_cucs': cuc_collecction}
    
    @expose('ucframe.templates.contribute_save')
    def contribute_save(self, **kw):
        self.taskManager.saveTaskCase(kw)
        #self.taskManager.saveOntologyFromTaskCase(kw)
        redirect('/index')
    
    @expose('json')
    def taskCase_TypeTag(self, **kw):
        
        fileLocation = os.sep.join(['ucframe', 'model', 'Tag', 'Tag Table.txt'])
        TagTable = ConfigObj(fileLocation, encoding='UTF8') 
        output = {}
        output['Actor'] = {}
        output['Message'] = {}
        output['System'] = {}
        
        for tag in TagTable:
            if TagTable[tag]['Category'] not in output:
                continue
            number = len(output[TagTable[tag]['Category']])
            output[TagTable[tag]['Category']][number] = {}
            name = TagTable[tag]['Name']
            tagType = ''
            if TagTable[tag]['Category'] == 'Actor':
                tagSig = '@'
            elif TagTable[tag]['Category'] == 'Message':
                tagSig = '$'
            elif TagTable[tag]['Category'] == 'System':
                tagSig = '*'
            output[TagTable[tag]['Category']][number]['id'] =  "number"
            output[TagTable[tag]['Category']][number]['name'] =  tagSig + name 
            output[TagTable[tag]['Category']][number]['type'] = 'contact'
            output[TagTable[tag]['Category']][number]['img'] = '/img/glyphicons-halflings.png'
        
        return output
    
    # when this method is called, it will scan the entire repository and 
    # generate a new tag table based on the exisiting content in the repository
    def create_tagtable(self,):
        
        table_location = os.sep.join(['ucframe', 'model', 'Tag', 'Tag Table.txt'])
        TagTable = ConfigObj(table_location, encoding='UTF8')
        
        export_nodes_data, export_edges_data =  utils.get_no_redundant_graph()
        
        for anode in export_nodes_data:
            TagTable[anode['text']] = {'Name':anode['text'],
                                       'RealWord':anode['text'],
                                       'Category':anode['type'],
                                       'Type':'Instance',
                                       'Abstraction':anode['text']}
        
        TagTable.write()
        
    
    @expose('ucframe.templates.view')
    def view(self):
        
        export_nodes_data, export_edges_data =  utils.get_no_redundant_graph()
        
        # return the json data to the page visualization
        import json
        jsonfile = open('graph.json', 'w')
        jsonfile.write(json.dumps(export_nodes_data))
        jsonfile.close()
        jsonfile = open('edges.json', 'w')
        jsonfile.write(json.dumps(export_edges_data))
        jsonfile.close()
        
        return dict(page='view', nodes=export_nodes_data, edges=export_edges_data)
    
    @expose('json')
    def graph(self):
        
        import json
        with open('graph.json') as data_file:
            data = json.load(data_file)
                
        return {'data': data}
    
    @expose('json')
    def edges(self):
        
        import json
        with open('edges.json') as data_file:
            data = json.load(data_file)
                
        return {'data': data}
    
    @expose('json')
    def local_graph(self):
        
        import json
        with open('local_graph.json') as data_file:
            data = json.load(data_file)
                
        return {'data': data}
    
    @expose('json')
    def local_edges(self):
        
        import json
        with open('local_edges.json') as data_file:
            data = json.load(data_file)
                
        return {'data': data}
    
    @expose('ucframe.templates.quality')
    def quality(self):
        
        nodes, edges = utils.get_no_redundant_graph()
        
        export_data = {'nodes':[], "links":[]}
        type2group = {'Actor':1, 'Message':2, 'System':3}
        
        # clustering is needed
        
        # prepare the nodes
        for anode in nodes:
            export_data['nodes'].append({'name':anode['text'], 'group':type2group[anode['type']]})
        # prepare the edges
        for aedge in edges:
            export_data['links'].append({'source':aedge['source-index'], 
                                         'target':aedge['target-index'],
                                         'value':aedge['count']})
        
        # return the json data to the page visualization
        import json
        jsonfile = open('ucframe/public/data/ams_matrix.json', 'w')
        jsonfile.write(json.dumps(export_data))
        jsonfile.close()
        
        return dict(page='quality')
    
    @expose('ucframe.templates.quality_rev')
    def quality_rev(self):
        
        nodes, edges = utils.get_no_redundant_graph()
        
        export_data = {'nodes':[], "links":[]}
        type2group = {'Actor':1, 'Message':2, 'System':3}
        
        # clustering is needed
        
        # prepare the nodes
        for anode in nodes:
            export_data['nodes'].append({'name':anode['text'], 'group':type2group[anode['type']]})
        
        # prepare the edges
        # note that the reverse edges are calculated, not natural from the graph
        # each calculated edge is made by comparing the similarity between two nodes
        
        ## prepare the node array
        ## each node array is made of node[linked_node1, linked_node2...]
        node_array = {}
        for anode in nodes:
            node_array[anode['text']] = {}
            for aedge in edges:
                #print '[in comp]', nodes.index(anode), aedge['source-index']
                if nodes.index(anode) is aedge['source-index']:
                    node_array[anode['text']][aedge['target-index']] = aedge['count']
        
        ## compare similarity
        for key_1 in node_array.keys():
            for key_2 in node_array.keys():
                node_1 = node_array[key_1]
                node_2 = node_array[key_2]
                # print '[in rev]', node_1, node_2
                overlaps = [min(node_1[x], node_2[x]) for x in node_1 if x in node_2]
                # print '[in rev]', key_1, key_2, overlaps
                ###### worked !!!!!!!!  but the correctness is questionable
                ###### DO THE CODE REVIEW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                export_data['links'].append({'source':node_array.keys().index(key_1),
                                             'target':node_array.keys().index(key_2),
                                             'value':sum(overlaps)})        
        
        '''
        for aedge in edges:
            export_data['links'].append({'source':aedge['source-index'], 
                                         'target':aedge['target-index'],
                                         'value':aedge['count']})
        '''
        
        # return the json data to the page visualization
        import json
        jsonfile = open('ucframe/public/data/ams_matrix_rev.json', 'w')
        jsonfile.write(json.dumps(export_data))
        jsonfile.close()
        
        return dict(page='quality_rev')
    
    @expose('ucframe.templates.quality_indiv')
    def quality_indiv(self):
        
        type_constraint = "Message"
        
        nodes, edges = utils.get_no_redundant_graph()
        
        export_data = {'nodes':[], "links":[]}
        type2group = {'Actor':1, 'Message':2, 'System':3}
        
        # clustering is needed
        
        # prepare the nodes. only the actor type is considered this time.
        for anode in nodes:
            if anode['type'] is type_constraint:
                export_data['nodes'].append({'name':anode['text'], 'group':type2group[anode['type']]})
        
        # prepare the edges
        # note that the reverse edges are calculated, not natural from the graph
        # each calculated edge is made by comparing the similarity between two nodes
        
        ## prepare the node array
        ## each node array is made of node[linked_node1, linked_node2...]
        node_array = {}
        for anode in nodes:
            if anode['type'] is not type_constraint:  # only the actor type is considered this time.
                continue
            node_array[anode['text']] = {}
            for aedge in edges:
                #print '[in comp]', nodes.index(anode), aedge['source-index']
                if nodes.index(anode) is aedge['source-index']:
                    node_array[anode['text']][aedge['target-index']] = aedge['count']
        
        ## compare similarity
        for key_1 in node_array.keys():
            for key_2 in node_array.keys():
                node_1 = node_array[key_1]
                node_2 = node_array[key_2]
                # print '[in rev]', node_1, node_2
                overlaps = [min(node_1[x], node_2[x]) for x in node_1 if x in node_2]
                # print '[in rev]', key_1, key_2, overlaps
                ###### worked !!!!!!!!  but the correctness is questionable
                ###### DO THE CODE REVIEW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                export_data['links'].append({'source':node_array.keys().index(key_1),
                                             'target':node_array.keys().index(key_2),
                                             'value':sum(overlaps)})        
        
        '''
        for aedge in edges:
            export_data['links'].append({'source':aedge['source-index'], 
                                         'target':aedge['target-index'],
                                         'value':aedge['count']})
        '''
        
        # return the json data to the page visualization
        import json
        jsonfile = open('ucframe/public/data/ams_matrix_indiv.json', 'w')
        jsonfile.write(json.dumps(export_data))
        jsonfile.close()
        
        return dict(page='quality_indiv')
    
    '''
    @expose('json')
    def ams_matrix(self):
        
        import json
        with open('ams_matrix.json') as data_file:
            data = json.load(data_file)
                
        return {'data': data}
    '''
    
    def is_ams_term(self, term):

        if term[0] in ['@', '$', '*']:
            return True
        return False

    # This method receives request for CUC_metrics measurement.
    # THe CUC metrics measures quality of the specific object term
    # - kw: the input term
    #
    @expose('json')
    def cuc_metrics(self, **kw):
        
        event_list = []
        for key in kw.keys():
            event_list.append(key.strip())

        current_terms = []
        for event in event_list:
            splitted_terms = event.split(' ')
            for aterm in splitted_terms:
                if self.is_ams_term(aterm) and aterm not in current_terms:
                    current_terms.append(aterm)

        print 'current_terms in cuc_metrics', current_terms

        # metrics evaluation
        nodes, edges = utils.get_no_redundant_graph()
        
        # calculate the number of senders
        # calculate the numder of receivers
        '''
        NOS = 0
        NOR = 0
        for aedge in edges:
            if current_term == nodes[aedge['target-index']]['text']:
                NOS += 1
            if current_term == nodes[aedge['source-index']]['text']:
                NOR += 1
        '''

        # CRT computation
        import metrics
        CRT_data = {} ## data to be returned
        ## calculate the CRT
        CRT_dict = metrics.CRT()
        CRT_data['terms'] = {}
        ## get the average CRT
        CRT_current_terms = []
        for aterm in current_terms:
            if aterm in CRT_dict.keys():
                CRT_current_terms.append(CRT_dict[aterm])
                CRT_data['terms'][aterm] = CRT_dict[aterm] ## put ony the context terms
        CRT_average = round(sum(CRT_current_terms)/len(CRT_current_terms), 2)
        CRT_data['average'] = CRT_average
        CRT_data['description'] = 'Contributor Ratio of a Term (CRT)' +'\\n\\n' + \
                                  '在目前輸入頁面中您所使用的 AMS 詞彙(Terms), ' + \
                                  '平均來說也被多少比例的其他使用案例貢獻者所使用.' + \
                                  '\\n\\n' + '舉例來說: PuzzleBreaker(57%) 代表有 57% 的貢獻者' + \
                                  '也使用了 PuzzleBreaker 在他們的使用案例中.'
        
        # LLC computation
        NLLC_data = {}
        ## calculate the LLC
        NLLC_result = metrics.NLLC(event_list)
        NLLC_data['value'] = NLLC_result
        NLLC_data['description'] = 'Normalized Local Logical Conherence (NLLC)' +'\\n\\n' + \
                                   '在目前輸入頁面中您所有敘述之間的邏輯連貫性高低.' + \
                                   '通常越高的 NLLC 代表所有敘述整體越容易被閱讀及理解.' + \
                                   '\\n\\n' + '我們提供了 Average NLLC 做為參考.' + \
                                   '這是其他已經被貢獻的使用案例之平均 NLLC 值.'
        ANLLC_result = metrics.ANLLC()
        NLLC_data['average'] = ANLLC_result


        return {'CRT': CRT_data, 'NLLC': NLLC_data}
    
    @expose('json')
    def precon_metrics(self, **kw):
        
        precon_list = []
        for key in kw.keys():
            precon_list.append(key.strip())

        current_terms = []
        for precon in precon_list:
            splitted_terms = precon.split(' ')
            for aterm in splitted_terms:
                if self.is_ams_term(aterm) and aterm not in current_terms:
                    current_terms.append(aterm)

        print 'current_terms in precon_metrics', current_terms

        # metrics evaluation
        nodes, edges = utils.get_no_redundant_graph()
        
        # CRT computation
        import metrics
        CRT_data = {} ## data to be returned
        ## calculate the CRT
        CRT_dict = metrics.CRT()
        CRT_data['terms'] = {}
        ## get the average CRT
        CRT_current_terms = []
        for aterm in current_terms:
            if aterm in CRT_dict.keys():
                CRT_current_terms.append(CRT_dict[aterm])
                CRT_data['terms'][aterm] = CRT_dict[aterm] ## put ony the context terms

        if len(CRT_current_terms) == 0:
            CRT_average = 0
        else:
            CRT_average = round(sum(CRT_current_terms)/len(CRT_current_terms), 2)

        CRT_data['average'] = CRT_average
        CRT_data['description'] = 'Contributor Ratio of a Term (CRT)' +'\\n\\n' + \
                                  '在目前輸入頁面中您所使用的 AMS 詞彙(Terms), ' + \
                                  '平均來說也被多少比例的其他使用案例貢獻者所使用.' + \
                                  '\\n\\n' + '舉例來說: PuzzleBreaker(57%) 代表有 57% 的貢獻者' + \
                                  '也使用了 PuzzleBreaker 在他們的使用案例中.'

        return {'CRT': CRT_data}
    
    @expose('json')
    def postcon_metrics(self, **kw):
        
        postcon_list = []
        for key in kw.keys():
            postcon_list.append(key.strip())

        current_terms = []
        for postcon in postcon_list:
            splitted_terms = postcon.split(' ')
            for aterm in splitted_terms:
                if self.is_ams_term(aterm) and aterm not in current_terms:
                    current_terms.append(aterm)

        print 'current_terms in postcon_metrics', current_terms

        # metrics evaluation
        nodes, edges = utils.get_no_redundant_graph()
        
        # CRT computation
        import metrics
        CRT_data = {} ## data to be returned
        ## calculate the CRT
        CRT_dict = metrics.CRT()
        CRT_data['terms'] = {}
        ## get the average CRT
        CRT_current_terms = []
        for aterm in current_terms:
            if aterm in CRT_dict.keys():
                CRT_current_terms.append(CRT_dict[aterm])
                CRT_data['terms'][aterm] = CRT_dict[aterm] ## put ony the context terms

        if len(CRT_current_terms) == 0:
            CRT_average = 0
        else:
            CRT_average = round(sum(CRT_current_terms)/len(CRT_current_terms), 2)
            
        CRT_data['average'] = CRT_average
        CRT_data['description'] = 'Contributor Ratio of a Term (CRT)' +'\\n\\n' + \
                                  '在目前輸入頁面中您所使用的 AMS 詞彙(Terms), ' + \
                                  '平均來說也被多少比例的其他使用案例貢獻者所使用.' + \
                                  '\\n\\n' + '舉例來說: PuzzleBreaker(57%) 代表有 57% 的貢獻者' + \
                                  '也使用了 PuzzleBreaker 在他們的使用案例中.'

        return {'CRT': CRT_data}

    # This method receives request for similar tags.
    # The similar tags are caculated by their adjencent terms
    # - kw: the input term
    #
    @expose('json')
    def similar_tags(self, **kw):

        similar_tags_group = {}
        tag_defs = {}
        
        context_terms = kw.keys()[0].split(' ')
        
        for aterm in context_terms:
            if aterm[0] not in ['@', '$', '*']: continue  # skip those not tagged
            sorted_tags = self.get_similar_tags(aterm, context_terms)
            if len(sorted_tags) > 6:
                sorted_tags = sorted_tags[1:6] # only get the first five, except the same one
            similar_tags_group[aterm] = sorted_tags
            # put the deinition of similar terms
            for sim_tag in sorted_tags:
                defition_dict = self.get_term_definition(sim_tag[0])
                print 'defition_dict:', defition_dict
                if defition_dict is None:
                    tag_defs[sim_tag[0]] = None
                else:
                    tag_defs[sim_tag[0]] = defition_dict['Description']
            # also put the deinition of context terms
            defition_dict = self.get_term_definition(aterm)
            if defition_dict is None:
                tag_defs[aterm] = None
            else:
                tag_defs[aterm] = defition_dict['Description']

        print 'tag_defs:', tag_defs
        
        return {'tags': similar_tags_group, 'glossaries': tag_defs}
    
    
    @expose('json')
    def similar_events(self, **kw):

        current_event = kw.keys()[0].strip()

        # determine similar events
        ## load all cuc
        from configobj import ConfigObj
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
        all_cuc_content = {}
        for afile in os.listdir(cuc_repo):
            cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
            all_cuc_content[afile] = cuc_content
        
        ## calculate the similarity score
        import utils
        all_events = {}  # preserves all event content and similarity
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            cuc = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]
            cuc_id = cuc['Task-Meta']['taskId']
            events = cuc['Event-Flow']
            for event_id in events.keys():
                all_events[(cuc_id, event_id)] = {'content': events[event_id],
                                                  'similarity': utils.event_similarity(current_event, 
                                                                                       events[event_id])}
        ## select the top K events
        similar_events_group = []
        sorted_events = sorted(all_events.iteritems(), key=lambda kvt: kvt[1]['similarity'], reverse=True)
        top_k_events = sorted_events[1:6]  # assume take the top 5 events, except the original one
        for an_event in top_k_events:  # transfer back to dict format
            similar_events_group.append(an_event[1])
            #similar_events_group[an_event[0][0]+'#'+an_event[0][1]] = an_event[1]

        return {'events': similar_events_group}
    
    @expose('json')
    def get_cuc(self, **kw):

        cuc_id = kw.keys()[0].strip()
        cuc_file = cuc_id + '.txt'
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
        cuc_content = ConfigObj(os.sep.join([cuc_repo, cuc_file]))[cuc_id]

        return {'cuc': cuc_content}

    #@expose('json')
    #def similar_cucs(self, **kw):
    def similar_cucs(self, event_list):
        
        '''
        event_list = []  # includes both precon, event, and postcon
        for key in kw.keys():
            event_list.append(key.strip())
        '''

        # determine similar events
        ## load all cuc
        from configobj import ConfigObj
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
        all_cuc_content = {}
        for afile in os.listdir(cuc_repo):
            cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
            all_cuc_content[afile] = cuc_content
        
        ## calculate the similarity score
        import utils
        all_cuc_similarity = {}  # preserves all event content and similarity
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            cuc = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]
            cuc_id = cuc['Task-Meta']['taskId']
            cuc_name = cuc['Task-Meta']['taskName']
            precons = cuc['Pre-Condition']
            events = cuc['Event-Flow']
            postcons = cuc['Post-Condition']
            compare_event_list = precons.values() + events.values() + postcons.values()
            all_cuc_similarity[cuc_id] = {'name': cuc_name,
                                          'id': cuc_id,
                                          'precons': precons,
                                          'events': events,
                                          'postcons': postcons,
                                          'similarity': utils.mass_event_similarity(event_list,
                                                                                    compare_event_list)}
        ## select the top K events
        similar_cucs_group = []
        sorted_cucs = sorted(all_cuc_similarity.iteritems(), key=lambda kvt: kvt[1]['similarity'], reverse=True)
        top_k_cucs = sorted_cucs[1:6]  # assume take the top 5 similar cucs, except the original one
        for a_cuc in top_k_cucs:  # transfer back to dict format
            similar_cucs_group.append(a_cuc[1])
            #similar_events_group[an_event[0][0]+'#'+an_event[0][1]] = an_event[1]
        print 'similar_cucs_group:', similar_cucs_group
        return {'cucs': similar_cucs_group}

    # [seLain] the code is basically the same with self.similar_events
    @expose('json')
    def similar_postcons(self, **kw):

        current_event = kw.keys()[0].strip()

        # determine similar events
        ## load all cuc
        from configobj import ConfigObj
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
        all_cuc_content = {}
        for afile in os.listdir(cuc_repo):
            cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
            all_cuc_content[afile] = cuc_content
        
        ## calculate the similarity score
        import utils
        all_events = {}  # preserves all event content and similarity
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            cuc = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]
            cuc_id = cuc['Task-Meta']['taskId']
            events = cuc['Post-Condition']
            for event_id in events.keys():
                all_events[(cuc_id, event_id)] = {'content': events[event_id],
                                                  'similarity': utils.event_similarity(current_event, 
                                                                                       events[event_id])}
        ## select the top K events
        similar_events_group = []
        sorted_events = sorted(all_events.iteritems(), key=lambda kvt: kvt[1]['similarity'], reverse=True)
        top_k_events = sorted_events[1:6]  # assume take the top 5 events, , except the original one
        for an_event in top_k_events:  # transfer back to dict format
            similar_events_group.append(an_event[1])
            #similar_events_group[an_event[0][0]+'#'+an_event[0][1]] = an_event[1]

        return {'postcons': similar_events_group}
    
    # [seLain] the code is basically the same with self.similar_events
    @expose('json')
    def similar_precons(self, **kw):

        current_event = kw.keys()[0].strip()

        # determine similar events
        ## load all cuc
        from configobj import ConfigObj
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
        all_cuc_content = {}
        for afile in os.listdir(cuc_repo):
            cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
            all_cuc_content[afile] = cuc_content
        
        ## calculate the similarity score
        import utils
        all_events = {}  # preserves all event content and similarity
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            cuc = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]
            cuc_id = cuc['Task-Meta']['taskId']
            events = cuc['Pre-Condition']
            for event_id in events.keys():
                all_events[(cuc_id, event_id)] = {'content': events[event_id],
                                                  'similarity': utils.event_similarity(current_event, 
                                                                                       events[event_id])}
        ## select the top K events
        similar_events_group = []
        sorted_events = sorted(all_events.iteritems(), key=lambda kvt: kvt[1]['similarity'], reverse=True)
        top_k_events = sorted_events[1:6]  # assume take the top 5 events, , except the original one
        for an_event in top_k_events:  # transfer back to dict format
            similar_events_group.append(an_event[1])
            #similar_events_group[an_event[0][0]+'#'+an_event[0][1]] = an_event[1]

        return {'precons': similar_events_group}

    def type_transform(self, text):

        if text == 'Actor': return '@'
        if text == 'Message': return '$'
        if text == 'System': return '*'
        if text == '@': return 'Actor'
        if text == '$': return 'Message'
        if text == '*': return 'System'

    def get_similar_tags(self, current_term, context_terms):
        
        # analyze the current word
        current_word = [current_term[1:], None]
        
        if current_term[0] == '@':
            current_word[1] = 'Actor'
        elif current_term[0] == '$':
            current_word[1] = 'Message'
        elif current_term[0] == '*':
            current_word[1] = 'System'
        else:
            # not a tag in AMS, return empty
            return []
        
        nodes, edges = utils.get_pure_graph()
        
        # calc the word similarity
        from difflib import SequenceMatcher
        
        word_similarity = {}
        for anode in nodes:
            # if the same type but not the same node
            if anode[1] == current_word[1] and anode[0] != current_word[0]:
                key = self.type_transform(anode[1]) + anode[0]
                word_similarity[key] = SequenceMatcher(None, current_word[0], anode[0]).ratio()
        
        # [TODO] calc the context similarity
        
        ## get the context of all words
        context = {}
        for anode in nodes:
            ### predecessor -> anode -> successor, usually actor->message->system
            key = self.type_transform(anode[1]) + anode[0]
            context[key] = {'predecessors':[],'successors':[]}
            for aedge in edges:
                ### if anode is source
                if aedge[0][0] is anode[0] and aedge[1][0] not in context[key]['successors']:
                    context[key]['successors'].append(aedge[1][0])
                elif aedge[1][0] is anode[0] and aedge[0][0] not in context[key]['predecessors']:
                    context[key]['predecessors'].append(aedge[0][0])
                
        ## get the context of current work
        cotext_current = {'predecessors':[], 'successors':[]}
        current_index = context_terms.index(current_term)
        for aterm in context_terms:
            if context_terms.index(aterm) < current_index:
                cotext_current['predecessors'].append(aterm[1:])
            elif context_terms.index(aterm) > current_index:
                cotext_current['successors'].append(aterm[1:])
        
        ## calculate similarity by matching context
        context_similarity = {}
        for key in context.keys():
            acontext = context[key]
            sim_predecessors = 0
            sim_successors = 0
            if len(acontext['predecessors']) is not 0:
                sim_predecessors = len([val for val in cotext_current['predecessors'] if val in acontext['predecessors']])/float(len(acontext['predecessors']))
            if len(acontext['successors']) is not 0:
                sim_successors = len([val for val in cotext_current['successors'] if val in acontext['successors']])/float(len(acontext['successors']))
            context_similarity[key] = 0.5 * sim_predecessors + 0.5 * sim_successors
        
        # [TODO] combine the similarity
        for key in word_similarity.keys():
            word_similarity[key] = round(0.5 * word_similarity[key] + 0.5 * context_similarity[key], 2)
        
        # [TODO] extract the top similarity
        from operator import itemgetter
        sorted_tags = sorted(word_similarity.items(), key=itemgetter(1), reverse=True)
        
        return sorted_tags
    
    def get_term_definition(self, aterm):

        tags_def_repo = os.sep.join(['ucframe', 'public', 'data', 'noun_def_repo'])
        
        if aterm.startswith('@'):
            content = aterm[1:]
            fname = os.sep.join([tags_def_repo, 'Actor_'+content+'.txt'])
            #print '[fname]', fname
            if os.path.isfile(fname):
                return ConfigObj(fname).dict()
            else:
                return None
        elif aterm.startswith('$'):
            content = aterm[1:]
            fname = os.sep.join([tags_def_repo, 'Message_'+content+'.txt'])
            #print '[fname]', fname
            if os.path.isfile(fname):
                return ConfigObj(fname).dict()
            else:
                return None
        elif aterm.startswith('*'):
            content = aterm[1:]
            fname = os.sep.join([tags_def_repo, 'System_'+content+'.txt'])
            #print '[fname]', fname
            if os.path.isfile(fname):
                return ConfigObj(fname).dict()
            else:
                return None
        else:
            return None
    
    # This method receives request for similar tags.
    # The similar tags are caculated by their adjencent terms
    # - kw: the input term
    #
    @expose('json')
    def local_input(self, **kw):
        
        print '[in local_input]', kw
        
        export_nodes_data = [] 
        export_edges_data = []
        
        # do local analysis
        local_nodes = []
        export_nodes_data_id = 1
        for key in kw.keys():
            terms = kw[key].split(' ')
            for aterm in terms:
                if aterm.startswith('@'):
                    if aterm not in local_nodes:
                        local_nodes.append(aterm)
                        node_text = aterm[1:]
                        export_nodes_data.append({'id': export_nodes_data_id, 
                                                  'reflexive': 'false',
                                                  'text': node_text,
                                                  'type': 'Actor'})
                        export_nodes_data_id += 1
                elif aterm.startswith('$'):
                    if aterm not in local_nodes:
                        local_nodes.append(aterm)
                        node_text = aterm[1:]
                        export_nodes_data.append({'id': export_nodes_data_id, 
                                                  'reflexive': 'false',
                                                  'text': node_text,
                                                  'type': 'Message'})
                        export_nodes_data_id += 1
                elif aterm.startswith('*'):
                    if aterm not in local_nodes:
                        local_nodes.append(aterm)
                        node_text = aterm[1:]
                        export_nodes_data.append({'id': export_nodes_data_id, 
                                                  'reflexive': 'false',
                                                  'text': node_text,
                                                  'type': 'System'})
                        export_nodes_data_id += 1
            
        # return the json data to the page visualization
        import json
        jsonfile = open('local_graph.json', 'w')
        jsonfile.write(json.dumps(export_nodes_data))
        jsonfile.close()
        jsonfile = open('local_edges.json', 'w')
        jsonfile.write(json.dumps(export_edges_data))
        jsonfile.close()
        
        
        return {'nodes': export_nodes_data, 'edges': export_edges_data}
    
    # This method receives request for similar tags.
    # The similar tags are caculated by their adjencent terms
    # - kw: the input term
    #
    @expose('json')
    def tags_def(self, **kw):
           
        tags_def_repo = os.sep.join(['ucframe', 'public', 'data', 'noun_def_repo'])
        matched_tags = []
        
        current_terms = kw.keys()[0].strip().split(' ')  # [TOFIX] handy code
        for aterm in current_terms:
            if aterm.startswith('@'):
                content = aterm[1:]
                fname = os.sep.join([tags_def_repo, 'Actor_'+content+'.txt'])
                print '[fname]', fname
                if os.path.isfile(fname):
                    matched_tags.append(ConfigObj(fname).dict())
            elif aterm.startswith('$'):
                content = aterm[1:]
                fname = os.sep.join([tags_def_repo, 'Message_'+content+'.txt'])
                if os.path.isfile(fname):
                    matched_tags.append(ConfigObj(fname).dict())
            elif aterm.startswith('*'):
                content = aterm[1:]
                fname = os.sep.join([tags_def_repo, 'System_'+content+'.txt'])
                if os.path.isfile(fname):
                    matched_tags.append(ConfigObj(fname).dict())

        return {'tags': matched_tags}
    
    
    @expose('ucframe.templates.quality_metrics')
    def quality_metrics(self):
        
        import metrics
        
        GLR = metrics.GLR()
        ACT = metrics.ACT()
        ACTC = metrics.ACTC()
        ALLC = metrics.ALLC()
        AGLC = metrics.AGLC()
        AAC = metrics.AAC()
        NCR = metrics.NCR()
        GCI = metrics.GCI()
        
        return { 'metrics':{'GLR':GLR, 'ACT':ACT, 'ACTC':ACTC, 'ALLC':ALLC, 'AGLC':AGLC, 'AAC':AAC, 'NCR':NCR, 'GCI':GCI } }

    @expose('ucframe.templates.terms_stat')
    def terms_stat(self):

        terms_data = {}

        fileLocation = os.sep.join(['ucframe', 'model', 'Tag', 'Tag Table.txt'])
        TagTable = ConfigObj(fileLocation, encoding='UTF8') 

        for tag_id in TagTable.keys():
            tag = TagTable[tag_id]
            tag_text = tag['Name']
            tag_type = tag['Category']
            terms_data[tag_id] = {'type': tag_type,
                                  'text': tag_text,
                                  'count': utils.term_occurence_count(tag_type, tag_text)}

        return {'terms_data': terms_data}

    @expose('ucframe.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('ucframe.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('ucframe.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)
    @expose('ucframe.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('ucframe.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('ucframe.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
