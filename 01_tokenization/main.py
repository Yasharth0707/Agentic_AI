import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")

text="Hello bro how are you doing today? I hope everything is going well. Let's catch up soon!"

tokens=enc.encode(text)


# Tokens: [13225, 3714, 1495, 553, 481, 5306, 4044, 30, 357, 5498, 5519, 382, 2966, 1775, 13, 41021, 3494, 869, 6780, 0]
print("Tokens:", tokens)

decoded=enc.decode([13225, 3714, 1495, 553, 481, 5306, 4044, 30, 357, 5498, 5519, 382, 2966, 1775, 13, 41021, 3494, 869, 6780, 0])
print("Decoded:", decoded)