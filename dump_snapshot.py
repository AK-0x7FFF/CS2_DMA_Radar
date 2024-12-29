from memory.process import CS2


def main() -> None:
    CS2.meow_mode()
    CS2.setup().dump_offset_snapshot("offset_snapshot.pkl")

if __name__ == '__main__':
    main()