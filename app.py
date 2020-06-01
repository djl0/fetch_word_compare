def split_words(text):
    if '.' in text:
        text = text.split('.')
    else:
        text = [text]
    sentences = [t.strip() for t in text if t]

    words = [[w.lower().strip(',') for w in s.split(' ')] for s in sentences]

    return words

def get_wordcounts(text):
    wordcounts = {}
    words = split_words(text)
    for sentence in words:
        for w in sentence:
            wordcounts[w] = wordcounts.get(w, 0) + 1
    return wordcounts

def compare_wordcounts(text1, text2):
    wordcount1 = get_wordcounts(text1)
    wordcount2 = get_wordcounts(text2)
    total_words1 = sum(wordcount1.values())
    total_words2 = sum(wordcount2.values())
    avg_total = (total_words1 + total_words2)/2.0
    comparisons = {}

    score = 1
    for w in wordcount1.keys():
        score -= 0.5 * abs(wordcount1.get(w, 0) - wordcount2.get(w, 0))/avg_total
    # get words in 2 but not in 1
    for w in wordcount2.keys():
        if w not in wordcount1:
            score -= 0.5 * abs(wordcount1.get(w, 0) - wordcount2.get(w, 0))/avg_total
    return max(0, score)

def direct_compare(text1, text2, reverse=False):
    total_words = 0
    total_matches = 0
    sentences1 = split_words(text1)
    sentences2 = split_words(text2)
    sentences_loop_range = range(len(sentences1))
    if reverse:
        sentences_loop_range = reversed(sentences_loop_range)
    for s_index in sentences_loop_range:
        word_loop_range = range(len(sentences1[s_index]))
        if reverse:
            word_loop_range = reversed(word_loop_range)
        for w_index in word_loop_range:
            w1 = sentences1[s_index][w_index]
            total_words += 1
            w2 = None
            if len(sentences2) >= s_index + 1 and len(sentences2[s_index]) >= w_index + 1:
                w2 = sentences2[s_index][w_index]
            if w1 == w2:
                total_matches += 1
    return total_matches/total_words



def compare_text(text1, text2):
    if text1 == text2:
        return 1
    wordcount_compare = compare_wordcounts(text1, text2)

    #compare each text each direction
    exact_order_compare_1f = direct_compare(text1, text2, reverse=False)
    exact_order_compare_1r = direct_compare(text1, text2, reverse=True)
    exact_order_compare_2f = direct_compare(text2, text1, reverse=False)
    exact_order_compare_2r = direct_compare(text2, text1, reverse=True)
    exact_order_compare_score = (exact_order_compare_1f + exact_order_compare_1r
                                 + exact_order_compare_2f + exact_order_compare_2r) \
                                / 4
    avg_score = (wordcount_compare + exact_order_compare_score) / 2
    return avg_score
