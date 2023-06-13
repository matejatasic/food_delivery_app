import re

def main():
    text: str = input("Text: ")
    letters_count: int = count_letters(text)
    words_count: int = len(text.split(" "))
    sentences = re.split(r"[\.!?]", text.strip())
    # For some reason an empty string
    # appears at the end of the list
    # and therefore it is removed
    sentences.pop()
    sentences_count: int = len(sentences)

    letters_per_100_words = letters_count / (words_count / 100)
    sentences_per_100_words = sentences_count / (words_count / 100)

    index = round(0.0588*letters_per_100_words - 0.296*sentences_per_100_words - 15.8)
    
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")

def count_letters(text: str) -> int:
    letters_count = 0

    for char in text:
        if char.isalpha():
            letters_count += 1

    return letters_count

main()