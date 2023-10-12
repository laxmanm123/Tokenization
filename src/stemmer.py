# Porter Stemmer
def step1a(token):
    
    if token[-4:] == 'sses': # if it ends in sses, replace it with ss
        return token[:-2]
    elif token[-3:] == 'ies' or token[-3:] == 'ied':
        string = token[:-3]
        return string + 'i' if len(string) > 1 else string + 'ie'
    elif token[-2:] == 'ss' or token[-2:] == 'us':
        return token
    elif token[-1:] == 's':
        string = token[:-2]
        for char in string:
            if char in vowels:
                return token[:-1]
        return token
    return token


def step1b(token):
    if token[-3:] == 'eed' or token[-5:] == 'eedly': #TODO
        for i, char in enumerate(token):
            if(char in vowels): # vowel found
                string = token[i+1:]
                if token[-3:] == 'eed' and ('eed' in string):
                    return step1c(token[:-1])
                if token[-5:] == 'eed' and ('eed' in string):
                    return step1c(token[:-3])
    elif token[-2:] == 'ed':
        return step1bHelper(token, 2)
    elif token[-4:] == 'edly':
        return step1bHelper(token, 4)
    elif token[-3:] == 'ing':
        return step1bHelper(token, 3)
    elif token[-5:] == 'ingly':
        return step1bHelper(token, 5)
    return step1c(token)    
        

        
def step1bHelper(strings, endLength):
    for char in strings[:-endLength]:
        if char in vowels: # if it does contain a vowel
            string = strings[:-endLength]
            if string[-2:] == 'at' or string[-2:] == 'bl' or string[-2:] == 'iz':
                return step1c(string + 'e')
            elif string[-2:] == 'bb' or string[-2:] == 'dd' or string[-2:] == 'gg' or string[-2:] == 'ff' or string[-2:] == 'mm' or string[-2:] == 'nn' or string[-2:] == 'pp' or string[-2:] == 'rr' or string[-2:] == 'tt':
                return step1c(string[:-1])
            elif (isShortStem(string)):
                return step1c(string + 'e')
            else:
                return step1c(string)
    return step1c(strings)


    
def isShortStem(string):
    # print(string + 'here')
    # it is only a vowel followed by a single consonant (e.g., at or ow (or “or”!) but not be)
    if (string[0] in vowels) and (string[1] in consonants) and (len(string) == 2): 
        return True
    
    # It is one or more consonants in a row followed by a single vowel and then followed by only 
    # one other consonant other than w and x
    if (string[0] in vowels): # check first letter is not vowel
        return False
    for i, char in enumerate(string):
        if(char in vowels): # vowel found
            if(i+1 < len(string)):
                # print(string[i+1] in consonants2)
                # print(i+2 == len(string))
                if ((string[i+1] in consonants2) and (i+2 == len(string))):
                    return True
                else: 
                    return False
    return False
    
    
        
def step1c(token):
    if(len(token) == 1):
        return token
    char = token[-1:] 
    if char == 'y':
        x = not token[-2] in vowels
        y = len(token) > 2
        if x and y:
            return token[:-1] + 'i'
    return token


# ['number', 'words', 'numberwords'] either gets this or ['spaces']
def stemmer(tokens):
    res = []
    for token in tokens:
        temp = token
        for i, item in enumerate(token):
            # print(item)
            temp[i] = step1b(step1a(item))
        res.append(temp)
    return res