def reverse_xy(xy: list[str]):
    l = []
    for i in xy:
        l.append(i[::-1])
    return l


def horizontal_flip(xy: list[str]):
    l = []
    for i in xy:
        l.append(i[0] + chr(19 - (ord(i[1]) - 96) + 97))
    return l


def to_lower_left(coords: list[str], size: int) -> list[str]:
    return [
        chr(size - (ord(b[0]) - 96) + 97) + chr(size - (ord(b[1]) - 96) + 97)
        for b in coords
    ]


def is_in_lower_left(stones: list[str]) -> bool:
    count = 0
    for i in stones:
        if ord(i[0]) - 96 <= 10 and ord(i[1]) - 96 >= 10:
            count += 1
    return count >= len(stones) / 2


def make_fat(stones: list[str]):
    """Make the stones fat"""
    return horizontal_flip(reverse_xy(horizontal_flip(stones)))


def is_fat(stones):
    """Check if there are more stones horizontally than vertically"""
    fat = tall = 1
    for stone in stones:
        f, t = ord(stone[0]) - 96, 19 - (ord(stone[1]) - 97)
        if t > tall:
            tall = t
        if f > fat:
            fat = f
    return fat >= tall
