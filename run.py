from commands.scrap import scrap
from commands.get_channel_information import get_channel_information
from click import group

@group
def main():
    pass

main.add_command(scrap)
main.add_command(get_channel_information)

if __name__ == "__main__":
    main()