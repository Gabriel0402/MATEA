from parsrml import *
from arena2kripke import *
from srml2lts import *
import time, sys, getopt
from ltl2nbw import *
from nbw2dpw import *
from gltl2gpar import convertG,drawGPar,convertG_cgs
from utils import *
from tnash import *
from temple import tnash_1

def print_performance(perfConstruction,perfParser,empCheck,GPar_v,GPar_e,TTPG_vmax,TTPG_emax):
    print('Temporal Equi Analysis performance (milisecond)',empCheck)
    print('GPar states', GPar_v)
    print('GPar edges', GPar_e)
    print('Max TTPG states', TTPG_vmax)
    print('Max TTPG edges', TTPG_emax)
    

def printhelp():
    print("usage: main.py [path/name of the file] [options]\n")
    print("\nList of optional arguments:")
    print("-d \t Draw the structures")
    print("-v \t verbose mode")
    print("-s \t Save the strategies into txt file")
    print("\n") 
    sys.exit()

def main(argv):


    args_list = list(sys.argv)
    file_name = args_list[1]
    
    save_flag = False

    with open("verbose_flag","w") as f:
        f.write("0")
    verbose = False
    
    with open("draw_flag","w") as f:
        f.write("0")
    draw_flag=False
    
    try:
        opts, args = getopt.getopt(argv,"vd")
    except getopt.GetoptError:
        printhelp()
        
    for o,a in opts:
        if o == "-d":
            with open("draw_flag","w") as f:
                f.write("1")
                draw_flag=True
        elif o == "-v":
            with open("verbose_flag","w") as f:
                f.write("1")
            verbose = True
        elif o == "-s":
            save_flag = True
        else:
            print("ERROR: Undefined option")
            printhelp()
            
            
    '''read and parse the file'''
    perfParser = 0.0
    start = time.time()*1000
    if (yacc.parse(open(str(file_name)).read())!=False):
        perfParser = time.time()*1000 - start
    
    perfConstruction = 0.0
    start = time.time()*1000

    '''get the property formula for E/A-Nash'''
    try:
        pf = str(propFormula[0])
    except IndexError:
        pf = None
    
    if pf==None:
        print("No property formula input...")
    else:
        print("Checking E-Nash property formula: "+replace_symbols(pf))
    '''need to add two players playing matching pennies with goal: \lnot \phi or (matching pennies goal)'''
    '''we can directly modify list modules by adding two players, can we?'''
    '''but the kripke structure will obviously change, is it a problem?'''

    '''convert \phi to NBW'''
    print("Propositional Formula",propFormula[0],PFAlphabets[0])
    NBW_prop = ltl2nbw(propFormula[0],PFAlphabets[0])
    DPW_prop = nbw2dpw(NBW_prop,PFAlphabets[0])

    M=(Arena2Kripke(modules))

    updateLabM(M)
    print("Kripke states", M.vcount())
    print("Kripke edges", M.ecount())
    # if draw_flag:
    #     drawM(M)
        
    '''Don't need to do LTL2DPW conversion for memoryless case'''
    NBWs = Graph(directed=True)
    DPWs = Graph(directed=True)

    '''Convert NBWs to DPWs'''
    for m in modules:
#        states = []
        NBWs[list(m[1])[0]]=ltl2nbw(list(m[5])[0],list(m[6]))
#           print list(m[5])[0],list(m[1])[0]
        NBWs[list(m[1])[0]]['goal']=list(m[5])[0]
        goal = list(m[5])[0]
        goal = replace_symbols(goal)
        # print(list(m[1])[0], goal)
#        print list(m[1])[0]
        DPWs[list(m[1])[0]] = nbw2dpw(NBWs[list(m[1])[0]],list(m[6]))
        # print("DPW states", DPWs[list(m[1])[0]])
    
    if verbose:
        print("\n Convert G_{LTL} to G_{PAR}...\n")
    GPar = convertG(modules,DPWs,M)

    GPar_v = GPar.vcount()
    GPar_e = GPar.ecount()
    perfConstruction = time.time()*1000 - start
    
    empCheck = 0.0
    TTPG_vmax=0
    TTPG_emax=0
    start = time.time()*1000
    TTPG_vmax,TTPG_emax=tnash(modules,GPar,draw_flag,save_flag,pf,DPW_prop,PFAlphabets[0])
    empCheck = time.time()*1000 - start
    
    if verbose:
        print_performance(perfConstruction,perfParser,empCheck,GPar_v,GPar_e,TTPG_vmax,TTPG_emax)
    else:
        TTPG_vmax,TTPG_emax=tnash_1(modules,GPar,draw_flag,save_flag,pf,DPW_prop,PFAlphabets[0]) 
if __name__ == "__main__":
    main(sys.argv[2:])
    
