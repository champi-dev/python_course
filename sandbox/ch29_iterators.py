from itertools import islice


def part1_protocol():
    print("--- 1) the iteration protocol ---")
    nums = [1, 2, 3]
    it = iter(nums)
    print(next(it), next(it), next(it))
    try:
        next(it)
    except StopIteration:
        print("4th next() -> StopIteration (the iterator is exhausted)")

    print("loop the same list twice:")
    for _ in range(2):
        print("  ", [n for n in nums])


class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


def count_down(start):
    while start > 0:
        print("  -> resumed, start =", start)
        yield start
        start -= 1


def part2_class_vs_generator():
    print("\n--- 2) class vs generator (both print 3, 2, 1) ---")
    print("class CountDown:", [n for n in CountDown(3)])


def part3_see_the_pause():
    print("\n--- 3) generators pause & resume ---")
    g = count_down(3)
    print("created generator (no output above this line)")
    print("next ->", next(g))
    print("next ->", next(g))
    print("next ->", next(g))
    try:
        next(g)
    except StopIteration:
        print("generator finished -> StopIteration")


def naturals():
    n = 1
    while True:
        yield n
        n += 1


def part4_infinite():
    print("\n--- 4) infinite generator + break (doesn't hang) ---")
    got = []
    for n in naturals():
        got.append(n)
        if len(got) == 5:
            break
    print("first 5 naturals:", got)


def part5_single_use():
    print("\n--- 5) iterators are single-use ---")
    g = count_down(3)
    print("first list(g): ", list(g))
    print("second list(g):", list(g))
    print("WHY ch19 messages render once: Django's `messages` is a CONSUMING iterator, so")
    print("the {% for message in messages %} loop walks it once and exhausts it -- a second")
    print("loop on the same page would find nothing left.")


def part6_genexpr():
    print("\n--- 6) generator expressions ---")
    mins = [25, 90, 10, 60]
    print("total minutes:", sum(m for m in mins))
    print("long sessions (>=60):", sum(1 for m in mins if m >= 60))


def take(gen, k):
    count = 0
    for item in gen:
        if count >= k:
            return
        yield item
        count += 1


def stretch():
    print("\n--- stretch) take() vs itertools.islice ---")
    print("take(naturals(), 5):  ", list(take(naturals(), 5)))
    print("islice(naturals(), 5):", list(islice(naturals(), 5)))


if __name__ == "__main__":
    part1_protocol()
    part2_class_vs_generator()
    part3_see_the_pause()
    part4_infinite()
    part5_single_use()
    part6_genexpr()
    stretch()
