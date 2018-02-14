# the utilities module

from difflib import SequenceMatcher

def similar_strings(string1, string2):
    return round(SequenceMatcher(None, string1, string2).ratio(), 2)

def mass_event_similarity(eventlist1, eventlist2):

    mass_similarity = 0

    similarity_scores = []
    for event_x in eventlist1:
        for event_y in eventlist2:
            similarity_scores.append(event_similarity(event_x, event_y))

    mass_similarity = round(sum(similarity_scores)/len(similarity_scores), 2)

    return mass_similarity


def event_similarity(event1, event2):

    event_similarity = 0
    
    # compute the average term similarity
    term_similarity = round(SequenceMatcher(None, extract_ams_terms(event1), extract_ams_terms(event2)).ratio(), 2)

    # compute the string similarity
    string_similarity = similar_strings(event1, event2)

    # mix the similairy score
    event_similarity = round(0.3*term_similarity + 0.7*string_similarity, 2)

    #print 'term_sim:', term_similarity
    #print 'string_sim:', string_similarity
    #print 'event_sim:', event_similarity

    return event_similarity

def extract_ams_terms(string1):
    
    abstract_string = []
    terms = string1.replace('\n', '').split(' ')
    for aterm in terms:
        if aterm.startswith('@') or aterm.startswith('$') or aterm.startswith('*'):
            abstract_string.append(aterm)

    #print string1, ':', abstract_string

    return abstract_string

# for testing
if __name__ == "__main__":
    
    event1 = "@Player completes the $PuzzleGame"
    event2 = "@Player want to share it on facebook"
    event3 = "@Player completes the $PuzzleGame"
    event4 = "@Player input the data or constrain of new puzzle that he want"
    event5 = "@Player checks the new $Record"
    event_similarity(event1, event2)
    event_similarity(event1, event3)
    event_similarity(event1, event4)
    event_similarity(event1, event5)

