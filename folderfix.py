import glob
from pathlib import Path

# Wordt gebruikt als standaard argument voor de functie get_empty()
rootdir = Path().absolute()


# Main functie met inputs vanuit CMD
def main():
    inputstr = input("Voer een path in om mogelijk lege folders te vinden:\n")
    if not inputstr:
        inputdir = rootdir
    else:
        inputdir = Path(inputstr)

    if not Path.exists(inputdir):
        print("Het ingevoerde path bestaat niet!")
    else:
        empty_dirs = get_empty(inputdir)
        if empty_dirs:
            print(f"\n\nFolders in {inputdir} zonder bestanden:")
            print(
                "-----------------------------------------------------------------------------"
            )
            for path in empty_dirs:
                print(path)
            print(
                "-----------------------------------------------------------------------------"
            )

            delete_empty = input("Lege folders verwijderen? (y/n)\n")
            removed = []
            if delete_empty.lower() == "y":
                for path in empty_dirs:
                    path.rmdir()
                    removed.append(path)

                # Checken of de folders verwijderen zijn en weergeven welke er verwijderd zijn
                print("Verwijderde folders:")
                for path in removed:
                    if not Path.exists(path):
                        print(path)
        else:
            print(f"Er zijn geen lege folders gevonden in {inputdir}")


# Functie voor het maken van een lijst van lege directories vanaf de startdirectory
def get_empty(startdir=rootdir):
    empty_list = []
    folders = [path for path in glob.glob(f"{startdir}/*/**/", recursive=True)]
    files = [str(x) for x in startdir.glob("**/*") if x.is_file()]
    for folder in folders:
        has_file = False
        for file in files:
            if folder in file:
                has_file = True
        if not has_file:
            empty_list.append(folder)

        # Lijst sorteren op lengte, anders werkt het verwijderen niet goed in functie main()
        empty_list.sort(key=len, reverse=True)
        result = [Path(x) for x in empty_list]
    return result


main()
