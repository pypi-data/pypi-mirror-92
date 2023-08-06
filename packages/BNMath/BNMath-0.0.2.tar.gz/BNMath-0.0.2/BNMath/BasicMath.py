class mlbnm:
    def ml1():
        print(f"import csv\n")

        print(f"with open('tennis.csv', 'r') as f: \n reader = csv.reader(f) \n your_list = list(reader)\n h = [['0', '0', '0', '0', '0', '0']]\nfor i in your_list:\n")
        print(f"if i[-1] == Yes:\n j = 0\n for x in i:\n if x != Yes:\n if x != h[0][j] and h[0][j] == '0':\nh[0][j] = x\nelif x != h[0][j] and h[0][j] != '0':\nh[0][j] = '?'\n")
        print(f"else:\npass\nj=j+1\nprint(h)")

    def ml2():
        a='''import pandas as pd
df = pd.read_csv('carmodel.csv')
hold=list()

for i in range(df.shape[0]):
  print(list(df.iloc[i]))
  hold.append(list(df.iloc[i]))
    
g=list()
s = hold[0].copy()# first row
#print(s)
s.pop() # first row without last column
print(s)
z=1

hold

for i in hold[1:]: 
  if i[-1] == 'Positive':
    print(f"Step {z}") 
    z=z+1
    for j in range(len(s)):
      if i[j] != s[j] :
        print(i[j],s[j])
        s[j] = '?'
        print('\n S:'.format(i),s)
        print('\n G:'.format(i),g)
  else:
    print(f"Step {z}")  
    z=z+1
    for j in range(len(s)):
      v = ['?','?','?','?','?','?']
      if i[j] != s[j] and s[j]!='?' :
        v[j]=s[j]
        # print(i[j],first[j])
        g.append(v)
        print('\n S:'.format(i),s)
        print('\n G:'.format(i),g)
 k=0
for i in g:
  for j in i:
    if j != '?' and j not in s:
      print(g[k])  
      g.pop(k)
  k=k+1 

print("\nFinal Hypothesis :")
print("\nSpecialized :",s)
print("Generalized :",g)
'''
        print(a)

    
        
        
            
