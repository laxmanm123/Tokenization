def removeStopWords(tokens): #array of array of strings
    stopWords = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                "was", "were", "with"]
    res = []
    for line in tokens:
        x = []
        for word in line:
            if word not in stopWords:
                x.append(word)
        res.append(x)
    return res