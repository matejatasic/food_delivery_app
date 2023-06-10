def main():
    greeting = str(input("Greeting: "))

    if "hello" in greeting.lower():
        print("$0")
    elif greeting[0].lower() == "h":
        print("$20")
    else:
        print("$100")

if __name__ == "__main__":
    main()