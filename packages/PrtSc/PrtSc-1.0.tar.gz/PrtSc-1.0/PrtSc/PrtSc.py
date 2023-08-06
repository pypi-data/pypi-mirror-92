import pyscreenshot as PrtScr
class PrtSc:
    def __init__(self,setVisible,filename):
        image = PrtScr.grab()
        if setVisible==True:
            image.show() 
        image.save(filename)