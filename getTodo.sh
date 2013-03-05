# find any TODOs and then output them with their line number
sed = PySnake.py | sed 'N;s/\n/\t/' | sed -e '/#\?### TODO:/!d'