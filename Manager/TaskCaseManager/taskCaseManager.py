# -*- coding: gbk -*-
import os 
import copy
from configobj import ConfigObj
import json
#from taskCase import TaskCase
from Manager.TaskCaseManager.taskCase import TaskCase
from graph_manager.graph import AMSGraph

class TaskCaseManager():
    
    def __init__(self, RepoLocationList):
        self.taskCase = self._get_all_taskCase(RepoLocationList)
        self.RepoLocationList = RepoLocationList
    
    def all_task_models(self):
        
        taskmodels = {}
        
        alltasks = self._get_all_taskCase(self.RepoLocationList)
        for taskid in alltasks.keys():
            taskcase = TaskCase(self.RepoLocationList, taskid)
            eventflow = taskcase.get_eventFlow()
            taskgraph = AMSGraph()
            for key in eventflow.keys():
                taskgraph.addDescription(eventflow[key])
            taskmodels[taskid] = taskgraph
            
        return taskmodels
    
    def _get_all_taskCase(self, RepoLocationList):
        
        RepoLocationList = ['ucframe', 'model', 'TaskCaseRepository']
        RepoLocation = os.sep.join(RepoLocationList)
        dirs = os.listdir(RepoLocation)
        taskCaseDic = {}
        for file in dirs:
            if '.txt' not in file:
                continue
            fileLocation = os.sep.join(['ucframe', 'model', 'TaskCaseRepository', file])
            singleTaskCase= ConfigObj(fileLocation, encoding='UTF8')
            for taskID in singleTaskCase:
                taskCaseDic[taskID] = singleTaskCase[taskID]
                
        return taskCaseDic
        
    def saveTaskCase(self, kw):
        other_input = {}
        self_input = {}
        pre_condition_name = ["PreCondition-Condition-"]
        pre_condition=[]
        post_condition_name = ["PostCondition-Condition-"]
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
        
        pre_condition_list = []
        post_condition_list = []
        event_flow_list = []
        
        for i in pre_condition:
            if i in kw and kw[i] != '':
                pre_condition_list.append(kw[i])
        for i in event_flow:
            if i in kw and kw[i] != '':
                event_flow_list.append(kw[i])
        for i in post_condition:
            if i in kw and kw[i] != '':
                post_condition_list.append(kw[i])
                
        if 'taskId' in kw:
            taskId = kw['taskId']
        else:
            taskId = None
        
        Project = kw['Project']
        Member = kw['Member']
        taskName = kw['taskName']
        TaskCase(self.RepoLocationList, taskId, taskName, Project, Member, pre_condition_list, event_flow_list, post_condition_list)    
        
        
    def get_author(self):
        taskCase = self._get_all_taskCase(self.RepoLocationList)
        outputList = []
        for taskID in taskCase:
            singleTask = TaskCase(self.RepoLocationList, taskID)
            if (singleTask.get_visible() == 'True') and (singleTask.get_taskId() == taskID) and (singleTask.get_author() not in outputList): 
                outputList.append(singleTask.get_author())
        return outputList
        
    def getTaskList(self):
        taskCase = self._get_all_taskCase(self.RepoLocationList)
        outputList = []
        for taskID in taskCase:
            singleTask = TaskCase(self.RepoLocationList, taskID)
            if singleTask.get_visible() == 'True' and singleTask.get_taskId() == taskID : 
                outputItem = {}
                outputItem['taskName'] = singleTask.get_name()
                outputItem['taskID'] = singleTask.get_taskId()
                outputItem['Member'] = singleTask.get_author()
                outputList.append(outputItem)
        return outputList
        
    def getTaskListByMember(self, author):
        taskCase = self._get_all_taskCase(self.RepoLocationList)
        outputList = []
        for taskID in taskCase:
            singleTask = TaskCase(self.RepoLocationList, taskID)
            if (singleTask.get_visible() == 'True') and (singleTask.get_author() == author) and singleTask.get_taskId() == taskID: 
                outputItem = {}
                outputItem['taskName'] = singleTask.get_name()
                outputItem['taskID'] = singleTask.get_taskId()
                outputItem['Member'] = singleTask.get_author()
                outputList.append(outputItem)
        return outputList
    
    def getTaskListByProject(self, project):
        taskCase = self._get_all_taskCase(self.RepoLocationList)
        outputList = []
        for taskID in taskCase:
            singleTask = TaskCase(self.RepoLocationList, taskID)
            if (singleTask.get_visible() == 'True') and (singleTask.get_project() == project) and singleTask.get_taskId() == taskID: 
                outputItem = {}
                outputItem['taskName'] = singleTask.get_name()
                outputItem['taskID'] = singleTask.get_taskId()
                outputItem['Member'] = singleTask.get_author()
                outputList.append(outputItem)
        return outputList
        
    def getSingleTask(self, taskID):
        taskCase = self._get_all_taskCase(self.RepoLocationList)
        outputItem = taskCase[taskID]
        
        return outputItem
    
    def saveOntologyFromTaskCase(self, kw):    
        pre_condition_name = ["PreCondition-Condition-"]
        post_condition_name = ["PostCondition-Condition-"]
        event_flow_name = ["EventFlow-"]
        
        sentenceList = []
        for i in range(1,10):
            for parameters_name in pre_condition_name:
                key =  parameters_name + str(i)
                if key in kw:
                    sentenceList.append(kw[key])
            for parameters_name in post_condition_name:
                key =  parameters_name + str(i)
                if key in kw:
                    sentenceList.append(kw[key])
            for parameters_name in event_flow_name:
                key =  parameters_name + str(i)
                if key in kw:
                    sentenceList.append(kw[key])
        for sentence in sentenceList:
            self.saveTagInSentence(sentence, "Actor")
            self.saveTagInSentence(sentence, "Message")
            self.saveTagInSentence(sentence, "System")
    
    
    def saveTagInSentence(self, sentence, tagType):
        fileLocation = os.sep.join(['ucframe', 'model', 'Tag', 'Tag Table.txt'])
        OntologyTable = ConfigObj(fileLocation, encoding='UTF8')
        if tagType == 'Actor':
            splitItem = '@'
        elif tagType == 'Message':
            splitItem = '$'
        elif tagType == 'System':
            splitItem = '*'
        
        sentenceList = sentence.split(splitItem)
        if len(sentenceList) == 1:
            return None
        else:
            output = {}
            output['Actor'] = []
            output['Message'] = []
            output['System'] = []
            for i in range(len(sentenceList)):
                if i == 0:
                    continue
                tagWithSentence = sentenceList[i]
                tagSplit = tagWithSentence.split(" ")
                tagName = tagSplit[0]
                if tagName not in output[tagType]:
                    output[tagType].append(tagName)
                    
            for tag in output[tagType]:
                if tag not in OntologyTable:
                    OntologyTable[tag] = {}
                    OntologyTable[tag]['Name'] = tag
                    OntologyTable[tag]['RealWord'] = tag
                    OntologyTable[tag]['Category'] = tagType
                    OntologyTable[tag]['Type'] = 'Instance'
                    OntologyTable[tag]['Abstraction'] = []
                    
                    
            OntologyTable.write()
        return output
    
    
    def removeTaskCase(self, taskID):
        
        fileName = taskID + '.txt'
        fileLocationList = []
        for dir in self.RepoLocationList:
            fileLocationList.append(dir)
        fileLocationList.append(fileName)
        
        fileLocation = os.sep.join(fileLocationList)
        #taskCase = ConfigObj(fileLocation, encoding='UTF8')
        taskCase = ConfigObj(fileLocation)
        if taskID in taskCase:
            taskCase[taskID]['Task-Meta']['Visible'] = 'False'
        taskCase.write()