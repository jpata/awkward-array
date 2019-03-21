import awkward
from awkward import JaggedArray

a = JaggedArray([0, 3, 3, 5], [3, 3, 5, 10], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
assert a[1:-1].tolist() == [[], [3.3, 4.4]]
 
a = JaggedArray([[0, 3], [3, 5]], [[3, 3], [5, 10]], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
assert a[:].tolist() == [[[0.0, 1.1, 2.2], []], [[3.3, 4.4], [5.5, 6.6, 7.7, 8.8, 9.9]]]
assert a[1:].tolist() == [[[3.3, 4.4], [5.5, 6.6, 7.7, 8.8, 9.9]]]

a = JaggedArray([0, 3, 3, 5], [3, 3, 5, 10], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
assert a[[False, True, True, False]].tolist() == [[], [3.3, 4.4]]

a = JaggedArray([[0, 3], [3, 5]], [[3, 3], [5, 10]], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
assert a[[True, True]].tolist() == [[[0.0, 1.1, 2.2], []], [[3.3, 4.4], [5.5, 6.6, 7.7, 8.8, 9.9]]]
assert a[[False, True]].tolist() == [[[3.3, 4.4], [5.5, 6.6, 7.7, 8.8, 9.9]]]

a = JaggedArray([0, 3, 3, 5], [3, 3, 5, 10], [[0.0], [1.1], [2.2], [3.3], [4.4], [5.5], [6.6], [7.7], [8.8], [9.9]])
assert a[[False, True, True, False]].tolist() == [[], [[3.3], [4.4]]]

a = JaggedArray([0, 3, 3, 5], [3, 3, 5, 10], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
assert a[[1, 2]].tolist() == [[], [3.3, 4.4]]

a = JaggedArray([[0, 3], [3, 5]], [[3, 3], [5, 10]], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
assert a[[0, 1]].tolist() == [[[0.0, 1.1, 2.2], []], [[3.3, 4.4], [5.5, 6.6, 7.7, 8.8, 9.9]]]
assert a[[1]].tolist() == [[[3.3, 4.4], [5.5, 6.6, 7.7, 8.8, 9.9]]]

a = JaggedArray([0, 3, 3, 5], [3, 3, 5, 10], [[0.0], [1.1], [2.2], [3.3], [4.4], [5.5], [6.6], [7.7], [8.8], [9.9]])
assert a[[1, 2]].tolist() == [[], [[3.3], [4.4]]]

a = JaggedArray.fromiter([[], [100, 101, 102], [200, 201, 202, 203], [300, 301, 302, 303, 304], [], [500, 501], [600], []])
for start in None, 0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5, -6:
    for stop in None, 0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5, -6:
        for step in None, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5:
            assert a[:, start:stop:step].tolist() == [x.tolist()[start:stop:step] for x in a]

a = JaggedArray.fromoffsets([0, 3, 3, 5], JaggedArray.fromoffsets([0, 3, 3, 8, 10, 10], [0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]))
assert [a[i].tolist() for i in range(len(a))] == [[[0.0, 1.1, 2.2], [], [3.3, 4.4, 5.5, 6.6, 7.7]], [], [[8.8, 9.9], []]]
assert [x.tolist() for x in a] == [[[0.0, 1.1, 2.2], [], [3.3, 4.4, 5.5, 6.6, 7.7]], [], [[8.8, 9.9], []]]
assert [x.tolist() for x in a[:]] == [[[0.0, 1.1, 2.2], [], [3.3, 4.4, 5.5, 6.6, 7.7]], [], [[8.8, 9.9], []]]
assert [x.tolist() for x in a[:-1]] == [[[0.0, 1.1, 2.2], [], [3.3, 4.4, 5.5, 6.6, 7.7]], []]
assert [x.tolist() for x in a[[2, 1, 0]]] == [[[8.8, 9.9], []], [], [[0.0, 1.1, 2.2], [], [3.3, 4.4, 5.5, 6.6, 7.7]]]
assert [x.tolist() for x in a[[True, True, False]]] == [[[0.0, 1.1, 2.2], [], [3.3, 4.4, 5.5, 6.6, 7.7]], []]
assert a[::2, 0].tolist() == [[0.0, 1.1, 2.2], [8.8, 9.9]]
assert a[::2, 1].tolist() == [[], []]
assert a[::2, 0, 1].tolist() == [1.1, 9.9]