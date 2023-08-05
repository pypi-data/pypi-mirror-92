#This is the list of all the functions for this project. This could change as the package is currently unstable.

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Invoke Libraries
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import pandas as pd
from nltk import pos_tag, word_tokenize, sent_tokenize, pos_tag, FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw, cmudict, wordnet as wn, brown, words
import re
from nltk.stem import WordNetLemmatizer
from essay_eval.lookup import helpingVrbs, comparisonWrds, additionWrds, exemplificationWrds, sequencing, result, contrast, qualifying, reformulation, highlighting, transition, cohesiveWrds, causalVerbs, mrc_psycholing
import os
from nltk.parse.stanford import StanfordDependencyParser
import math
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Look up data
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
helpingVrbs = helpingVrbs()
cohesiveWrds = cohesiveWrds()
causalVerbs = causalVerbs()
result = result()
#Concreteness and Meaningfulness scores from MRC Psycholinguistic database.
mrc_psycholing = mrc_psycholing()


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Build  Functions
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#function to remove punctuation
def remov_punct(withpunct):
    punctuations = set(['!','(',')','-','[',']','{','}',';',':',',','<','>','.','/','?','@','#','$','%','^','&','*','_','~',"\\"])
    without_punct = ""
    char = 'nan'
    for char in withpunct:
        if char not in punctuations:
            without_punct = without_punct + char
    return(without_punct)

#Retrieve the POS tag
def ptb_to_wn(tag):    
    if tag.startswith('N'):
        return 'n' 
    if tag.startswith('V'):
        return 'v' 
    if tag.startswith('J'):
        return 'a' 
    if tag.startswith('R'):
        return 'r' 
    return None


def tagged_to_synset(word, tag):
    wn_tag = ptb_to_wn(tag)
    if wn_tag is None:
        return None 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
    
    
def sentence_similarity(s1, s2):        
    s1 = pos_tag(word_tokenize(s1))
    s2 = pos_tag(word_tokenize(s2)) 
    
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in s1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in s2]
 
    #suppress "none"
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
        
    scoreList = list()
    
    for i in range(0,len(synsets1)):           
        best_score = max([synsets1[i].path_similarity(ss) for ss in synsets2])                
        scoreList.append(best_score)    
    
    #drop None values if any from the list
    scoreListUpdated = [i for i in scoreList if i]
    
    #average the best_score values
    avgScore = (sum(scoreListUpdated)/len(scoreListUpdated))   

    return(avgScore)

#compute the symmetric sentence similarity
def symSentSim(s1, s2):     
    try:
        sssScoreSide1 = sentence_similarity(s1, s2)                                              
    except:        
        sssScoreSide1 = 0        
    
    try:
        sssScoreSide2 = sentence_similarity(s2, s1)                                              
    except:        
        sssScoreSide2 = 0       
    
    sss_score = (sssScoreSide1 + sssScoreSide2)/2        

    return (sss_score)

#function to suppress stop words and special characters
def dropStopWrds(s):
    withoutpunct = remov_punct(s)
    stopWords = set(sw.words('english'))
    withStopwords = word_tokenize(withoutpunct)
    withoutStopwords = [w for w in withStopwords if not w in stopWords]
    return(withoutStopwords)

#function to count total words(including stop words)
def wrdCnt(s):
    withoutpunct = remov_punct(s)
    wrds = withoutpunct.split(' ')
    wrd_cnt = len(wrds)
    return(wrd_cnt)

#function to count correctly spelt words
def realWrds(s):
    realWrds = []
    withoutpunct = remov_punct(s)
    wrds = withoutpunct.split(' ')
    realwordCnt = len(set(wrds).intersection(set(words.words())))
    return(realwordCnt)       

#function to measure size of vocabulary post stop words suppression.
def vocabSize(s):
    withoutpunct = remov_punct(s)
    withoutStopwords = dropStopWrds(withoutpunct)
    vocabLen = len(set(withoutStopwords))
    return(vocabLen)

#function to count # sentences and paragraphs. This doesnt work when the period is not followed by a space. fix that later
def cntSentences(d):    
    sentences = sent_tokenize(d)    
    sentLen = len(sentences)
    return(sentLen)

    #function to identify subject verb aggreement in number.
def sbjVrbAgreement(s):
    tag = pos_tag(word_tokenize(s))
    sbj_pos = ''
    vb_pos = ''
    agreement = 0
    NoAgreement = 0
    causal_verbs = 0
    causal_particles = 0
    for i in range(0,len(tag)):
       if re.search(r"N(N|S|P)",str(tag[i][1])):
           if (len(sbj_pos)==0):
             sbj_pos = str(tag[i][1])
       if re.search(r"VB(P|Z)",str(tag[i][1])):
           if (len(vb_pos)==0):
             vb_pos = str(tag[i][1])
       if (re.search(r"(CC|IN)",str(tag[i][1]))) or (str(tag[i][0]) in result):
           causal_particles += 1
       elif(str(tag[i][0]) in causalVerbs):
           causal_verbs += 1
    if(sbj_pos == '' or vb_pos == ''):
        agreement = agreement
    else:
        if((sbj_pos == 'NN' and vb_pos == 'VBZ') or (sbj_pos == 'NNS' and vb_pos == 'VBP') ):
            agreement = 1            
        elif((sbj_pos == 'NN' and vb_pos == 'VBP') or (sbj_pos == 'NNS' and vb_pos == 'VBZ') ):
            NoAgreement = 1
              
        else:
            agreement = agreement
       
    return(agreement,NoAgreement,causal_verbs,causal_particles)

#check if modal verb precendence holds good. Each part is optional, but modals always precede Have and Be, and Have always precedes Be.
def modalRuleError(s):
    wnlemma = WordNetLemmatizer()
    modalError = 0
    modalNoError = 0
    lemma2 = ''
    lemma_prev = ''
    lemma_prev2 = ''
    tag = pos_tag(word_tokenize(s))
    for i in range(0,len(tag)):
        if re.search(r"MD",str(tag[i][1])):           
            lemma_prev = wnlemma.lemmatize(str(tag[i-1][0]),pos='v')
            lemma_nxt = wnlemma.lemmatize(str(tag[i+1][0]),pos='v')
            if (lemma_prev == 'have' or lemma_prev == 'be'):
               modalError += 1
            elif (lemma_nxt == 'have' or lemma_nxt == 'be'):
               modalNoError += 1
        else:
           if re.search(r"VB(|.)",str(tag[i][1])):            
              lemma2 = wnlemma.lemmatize(str(tag[i][0]),pos='v')
              if (lemma2 == 'have'):
                 lemma_prev2 = wnlemma.lemmatize(str(tag[i-1][0]),pos='v')
                 lemma_nxt2 = wnlemma.lemmatize(str(tag[i+1][0]),pos='v')
                 if (lemma_prev2 == 'be'):
                     modalError += 1
                 elif(lemma_nxt2 == 'be'):
                     modalNoError += 1
    return(modalNoError,modalError)

#check if possessive pronoun is followed by "do". "he do not..", "he have not"
def PrpDonot(s):
    PrpDoNotNoError = 0
    PrpDoNotError = 0
    tag = pos_tag(word_tokenize(s))
    for j in range(0,len(tag)):
        if (re.search(r"PRP",str(tag[j][1]))):
            nxt_wrd = str(tag[j+1][0])
            if (nxt_wrd == 'do'):
                PrpDoNotError += 1
            elif(nxt_wrd == 'does'):
                PrpDoNotNoError += 1            
        else:
            PrpDoNotNoError = PrpDoNotNoError
            PrpDoNotError = PrpDoNotError
    return(PrpDoNotNoError, PrpDoNotError)

#check for helping verb and main verb tense agreement
def VrbTenseAgreementError(s):
    tenseError_flag = 'n'
    tense_hlp_vrb = 'n'
    tense_main_vrb = 'n'
    tag = pos_tag(word_tokenize(s))
    for i in range(0,len(tag)):
        if (set(helpingVrbs) & set(word_tokenize(tag[i][0]))):             
            tense_hlp_vrb = str(tag[i][1])            
            for j in range(i+1,len(tag)):
                if(re.search(r"VB(|.)",str(tag[j][1]))):
                    tense_main_vrb = str(tag[j][1])                    
                    if(tense_hlp_vrb == tense_main_vrb and tense_hlp_vrb == 'VBD' or tense_hlp_vrb == 'VBN'):
                        tenseError_flag = 'y'
                    if(tense_hlp_vrb == tense_main_vrb and tense_hlp_vrb == 'VBG' or tense_hlp_vrb == 'VBP'):
                        tenseError_flag = 'y'                
                    else:
                        tenseError_flag = tenseError_flag    
    return(tenseError_flag)

#check for "a" vs "an" before vowels.
def a_an_error(s):
    a_an_error = 0
    a_an_NoError = 0
    vowel_flag = 'n'
    wrds = word_tokenize(s)
    loaded_dict = cmudict.dict()
    for i in range(0,len(wrds)):
        try:
            frst_alpha = str(loaded_dict.get(wrds[i+1])[0][0])
        except:
            break
        if (wrds[i] == 'a' or wrds[i] == 'an'):
            frst_alpha = str(loaded_dict.get(wrds[i+1])[0][0])            
            if frst_alpha in ['a','e','i','o','u']:
                vowel_flag = 'y'
            if ((wrds[i] == 'a' and vowel_flag == 'y') or (wrds[i] == 'an' and vowel_flag == 'n')):
                a_an_error += 1
            elif ((wrds[i] == 'a' and vowel_flag == 'n') or (wrds[i] == 'an' and vowel_flag == 'y')):
                a_an_NoError += 1
        else:
            a_an_error = a_an_error
            a_an_NoError = a_an_NoError  
    return (a_an_NoError, a_an_error)            

#coherent words per sentence
def coherentWrds(s):
    coherenceCnt = 0
    for i in range(0,len(cohesiveWrds)):
       match = re.search(cohesiveWrds[i],s)
       if match is not None:
          coherenceCnt += 1
          break
    return(coherenceCnt)

#hypernymy and polysemy
def hyponymPolysem_cnt(s):
    hyponyms_cnt = 0
    polysem_cnt = 0
    hyponym_perWrd = 0
    polysem_perWrd = 0
    wrds = dropStopWrds(s)
    for w in wrds:      
        wrd_synsets = wn.synsets(w)
        polysem_cnt += len(wrd_synsets)
        try:
            wrd = wrd_synsets[0]
            hyponyms = len(wrd.hyponyms())        
            hyponyms_cnt += hyponyms 
        except:
            next 
        hyponym_perWrd = hyponyms_cnt/len(wrds)
        polysem_perWrd = polysem_cnt/len(wrds)
    return(hyponym_perWrd,polysem_perWrd)
    
    
#This is at document level. Compute the avg frequency of the words used. This indicates how many frequently used words did the author use. This will have a correlation with the vocabulary size as well.
def commonWrd(d):
    sumWrdFreq = 0
    all_text = brown.words()
    wrdfreq = FreqDist([w.lower() for w in all_text])
    wrdlist = list(set(dropStopWrds(d)))
    for wrd in wrdlist:        
        sumWrdFreq += wrdfreq[wrd.lower()]
    commonWrds_Score = sumWrdFreq/float(len(wrdlist))
    return(commonWrds_Score)

#concreteness and meaningfulness scores
def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']
def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']
def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']
def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return wn.NOUN 

def concretMeaningPOS(s):
    wnlemma = WordNetLemmatizer()
    tag = pos_tag(word_tokenize(s))
    wrds = dropStopWrds(s)
    lemma_final = []
    concrete_denom = 0
    concreteSum = 0
    meaning_denom = 0
    meaningSum = 0
    adverbCnt = 0
    verbCnt = 0
    adjectiveCnt = 0
    nounCnt = 0    
    for i in range(0,len(tag)):
        if tag[i][0] in wrds:
            lemma = wnlemma.lemmatize(str(tag[i][0]),pos= penn_to_wn((tag)[i][1]))            
            lemma_final.append(str(lemma))
        #embedding the pos freq
        if (penn_to_wn((tag)[i][1]) == 'r'):
            adverbCnt += 1
        elif (penn_to_wn((tag)[i][1]) == 'v'):
            verbCnt += 1
        elif (penn_to_wn((tag)[i][1]) == 'a'):
            adjectiveCnt += 1
        elif (penn_to_wn((tag)[i][1]) == 'n'):
            nounCnt += 1        
    
    psycholin_match = set(lemma_final) & set(mrc_psycholing['WORD'].str.lower())   
    
    for j in lemma_final:
        if set({j}) & psycholin_match:
            concrete_denom += 1
            index_wrd = mrc_psycholing.loc[mrc_psycholing['WORD'].str.lower()==j].index[0]
            concreteSum += mrc_psycholing['CNC'].iloc[index_wrd]            
            if (mrc_psycholing['mean_meaningfulness'].iloc[index_wrd] > 0):
                meaning_denom += 1
                meaningSum = mrc_psycholing['mean_meaningfulness'].iloc[index_wrd]
    return(concreteSum,concrete_denom, meaningSum,meaning_denom, adverbCnt, verbCnt, adjectiveCnt,nounCnt)

#Spatial cohesion score.
def _recurse_all_hyponyms(synset, all_hyponyms):
    synset_hyponyms = synset.hyponyms()
    if synset_hyponyms:
        all_hyponyms += synset_hyponyms
        for hyponym in synset_hyponyms:
            _recurse_all_hyponyms(hyponym, all_hyponyms)

def all_hyponyms(synset):
    """Get the set of the tree of hyponyms under the synset"""
    hyponyms = []
    _recurse_all_hyponyms(synset, hyponyms)
    return hyponyms

#motion verbs using the above functions.
MotionVerbsList = []
for syn in wn.synsets('move'):
    if re.search(r'move.v.',str(syn)):
        listOfHyponyms = all_hyponyms(syn)
        for hypo in listOfHyponyms:
            MotionVerbsList.append(hypo.name().split('.')[0])
MotionVerbs = set(MotionVerbsList)

def motionVerbs(s):
    motionVerbsCnt = 0
    wnlemma = WordNetLemmatizer()#move this to the start of the evaluat function for efficiency
    tag = pos_tag(word_tokenize(s))
    wrds = dropStopWrds(s)    
    for i in range(0,len(tag)):
        if tag[i][0] in wrds:
            lemma = wnlemma.lemmatize(str(tag[i][0]),pos= penn_to_wn((tag)[i][1]))
            if str(lemma) in MotionVerbs:
                motionVerbsCnt += 1
                break
    return(motionVerbsCnt)

def buildFeatures(d):        
    vocab_size = 0
    sbjVrbAgreement_err = 0
    sbjVrbAgreement_noerr = 0
    sbjVrbAgreement_errscore = 0    
    modalErrorCnt = 0
    modalNoErrorCnt = 0
    modalRule_errscore = 0
    PrpDoNotNoErrorCnt = 0
    PrpDoNotErrorCnt = 0
    PrpDonot_errscore = 0
    VrbTenseAgreement_errscore = 0
    a_an_NoErrorCnt = 0
    a_an_ErrorCnt = 0
    a_an_errscore = 0
    real_wrd = 0
    sss_score = 0
    cosine_score = 0
    coherenceCnt = 0
    coherence_score = 0
    hyponymCnt = 0
    hyponym_score = 0
    polysemCnt = 0
    polysem_score = 0
    commonWrd_score = 0
    concrete_sum = 0
    concrete_score = 0
    meaning_sum = 0
    meaning_score = 0
    causalVerb_score = 0
    causalParticle_score = 0
    causalVerbCnt = 0
    causalParticleCnt = 0
    motionVerbCnt = 0
    motionVerb_score = 0
    adverbCnt = 0
    verbCnt = 0 
    adjectiveCnt = 0
    nounCnt = 0
    adverb_score = 0
    verb_score = 0
    adjective_score = 0
    noun_score = 0    
    lcase = d.lower()
    sentences = lcase.split('.')
    no_of_sents = len(sentences)
    for i in range(0,len(sentences)):
        s = sentences[i]              
        vocab_size += vocabSize(s)             

        try:
            sub_verb_agre,sub_verb_notagre,causalVerb,causalParticle = sbjVrbAgreement(s)
            sbjVrbAgreement_noerr += sub_verb_agre
            sbjVrbAgreement_err += sub_verb_notagre
            causalVerbCnt += causalVerb
            causalParticleCnt += causalParticle
        except:
            sbjVrbAgreement_noerr = sbjVrbAgreement_noerr  
            sbjVrbAgreement_err = sbjVrbAgreement_err  

        try:
            modalNoError,modalError = modalRuleError(s)
            modalNoErrorCnt += modalNoError
            modalErrorCnt += modalError
        except:
            modalNoErrorCnt = modalNoErrorCnt
            modalErrorCnt = modalErrorCnt
        try:
            PrpDoNotNoError,PrpDoNotError = PrpDonot(s)
            PrpDoNotNoErrorCnt += PrpDoNotNoError
            PrpDoNotErrorCnt += PrpDoNotError
        except:
            PrpDoNotNoErrorCnt = PrpDoNotNoErrorCnt
            PrpDoNotErrorCnt = PrpDoNotErrorCnt
        
        try:
            verb_tense_agree = VrbTenseAgreementError(s)
            if(verb_tense_agree == 'y'):
              VrbTenseAgreement_errscore += 1
        except:
            VrbTenseAgreement_errscore = VrbTenseAgreement_errscore
        
        try:
            a_an_NoError, a_an_Error = a_an_error(s)    
            a_an_NoErrorCnt += a_an_NoError
            a_an_ErrorCnt += a_an_ErrorCnt
        except:
            a_an_NoErrorCnt  = a_an_NoErrorCnt
            a_an_ErrorCnt = a_an_ErrorCnt
        
        try:
            real_wrd += realWrds(s)                   
        except:
            real_wrd = real_wrd
        
        if (i == 0):
            sss_score = sss_score
            cosine_score = cosine_score
        else:
            try:
               sss_score += symSentSim(s, sentences[i-1])    
            except:
                sss_score = sss_score                               
        
        try:
            motionVerbCnt += motionVerbs(s)
        except:
            motionVerbCnt = motionVerbCnt
            
        coherenceCnt += coherentWrds(s)
        hyponym, polysem =  hyponymPolysem_cnt(s)
        hyponymCnt += hyponym
        polysemCnt += polysem
        concret, concreteDenom ,meaning, meaningDenom, adverb, verb, adjective, noun = concretMeaningPOS(s)        
        concrete_sum += concret
        meaning_sum += meaning
        adverbCnt += adverb
        verbCnt += verb
        adjectiveCnt += adjective
        nounCnt += noun
    
    #start creating derived features(rational)    
    if (sbjVrbAgreement_err == 0 or sbjVrbAgreement_noerr == 0):
        sbjVrbAgreement_errscore = 0
    else:
        sbjVrbAgreement_errscore = math.log(sbjVrbAgreement_err/float(sbjVrbAgreement_noerr))
    
    
    if (modalNoErrorCnt == 0 or modalErrorCnt == 0):
        modalRule_errscore = 0
    else:
        modalRule_errscore = math.log(modalErrorCnt/float(modalNoErrorCnt))
    
    if (PrpDoNotNoErrorCnt == 0 or PrpDoNotErrorCnt == 0):
        PrpDonot_errscore = 0
    else:
        PrpDonot_errscore = math.log(PrpDoNotErrorCnt/float(PrpDoNotNoErrorCnt))
    
    if (a_an_NoErrorCnt == 0 or a_an_ErrorCnt == 0):
        a_an_errscore = 0
    else:
        a_an_errscore = math.log(a_an_ErrorCnt/float(a_an_NoErrorCnt))
    
    if (coherenceCnt == 0):
        coherence_score = 0
    else:
        coherence_score = math.log(coherenceCnt/float(no_of_sents))    
    
    if (no_of_sents == 1 or sss_score == 0):
        sss_score_avg = 0
        causalVerb_score = causalVerbCnt
        causalParticle_score = causalParticleCnt
    else:        
        sss_score_avg = math.log(sss_score/float(no_of_sents-1))
        if (causalVerbCnt == 0):
            causalVerb_score = 0
        else:
            causalVerb_score = math.log(causalVerbCnt/float(no_of_sents-1))
        if(causalParticle_score == 0):
            causalParticle_score = 0
        else:
            causalParticle_score = math.log(causalParticleCnt/float(no_of_sents-1))
    
    if (hyponymCnt == 0):
        hyponym_score = 0
    else:
        hyponym_score = math.log(hyponymCnt/float(no_of_sents))
    
    if (polysemCnt == 0):
        polysem_score = 0
    else:
        polysem_score = math.log(polysemCnt/float(no_of_sents))
    
    commonWrd_score = commonWrd(d)
    
    if (concrete_sum == 0):
        concrete_score = 0
    else:
        concrete_score = math.log(concrete_sum/float(no_of_sents))
        
    if (meaning_sum == 0):
        meaning_score = 0
    else:
        meaning_score = math.log(meaning_sum/float(no_of_sents))
        
    if (motionVerbCnt ==0):
        motionVerb_score = 0
    else:
        motionVerb_score = math.log(motionVerbCnt/float(no_of_sents))
    
    if (adverbCnt == 0):
        adverb_score = 0
    else:
        adverb_score = math.log(adverbCnt/float(no_of_sents))
    
    if (verbCnt == 0):
        verb_score = 0
    else:
        verb_score = math.log(verbCnt/float(no_of_sents))
    
    if (adjectiveCnt == 0):
        adjective_score = 0
    else:
        adjective_score = math.log(adjectiveCnt/float(no_of_sents))
    
    if (nounCnt == 0):
        noun_score = 0
    else:
        noun_score = math.log(nounCnt/float(no_of_sents))

    temp_feats = {'vocab_size':[vocab_size],'adverb_score':[adverb_score], 'verb_score':[verb_score], 'adjective_score':[adjective_score], 'noun_score':[noun_score], 'sbjVrbAgreement_errscore':[sbjVrbAgreement_errscore],'modalRule_errscore':[modalRule_errscore],'PrpDonot_errscore':[PrpDonot_errscore],'VrbTenseAgreement_errscore':[VrbTenseAgreement_errscore],'a_an_errscore':[a_an_errscore], 'sss_score_avg':[sss_score_avg],'coherence_score':[coherence_score],'hyponym_score':[hyponym_score],'polysem_score':[polysem_score],'commonWrd_score':[commonWrd_score], 'concreteness_score':[concrete_score], 'meaningfulness_score':[meaning_score], 'causalVerb_score':[causalVerb_score], 'causalParticle_score':[causalParticle_score],
 'motionVerb_score':[motionVerb_score]}

    return(temp_feats)


