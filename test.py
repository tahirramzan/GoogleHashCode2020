import os.path
import glob
from collections import defaultdict
import time
start_time1 = time.time()


class Library:
    def __init__(self, id, books_ids, nb_books_N, nb_books_per_day_M, time_sign_T):
        self.id = id
        self.books_ids = set(books_ids)
        self.nb_books_N = nb_books_N
        self.nb_books_per_day_M = nb_books_per_day_M
        self.time_sign_T = time_sign_T
        self.score = 0
        self.scanned_books = []
        self.coefficient = 0

    def update_books(self, books_taken):
        self.books_ids = self.books_ids.difference(books_taken)

    def update_score(self, books_scores):
        self.score = sum(books_scores[b] for b in self.books_ids)

    def update_coefficient(self):
        self.coefficient = self.score / self.time_sign_T

    def update(self, books_taken, books_scores):
        self.update_books(books_taken)
        self.update_score(books_scores)
        self.update_coefficient()

    def sort_books_by_score(self, books_scores, reverse=True):
        self.books_ids = set(sorted(self.books_ids, key=lambda o: books_scores[o], reverse=reverse))

    def consolidate_book_search(self, book_search):
        for book_id in self.books_ids:
            book_search[book_id].append(self)


filesList = glob.glob('.\input/*.txt')
for filename in filesList:
    start_time2 = time.time()

    books_taken = set()
    libs_taken = []
    books_scores = {}
    book_search = defaultdict(list)

    f = open(filename)
    nb_books_B, nb_libs_L, deadline_D = (int(n) for n in f.readline().split())
    books = f.readline().split()
    books_scores = dict([(i, int(books[i])) for i in range(len(books))])

    libraries = []
    for i in range(nb_libs_L):
        nb_books_N, time_sign_T, nb_books_per_day_M = (int(n) for n in f.readline().split())
        books_ids = [int(n) for n in f.readline().split()]
        lib = Library(i, books_ids, nb_books_N, nb_books_per_day_M, time_sign_T)
        lib.update_score(books_scores)
        lib.update_coefficient()
        lib.sort_books_by_score(books_scores)
        lib.consolidate_book_search(book_search)
        libraries.append(lib)
    f.close()

    libraries_chosen = []
    libraries = sorted(libraries, key=lambda o: o.coefficient, reverse=True)
    days = deadline_D
    while days > 0 and len(libraries) > 0:
        l = libraries.pop(0)
        if days - l.time_sign_T < 0:
            continue
        days -= l.time_sign_T
        libraries_chosen.append(l)
        if len(l.books_ids) < days * l.nb_books_per_day_M:
            l.scanned_books = set(list(l.books_ids)[:days * l.nb_books_per_day_M])
            books_taken = books_taken.union(l.scanned_books)
        else:
            l.scanned_books = l.books_ids
            books_taken = books_taken.union(l.scanned_books)
        for lib in libraries:
            lib.update(books_taken, books_scores)
        libraries = sorted(libraries, key=lambda o: o.coefficient, reverse=True)

    print(f"Final score: {sum([books_scores[b] for b in books_taken])}")
    print("--- %s seconds ---" % (time.time() - start_time2))

    with open(os.path.join('output', os.path.basename(os.path.splitext(filename)[0] + '.txt')), 'w') as f:
        f.write(f"{len(libraries_chosen)}\n")
        for l in libraries_chosen:
            f.write(f"{l.id} {len(l.scanned_books)}\n")
            f.write(" ".join([str(x) for x in l.scanned_books]))
            f.write("\n")


print("--- %s total seconds ---" % (time.time() - start_time1))


