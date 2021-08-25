'''
Name: Kerry Kanhai
Student number: 501063750
Assignment 2: Translator
'''

english_to_french = {
    'hello': 'bonjour', 
    'are':'sont',
    'book':'reserver', 
    'take':'prender', 
    'suitcase':'valise', 
    'beaches':'plages', 
    'the':'le',
    'took':'a pris',
    'lot':'beaucoup',
    'photo':'photo', 
    'to':'a', 
    'on':'sur', 
    'a':'une',
    'was':'etait', 
    'for':'pour', 
    'popular':'populaires', 
    'boat':'beateau', 
    'can':'pouvez', 
    'room':'chambre', 
    'night':'nuit', 
    'tomorrow':'demain', 
    'want':'veut', 
    'in':'dans',
    'taxi':'taxi',
    'eat':'manger', 
    'would':'aurait',
    'like':'aimer', 
    'spectacular':'spectaculaire', 
    'view':'vue', 
    'going':'aller', 
    'tour':'tour', 
    'city':'ville', 
    'steakhouse':'steakhouse', 
    'tonight':'ce soir', 
    'buy':'acheter',
    'ordered':'commande',
    'ticket':'billet',
    'of':'de',
    'they':'elles',
    'roam':'parcourir',
    'is': 'est'
}

pronouns = {'he':'il', 'her':'elle', 'you':'vous', 'i':'je', 'we':'nous', 'they':'elles', 'she': 'elle'}

regular_verbs = ['er', 're', 'ir']

regular_verb_trans = {
    'i':{
        'er':'e',
        'ir':'is',
        're':'s'
        },
    'we':'ons',
    'you':'ez',
    'they':'ent',
    'he': {
        'er':'e',
        'ir':'it',
        're':''
    },
    'her':{
        'er':'e',
        'ir':'it',
        're':''
    }
}

gender_words = {
    'une': ['un', 'une'],
    'le': ['le', 'la', 'les']
}

feminine_endings = ['e', 'ion']

# Function that determines if a noun is masculine or feminine
def gender_fix(phrase, gender_words, feminine_endings):

    # Converts to list for easy index based searching
    words = phrase.split(' ')

    for i in range(0, len(words)):
        # if either une or le are used, it will check for the word after that one to check which correct version to use
        if words[i] in gender_words.keys():
            if words[i + 1][-1] in feminine_endings or words[i + 1][len(words[i + 1]) - 3:len(words[i + 1])] in feminine_endings:
                words[i] = gender_words[words[i]][1]
            elif words[i + 1][-1] == 's':
                words[i] = gender_words[words[i]][2]
            else:
                words[i] = gender_words[words[i]][0]

    # Rejoins the words into a string
    new_phrase = ' '.join(words)

    return new_phrase


# Translates words if they have a regular verb ending
def regular_verb_translation(pronoun, word, verb_trans):

    last_two = word[len(word) - 2:]
    ending = ''

    # If these specific pronouns are used, then it will go through a loop of possible endings based on the regular verb ending
    if pronoun == 'i' or pronoun == 'he' or pronoun == 'she':
        for key, values in verb_trans.items():
            if pronoun == key:
                if last_two == 'er':
                    ending = values[last_two]
                elif last_two == 'ir':
                    ending = values[last_two]
                else:
                    ending = values[last_two]
    else:
        ending = verb_trans[pronoun]
    
    translated_word = word[0:-2] + ending

    return translated_word


def translate_word(word, dictionary) :

    if word in dictionary.keys():
        return dictionary[word]
    elif word != '' :
        return '"' + word + '"'
    return word


def translate(phrase, dictionary, reg_verbs, pronouns, reg_verb_trans, gender_words, feminine_endings):

    number_translations = {'0':'zero', '1':'un', '2':'deux', '3':'trois', '4':'quatre', '5':'cinq', '6':'six', '7':'sept', '8':'huit', '9':'neuf', '10':'dix'}
    vowels = ['a', 'e', 'i', 'o', 'u'] 
    verbs = ['was', 'is']

    verb_trans = reg_verb_trans
    
    # A boolean variable to keep track if numbers are used for plural purposes 
    isPreviousDigit = False
    digit = 0
    pronoun = ''
    temp_trans = ''
    translation = ''
    word = ''
    last_char = phrase[-1]
    for character in phrase:
        if character.isalpha():
            word += character
        elif word in pronouns.keys():
            # Converts pronouns
            translation += pronouns[word] + character
            word = ''
        elif character.isdigit():
            # Converts numbers to their French equivalent
            translation += number_translations[character]
            isPreviousDigit = True
            digit = int(character)
        else:
            # Checks for plural and removes the final 's' if inputted in the sentence since no plurals in the dictionary
            if word and word[-1] == 's' and word not in verbs:
                word = word[0:len(word) - 1]
            temp_trans = translate_word(word, dictionary)
            if pronoun:
                if pronoun == 'i' and temp_trans[0] in vowels:
                    translation = pronouns[pronoun][0] + '\''
                if temp_trans[len(temp_trans) - 2:] in reg_verbs:
                    translation += regular_verb_translation(pronoun, temp_trans, verb_trans) + character
                else:
                    translation += temp_trans + character
            elif isPreviousDigit and word:
                if temp_trans[-1] != 's' and digit > 1:
                    translation += temp_trans + 's' + character
                    isPreviousDigit = False
                    digit = 0
                else:
                    translation += temp_trans + character
            else:
                translation += temp_trans + character
            pronoun = ''
            word = ''

        if word in pronouns.keys():
            pronoun = word
    
    translation = gender_fix(translation[0:len(translation) - 1], gender_words, feminine_endings)

    return translation + last_char


def reverse_translate_word(word, gender_words, regular_verb_trans, dictionary, pronouns, reg_verbs):

    translated = ''

    if word[len(word) - 3:] == 'ons' or word[len(word) - 3:] == 'ent':
        last = word[len(word) - 3:]
    else:
        last = word[len(word) - 2:]

    for eng_word, translation in dictionary.items():
        if word == translation:
            translated = eng_word
            return translated

    for key, value in pronouns.items():
        if word == value:
            translated = key
            return translated

    for key, values in gender_words.items():
        if word in values:
            translated = key
            for eng_word, translation in dictionary.items():
                if translated == translation:
                    return eng_word

    for key, values in regular_verb_trans.items():
        if type(values) is dict:
            for verbs, trans in values:
                if last == trans:
                    word = word[0:len(word) - 2] + verbs
                    
                    for eng_word, translation in dictionary.items():
                        if word == translation:
                            translated = eng_word
                            return translated        
        else:
            if last in reg_verbs:
                word = word[0:len(word) - 2]
            for eng_word, translation in dictionary.items():
                if word == translation[0:len(translation) - 2]:
                    translated = eng_word
                    return translated


def reverse_dictionary(phrase, dictionary, gender_words, regular_verb_trans, pronouns, reg_verbs):
    translation = ''
    word = ''

    for character in phrase:
        if character.isalpha():
            word += character
        else:
            translation += reverse_translate_word(word, gender_words, regular_verb_trans, dictionary, pronouns, reg_verbs) + character
            word = ''

    return translation

        

sentence1 = 'They like the view.'
translated1 = translate(sentence1.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print(f"English: {sentence1}")
print(f'Translation: {translated1.capitalize()}')

print("*" * 100)

sentence2 = 'I like the view.'
translated2 = translate(sentence2.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print("Verb conjugated to 'Je': ")
print(f"English: {sentence2}")
print(f'Translation: {translated2.capitalize()}')


print("*" * 100)

sentence3 = 'They take the boat tour tomorrow.'
translated3 = translate(sentence3.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print("Verb conjugated to 'They' and a different regular verb ending ('prender' which is in the dictionary is changed to 'prendent' because of the pronoun): ")
print(f"English: {sentence3}")
print(f'Translation: {translated3.capitalize()}')


print("*" * 100)
print("*" * 100)

print("Demonstrating gender nouns: ")
sentence4 = 'The boat tour was spectacular.'
translated4 = translate(sentence4.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print("Since boat in French is masculine, the masculine version of 'the' is used")
print(f"English: {sentence4}")
print(f'Translation: {translated4.capitalize()}')


print("*" * 100)

sentence5 = 'We are going on a tour of the city tomorrow.'
translated5 = translate(sentence5.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print("Since city is feminine, the feminine version of 'le' is used: ")
print(f"English: {sentence5}")
print(f'Translation: {translated5.capitalize()}')

print("*" * 100)
print("*" * 100)

sentence6 = 'Can you book 1 room?.'
translated6 = translate(sentence6.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print("Demonstrating plural and number conversion: ")
print(f"English: {sentence6}")
print(f'Translation: {translated6.capitalize()}')


print("*" * 100)

sentence7 = ' Can you book 3 rooms?'
translated7 = translate(sentence7.lower(), english_to_french, regular_verbs, pronouns, regular_verb_trans, gender_words, feminine_endings)

print("Demonstrating plural and number conversion: ")
print(f"English: {sentence7}")
print(f'Translation: {translated7.capitalize()}')

print("*" * 100)
print("*" * 100)
print("Translating from French to English: ")
sentence8 = 'Il pouvez prender le taxi.'
translated8 = reverse_dictionary(sentence8.lower(), english_to_french, gender_words, regular_verb_trans, pronouns, regular_verbs)
print(f"French: {sentence8}")
print(f'Translation: {translated8.capitalize()}')
