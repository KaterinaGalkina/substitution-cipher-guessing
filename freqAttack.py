# Transforms the text file 30k.txt into a Python dictionary 
# where keys are word lengths and values are the words in the file with that specific length
def populate_dico_words_len():
    dico_words_len = {}
    file = open("30k.txt")
    most_frequent_words = file.read().splitlines()
    file.close()
    for word in most_frequent_words:
        word = word.strip().lower()
        if len(word) == 0:
            continue
        dico_words_len.setdefault(len(word), []).append(word)
    return dico_words_len


# Function that defines the distance between encrypted word w1 and probably decrypted word w2
# The full explanation of the chosen distance values : 
# I first look if letters that I know for sure (known_letters) 
# in w1 match w2, because if not then it is 100% sure that it is not the word I am comparing to. 
# And then if at the same time the current letter in w1 (l1) is not in known letters 
# (decrypted) and the current letter in w2 (l2) is not in known letters (encrypted) 
# then it is one missed letter and it still might be this word. Now for the final line : 
# if I have 0 missed letters found, then I have no interest to consider this word as correct because 
# all letter associations are already guessed (thus it is 1000), 
# but otherwise : if the word is long and few letters are missing there 
# is more chances that we found a correct word, than if the word is short but fewer letters are missing
# Therefore, the final distance is inverted. Voilaaa 
def word_distance(w1, w2, known_letters):
    if len(w1) != len(w2):
        return 10000
    missed_letters = 0
    for l1, l2 in zip(w1, w2):
        if l1 in known_letters and known_letters[l1] == l2:
            continue
        elif l1 in known_letters and known_letters[l1] != l2:
            return 10000
        elif l1 not in known_letters.keys() and l2 not in known_letters.values():
            missed_letters += 1
        else:
            return 10000
    return 1000 if missed_letters == 0 else missed_letters / len(w1) 


# Transforms a given encrypted text into a list of words, 
# each word is separated by a non alphabetic caracter (,.; ...)
def populate_given_words(message):
    given_words = []
    message = message.lower()
    word = ""
    for i in message:
        if i in "QWERTYUIOPASDFGHJKLZXCVBNM" + "QWERTYUIOPASDFGHJKLZXCVBNM".lower():
            word += i
        else :
            if word != "":
                given_words.append(word)
                word = ""
    if word: 
        given_words.append(word)
    return given_words

# Substitutes known letters in the encrypted message by their decrypted associations, 
# if there are missing letters, they are replaced by a slash (/) so we can see them
def partial_subst(known_letters, message):
    new_mess = ""
    for lettre in message:
        if lettre in known_letters.keys() or lettre.lower() in known_letters.keys():
            current_lett = known_letters.get(lettre.lower())
            if lettre.lower() != lettre:
                new_mess += current_lett.upper()
            else :
                new_mess += current_lett
        elif lettre not in "qwertyuiopasdfghjklzxcvbnm" + "qwertyuiopasdfghjklzxcvbnm".upper():
            new_mess += lettre
        else :
            new_mess += "/"
    return new_mess


# Based on words that are probably the same (w1 is encrypted version of w2), 
# this function finds missing letter associations    
def add_missing_letter(w1, w2, known_letters):
    for i in range(len(w1)):
        c1, c2 = w1[i], w2[i]
        if c1 not in known_letters and c2 not in known_letters.values():
            known_letters[c1] = c2
            print(f"New known letters pair : {c1} - {c2}")
    return known_letters


# For each given word in the given text, this function finds the closest one in the dataset 
def best_pred_each_word(given_words, dico_words_len, known_letters):
    best_pred = [None] * len(given_words)
    for i, word in enumerate(given_words):
        if len(word) not in dico_words_len:
            continue 
        min_dist = 1000
        possible_matches = dico_words_len[len(word)]
        for word2 in possible_matches:
            dist = word_distance(word, word2, known_letters)
            if min_dist > dist:
                min_dist = dist
                best_pred[i] = word2
    return best_pred


# The program that predicts the most probable next letter association
def prediction(message, known_letters, dico_words_len):
    message = message.lower()
    given_words = populate_given_words(message)
    best_pred = best_pred_each_word(given_words, dico_words_len, known_letters)

    min_dist = 1000

    best_pred_w1_w2 = None
    for word, word2 in zip(given_words, best_pred):
        if word2 is not None:
            dist = word_distance(word, word2, known_letters)
            if dist < min_dist and dist != 1000:
                min_dist = dist
                best_pred_w1_w2 = (word, word2)

    
    if best_pred_w1_w2 != None :
        known_letters = add_missing_letter(best_pred_w1_w2[0], best_pred_w1_w2[1], known_letters)
        return 0
    else : # We didn't found a new letter association which means that either we found everything we could or ...
        print("Either it is done, or we are in shit.")
        return 1


# Example of application : 

message = """

Ifnfuxpz Wfyndzk dnpaf, oqbi d yndsf dzk abdbfwv dqn, dzk enpuyib tf bif effbwf
mnpt d ywdaa cdaf qz oiqci qb oda fzcwpafk. Qb oda d efdubqmuw acdndedfua, dzk, db
bidb bqtf, uzrzpoz bp zdbundwqaba—pm cpunaf d ynfdb xnqhf qz d acqfzbqmqc xpqzb
pm sqfo. Bifnf ofnf bop npuzk ewdcr axpba zfdn pzf flbnftqbv pm bif edcr, dzk d
wpzy pzf zfdn bif pbifn. Bif acdwfa ofnf flcffkqzywv idnk dzk ywpaav, oqbi dww bif
dxxfdndzcf pm eunzqaifk ypwk. Bif ofqyib pm bif qzafcb oda sfnv nftdnrdewf, dzk,
bdrqzy dww biqzya qzbp cpzaqkfndbqpz, Q cpuwk idnkwv ewdtf Juxqbfn mpn iqa pxqzqpz
nfaxfcbqzy qb.

"""

flag = "Bif mwdy qa: xqcpCBM{5UE5717U710Z_3S0WU710Z_59533D2F}"

# We can guess them because the flag starts by xqcpCBM{...} which is supposed to be picoCTF{...}
known_letters = {"x": "p",
                 "q": "i", 
                 "c": "c", 
                 "p": "o", 
                 "b": "t",
                 "m": "f"}


# The main program 
dico_words_len = populate_dico_words_len()
max_it = 26
i=0
while i != max_it and prediction(message, known_letters, dico_words_len) == 0:
    i+=1

# We are printing the entire text hopefully correctly decrypted 
print()
new_mess = partial_subst(known_letters, message)
print("Decrypted text : " + new_mess)

# We are printing missing letters that were not associated 
# (because they were missing in the text or for other reasons)
missing_letters = []
for lettre in "qwertyuiopasdfghjklzxcvbnm":
    if lettre not in known_letters.values():
        missing_letters.append(lettre)
print("Missing letters are : ", missing_letters)
print()

# We are printing the flag using the letter associattion we previsouly found 
print(f"{partial_subst(known_letters, flag)}")
print()
