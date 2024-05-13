

import sys
sys.path.append('C:/Users/nicol/OneDrive/Escritorio/prog/prog/PROYECTO/PROYECTO2/0-2-proyecto-segunda-parte-nicolle-y-daniela/Controllers')

from Controllers.EveController import EveController
from View.View import View
from Model.Evento import Evento



def main():
    controller_instance = EveController()
    controller_instance.showmenu()

if __name__ == '__main__':
    main()
