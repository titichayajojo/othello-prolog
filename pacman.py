from pyswip import Prolog
temp = open("resources/maze_data.txt")
prolog = Prolog()
prolog.consult("pacman_prolog.pl")

data = temp.read().splitlines()
for line_count, line in enumerate(data):
    for char_count, char in enumerate(line):
        assert_text = 'node({},{})'.format( char_count,line_count)
        print(assert_text)
print(data)