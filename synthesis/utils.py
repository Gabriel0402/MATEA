# -*- coding: utf-8 -*-

import itertools
import copy
from igraph import *

def jointGoal(modules):
#    jointGoal=[]
    for m in modules:
#        jointGoal = jointGoal.append(list)
        print("player "+str(m[1])+" goal is "+str(m[5]))
        for l in list(m[5])[0].split(" "):
            print(l)

def evalNBWedge(AP,word):
    for a in AP:
        if a[0]=='~':
            if a.strip('~') in word:
                return False
        else:
            if a not in word:
                return False
    return True

'''constructs the powerset of a set of alphabets'''
def alpha2wordset(alphabets):
    wordset = set()
    for n in range(len(alphabets)+1):
        for subset in itertools.combinations(alphabets,n):
            wordset.add(subset)
    return wordset



def graph_product(GPar, DPW_prop, alphabets):
    DPW_product = Graph(directed=True)
    S = set()
    colour_dict = dict()
    val_dict = dict()  # Dictionary to store merged nodes based on 'val' attribute

    '''add init state for RMG'''
    colour_dict = GPar.vs[0]['colour']
    colour_dict['environment'] = DPW_prop.vs[0]['colour']

    if GPar.vs[0]['val'] not in val_dict:
        v = DPW_product.add_vertex(label=(0, 0), colour=copy.copy(colour_dict), val=GPar.vs[0]['val'])
        val_dict[GPar.vs[0]['val']] = v.index
    else:
        v = DPW_product.vs[val_dict[GPar.vs[0]['val']]]
        v['colour']['environment'] = DPW_prop.vs[0]['colour']

    S.add(frozenset(['s' + str(0), 'q' + str(0)]))

    prevS = set()
    while prevS != S:
        prevS = copy.copy(S)
        for state in DPW_product.vs:
            for succ in GPar.vs[state['label'][0]].successors():
                L_t = set(alphabets).intersection(GPar.vs[succ.index]['val'])
                if L_t == set([]):
                    L_t = set([''])

                q = DPW_prop.es.find(_source=state['label'][1], word=L_t).target

                colour_dict = GPar.vs[succ.index]['colour']
                colour_dict['environment'] = DPW_prop.vs[q]['colour']

                if GPar.vs[succ.index]['val'] not in val_dict:
                    v = DPW_product.add_vertex(label=(succ.index, q), colour=copy.copy(colour_dict), val=GPar.vs[succ.index]['val'])
                    val_dict[GPar.vs[succ.index]['val']] = v.index
                    S.add(frozenset(['s' + str(succ.index), 'q' + str(q)]))
                else:
                    v = DPW_product.vs[val_dict[GPar.vs[succ.index]['val']]]
                    v['colour']['environment'] = DPW_prop.vs[q]['colour']
                    S.add(frozenset(['s' + str(succ.index), 'q' + str(q)]))

    for v in DPW_product.vs:
        for e in GPar.es.select(_source=v['label'][0]):
            d = e['word']
            t = e.target
            L_t = set(alphabets).intersection(GPar.vs[t]['val'])
            if L_t == set([]):
                L_t = set([''])

            r = DPW_prop.es.find(_source=v['label'][1], word=L_t).target

            tr_idx = DPW_product.vs[val_dict[GPar.vs[t]['val']]].index

            if tr_idx not in DPW_product.vs[v.index].successors():
                DPW_product.add_edge(v.index, tr_idx, word=d)

    for v in DPW_product.vs():
        v['name'] = v.index

    return DPW_product

'''this function adds two MP players for E/A-Nash'''
'''for CGSs'''
def addMPPlayers_cgs(file_name,pf):
    with open("../temp/add_mp","w") as f:
            f.write(" module matching_pennies_player_1 controls matching_pennies_player_1_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   update\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or X (matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            
            f.write(" module matching_pennies_player_2 controls matching_pennies_player_2_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   update\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or X !(matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            with open(file_name) as f_ori:
                f.write(f_ori.read())
                
                
'''for RMGs'''                
def addMPPlayers_rmg(file_name,pf):
    with open("../temp/add_mp","w") as f:
            f.write(" module matching_pennies_player_1 controls matching_pennies_player_1_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   update\n   :: true ~> matching_pennies_player_1_var' := true;\n   :: true ~> matching_pennies_player_1_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or (matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            
            f.write(" module matching_pennies_player_2 controls matching_pennies_player_2_var\n")
            f.write("   init\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   update\n   :: true ~> matching_pennies_player_2_var' := true;\n   :: true ~> matching_pennies_player_2_var' := false;\n   goal\n")
            f.write("   :: ("+pf+") or !(matching_pennies_player_1_var <-> matching_pennies_player_2_var);\n\n")
            with open(file_name) as f_ori:
                f.write(f_ori.read())

def printGParDetails(GPar):
    print ("\n######## Vertex List ########")
    for v in GPar.vs():
        print(v)
    print ("############################################################\n")

    print ("\n######## Edge List ########")
    print(GPar.get_edgelist())
    print ("############################################################\n")

    print ("\n######## Edge labels ########")
    for e in GPar.es():
        print(e)
    print ("############################################################\n")

    return True

def printSynthSigmaDetails(GPar):
    all_source=[]
    all_target=[]
    save=[]
    #print ("\n\n######## Vertex List ########")
    for v in GPar.vs():
        # print v
        if v['val'] is None:
            v['val'] = []
        print("state:", v['label'], "| val:", list(v['val']))
       
        list_str = ', '.join(list(v['val']))
        save.append(list_str)
        
        # try:
        #     print "state:", v['label'], "| val:", list(v['val'])
        # except TypeError:
        #     # print "state:", v['label'], "| val:", list([''])
        #     print "\n"
    #print ("############################################################\n")
    #print ("\n######## Edge List ########")
    #print(GPar.get_edgelist())
    s=str(GPar.get_edgelist())
    # print(s)
    # save.append(s)
    #print ("############################################################\n")

    # for e in GPar.es:
    #     del e['label']
    # try:
    #     del GPar.es['label']
    # except KeyError:
    #     pass
    # GPar.es['Action Profile'] = GPar.es['word']

    #print ("\n######## Transition Profile ########")
    for e in GPar.es():
        print(e.source, " --(", list(e['word']), ") ", e.target)
        all_source.append(e.source)
        all_target.append(e.target)
    #print ("############################################################\n")
    #print(save)
    return save,all_source,all_target,e.target

def mergeGPar(GPar):
    vertices = GPar.vs()
    value_dict = {}
    for v in vertices:
        value = v['val']
        value_key = str(sorted(value))
        if value_key not in value_dict:
            value_dict[value_key] = []
        value_dict[value_key].append(v.index)
    for value_key, indices in value_dict.items():
        if len(indices) > 1:
            mapping = [indices[0] if i in indices else i for i in range(GPar.vcount())]
            GPar.contract_vertices(mapping, combine_attrs="first")
    GPar.delete_vertices([v.index for v in GPar.vs if v['label'] is None])
    GPar.simplify(multiple=True, loops=False,combine_edges = "first")
    updateLabel(GPar)
    return GPar

def vertDict(GPar):
    vertices = GPar.vs()
    value_dict = {}
    for v in vertices:
        value_dict[v['label']] = set(v['val'])
    return value_dict

def updateLabel(GPar):
    for vertex_id in range(GPar.vcount()):
        GPar.vs[vertex_id]['label'] = vertex_id

def decomposeStrategy(GPar, modules):
    res = []
    union_set = set()
    for m in modules:
        union_set = union_set.union(m[2])
    for m in modules:
        g = GPar.copy()
        vd = vertDict(g)
        mapping = [i for i in range(g.vcount())]
        trans={}
        for e in g.es():
            action = vd[e.source].symmetric_difference(vd[e.target])
            if action.issubset(union_set-m[2]):              
                mapping[e.target] = e.source
            if  len(union_set-m[2])==6:
                if trans=={}:
                    da= action-set(trans.keys())
                else:
                    da=action-trans
                if da.issubset(union_set-m[2]):               
                    mapping[e.target] =0
                trans=action       
        g.contract_vertices(mapping, combine_attrs="first")
        g.delete_vertices([v.index for v in g.vs if v['label'] is None])
        g.simplify(multiple=True, loops=True,combine_edges = "first")
        updateLabel(g)
        res.append(g)
    return res
    
def num2name(w,modules):
    coal=[]
    for i in w:
        coal.append(list((modules[i])[1])[0])
    return coal

def check_draw_flag():
    with open("draw_flag","r") as f:
        data = f.read()
        if data == "1":
            return True
        else:
            return False

def check_verbose_flag():
    with open("verbose_flag","r") as f:
        data = f.read()
        if data == "1":
            return True
        else:
            return False

def generate_set_W(modules):
    W = []
    for n in range(len(modules)+1):
        for subset in itertools.combinations(list(range(0,len(modules))),n):
#            print subse t
            #W.add(subset)
            W.append(subset)
    return W
    
def generate_set_modules(modules):
    W = []
    for n in range(len(modules)+1):
        for subset in itertools.combinations((modules),n):
            print(subset)
            #W.add(subset)
            W.append(subset)
    return W
    
def get_l(w,modules):
    N = list(range(0,len(modules)))
    l = [item for item in N if item not in w]
    return l
    
def build_GPar_L(GPar,w,l,PUN_L):
    GPar_L=copy.copy(GPar)
    to_del=[]
    for v in GPar_L.vs:
            if v['name'] not in PUN_L:
#                print 'VINDEX', v.index
                to_del.append(v.index)
#                GPar_L[frozenset(l)].delete_vertices(v.index)
    GPar_L.delete_vertices(to_del)
    return GPar_L

'''
This function builds product of streett automata
'''    
def build_streett_prod(GPar_L,w,modules):
    '''build streett automata from GPar_L'''
    # print("build_streett_prod:")
    # printSynthSigmaDetails(GPar_L)
    # print(modules)
    s_Alpha=[]
    max_colour = get_max_colour(GPar_L)
#    print 'MAX',max_colour
#     print '#####w######',w,modules
    for pl in w:
        Alpha=[]
        for i in range(max_colour):
            j=2*i
            a={}
            if i==0:
                a['C'+str(i)]=[]
            else:
                a['C'+str(i)]=copy.copy(list(Alpha[i-1]['C'+str(i-1)]))
            a['E'+str(i)]=[]
        
            pl_name = list(modules[pl][1])[0]
            # print pl_name
            for v in GPar_L.vs.select(lambda vertex: vertex['colour'][pl_name]==j):
                a['C'+str(i)].append(v['name'])
            for v in GPar_L.vs.select(lambda vertex: vertex['colour'][pl_name]==j+1):
                a['E'+str(i)].append(v['name'])
            a['C'+str(i)]=set(a['C'+str(i)])
            a['E'+str(i)]=set(a['E'+str(i)])
            Alpha.append(a)
        s_Alpha.append(Alpha)
    # print '>>>> s_ALPHA',s_Alpha
    # print("output")
    # print(s_Alpha)
    return s_Alpha
    
    
'''
This function check Street automaton emptiness
'''            
def Streett_emptyness(GPar_L,s_Alpha,modules):   
    # print("Streett_emptyness:")
    # printSynthSigmaDetails(GPar_L)
    S = copy.copy(GPar_L)
#    for v in S.vs:
#        print v
#     print S.get_edgelist()
#     for e in S.es():
#         print e

    max_colour = get_max_colour(GPar_L)
    while True:
        '''to nontrivial SCC'''
        '''selfloop'''

        SCC=[]
        for v in S.vs():
#            print "XXX", v
            if v in v.successors():
#                print v
                SCC.append([v['name']])
        '''clusters'''
        for c in S.components():
            if len(c)>1:
                SCC.append([S.vs[v]['name'] for v in c])
#            print SCC
        changed=False
        for c in SCC:
#            print 'C',c
            del_flag=False
#            for Alpha in s_Alpha:1
            for i in range(max_colour):
                e_to_del=[]
                v_to_del=[]
#                for i,a in enumerate(Alpha):
                for x,Alpha in enumerate(s_Alpha):
#                    print 'ALP',x, Alpha
                    c_cap_E=Alpha[i]['E'+str(i)].intersection(set(c))
                    c_cap_C=Alpha[i]['C'+str(i)].intersection(set(c))
                    if c_cap_E and not c_cap_C:
#                        print '##',c_cap_E
                        
                        '''need to also check if the edge exists in DSW S'''
                        if len(c_cap_E)==1 and ((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])) in S.get_edgelist()):
#                        if len(c_cap_E):
#                            S.delete_edges((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])))
                            e_to_del.append((name2idx(S,list(c_cap_E)[0]),name2idx(S,list(c_cap_E)[0])))
#                            break
                        else:
#                            S.delete_vertices(namelist2idxlist(S,list(c_cap_E)))
#                            print 'namelist2idxlist', namelist2idxlist(S,list(c_cap_E))
#                            v_to_del.append(namelist2idxlist(S,list(c_cap_E))[0])
                            v_to_del = v_to_del + namelist2idxlist(S,list(c_cap_E))
                        del_flag=True
                        changed=True
#                        break
                if del_flag:
#                    print 'e_to_del',e_to_del
#                    print 'v_to_del',idxlist2namelist(S,v_to_del)
                    S.delete_edges(list(set(e_to_del)))
#                    try:
#                        S.delete_edges(list(set(e_to_del)))
#                    except ValueError:
#                        print 'e_to_del',e_to_del
#                        for v in S.vs():
#                            print v
#                        print S.get_edgelist()
                    S.delete_vertices(list(set(v_to_del)))
                    break
            if del_flag:
                break
            
            
        if not changed:
            break
        
    '''delete trivial SCC and non-SCC'''
    to_del=[]
    to_del_sigma=[]
    self_loop=[]
    '''trivial'''
    for v in S.vs:
        if len(v.successors())==0:
            to_del.append(v.index)
            to_del_sigma.append(v.index)
        else:
            '''self-loop'''
            if v in v.successors():
                self_loop.append(v.index)
            
    '''non-SCC'''
#    print 'SSSSSSLLLLLLL', self_loop
    for c in S.components():
#        print c
        if len(c)==1 and c[0] not in self_loop:
            to_del.append(c[0])
            
    '''return strategy profile \vec{sigma}'''
    S_cpy = copy.copy(S)
    S_cpy.delete_vertices(to_del_sigma)
    
    '''emptiness check'''
    S.delete_vertices(to_del)
                
#    return S.simplify(multiple=True,loops=False)
    # print("Streett_emptyness:")
    # printSynthSigmaDetails(GPar_L)
    return S,S_cpy
    
def get_max_colour(GPar):
    vcolour_max=0
    for v in GPar.vs:
        if max(v['colour'].values())>vcolour_max:
#            print 'asdas',max(v['colour'].values())
            vcolour_max = max(v['colour'].values())
    return vcolour_max
    
def idxlist2namelist(G,idxlist):
    namelist=[]
    for v in idxlist:
        namelist.append(G.vs[v]['name'])
    return namelist

def name2idx(G,name):
    for v in G.vs.select(name=name):
        return v.index

def label2idx(G,label):
    return G.vs.find(label=label).index
        
def namelist2idxlist(G,namelist):
    idxlist=[]
    for name in namelist:
        idxlist.append(name2idx(G,name))
    return idxlist

def drawTTPG_kk(TTPG):
    layout = TTPG.layout('kk')
#    mc = get_max_prior(TTPG)+1
#    r = 3*(float(TTPG.vcount())/mc)
    for v in TTPG.vs:
        v['color']=hsv_to_rgb(float(v.index)/TTPG.vcount(),1,1)
        v['size']=20
        if v['itd']:
            v['shape']='circle'
        else:
            v['shape']='square'
    for e in TTPG.es:
        e['color']=TTPG.vs[e.source]['color']
    TTPG.vs['label']=[None for v in TTPG.vs]
    TTPG.vs[0]['label']='S0'
    visual_style = {}
    visual_style['layout']=layout
    visual_style['bbox']=(1000,1000)
    visual_style['margin']=40
#    visual_style['vertex_label_dist']=2
    visual_style['autocurve']=True
    visual_style['vertex_frame_width']=0
    plot(TTPG, **visual_style)


def replace_symbols(string):
    old = ['&&', '||', '[]', '<>']
    new = ['and', 'or', 'G', 'F']
    for i, j in enumerate(old):  ## replace symbols into 'normal' ones
        string = string.replace(j, new[i])
    return string

def trans(moudles,c,liness):
    
    import re

    lines = c
    i = 1
    output_lines = []
    for line in lines:
        line = line.strip()
        if line == "endline":
            if i==1:
                with open(f"agent.txt", "w") as output_file:
                    output_file.write('\n'.join(output_lines))
            else:
                with open(f"agent{i-1}.txt", "w") as output_file:          
                    output_file.write('\n'.join(output_lines))
            i += 1
            output_lines = []
        else:
            output_lines.append(line)
    if output_lines:
        with open(f"agent{i}.txt", "w") as output_file:
            output_file.write('\n'.join(output_lines))
    filename = f"agent.txt"
    with open(filename, "r") as file:
        lines = file.readlines()
    last_line = lines[-1]
    last_tuple = eval(last_line)  
    max_number = max(max(last_tuple)) + 1
    ts = max_number
    #print(f"ts: {ts}")
    file1='agenttt.txt'
    with open(file1, "w") as file:
        file.write(f"0 # initial state\n{[ts]} # terminal state\n")
    for tup in last_tuple:
        line1 = lines[tup[0]]
        line2 = lines[tup[1]]
        
        line1 = line1.replace(',', '').replace(' ', '')
        line2 = line2.replace(',', '').replace(' ', '')
        line1=line1.strip()
        line2=line2.strip()
        result1 = []
        for letter in line1:
            if letter not in line2:
                result1.append(f"!{letter}")
        result2 = []
        for letter in line2:
            if letter not in line1:
                result2.append(letter)
        result = "&".join(result1 + result2)          
        with open(file1, "a") as file:
            if 'g&e'in result:
                file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(1))\n")
            else:
                file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(0))\n")
    num = 0
    for line in c:
        if line.strip() == "endline":
            num += 1
    for i in range(1, num):
        letters_to_keep=moudles[i-1]
        letters_to_keep = letters_to_keep[2]
        letters_to_keep = list(letters_to_keep)
        filename = f"agent{i}.txt"
        with open(filename, "r") as file:
            lines = file.readlines()
        last_line = lines[-1]
        last_tuple = eval(last_line)  
        max_number = max(max(last_tuple)) + 1
        ts = max_number
        filename1 = f"agenttt{i}.txt"
        with open(filename1, "w") as file:
            file.write(f"0 # initial state\n{[ts]} # terminal state\n")
        number1=1
        number2=1
        number3=1
        second_line = liness[1].strip()  
        state_start_index = second_line.rfind('[')  
        #state = eval(second_line[state_start_index:])  
        for tup in last_tuple:
            line1 = lines[tup[0]]
            line2 = lines[tup[1]]
            
            line1 = line1.replace(',', '').replace(' ', '')
            line2 = line2.replace(',', '').replace(' ', '')
            line1=line1.strip()
            line2=line2.strip()
            result1 = []
            for letter in line1:
                if letter not in line2:
                    result1.append(f"!{letter}")
            result2 = []
            for letter in line2:
                if letter not in line1:
                    result2.append(letter)
            result = "&".join(result1 + result2)
            result=result.split('&')
            new_list = letters_to_keep+ ['!' + item for item in letters_to_keep]
            result = [item for item in result if item in new_list]
            result = '&'.join(result)       
            with open(filename1, "a") as file:
                if i==1:
                    if liness[i-1]in result and number1==1:
                        file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(1))\n")
                        number1+=1
                    else:        
                        file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(0))\n")
                if i==2:
                    if liness[i-1]in result and number2==1:
                        file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(1))\n")
                        number2+=1
                    else:        
                        file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(0))\n")    
                if i==3:
                    if liness[i-1]in result and number3==1:
                        file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(1))\n")
                        number3+=1     
                    else:        
                        file.write(f"({tup[0]},{tup[1]},'{result}',ConstantRewardFunction(0))\n")
    import os
    if os.path.exists("agent.txt"):
        os.remove("agent.txt")
    else:
        print("File 'agent.txt' does not exist.")
    if os.path.exists("agenttt.txt"):
        os.rename("agenttt.txt", "agent.txt")
    else:
        print("File 'agenttt.txt' does not exist.")     
    for i in range(1, num):  
        agent_filename = f"agent{i}.txt"
        agenttt_filename = f"agenttt{i}.txt"
        if os.path.exists(agent_filename):
            os.remove(agent_filename)
        else:
            print(f"File '{agent_filename}' does not exist.")
        if os.path.exists(agenttt_filename):
            os.rename(agenttt_filename, agent_filename)
        else:
            print(f"File '{agenttt_filename}' does not exist.")
def nodes_trans(alphabets):
    if alphabets == "g"  :
        return True

