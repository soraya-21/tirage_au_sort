from fpdf import FPDF

# Créer une classe qui hérite de FPDF
#pdf = FPDF('P', 'mm')
#pdf.add_page(orientation= 'l')

# # le cardre + la barre blanche
# pdf.image('images\mquette\\demiRec.png', x = 10, y = 20)
# pdf.image('images\mquette\\demiRec2.png', x = 90, y = 20)
# pdf.image('images\\mquette\\barre.png', x = 90, y = 35)

# #logo dommicille et exterieur
# pdf.image('images\\mquette\\home.png', x = 50,y=30,w=25 ,h=25)
# pdf.image('images\\mquette\\away.png',x = 130,y=30, w=25 ,h=25)

# #Equipe a domicile
# pdf.image('logos\\Atalanta_Bergame.png',x = 20,y=70, w=35 ,h=35)
# pdf.image('logos\\Aston_Villa.png', x = 60, y=70, w=35,h=35)
# pdf.image('logos\\Celtic_fc.png', x = 20,y=130, w=35,h=35)
# pdf.image('logos\\Logo_Atletico.png', x = 60, y=130, w=35,h=35)

# #Equipe a l'exterieur
# pdf.image('logos\\Paris_Saint-Germain.png', x = 110,y=130, w=35,h=35)
# pdf.image('logos\\manchester-city.png', x = 110,y=70, w=35,h=35)
# pdf.image('logos\\LOSC_Lille.png', x = 150,y=130, w=35,h=35)
# pdf.image('logos\\crvena-zvezda.png', x = 150,y=70, w=35,h=35)

# # Affichage du PDF
# pdf.image('logos\\SLB.png', x =200,y=65, w=85,h=85)
# pdf.output('tuto1.pdf')

# Créer une classe qui hérite de FPDF
class MonPDF(FPDF):

    def _background(self):
           
        self.image('images\m3.jpg',x= 0,y=0)

#logo dommicile et exterieur
    def _logodoEx(self):

        self.image('images\\mquette\\home.png', x = 50,y=30,w=25 ,h=25)
        self.image('images\\mquette\\away.png',x = 130,y=30, w=25 ,h=25)

#le cardre et la barre blanche sur limage
    def _cadre(self):

         self.image('images\mquette\\demiRec.png', x = 10, y = 20)
         self.image('images\mquette\\demiRec2.png', x = 90, y = 20)
         self.image('images\\mquette\\barre.png', x = 90, y = 35)

#Equipe principal

    def _EquipePrincipal(self):
         self.image('logos\\SLB.png', x =200,y=65, w=85,h=85)

# Equipe a domicile
    def _equipeDomicile(self):
            self.image('logos\\Atalanta_Bergame.png',x = 20,y=70, w=35 ,h=35)
            self.image('logos\\Aston_Villa.png', x = 60, y=70, w=35,h=35)
            self.image('logos\\Celtic_fc.png', x = 20,y=130, w=35,h=35)
            self.image('logos\\Logo_Atletico.png', x = 60, y=130, w=35,h=35)

            
#Equipe a l'exterieur
    def _equipeExterieur(self):
            self.image('logos\\Paris_Saint-Germain.png', x = 110,y=130, w=35,h=35)
            self.image('logos\\manchester-city.png', x = 110,y=70, w=35,h=35)
            self.image('logos\\LOSC_Lille.png', x = 150,y=130, w=35,h=35)
            self.image('logos\\crvena-zvezda.png', x = 150,y=70, w=35,h=35)


    def make_draw(self):
            self.add_page()
            self._background()
            self._logodoEx()
            self._EquipePrincipal()
            self._cadre()
            self._equipeExterieur()
            self._equipeDomicile()
           
            self.output("monpdf.pdf")


mon_pdf = MonPDF(orientation='L')
mon_pdf.make_draw()