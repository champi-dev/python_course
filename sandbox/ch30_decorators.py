import functools
import time


def part1_functions_are_objects():
    print("--- 1) functions are objects ---")

    def shout(text):
        return text.upper() + "!"

    f = shout
    print("f('hi') ->", f("hi"))
    print("same object?:", f is shout, "| name:", shout.__name__)


def make_loud(func):
    def wrapper(text):
        return func(text) + " [LOUD]"
    return wrapper


def part2_sugar_equivalence():
    print("\n--- 2) @ is sugar for f = deco(f) ---")

    def shout_a(text):
        return text.upper() + "!"
    shout_a = make_loud(shout_a)
    print("manual :", shout_a("hi"))

    @make_loud
    def shout_b(text):
        return text.upper() + "!"
    print("@sugar :", shout_b("hi"))


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  calling {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result!r}")
        return result
    return wrapper


def part3_universal_wrapper():
    print("\n--- 3) one decorator, different signatures ---")

    @log_calls
    def add(a, b):
        return a + b

    @log_calls
    def greet(name, excited=False):
        return f"hi {name}" + ("!" if excited else "")

    add(2, 3)
    greet("dan", excited=True)


def log_calls_no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def part4_why_wraps():
    print("\n--- 4) why functools.wraps ---")

    @log_calls_no_wraps
    def add(a, b):
        return a + b
    print("without wraps, add.__name__ =", add.__name__, "(wrong -- it's the wrapper)")

    @log_calls
    def add2(a, b):
        return a + b
    print("with wraps,    add2.__name__ =", add2.__name__, "(correct)")
    print("  Frameworks (Django URLs, DRF, pytest) read __name__/docstring to identify")
    print("  your function; without wraps they'd all see 'wrapper' instead.")


class FakeUser:
    def __init__(self, is_authenticated):
        self.is_authenticated = is_authenticated


class FakeRequest:
    def __init__(self, is_authenticated):
        self.user = FakeUser(is_authenticated)


def my_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return "redirect to login"
        return view_func(request, *args, **kwargs)
    return wrapper


def part5_rebuild_login_required():
    print("\n--- 5) rebuilt @login_required ---")

    @my_login_required
    def add_entry(request):
        return "the add-entry page"

    print("authenticated:", add_entry(FakeRequest(is_authenticated=True)))
    print("anonymous    :", add_entry(FakeRequest(is_authenticated=False)))


def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def part6_factory():
    print("\n--- 6) decorator factory @repeat(n) ---")

    @repeat(3)
    def greet(name):
        print(f"  hi {name}")

    greet("dan")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed*1000:.2f} ms")
        return result
    return wrapper


def part_stretch():
    print("\n--- stretch) @timer, and stacking order ---")

    @timer
    def slow_sum(n):
        return sum(range(n))
    slow_sum(1_000_000)

    @log_calls
    @timer
    def work(n):
        return sum(range(n))
    print("  stacked call:")
    work(500_000)


if __name__ == "__main__":
    part1_functions_are_objects()
    part2_sugar_equivalence()
    part3_universal_wrapper()
    part4_why_wraps()
    part5_rebuild_login_required()
    part6_factory()
    part_stretch()
