import string

vowels = 'aeiouy'
consonants = 'bcdfghjklmnpqrstvwxz'
consonants2 = 'bcdfghjklmnpqrstvz'

def tokenize(token):
    cur = token
    # step 2: URL
    if(isUrl(cur)):
        return cleanUrl(cur)
    
    # step 3: Convert to lowercase
    cur = cur.lower()
    
    # step 4: Check number token
    if(isNumberToken(cur)):
        return cur
    
    # step 5: Squeeze Apostrophe
    cur = removeApostrophe(cur)
    
    # step 6: Remove abbreviations
    if(isAbbreviation(cur) and not isUrl(cur) and not isNumberToken(cur)):
        cur = removeAbbreviation(cur)
        
    # step 7: Hyphens
    if "-" in cur:
        # res = removeHyphens(cur)
        # fin = []
        # for item in res:
        #     fin.append(tokenize(item))
        # return fin
        arr = removeHyphens(cur)
        for i, item in enumerate(arr):
            arr[i] = tokenize(item)
        if needsFlattening(arr):
            cur = flatten(arr)
        cur = arr
    # step 8: Remaining Punctuation
    if checkRemovePunctuation(cur):
        arr = removePunctuation(cur)
        for i, item in enumerate(arr):
            arr[i] = tokenize(item)
        if needsFlattening(arr):
            cur = flatten(arr)
        cur = arr
    return cur    


def isUrl(token):
    return token.startswith('https://') or token.startswith('http://')


def cleanUrl(token):
    while(token[-1] in string.punctuation):
        token = token[:-1]
    return token


def removeApostrophe(token):
    for i, char in enumerate(token):
        if char == "'" or char == '’':
            return token[:i] + token[i + 1:]
    return token
    # return token.replace("'","")


def isNumberToken(token):
    hasNumber = False
    for char in token:
        if(char.isnumeric()):
            hasNumber = True
        if(not(char.isnumeric() or char == '+' or char == '-' or char == '.' or char == ',' )):
            return False
    return hasNumber


def isAbbreviation(token):
    containsOtherPunc = False
    containsPeriod = False
    for char in token:
        if(char == '.'):
            containsPeriod = True
        if((char in string.punctuation) and (char != '.')):
            containsOtherPunc = True
    return not(isNumberToken(token)) and not(isUrl(token)) and not(containsOtherPunc) and containsPeriod


def removeAbbreviation(token):
    res = token.replace('.', '')
    return res


def removeHyphens(token):
    if not '-' in token:
        return [token]
    res = token.split('-')
    res.append(token.replace('-',''))
    return res


def checkRemovePunctuation(token):
    for punc in string.punctuation:
        if punc in token:
            if punc != '.' and punc != '-':
                return True
    return False


def removePunctuation(token):
    res = []
    for punc in string.punctuation:
        if punc in token:
            if punc != '.' and punc != '-':
                res.append(token.split(punc))
    if len(res) == 0:
        return token
    res = res[0]
    for word in res:
        if word == '':
            res.remove(word)
    return res


def needsFlattening(arr):
    for item in arr:
        if type(item) is list:
            return True
    return False


def flatten(arr):
    flat = []
    for sublist in arr:
        if isinstance(sublist, str):
            flat.append(sublist)
            continue
        for item in sublist:
            flat.append(item)
    return flat

def tokenizer(tokens):
    res = []
    for token in tokens:
        cur = tokenize(token)
        if type(cur) == list: # list returned
            if needsFlattening(cur): # if its nested list, flatten it
                res.append(flatten(cur))
            else:
                res.append(cur)
        else:
            res.append([cur]) # is a string, wrap as a list
    return res    
