from collections import defaultdict 

class Graph: 
    # 构造函数
    def __init__(self,vertices): 
        # 创建用处存储图中点之间关系的dict{v: [u, i]}(v,u,i都是点,表示边<v, u>, <v, i>)：边集合
        self.graph = defaultdict(list) 
        # 存储图中点的个数
        self.V = vertices
        self.Time = 0
        self.state = []

    # 添加边
    def add_edge(self,u,v): 
        # 添加边<u, v>
        self.graph[u].append(v) 
        if u not in self.state:
            self.state.append(u)
        if v not in self.state:
            self.state.append(v)
    # 获取一个存储图中所有点的状态:dict{key: Boolean}
    # 初始时全为False
    def set_keys_station(self):
        keyStation = {}
        key = list(self.graph.keys())
        print('---------')
        print(key)
        # 因为有些点，没有出边，所以在key中找不到，需要对图遍历找出没有出边的点
        if len(key) < self.V:
            for i in key:
                for j in self.graph[i]:
                    if j not in key:
                        key.append(j)
        for ele in key:
            keyStation[ele] = False
        print(keyStation)
        return keyStation
    
    def SCCUtil(self,u, low, disc, stackMember, st,res):
 
        # Initialize discovery time and low value
        print("---------")
        print((u,self.graph[u],low, disc, stackMember, st))
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
 
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
             
            # If v is not visited yet, then recur for it
            if disc[v] == -1 :
                self.SCCUtil(v, low, disc, stackMember, st, res)
 
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 (per above discussion on Disc and Low value)
                low[u] = min(low[u], low[v])
                         
            elif stackMember[v] == True:
 
                '''Update low value of 'u' only if 'v' is still in stack
                (i.e. it's a back edge, not cross edge).
                Case 2 (per above discussion on Disc and Low value) '''
                low[u] = min(low[u], disc[v])
 
        # head node found, pop the stack and print an SCC
        w = -1 #To store stack extracted vertices
        a = []
        if low[u] == disc[u]:
            print("******")
            print((u,st))
            while w != u:
                w = st.pop()
                a.append(w)
                # print (w, end=" ")
                stackMember[w] = False
            res.insert(0,a)
             
     
 
    #The function to do DFS traversal.
    # It uses recursive SCCUtil()
    def SCC(self):
  
        # Mark all the vertices as not visited
        # and Initialize parent and visited,
        # and ap(articulation point) arrays
        disc = [-1] * (self.V)
        low = [-1] * (self.V)
        stackMember = [False] * (self.V)
        st =[]
         
 
        # Call the recursive helper function
        # to find articulation points
        # in DFS tree rooted with vertex 'i'
        res = []
        for i in self.state:
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st ,res )               
        return res

    # 拓扑排序
    def topological_sort(self):
        # 拓扑序列
        queue = []
        # 点状态字典
        station = self.set_keys_station()
        # 由于最坏情况下每一次循环都只能排序一个点，所以需要循环点的个数次
        for i in range(self.V):
            # 循环点状态字典，elem：点
            for elem in station:
                # 这里如果是已经排序好的点就不进行排序操作了
                if not station[elem]:
                    self.topological_sort_util(elem, queue, station)
        return queue   
    # 对于点进行排序     
    def topological_sort_util(self, elem, queue, station):
        # 设置点的状态为True，表示已经排序完成
        station[elem] = True
        # 循环查看该点是否有入边，如果存在入边，修改状态为False
        # 状态为True的点，相当于排序完成，其的边集合不需要扫描
        for i in station:
            if elem in self.graph[i] and not station[i]:
                station[elem] = False
        # 如果没有入边，排序成功，添加到拓扑序列中
        if station[elem]:
            queue.append(elem)
    
    

def join_strings_with_ampersand(true_props):
    # Filter out empty strings from the list
        non_empty_strings = [string for string in true_props if string]

        # Join the non-empty strings with "&"
        result = "&".join(non_empty_strings)

        return result
def evaluate_dnf(formula,true_props):
    """
    Evaluates 'formula' assuming 'true_props' are the only true propositions and the rest are false. 
    e.g. evaluate_dnf("a&b|!c&d","d") returns True 
    """
    # ORs
    if "|" in formula:
        for f in formula.split("|"):
            if evaluate_dnf(f,true_props):
                return True
        return False
    # ANDs
    if "&" in formula:
        for f in formula.split("&"):
            if not evaluate_dnf(f,true_props):
                return False
        return True
    # NOT
    if formula.startswith("!"):
        return not evaluate_dnf(formula[1:],true_props)

    # Base cases
    if formula == "True":  return True
    if formula == "False": return False
    return formula in true_props
#值迭代法
def value_iteration(U, delta_u, delta_r, terminal_u, gamma):
    """
    Standard value iteration approach. 
    We use it to compute the potential function for the automated reward shaping
    """
    print ("------USING VALUE ITERATION--------")
    print(U)
    print(delta_u)
    print(delta_r)
    print(terminal_u)
    V = dict([(u,0) for u in U])
    V[terminal_u] = 0
    V_error = 1
    while V_error > 0.0000001:
        V_error = 0
        for u1 in U:
            q_u2 = []
            for u2 in delta_u[u1]:
                if delta_r[u1][u2].get_type() == "constant": 
                    r = delta_r[u1][u2].get_reward(None)
                else:
                    r = 0 # If the reward function is not constant, we assume it returns a reward of zero
                q_u2.append(r+gamma*V[u2])
            v_new = max(q_u2)
            V_error = max([V_error, abs(v_new-V[u1])])
            V[u1] = v_new
    print(V)
    print ("------测试结束--------")
    return V


def deep_index(lst, w):
    return [(i, sub.index(w)) for (i, sub) in enumerate(lst) if w in sub]

#有向有环图
def value_dcg(U, delta_u, delta_r, terminal_u, gamma):
    print ("------USING DCG--------")
    V = dict([(u,0) for u in U])
    g= Graph(len(U)+1)
    for u1 in U:
        for u2 in delta_u[u1]:
            if u1!=u2:
                g.add_edge(u1,u2)
    for u1 in U:
        print(u1)
        print(g.graph[u1])
    res= g.SCC()
    print(res)
    weight = {}
    tmp = 0
    for i in range(len(res)):
        weight[i]=len(res[i])+tmp
        tmp=weight[i]
        # if len(res[i])>1:
        #     weight[i] = 0
    print(res)
    for u1 in U:
        V[u1] = round(weight[deep_index(res,u1)[0][0]]/tmp,4) 
    V[terminal_u] = 0
    print(V)
    # V={0: 0.0, 1: 0.0, 3: 0.0, 4: 0.3, 5: 0.5, 6: 0.5, 7: 0.5, 8: 0.9286, 9: 0.8571, 10: 0.7143, 11: 0.7, 12: 0.6429, 13: 0.5714, 14: 1.0, -1: 0}
    return V
