#!venv/bin/python3

from modules import oikotie

def CasaEx():

    items_oikotie = oikotie.fetch_data()
    for item in items_oikotie:
        print (item)


if __name__ == "__main__":
    #CasaEx()
    print ("moro")