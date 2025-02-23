import numpy as np

def flip_with_probability(value, p):
    # value 是要翻转的数字，p 是翻转的概率
    if np.random.rand() < p:  # 生成一个在 [0, 1) 范围内的随机数
        return  -1*value  # 翻转值
    else:
        return value  # 不翻转，保持原值
def encode_even(N,p,R=3):
    varia_node={}#原始码记录i to a

    func_node={}#编码记录a to i
    all_indices=np.arange(N)
    np.random.shuffle(all_indices)

    selected_indices=[]
    for i in range(2*N):
        available_indices = np.setdiff1d(all_indices, selected_indices)
        if len(available_indices) < R:
            available_indices = all_indices  # 如果剩余不足3个，则全体可选

        b = np.random.choice(available_indices, R, replace=False)

        selected_indices.extend(b)
        func_node[i] = b
        for j in b:
            if j not in varia_node:
                varia_node[j] = []
            varia_node[j].append(i)

    source_code = np.random.choice((-1, 1), N)
    #print(f'source code is', source_code, '\n')
    J = {}
    J_withnoise={}
    for funcnode in func_node.keys():  # 生成相互作用，即编码
        j = 1
        for varianode in func_node[funcnode]:
            j *= source_code[varianode]
        J[funcnode] = j
        J_withnoise[funcnode] = flip_with_probability(j, p)
    #print(f'J is\n', J, "\n")
    #print(f'J_n is\n', J_withnoise, "\n")
    #print(varia_node)
    return varia_node, func_node, J, J_withnoise,source_code


def encode(N,p):
    varia_node={}#原始码记录i to a
    func_node={}#编码记录a to i
    for i in range(2*N):
        b = np.random.choice(range(N), 3, replace=False)
        func_node[i]=b
        for j in b:
            if j not in varia_node:
                varia_node[j]=[]
            varia_node[j].append(i)
    source_code=np.random.choice((-1,1),N)
    #print(f'source code is',source_code,'\n')
    J={}
    J_withnoise = {}
    for funcnode in func_node.keys():#生成相互作用，即编码
        j=1
        for varianode in func_node[funcnode]:
            j *= source_code[varianode]
        J[funcnode]=j
        J_withnoise[funcnode] = flip_with_probability(j, p)
    #print(f'J is\n',J,"\n")
    return varia_node,func_node,J,J_withnoise,source_code


def iteration(v,f,J,beta,N,max_iter=500,tol=1e-4,K=3):
    flag=False
    h={}
    u={}
    #np.random.seed(42)
    for varianode in v.keys():#h_{i\to a}初始化
        for funcnode in v[varianode]:
            if varianode not in h:
                h[varianode] = {}
            #h[varianode][funcnode]=np.random.normal(0,1,1)
            h[varianode][funcnode] = np.random.uniform(-1, 1, 1)
            #h[varianode][funcnode] = np.random.choice((-1,1), 1)
    for funcnode in f.keys():#u_{a\to i}初始化
        for varianode in f[funcnode]:
            if funcnode not in u:
                u[funcnode] = {}
            #u[funcnode][varianode]=np.random.normal(0,1,1)
            u[funcnode][varianode] = np.random.uniform(-1, 1, 1)
            #u[funcnode][varianode] = np.random.choice((-1,1), 1)
    for t in range(max_iter):#迭代更新
        delta=0.0
        for i in v.keys():
            for a in v[i]:#h_{ia}
                h_new=0
                for b in v[i]:#连接i的所有节点
                    if b!=a:
                        h_new += u[b][i]
                        #print(u[b][i])
                delta+=abs(h_new-h[i][a])
                h[i][a]=h_new

        for a in f.keys():
            for i in f[a]:#u_{ai}
                tanhprod=1
                for j in f[a]:#连接a的所有节点
                    if j!=i:
                        tanhprod *= np.tanh(beta*h[j][a])
                u_new=(np.arctanh(np.tanh(beta*J[a])*tanhprod))/(beta)
                delta+=abs(u_new-u[a][i])
                u[a][i]=u_new


        if delta/(N*K)<tol:
            flag=True
            break
    if flag:
        print(t,'time Converged')
    else:
        print('Not Converged')
    return h,u,flag

def decode(v,u,beta,N,origin):
    decoded_code=np.zeros(N)
    #print(f'u is\n',u,'\n')
    for i in range(N):
        sum=0
        if i not in v:
            continue
        for b in v[i]:
            #print(u[funcnode][i])
            sum+=u[b][i]
        #print(sum)

        decoded_code[i]=np.sign(sum)

    #print(f'decoded code is\n',decoded_code)
    overlap=(np.inner(origin,decoded_code))/N
    # l=0
    # for i in range(N):
    #     if decoded_code[i]!=origin[i]:
    #         print(f'wrong length is',len(v[i]))
    #         l+=len(v[i])
    #     else:
    #         print(f'right length is',len(v[i]))
    #         l+=len(v[i])

    print(f'Overlap:\n {overlap}')
    return overlap
#--------------------------------------------

