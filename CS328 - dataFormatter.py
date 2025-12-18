import re

def classify(sentence: str):
    s = sentence.lower()

    categories = set()

    # WHAT: Almost all instructions answer "what"
    categories.add("what")

    # WHICH: choosing between items, positions, utensils, sides
    if re.search(r"\b(left|right|outer|inner|smaller|larger|first|second|third|best|worst|which)\b", s):
        categories.add("which")

    # WHERE: placement, position, movement, location
    if re.search(r"\b(on|in|at|to|from|under|over|between|beside|across|around|inside|outside)\b", s):
        categories.add("where")

    # WHEN: timing, sequencing
    if re.search(r"\b(before|after|during|when|while|as soon as|always|never|first|last)\b", s):
        categories.add("when")

    # HOW: adverbs or manner
    if re.search(r"\b(slowly|gently|politely|quietly|carefully|subtly|neatly|properly|correctly|firmly|softly|in a|with your|when)\b", s):
        categories.add("how")

    # WHO: references to roles or people
    if re.search(r"\b(host|hostess|guest|person|waiter|server|lady|man|friend|boss)\b", s):
        categories.add("who")

    # WHY: only when explanation exists
    if re.search(r"\b(because|so that|so you|in order to)\b", s):
        categories.add("why")

    return list(categories)

stopWords = [w.lower() for w in [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
]]

# Clear the output file first
with open("cleanedInfo.txt", "w", encoding="utf-8"):
    pass

with open("info.txt", 'r', encoding="utf-8") as file:
    content = file.read()
    lines = content.split('\n')

    # Open cleanedInfo.txt once outside the loop (more efficient)
    with open("cleanedInfo.txt", 'a', encoding="utf-8") as f:
        for line in lines:
            keyWords = []
            for word in line.split():
                cleanWord = ''.join(c for c in word if c.isalnum()).lower()
                if not cleanWord:
                    continue
                if cleanWord in stopWords:
                    continue
                keyWords.append(cleanWord)
    
            # FIXED: convert set and classify output to list to avoid parse errors
            f.write(f"{line.strip()}|{list(keyWords)}|{list(classify(line))}\n")

f.close()
print("Done")
