#
# This module contains metrics for the CUC
#
import os

# GLR = GlossaryRatio
# defined by NumberOfGlossary / NumberOfTerms
#
def GLR(glossary_repo=None):
    
    ratio = 0
    
    # get the NumberOfGlossary
    num_of_glossary = 0
    if glossary_repo is None:
        glossary_repo = os.sep.join(['ucframe','public','data', 'noun_def_repo'])
    for afile in os.listdir(glossary_repo):
        if afile.split('_')[0] in ['Actor', 'Message', 'System']:
            num_of_glossary += 1
    
    # get the NumberOfTerms
    from ucframe.model import utils
    nodes, edges = utils.get_pure_graph()
    num_of_terms = len(nodes)
    
    if num_of_terms is 0:
        return 0
    else:
        ratio = round((float)(num_of_glossary)/num_of_terms, 2)
    
    return ratio

# CRT = Contributor Ratio of a Term
def CRT(cuc_repo=None):

    term_member_dict = {}
    all_members = []

    # get the terms
    from ucframe.model import utils
    nodes, edges = utils.get_pure_graph()
    all_terms = []
    for anode in nodes:
        if anode[1] is "Actor":
            all_terms.append('@'+anode[0])
        elif anode[1] is "Message":
            all_terms.append('$'+anode[0])
        elif anode[1] is "System":
            all_terms.append('*'+anode[0])
    
    # load all cuc
    from configobj import ConfigObj
    if cuc_repo is None:
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    all_cuc_content = {}
    for afile in os.listdir(cuc_repo):
        cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
        all_cuc_content[afile] = cuc_content
        
    # determine the term_member_dict
    for aterm in all_terms:
        term_member_dict[aterm] = []
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            member = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Task-Meta']['Member']
            if aterm in all_cuc_content[afile] and member not in term_member_dict[aterm]:
                term_member_dict[aterm].append(member)
            if member not in all_members:  # accumulate the member list, for later calculation
                all_members.append(member)
    
    # calculate average
    CRT_dict = {}
    for aterm in term_member_dict.keys():
        if len(all_members) == 0:
            CRT_dict[aterm] = 0
            continue
        CRT_dict[aterm] = round((float)(len(term_member_dict[aterm]))/(len(all_members)), 2)
    
    return CRT_dict


# ACT = Average Contributors of Terms
# defined by average(sum(len(term.contributors) for each term))
#
def ACT(cuc_repo=None):
    
    term_member_dict = {}
    
    # get the terms
    from ucframe.model import utils
    nodes, edges = utils.get_pure_graph()
    all_terms = []
    for anode in nodes:
        if anode[1] is "Actor":
            all_terms.append('@'+anode[0])
        elif anode[1] is "Message":
            all_terms.append('$'+anode[0])
        elif anode[1] is "System":
            all_terms.append('*'+anode[0])
    
    # load all cuc
    from configobj import ConfigObj
    if cuc_repo is None:
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    all_cuc_content = {}
    for afile in os.listdir(cuc_repo):
        cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
        all_cuc_content[afile] = cuc_content
        
    # determine the term_member_dict
    for aterm in all_terms:
        term_member_dict[aterm] = []
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            member = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Task-Meta']['Member']
            if aterm in all_cuc_content[afile] and member not in term_member_dict[aterm]:
                term_member_dict[aterm].append(member)
                
    # calculate average
    total = 0
    for aterm in term_member_dict.keys():
        total += len(term_member_dict[aterm])
    avg_contributors = round((float)(total)/len(term_member_dict.keys()), 2)
    
    return avg_contributors

# ACTC = Average Contributors of Terms over All Contributors
# defined by average(sum(len(term.contributors) for each term)) / all_contributors.size
#
def ACTC(cuc_repo=None):
    
    term_member_dict = {}
    
    # get the terms
    from ucframe.model import utils
    nodes, edges = utils.get_pure_graph()
    all_terms = []
    for anode in nodes:
        if anode[1] is "Actor":
            all_terms.append('@'+anode[0])
        elif anode[1] is "Message":
            all_terms.append('$'+anode[0])
        elif anode[1] is "System":
            all_terms.append('*'+anode[0])
    
    # load all cuc
    from configobj import ConfigObj
    if cuc_repo is None:
        cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    all_cuc_content = {}
    for afile in os.listdir(cuc_repo):
        cuc_content = open(os.sep.join([cuc_repo, afile]), 'r').read().replace('\n', ' ')
        all_cuc_content[afile] = cuc_content
        
    # determine the term_member_dict
    for aterm in all_terms:
        term_member_dict[aterm] = []
        for afile in all_cuc_content.keys():
            ## [TOFIX] This is super handy code due to the bad structure of the CUC task case
            member = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Task-Meta']['Member']
            if aterm in all_cuc_content[afile] and member not in term_member_dict[aterm]:
                term_member_dict[aterm].append(member)
    
    # prepare all_contributors:
    all_contributors = []
    for afile in all_cuc_content.keys():
        member = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Task-Meta']['Member']
        if member not in all_contributors:
            all_contributors.append(member)
    
    # calculate average
    total = 0
    for aterm in term_member_dict.keys():
        total += len(term_member_dict[aterm])
    avg_contributors = round((float)(total)/len(term_member_dict.keys()), 2)
    ACTC = round(avg_contributors/len(all_contributors), 2)
    
    return ACTC



# LLC = Local Logical Coherence
# defined by the total local association of terms / number of terms
# 
def LLC(event_list):
    
    LLC = 0
    
    # abatract the event list to term list
    abstract_event_list = []
    for event in event_list:
        abstract_event = []
        terms = event.replace('\n', '').split(' ')
        for aterm in terms:
            if aterm.startswith('@') or aterm.startswith('$') or aterm.startswith('*'):
                abstract_event.append(aterm)
        abstract_event_list.append(abstract_event)
    
    # calculate LLC
    lc = 0
    gc = 0
    ## check if there is only 1 event
    if len(abstract_event_list) <= 1:
        return 0  ### LLC = 0
    ## the first event has no lc or gc
    for index in range(1, len(abstract_event_list)):
        last_event = abstract_event_list[index-1]
        cur_event = abstract_event_list[index]
        ### the events before the last one for gc
        pre_events = abstract_event_list[0:index-1]
        for aterm in cur_event:
            for bterm in last_event:
                if aterm == bterm:
                    lc += 1
            for event in pre_events:
                for cterm in event:
                    if aterm == cterm:
                        gc += 1
    
    LLC = lc + gc
    
    return LLC

def NLLC(event_list):

    LLC_result = LLC(event_list)
    normalized_LLC = 0
    if len(event_list)-1 > 0:
        normalized_LLC = round((float)(LLC_result)/(len(event_list)-1), 2)

    return normalized_LLC

# ALLC = Average Local Logical Coherence
# defined by the the total local association of terms / number of terms
# 
def ALLC():
    
    from configobj import ConfigObj
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    all_LLC = {}
    for afile in os.listdir(cuc_repo):
        event_flow = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Event-Flow']
        event_list = event_flow.values()
        all_LLC[afile.split('.')[0]] = LLC(event_list)
    
    total = 0
    for key in all_LLC.keys():
        total += all_LLC[key]
    ALLC = round((float)(total)/len(all_LLC.keys()), 2)
    
    return ALLC

def ANLLC():

    from configobj import ConfigObj
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    all_NLLC = {}
    for afile in os.listdir(cuc_repo):
        event_flow = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Event-Flow']
        event_list = event_flow.values()
        all_NLLC[afile.split('.')[0]] = NLLC(event_list)
    
    total = 0
    for key in all_NLLC.keys():
        total += all_NLLC[key]
    ANLLC = round((float)(total)/len(all_NLLC.keys()), 2)
    
    return ANLLC


# GLC = Global Logical Coherence
# defined by the total global association of terms across CUC
# 
def GLC(cuc_id, all_abstract_CUCs):
    
    abstract_CUCs = all_abstract_CUCs
    # calculate the GLC of each CUC
    host_cuc = abstract_CUCs[cuc_id]
    GLC = 0
    
    for id_key in abstract_CUCs.keys():
        mapping_cuc = abstract_CUCs[id_key]
        for aterm in host_cuc:
            if aterm in mapping_cuc:
                GLC += 1
    
    return GLC
    
# AGLC = Average Global Logical Coherence
# defined by the average global association of terms of each CUC
# 
def AGLC():

    # abatract the event list to term list for each CUC
    # [TOFIX] This section of code should be moved to the utils
    abstract_CUCs = {}
    from configobj import ConfigObj
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    for afile in os.listdir(cuc_repo):
        abstract_uc = []
        event_flow = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Event-Flow']
        event_list = event_flow.values()
        for event in event_list:
            terms = event.replace('\n', '').split(' ')
            for aterm in terms:
                if aterm.startswith('@') or aterm.startswith('$') or aterm.startswith('*') and aterm not in abstract_uc:
                    abstract_uc.append(aterm)
        abstract_CUCs[afile.split('.')[0]] = abstract_uc
    
    
    all_GLC = {}
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    for afile in os.listdir(cuc_repo):
        cuc_id = afile.split('.')[0]
        all_GLC[cuc_id] = GLC(cuc_id, abstract_CUCs)
        
    total = 0
    for score in all_GLC.values():
        total += score
    
    print '[highest GLC]', max(all_GLC.values())
    print '[lowest GLC]', min(all_GLC.values())
    
    AGLC = round((float)(total)/len(all_GLC.keys()), 2)
    
    return AGLC
    
# AAC = Average Approval of CUCs
# defined by the average approval of each CUC
# 
def AAC():
    
    from configobj import ConfigObj
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    approval_CUCs = {}
    for afile in os.listdir(cuc_repo):
        members = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Task-Meta']['Member']
        approvals = members[1:]
        approval_CUCs[afile.split('.')[0]] = len(approvals)
        
    AAC = round((float)(sum(approval_CUCs.values()))/len(approval_CUCs.keys()), 2)
    
    return AAC

# NCR = New CUC Ratio
# defined by number of new CUC / total number of CUC
def NCR(date=None):
    
    import time
    
    format = '%Y-%m-%d %H:%M:%S'
    if date is None:  # fixed date as threshold
        date = "2015-5-20 12:00:00"
    dtime = time.mktime(time.strptime(date, format))
    
    from configobj import ConfigObj
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    recent_CUCs = []
    for afile in os.listdir(cuc_repo):
        submit_time = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Task-Meta']['SubmitTime']
        stime = time.mktime(time.strptime(submit_time, format))
        if stime > dtime:
            recent_CUCs.append(afile.split('.')[0])
    
    NCR = round((float)(len(recent_CUCs))/len(os.listdir(cuc_repo)), 2)
    
    return NCR

# LCI: Local CUC Interconnectivity
# defined by the average pre & post connectivity of target CUC to all other CUC
def LCI(cuc_id, all_abstract_CUCs):
    
    abstract_CUCs = all_abstract_CUCs
    
    ## deal with pre first
    host_cuc = abstract_CUCs[cuc_id]['Pre']
    pre_ratio_list = []
    for id_key in abstract_CUCs.keys():
        mapping_cuc = abstract_CUCs[id_key]['Pre']
        total = 0  # the total common terms in pre-con of two CUC
        for aterm in host_cuc:
            if aterm in mapping_cuc:
                total += 1
        # calculate the ratio. note that the 2* is for normalization because of double ways
        if (len(host_cuc)+len(mapping_cuc)) == 0:
            pre_ratio_list.append(0)
        else:
            pre_ratio_list.append((float)(2*total)/(len(host_cuc)+len(mapping_cuc)))
    
    ## then deal with post
    host_cuc = abstract_CUCs[cuc_id]['Post']
    post_ratio_list = []
    for id_key in abstract_CUCs.keys():
        mapping_cuc = abstract_CUCs[id_key]['Post']
        total = 0  # the total common terms in pre-con of two CUC
        for aterm in host_cuc:
            if aterm in mapping_cuc:
                total += 1
        # calculate the ratio. note that the 2* is for normalization because of double ways
        if (len(host_cuc)+len(mapping_cuc)) == 0:
            post_ratio_list.append(0)
        else:
            post_ratio_list.append((float)(2*total)/(len(host_cuc)+len(mapping_cuc)))
    
    ## combine the score
    LCI = round((0.5*sum(pre_ratio_list)/len(pre_ratio_list) + 0.5*sum(post_ratio_list)/len(post_ratio_list)), 2)
    
    return LCI

# GCI Global CUC Interconnectivity
# definec by the average LCI of all CUCs

def GCI():
    
    # abatract the pre & post list to term list for each CUC
    # [TOFIX] This section of code should be moved to the utils
    abstract_CUCs = {}
    from configobj import ConfigObj
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    for afile in os.listdir(cuc_repo):
        ## deal with pre-con
        abstract_uc_pre = []
        precons = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Pre-Condition']
        precon_list = precons.values()
        for event in precon_list:
            terms = event.replace('\n', '').split(' ')
            for aterm in terms:
                if aterm.startswith('@') or aterm.startswith('$') or aterm.startswith('*') and aterm not in abstract_uc_pre:
                    abstract_uc_pre.append(aterm)
        ## deal with post-con
        abstract_uc_post = []            
        postcons = ConfigObj(os.sep.join([cuc_repo, afile]))[afile.split('.')[0]]['Post-Condition']            
        postcon_list = postcons.values()
        for event in postcon_list:
            terms = event.replace('\n', '').split(' ')
            for aterm in terms:
                if aterm.startswith('@') or aterm.startswith('$') or aterm.startswith('*') and aterm not in abstract_uc_post:
                    abstract_uc_post.append(aterm)
        
        abstract_CUCs[afile.split('.')[0]] = {'Pre':abstract_uc_pre, 'Post':abstract_uc_post}
    
    # calculate all LCI
    all_LCI = {}
    cuc_repo = os.sep.join(['ucframe', 'model', 'TaskCaseRepository'])
    for afile in os.listdir(cuc_repo):
        cuc_id = afile.split('.')[0]
        all_LCI[cuc_id] = LCI(cuc_id, abstract_CUCs)
        
    total = 0
    for score in all_LCI.values():
        total += score
    
    print '[highest LCI]', max(all_LCI.values())
    print '[lowest LCI]', min(all_LCI.values())
    
    GCI = round((float)(total)/len(all_LCI.keys()), 2)
                                              
    return GCI


if __name__ == "__main__":
    
    print 'GLR:', GLR(os.sep.join(['ucframe','public','data', 'noun_def_repo']))