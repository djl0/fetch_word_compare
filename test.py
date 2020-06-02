from .word_compare import WordComparer

sample1 = ("The easiest way to earn points with Fetch Rewards is to just shop "
           "for the products you already love. If you have any participating brands "
           "on your receipt, you'll get points based on the cost of the products. "
           "You don't need to clip any coupons or scan individual barcodes. "
           "Just scan each grocery receipt after you shop and we'll find the "
           "savings for you.")
sample2 = ("The easiest way to earn points with Fetch Rewards is to just shop "
           "for the items you already buy. If you have any eligible brands on your "
           "receipt, you will get points based on the total cost of the products. "
           "You do not need to cut out any coupons or scan individual UPCs. Just "
           "scan your receipt after you check out and we will find the savings "
           "for you.")
sample3 = ("We are always looking for opportunities for you to earn more points, "
           "which is why we also give you a selection of Special Offers. These "
           "Special Offers are opportunities to earn bonus points on top of the "
           "regular points you earn every time you purchase a participating brand. "
           "No need to pre-select these offers, we'll give you the points whether "
           "or not you knew about the offer. We just think it is easier that way.")

def test_equal():
    text = 'ab cd ef. Ghi j.'
    comparer = WordComparer(text, text)
    assert comparer.compare_text() == 1

def test_unequal():
    text1 = 'ab cd ef. Ghi j.'
    text2 = 'zz yy xx.'
    comparer = WordComparer(text1, text2)
    assert comparer.compare_text() == 0

def test_kinda_close():
    text1 = 'ab cd ef. Ghi j.'
    text2 = 'ab cd ef. Ghi z.'
    comparer = WordComparer(text1, text2)
    assert comparer.compare_text() > 0.7

def test_samples():
    comparer_1_2 = WordComparer(sample1, sample2)
    comparer_1_3 = WordComparer(sample1, sample3)
    assert comparer_1_2.compare_text() > comparer_1_3.compare_text()
