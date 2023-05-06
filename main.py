from LibManSystem import LibManSystem


def main():
    library_system = None
    try:
        library_system = LibManSystem()
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        if library_system is not None:
            library_system.database.close()


if __name__ == "__main__":
    main()
