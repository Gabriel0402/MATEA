# -*- coding: utf-8 -*-
from utils import *
from gltl2gpar import drawGPar
import time
import pickle

def tnash(modules,GPar,draw_flag,save_flag,pf,DPW_prop,alphabets):
    TTPG_vmax=0 #count the max number of vertices in TTPG/GPar sequentialisation
    TTPG_emax=0 #count the max number of edges in TTPG/GPar sequentialisation
    TTPG = Graph(directed=True) #init GPar sequentialisation

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

        if E.vcount() != 0:
            print('>>> YES, the property '+ replace_symbols(pf) +' is satisfied in some NE <<<')
            print('Winning Coalition',(num2name(w,modules)))
            NE_flag=True
            if draw_flag:
                '''draw & printout strategy progile \vec{sigma}'''
                drawGPar(E_sigma)
                # print('Original')
                symbol = printSynthSigmaDetails(E_sigma)
                
                # print(modules)
                # print('Merged')
                # res = mergeGPar(E_sigma)
                # printSynthSigmaDetails(res)
                strategies = decomposeStrategy(E_sigma, modules)
                print("Decomposed strategies: ")
                for s in strategies:
                    symbol = symbol+printSynthSigmaDetails(s)
            if save_flag:
                trans(modules, symbol, alphabets)
        else:
            print("There is no nash equilibrium for this game")
            
            
    if not NE_flag:
        print('>>> NO, the property '+ replace_symbols(pf) +' is not satisfied in any NE <<<')
    return TTPG_vmax,TTPG_emax

