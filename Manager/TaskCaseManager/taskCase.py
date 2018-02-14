# -*- coding: gbk -*-
import os, time
import copy
from configobj import ConfigObj

class TaskCase():
         
    def __init__(self, RepoLocationList, taskId=None, taskName=None, project=None, author=None, preCondition=None, eventFlow=None, postCondition=None):
        if taskId != None and taskName == None:
            #taskCaseDic = ConfigObj(fileLocation, encoding='UTF8')
            taskCaseDic = self._get_all_taskCase(RepoLocationList)
            # Make sure taskId is in taskCaseDic
            if taskId in taskCaseDic:
                # Make sure taskCase haven't been modified
                # [seLain] commented for later refinement. the revision policy may be altered.
                '''
                while (taskCaseDic[taskId]['Task-Meta']['RevisedId'] != "None" 
                       and taskCaseDic[taskId]['Task-Meta']['RevisedId'] in taskCaseDic):
                    taskId = taskCaseDic[taskId]['Task-Meta']['RevisedId']
                '''
                self.taskCase = taskCaseDic[taskId]
            else:
                self.taskCase = None
        elif taskId != None:
            newTaskCaseId = self._new_taskCase(RepoLocationList, taskName, project, author, preCondition, eventFlow, postCondition)
            self._revise_taskCase(RepoLocationList, taskId, newTaskCaseId)
        else:
            self._new_taskCase(RepoLocationList, taskName, project, author, preCondition, eventFlow, postCondition)
        
    
    def get_name(self):
        return self.taskCase['Task-Meta']['taskName']
    def get_author(self):
        return self.taskCase['Task-Meta']['Member']
    def get_project(self):
        return self.taskCase['Task-Meta']['Project']
    def get_taskId(self):
        return self.taskCase['Task-Meta']['taskId']
    def get_visible(self):
        return self.taskCase['Task-Meta']['Visible']
    def get_preCondition(self):
        return self.taskCase['Pre-Condition']
    def get_eventFlow(self):
        return self.taskCase['Event-Flow']
    def get_postCondition(self):
        return self.taskCase['Post-Condition']
    
    def _revise_taskCase(self, RepoLocationList, oriTask, newTask):        
        taskCaseDic = ConfigObj(RepoLocationList, encoding='UTF8')
        if (oriTask in taskCaseDic) and (taskCaseDic[oriTask]['Task-Meta']['RevisedId'] == "None") and (newTask in taskCaseDic):
             taskCaseDic[oriTask]['Task-Meta']['Visible'] = newTask
             taskCaseDic[oriTask]['Task-Meta']['RevisedId'] = newTask
             taskCaseDic.write()
        else: 
            print "Task Case have been revised"
    
    def _new_taskCase(self, RepoLocationList, taskName, project, author, preCondition, eventFlow, postCondition):
        taskCaseDic = self._get_all_taskCase(RepoLocationList)

        ## [seLain] determine the task case id
        last_id_number = None
        for key in taskCaseDic.keys():
            taskcase = taskCaseDic[key]
            #print '>>>>>>>', taskcase['Task-Meta']['taskId'].split('_')[-1].replace('0', '')
            try:
                number = int(taskcase['Task-Meta']['taskId'].split('_')[-1])
            except:
                print 'exception: task id not found:', number
                continue
            if last_id_number < number:
                last_id_number = number
        last_id_number += 1

        number = "Task_Case_%05d" % last_id_number
        
        fileName = number + ".txt"
        RepoLocation = os.sep.join(RepoLocationList)
        fileLocationList = []
        for dir in RepoLocationList:
            fileLocationList.append(dir)
        fileLocationList.append(fileName)
        
        fileLocation = os.sep.join(fileLocationList)
        
        taskCaseFile = ConfigObj(fileLocation, encoding='UTF8')
        
        taskCaseFile[number] = {}
        taskCaseFile[number]['Task-Meta'] = {}
        taskCaseFile[number]['Pre-Condition'] = {}
        taskCaseFile[number]['Event-Flow'] = {}
        taskCaseFile[number]['Post-Condition'] = {}
        
        taskCaseFile[number]['Task-Meta']['taskName'] = taskName
        taskCaseFile[number]['Task-Meta']['taskId'] = number
        taskCaseFile[number]['Task-Meta']['Project'] = project
        taskCaseFile[number]['Task-Meta']['Member'] = author
        taskCaseFile[number]['Task-Meta']['Visible'] = 'True'
        taskCaseFile[number]['Task-Meta']['RevisedId'] = "None"
        taskCaseFile[number]['Task-Meta']['SubmitTime'] = self._get_time()
        
        i=0
        for condition in preCondition:
            key = 'PreCondition-Condition-' + str(i)
            taskCaseFile[number]['Pre-Condition'][key] = condition
            i = i + 1
        i=0
        for condition in eventFlow:
            key = 'EventFlow-' + str(i)
            taskCaseFile[number]['Event-Flow'][key] = condition
            i = i + 1
        i=0
        for condition in postCondition:
            key = 'PostCondition-Condition-' + str(i)
            taskCaseFile[number]['Post-Condition'][key] = condition
            i = i + 1

        taskCaseFile.write()
        
        self.taskCase = taskCaseFile[number]
        return number
        
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
        
    
    def _get_time(self):
        temp = time.localtime()
        y = str(temp[0])
        m = '%02d' %temp[1]
        d = '%02d' %temp[2]
        h = '%02d' %temp[3]
        mi = '%02d' %temp[4]
        s = '%02d' %temp[5]
        return y + '-' + m + '-' + d + ' ' + h + ':' + mi + ':' + s

        
if __name__ == '__main__':
        fileLocation = os.sep.join(['Tag Table.txt'])
        NewOntologyTable = ConfigObj(fileLocation, encoding='UTF8')
        fileLocation = os.sep.join(['New Tag Table.txt'])
        OntologyTable = ConfigObj(fileLocation, encoding='UTF8')
        for ontology in OntologyTable:
            NameSplit = OntologyTable[ontology]['Name'].split(" ")
            ontologyName = ""
            for item in NameSplit:
                name = item[0].upper() + item[1:].lower()
                ontologyName = ontologyName + name
            ontologyRealWord = OntologyTable[ontology]['RealWord'].replace(" ","")
            if ontologyName not in NewOntologyTable:
                NewOntologyTable[ontologyName] = {}
                NewOntologyTable[ontologyName]['Name'] = ontologyName
                NewOntologyTable[ontologyName]['RealWord'] = ontologyRealWord
                NewOntologyTable[ontologyName]['Category'] = OntologyTable[ontology]['Category']
                NewOntologyTable[ontologyName]['Type'] = OntologyTable[ontology]['Type']
                NewOntologyTable[ontologyName]['Abstraction'] = OntologyTable[ontology]['Abstraction']
        NewOntologyTable.write()