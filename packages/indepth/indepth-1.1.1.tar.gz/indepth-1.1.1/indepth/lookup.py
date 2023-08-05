
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Invoke Libraries
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import pickle
import os.path

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Functions
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#look up helpingVrbs
def helpingVrbs():
    helpingVrbsList = ['am','is','are','were', 'being', 'been', 'be', 'Have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could']
    return(helpingVrbsList)

#look up comparisonWrds
def comparisonWrds():
    comparisonWrdsList = ['also','equally','similarly','likewise','compare' ]
    return(comparisonWrdsList)

#look up additionWrds
def additionWrds():
    additionWrdsList = ['and','also','furthermore','too','what is more']
    return(additionWrdsList)

#look up exemplificationWrds
def exemplificationWrds():
    exemplificationWrdsList = ['example','instance','illustrate','such', 'namely']
    return(exemplificationWrdsList)

#look up sequencing
def sequencing():
    sequencingList = ['first','second','next','then','after']
    return(sequencingList)

#look up result
def result():
    resultList = ['so','therefore','as a result','thus','because','hence']
    return(resultList)

#look up contrast
def contrast():
    contrastList = ['contrast', 'instead','contrary','conversely']
    return(contrastList)

#look up qualifying
def qualifying():
    qualifyingList = ['but','however','although','except','unless']
    return(qualifyingList)

#look up reformulation
def reformulation():
    reformulationList = ['in other words','put more simply','that is to say','rather','in simple terms']
    return(reformulationList)

#look up highlighting
def highlighting():
    highlightingList = ['in particular','especially','specifically','implicitly','explicitly']
    return(highlightingList)

#look up transition
def transition():
    transitionList = ['turning to','with regard to', 'with regards to','regarding','with reference to','as far as','concerned']
    return(transitionList)

#look up cohesiveWrds
def cohesiveWrds():
    cohesiveWrdsList = comparisonWrds() + additionWrds() + exemplificationWrds() + sequencing() + result() + contrast() + qualifying() + reformulation() + highlighting() + transition()
    return(cohesiveWrdsList)

#look up causalVerbs
def causalVerbs():
    causalVerbsList = ['let','allow','permit','make','force','require','have','get','help','enable','assist','ask','motivate','lead','inspire','permit','persuade','convince','bribe','beg','encourage','pay']
    return(causalVerbsList)

def mrc_psycholing():        
    pklPath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))+"\data\mrc_psycholing.pkl"      
    with open(pklPath, 'rb') as f:
        mrc_psycholing = pickle.load(f)
    return(mrc_psycholing)
