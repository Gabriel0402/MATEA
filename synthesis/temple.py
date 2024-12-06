# -*- coding: utf-8 -*-
from utils import *
from gltl2gpar import drawGPar
import time
import pickle
from output import cent_output,decent_output

def tnash_1(modules,GPar,draw_flag,save_flag,pf,DPW_prop,alphabets):
    results = []
    TTPG_vmax=0 #count the max number of vertices in TTPG/GPar sequentialisation
    TTPG_emax=0 #count the max number of edges in TTPG/GPar sequentialisation
    TTPG = Graph(directed=True) #init GPar sequentialisation
    for module in modules:
        for key, value in module.items():
            # 检查值是否为集合且包含所需格式
            if isinstance(value, set):
                for item in value:
                    if '[]  <>' in item and '(' in item and ')' in item:
                        results.append(item)
    #print("modules:",len(modules))
    #print(modules)
    '''
    generate W (winning coalitions)
    reverse the list to generate from big to small
    hence always gets pareto optimal if NE exists    
    '''
    W = list(reversed(generate_set_W(modules)))
    NE_flag=False
    PUN = {}
    '''trivial cases all win/lose'''
    w=W[0]
    s_Alpha = build_streett_prod(GPar,w,modules)
    L,L_sigma = Streett_emptyness(GPar,s_Alpha,modules)

    '''if not empty'''
    if L.vcount()!= 0:
        DPW_product = graph_product(GPar, DPW_prop, alphabets)
        e_Alpha = build_streett_prod(DPW_product, w+(len(modules),), modules+[{1:set(['environment'])}])
        E, E_sigma = Streett_emptyness(DPW_product, e_Alpha, modules+[{1:set(['environment'])}])
        num=len(results)
        
        if E.vcount() != 0:
            #print('>>> YES, the property '+ replace_symbols(pf) +' is satisfied in some NE <<<')
            #print('Winning Coalition',(num2name(w,modules)))
            NE_flag=True
            draw_flag = True
            if draw_flag:
                '''draw & printout strategy progile \vec{sigma}'''
                drawGPar(E_sigma)
                print('Original')
                symbol,begin,end,target= printSynthSigmaDetails(E_sigma)
                # print('############################################')
                cent_output(symbol,num,target)
                # print(num)
                decent_output(symbol,num,target,alphabets)
                #print('############################################')
                # print(modules)
                # print('Merged')
                # res = mergeGPar(E_sigma)
                # printSynthSigmaDetails(res)
        #         strategies = decomposeStrategy(E_sigma, modules)
        #         print("Decomposed strategies: ")
        #         for s in strategies:
        #             symbol1,target1 = printSynthSigmaDetails(E_sigma)
        #             symbol = symbol+symbol1
        #     if save_flag:
        #         trans(modules, symbol, alphabets)
        # else:
        #     print("There is no nash equilibrium for this game")
            
            
    if not NE_flag:
        print('>>> NO, the property '+ replace_symbols(pf) +' is not satisfied in any NE <<<')
    return TTPG_vmax,TTPG_emax

