from datetime import datetime


NUMEROLOGY_MAP = {
    1: "Sun energy: leadership, confidence, and initiative.",
    2: "Moon energy: intuition, balance, and sensitivity.",
    3: "Jupiter energy: wisdom, creativity, and growth.",
    4: "Rahu energy: discipline, structure, and persistence.",
    5: "Mercury energy: adaptability, communication, and curiosity.",
    6: "Venus energy: love, harmony, and beauty.",
    7: "Ketu energy: introspection, spirituality, and analysis.",
    8: "Saturn energy: ambition, responsibility, and endurance.",
    9: "Mars energy: courage, drive, and transformation.",
}


def reduce_to_single_digit(value: int) -> int:
    while value > 9:
        value = sum(int(d) for d in str(value))
    return value


def calculate_moolank_and_bhagyank(dob: str):
    try:
        dt = datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        raise ValueError("DOB must be in YYYY-MM-DD format")

    day = dt.day
    moolank = reduce_to_single_digit(day)

    digits_sum = sum(int(d) for d in dt.strftime("%d%m%Y"))
    bhagyank = reduce_to_single_digit(digits_sum)

    prediction = NUMEROLOGY_MAP.get(bhagyank, "Your numbers indicate a unique path of growth.")
    return moolank, bhagyank, prediction
