bad_words = []
#word = ()

#getting the bad word list into the script; removing /n from line break with splitlines
with open ('Material/Mike_Bad_Words.txt', 'r') as f:
    bad_words = f.read().splitlines()
print(bad_words)

#Asking for User input and splitting the text
input = input('Paste your text here: ').split(' ')
print(input)

#Check list of inputs against bad word list
for word in input:
    if word in bad_words:
        print(word, "is a bad word")