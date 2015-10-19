__author__ = 'hao'
from collections import Counter

truth      = [1, 2, 1, 2, 1, 1, 1, 2, 1, 3, 4, 1]
prediction = [1, 1, 2, 1, 1, 2, 1, 2, 1, 4, 4, 3]

# make confusion matrix
confusion_matrix = Counter()
for t, p in zip(truth, prediction):
    confusion_matrix[t,p] += 1

# print confusion matrix
labels = set(truth + prediction)
print "t/p",
for p in sorted(labels):
    print p,
print
for t in sorted(labels):
    print t,
    for p in sorted(labels):
        print confusion_matrix[t,p],
    print
