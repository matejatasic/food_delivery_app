import sys
import random
from pyfiglet import Figlet

def main():
    figlet = Figlet()

    if len(sys.argv) == 2:
        sys.exit("Invalid Usage")
    if len(sys.argv) == 3:
        invalid_argument = sys.argv[1] not in ["-f", "--font"]
        invalid_font = sys.argv[2] not in figlet.getFonts()

        if invalid_argument or invalid_font:
            sys.exit("Invalid usage")

    text = input("Enter text: ")

    font_string = determine_font(figlet)
    figlet.setFont(font=font_string)
    print(figlet.renderText(text))

def determine_font(figlet: Figlet) -> str:
    if len(sys.argv) == 1:
        random_num = random.randint(0, len(figlet.getFonts()))
        return figlet.getFonts()[random_num]

    return sys.argv[2]

if __name__ == "__main__":
    main()