import generation

print(
    generation.generate(
        [
            {"role": "user", "parts": [{"text": "Give me some life advice"}]},
        ],
        system="You are a cool guy.",
    )
)
