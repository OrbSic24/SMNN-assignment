import matplotlib.pyplot as plt
import numpy as np
import func

def main(p,beta):
 #

 N=50
 v,f,J,J_n,s=func.encode(N,p)
 #print(v)
 #print(f'v is',v)
 h,u,flag=func.iteration(v,f,J_n,beta,N)
 o=func.decode(v,u,beta,N,s)
 return o,flag

# o=0
# R=10
P=np.arange(0.01,0.4,0.01)
s=0
overlapc=[]
overlaph=[]
overlapl=[]

# for p in P:
#     beta=np.log((1-p)/p)*0.5
#
#     for i in range(100):
#         ele_oc,flagc=main(p,beta)
#
#         while len(overlapc) <= s:
#             overlapc.append([])
#         if flagc:
#             overlapc[s].append(ele_oc)
#         print(f'now p is {p}')
#         if len(overlapc[s])>=5:
#             break
#     s+=1
#
#
# overlapmeanc=[np.mean(i) for i in overlapc]
# overlapstdc=[np.std(i) for i in overlapc]
# plt.figure(figsize=(8, 6))
# plt.xlabel('flipping rate p')
# plt.ylabel('Overlap')
# plt.errorbar(P,overlapmeanc,overlapstdc,ecolor='r',color='b')
# plt.title(r'$\beta_c=\frac{1}{2}\ln{\frac{1-p}{p}}$')
# plt.savefig('overlapc.png',dpi=1000)
# plt.show()
s=0
for p in P:
    beta=np.log((1-p)/p)*0.5

    for i in range(100):
        ele_oh,flagh=main(p,0.1*beta)

        while len(overlaph) <= s:
            overlaph.append([])
        if flagh:
            overlaph[s].append(ele_oh)
        print(f'now p is {p}')
        if len(overlaph[s])>=5:
            break
    s+=1
overlapmeanh=[np.mean(i) for i in overlaph]
overlapstdh=[np.std(i) for i in overlaph]
plt.figure(figsize=(8, 6))
plt.xlabel('flipping rate p')
plt.ylabel('Overlap')
plt.errorbar(P,overlapmeanh,overlapstdh,ecolor='r',color='b')
plt.ylim([-0.28,1])
plt.title(r'$\beta=0.1\beta_c$')
plt.savefig('overlaph1.png',dpi=1000)
plt.show()
# s=0
# for p in P:
#     beta=np.log((1-p)/p)*0.5
#
#     for i in range(10):
#         ele_ol,flagl=main(p,5*beta)
#
#         while len(overlapl) <= s:
#             overlapl.append([])
#         if flagl:
#             overlapl[s].append(ele_ol)
#         print(f'now p is {p}')
#         if len(overlapl[s])>=5:
#             break
#         if i==9:
#             overlapl[s].append(0)
#     s+=1
# overlapmeanl=[np.mean(i) for i in overlapl]
# overlapstdl=[np.std(i) for i in overlapl]
# plt.figure(figsize=(8, 6))
# plt.xlabel('flipping rate p')
# plt.ylabel('Overlap')
# plt.errorbar(P,overlapmeanl,overlapstdl,ecolor='r',color='b')
# plt.title(r'$\beta=5\beta_c$')
# plt.savefig('overlapl.png',dpi=1000)
# plt.show()