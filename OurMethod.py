import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

graph =pd.read_csv('karatedata.csv')
train,test = train_test_split(graph,test_size=0.1,random_state=None)

#removing header and saving
graph.to_csv('graph_edges.csv',header=False,index=False)
train.to_csv('train_edges.csv', header=False,index=False)
test.to_csv('test_edges.csv', header=False, index=False)

g = nx.read_edgelist('graph_edges.csv',delimiter=',',nodetype=int)
train_graph=nx.read_edgelist('train_edges.csv',delimiter=',',nodetype=int)
test_graph=nx.read_edgelist('test_edges.csv',delimiter=',',nodetype=int)
    
#print(nx.info(g))
#print(nx.info(train_graph))
#print(nx.info(test_graph))
#pos=nx.spring_layout(train_graph)
#nx.draw(train_graph,pos,node_color='#A0CBE2',edge_color='#00bb5e',width=1,edge_cmap=plt.cm.Blues,with_labels=True)
#plt.show()
#pos=nx.spring_layout(test_graph)
#nx.draw(test_graph,pos,node_color='#A0CBE2',edge_color='#00bb5e',width=1,edge_cmap=plt.cm.Blues,with_labels=True)
#plt.show()
            
def Distance(i,j):
    try:
        return nx.shortest_path_length(train_graph,source = i,target  = j)
    except KeyError:
        return 0;

def CN(a,b):
    try:
        if len(set(train_graph[a])) == 0  | len(set(train_graph[b])) == 0:
            return 0
        return len(set(train_graph[a]).intersection(set(train_graph[b])))
    except:
        return 0

def Score(a,b):
    try:
        if CN(a,b) == 0:
            return (1/Distance(a,b))  
        else:
            return (CN(a,b)+Distance(a,b))/(Distance(a,b)+1)#(len(set(train_graph[a]))+len(set(train_graph[b])))
    except:
        return 0
    '''
    try:
        if CN(a,b) == 0:
            return (1/Distance(a,b))  
        else:
            return (1+CN(a,b))/2#(len(set(train_graph[a]))+len(set(train_graph[b])))
    except:
        return 0'''

#generating Missing edges
edges_in_g = dict()
for i in g.edges:
    edges_in_g[(i[0],i[1])] = 1; 
                   
length = len(test_graph.edges)
M_set = []
N_list = list(g.nodes)
N = len(N_list)
i = 0
while (i<N):
    j = i + 1
    while j<N:
        tmp1 = edges_in_g.get((N_list[i],N_list[j]),-1)
        tmp2 = edges_in_g.get((N_list[i],N_list[j]),-1)
        if tmp1 != 1 and  tmp2 != 1:
            M_set.append((N_list[i],N_list[j]))
        j = j + 1
    i = i + 1

test_edge_list = list(test_graph.edges)
    
def OurMethod():      
    scores = []
    for i in M_set:
        scores.append((Score(i[0],i[1]),0))
    for i in test_edge_list:
        scores.append((Score(i[0],i[1]),1))
    scores.sort(reverse = True)
    scores=scores[0:length]  
    #print(scores)
    Lr = 0
    for i in scores:
        if i[1]==1:
            Lr += 1
    print("Precision:",(Lr/length))
            
OurMethod()   
    
                
                   


         
            
