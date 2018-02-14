# this module include automatic use case generation toolkits
import os, random
from configobj import ConfigObj

class CrowdUseCaseGenerator:
    
    def __init__(self,):
        
        # configurations
        self.ucid_range = [50000, 50050]
        
        self.proj_name = 'PuzzleBreaker'
        self.actors = ['Elvis', 'Marry', 'Jonny', 'Emma', 'Pearl', 'Hank']
        self.messages = ['PuzzlePiece', 'Puzzle', 'PuzzleImage', 'PuzzlePhoto', 'FullPicture', 'DetectCommand']
        self.systems = ['PhoneCamera', 'Phone', 'System', 'App', 'PuzzleBreaker']
        
        self.flow_range = [1, 6]
        
        
    # this method performs the auto-generation, and preserve the files
    # - repo: the directory of the CUC files to be preserved
    #
    def generate(self, repo):
        
        for i in range(self.ucid_range[0], self.ucid_range[1]):
            # outline the CUC
            cuc_name = 'Task_Case_'+str(i)
            cuc_file = ConfigObj()
            cuc_file[cuc_name] = {'Task-Meta':{},
                                  'Pre-Condition':{},
                                  'Event-Flow':{},
                                  'Post-Condition':{}}
            # append meta data
            cuc_file[cuc_name]['Task-Meta'] = {'taskName':'',
                                               'taskId':cuc_name,
                                               'Project':self.proj_name,
                                               'Member':self._get_members(),  # the first one is creator
                                               'Visible':'False',
                                               'RevisedId':'None',
                                               'SubmitTime':self._get_submit_time()}
            # append pre condition
            for flow_index in range(self.flow_range[0], random.randint(self.flow_range[0], self.flow_range[1])):
                flow_name = 'PreCondition-Condition-' + str(flow_index)
                flow_content = ' '.join(['*'+self.systems[random.randint(0, len(self.systems)-1)],
                                         'has',
                                         '$'+self.messages[random.randint(0, len(self.messages)-1)]])
                cuc_file[cuc_name]['Pre-Condition'][flow_name] = flow_content
            # append post condition
            for flow_index in range(self.flow_range[0], random.randint(self.flow_range[0], self.flow_range[1])):
                flow_name = 'PostCondition-Condition-' + str(flow_index)
                flow_content = ' '.join(['*'+self.systems[random.randint(0, len(self.systems)-1)],
                                         'has changed',
                                         '$'+self.messages[random.randint(0, len(self.messages)-1)]])
                cuc_file[cuc_name]['Post-Condition'][flow_name] = flow_content
            # append event flow
            for flow_index in range(self.flow_range[0], self.flow_range[1]):
                flow_name = 'EventFlow-' + str(flow_index)
                flow_content = ' '.join(['@'+self.actors[random.randint(0, len(self.actors)-1)],
                                         'sends',
                                         '$'+self.messages[random.randint(0, len(self.messages)-1)],
                                         'to',
                                         '*'+self.systems[random.randint(0, len(self.systems)-1)],])
                cuc_file[cuc_name]['Event-Flow'][flow_name] = flow_content
            # output
            cuc_file.write(open(os.sep.join([repo, cuc_name+'.txt']), 'w+'))
    
    # This internal method returns a creator + random number of approval contributors
    #
    def _get_members(self):
        
        members = []
        creator = self.actors[random.randint(0, len(self.actors)-1)]
        members.append(creator)
        max_approval = (int)(0.5 * random.randint(0, len(self.actors)-1))
        
        # add max_approval times
        for i in range(0, max_approval):
            ## randomly choose one
            approval = self.actors[random.randint(0, len(self.actors)-1)]
            ## add only if not already in, which means the actual approval may be less than max_approval
            if approval not in members:
                members.append(approval)
        
        return members
    
    # This internal method returns a time between period
    #
    def _get_submit_time(self):
    
        import random, time
        
        start = "2015-5-1 13:30:31"
        end = "2015-5-25 04:50:55"
        format = '%Y-%m-%d %H:%M:%S'
        
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))
        
        prop = random.random() # get random mutiplier between 0~1
        ptime = stime + prop * (etime - stime)
        
        submit_time = time.strftime(format, time.localtime(ptime))
        
        return submit_time
    
    
if __name__ == "__main__":
    
    cucgen = CrowdUseCaseGenerator()
    cucgen.generate(os.sep.join(['..','ucframe', 'model', 'TaskCaseRepository']))

