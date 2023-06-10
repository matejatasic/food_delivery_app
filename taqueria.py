def main():
    total = 0
    items = {
        "Baja Taco": 4.00,
        "Burrito": 7.50,
        "Bowl": 8.50,
        "Nachos": 11.00,
        "Quesadilla": 8.50,
        "Super Burrito": 8.50,
        "Super Quesadilla": 9.50,
        "Taco": 3.00,
        "Tortilla Salad": 8.00
    }

    try:
        while True:
            item = input("Choose Item: ")
            if(item == ""):
                raise EOFError()
            total += items.get(item.lower().title(), 0)
    except EOFError:
        print("\n")
        print(f"Total: ${total:.2f}")

main()