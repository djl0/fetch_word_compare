import sys

class WordComparer():
    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2

    def split_words(self, text):
        """
        Split words from paragraph form into more computer-readable array of
        sentences and words
        """
        text = text.replace('?', '.').replace('!', '.')
        if '.' in text:
            text = text.split('.')
        else:
            text = [text]
        sentences = [t.strip() for t in text if t]
        words = [[w.lower().strip(',') for w in s.split(' ')] for s in sentences]
        return words

    def get_wordcounts(self, text):
        """returns dictionary of counts by word"""
        wordcounts = {}
        words = self.split_words(text)
        for sentence in words:
            for w in sentence:
                wordcounts[w] = wordcounts.get(w, 0) + 1
        return wordcounts

    def compare_wordcounts(self, text1, text2):
        wordcount1 = self.get_wordcounts(text1)
        wordcount2 = self.get_wordcounts(text2)
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

    def direct_compare(self, text1, text2, reverse=False):
        """
        Loops through sentences, then words and tests for presence of equal word.
        """
        total_words = 0
        total_matches = 0
        sentences1 = self.split_words(text1)
        sentences2 = self.split_words(text2)
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

    def direct_compare_helper(self, text1, text2):
        """
        direct_compare style comparison returns different results depending argument order
        as well as comparison order (text1 v text2, and front -> back v back -> front).
        This helper averages each scenario.
        """
        exact_order_compare_1f = self.direct_compare(text1, text2, reverse=False)
        exact_order_compare_1r = self.direct_compare(text1, text2, reverse=True)
        exact_order_compare_2f = self.direct_compare(text2, text1, reverse=False)
        exact_order_compare_2r = self.direct_compare(text2, text1, reverse=True)
        return (exact_order_compare_1f + exact_order_compare_1r
                                     + exact_order_compare_2f + exact_order_compare_2r) \
                                    / 4

    def compare_text(self):
        if self.text1 == self.text2:
            return 1
        wordcount_compare = self.compare_wordcounts(self.text1, self.text2)
        direct_compare_score = self.direct_compare_helper(self.text1, self.text2)
        avg_score = (wordcount_compare + direct_compare_score) / 2
        return avg_score


if __name__ == "__main__":
    text1 = text2 = None
    try:
        text1 = sys.argv[1]
        text2 = sys.argv[2]
    except:
        raise Exception("We need 2 word sets!")

    comparer = WordComparer(text1, text2)
    final_score = comparer.compare_text()
    print(round(final_score, 4))
