import numpy,string
import sys, os
import random

def get_scores_from_file(score_file):
    
    scores=[]
    a=[]
    b=[]
    sf=open(score_file,'r')
    for ln in sf.readlines():
        a =str(ln.strip().split())
        #print (a)
        #print (a.split(",")[3])
        c=a.split(",")[3]
        d=eval(c)
        #print(d)
        scores.append(eval(a.split(",")[3]))
        #print (scores)
    return map(float, scores)


def get_random_score_set(scores_list,num_models):
    
    scores_chosen=[]
    score_indices_chosen=[]
    
    while len(scores_chosen)<num_models:
        
        newindex=random.randint(0,len(scores_list)-1)
        
        if newindex not in score_indices_chosen:
            score_indices_chosen.append(newindex)
            scores_chosen.append(scores_list[newindex])
            
    return scores_chosen

    
# Files with lists of scores from run1 and run2 
run1_scores_file=sys.argv[1]
run2_scores_file=sys.argv[2]

run1_scores=(get_scores_from_file(run1_scores_file))
run2_scores=(get_scores_from_file(run2_scores_file))
#print (run1_scores)
#print (run2_scores)
replicates=100

numModels=len(run1_scores)
#print (numModels)
#randomSubsets=[int(0.2*numModels),int(0.4*numModels),int(0.6*numModels),int(0.8*numModels),numModels]
randomSubsets=range(50,10000,200)
print (randomSubsets)
print "Subset","run1_topscore_mean","run1_topscore_stderr","run2_topscore_mean","run2_topscore_stderr"

for r in randomSubsets:
    # for each random subset, get the mean top scoring model and the standard error
    
    topScoresRun1=[]
    topScoresRun2=[]
    
    for i in range(replicates):
        newTopScoreRun1=min((get_random_score_set(run1_scores,r)))
        newTopScoreRun2=min((get_random_score_set(run2_scores,r)))
        topScoresRun1.append(newTopScoreRun1)
        topScoresRun2.append(newTopScoreRun2)
        
    topScoresRun1=numpy.array(topScoresRun1)
    topScoresRun2=numpy.array(topScoresRun2)
    print r,numpy.mean(topScoresRun1),numpy.std(topScoresRun1),numpy.mean(topScoresRun2),numpy.std(topScoresRun2)
    
    















