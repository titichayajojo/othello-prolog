# from pyswip import Prolog
temp = open("resources/maze_data.txt")
# prolog = Prolog()
# prolog.consult("pacman_prolog")
# c = list(prolog.query("node(A)"))
data = temp.read().splitlines()
nodes = []
ct = 0
# print(c)
for line_count, line in enumerate(data):
    nodes.append("")
    for char_count, char in enumerate(line):
        if char not in '1PICSG' and (not(line_count == 13 and char_count == 13) and not(line_count == 13 and char_count == 14)):
        # assert_text = 'node({},{})'.format( char_count,line_count)
            # print("(",char_count,char,line_count,')',end = '')
            # print(1, end = '')
            nodes[line_count] += '1'
            ct += 1
        else:
            # print(' ', end = '')
            nodes[line_count] += ' '
    # print()
print( "\n".join((nodes )))
print(ct)

facts = []
for i in range (len(nodes)):
    for j in range(len(nodes[i])):
        if nodes[i][j] == '1':

            if nodes[i][j+1] == '1':
                fact1 = "edge(node({},{}),node({},{}),1).".format(j,i,j+1,i)
                fact2 = "edge(node({},{}),node({},{}),1).".format(j+1,i,j,i)
                if fact1 and fact2 not in facts:
                    facts.append(fact1)

            if nodes[i][j-1] == '1':
                fact1 = "edge(node({},{}),node({},{}),1).".format(j,i,j-1,i)
                fact2 = "edge(node({},{}),node({},{}),1).".format(j-1,i,j,i)
                if fact1 and fact2 not in facts:
                    facts.append(fact1)

            if nodes[i+1][j] == '1':
                fact1 = "edge(node({},{}),node({},{}),1).".format(j,i,j,i+1)
                fact2 = "edge(node({},{}),node({},{}),1).".format(j,i+1,j,i)
                if fact1 and fact2 not in facts:
                    facts.append(fact1)

            if nodes[i-1][j] == '1':
                fact1 = "edge(node({},{}),node({},{}),1).".format(j,i,j,i-1)
                fact2 = "edge(node({},{}),node({},{}),1).".format(j,i-1,j,i)
                if fact1 and fact2 not in facts:
                    facts.append(fact1)
print( "\n".join((facts )))
print(len(facts))

# print(data)