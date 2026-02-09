def numerology_prediction(expression):
    if expression == "Calm":
        return (
            "Moon (Number 2)",
            "You are intuitive, emotionally balanced, and spiritually receptive."
        )

    if expression == "Happy":
        return (
            "Sun (Number 1)",
            "Leadership energy, confidence, and success are strong in you."
        )

    if expression == "Angry":
        return (
            "Mars (Number 9)",
            "Strong willpower, aggression, and transformative life events."
        )

    return (
        "Unknown",
        "More clarity is needed. Try a clearer image."
    )
