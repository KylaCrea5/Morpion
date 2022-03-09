import pygame,sys
pygame.init()
police = pygame.font.Font('led.ttf',70)
import random as rd


class Morpion :
    def __init__(self,profondeur):
        self.J1="X"
        self.IA="O"
        self.ecran=pygame.display.set_mode((600,600))
        self.grille=Grille(self.ecran)
        self.ecran.fill('red')
        self.compteur=0
        self.profondeur=profondeur
        self.alpha=-1000
        self.beta=1000

        
    
    def test_fin_jeu(self,player):
        for i in range(3):
            if self.grille.grille[i][0]==self.grille.grille[i][1]==self.grille.grille[i][2]==player:
                return player
        for j in range(3):
            if self.grille.grille[0][j]==self.grille.grille[1][j]==self.grille.grille[2][j]==player:
                return player
        if self.grille.grille[0][0]==self.grille.grille[1][1]==self.grille.grille[2][2]==player:
            return player
        if self.grille.grille[2][0]==self.grille.grille[1][1]==self.grille.grille[0][2]==player:
            return player
        for i in range(3):
            for j in range(3):
                if self.grille.grille[i][j]==None:
                    return True
        return False
    
    
    def jeu(self):
        pygame.display.set_caption("MORPION")
        players=[self.IA,self.J1]
        fin=False
        
        clock = pygame.time.Clock()
        
        while not fin:
            time = clock.tick(10)  
            for event in pygame.event.get():
                player=players[self.compteur%2]
                
                if player==self.IA :
                    self.intelligence_artificielle(self.profondeur,self.alpha,self.beta)
                        
                else:
                    if player==self.J1 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                        position = event.pos
                        position_x ,position_y = position[1]//200 ,position[0]//200
                        self.grille.fixer_la_valeur(position_x, position_y, self.J1)
                     
                if self.test_fin_jeu(player)==player or self.test_fin_jeu(player)==False:
                    fin=True
                    
                elif self.grille.compteur_on:
                    self.compteur += 1
                    self.grille.compteur_on = False
                    
            self.ecran.fill((240,240,240))
            self.grille.afficher()
            pygame.display.flip()
            
                    
        if self.test_fin_jeu(player)==player:
            if player == self.IA :
                texte = police.render(f"Gagnant : IA",True,pygame.Color("#000000"))
            else:
                texte = police.render(f"Gagnant : J1",True,pygame.Color("#000000"))
            rectTexte = texte.get_rect()
            rectScreen = self.ecran.get_rect()
            rectTexte.center = rectScreen.center
            self.ecran.blit(texte,rectTexte)
            pygame.display.flip()
                    
        else:
            texte = police.render("Egalité",True,pygame.Color("#000000"))
            rectTexte = texte.get_rect()
            rectScreen = self.ecran.get_rect()
            rectTexte.center = rectScreen.center
            self.ecran.blit(texte,rectTexte)
            pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
        
        
    def intelligence_artificielle(self,depth,al,be): #Joue le coup
        max_i,max_j=None,None
        maximum = -10000
        jeu = self.grille.grille # On copie le jeu dans une variable temporaire
        for i in range(3):
            for j in range(3):
                if jeu[i][j] == None: # La case est libre: on lance l'IA
                    jeu[i][j] = self.IA
                    tmp = self.valeur_mini(jeu, depth-1,al,be)
                
                    if tmp > al:
                        al = tmp
                        max_i = i
                        max_j = j
                    jeu[i][j] = None
        if self.test_fin_jeu(self.IA)==True:
            self.grille.fixer_la_valeur(max_i, max_j, self.IA)#On joue le (meilleur) coup
    
        
    def valeur_maxi(self,jeu, depth, al, bet):
        maximum = -10000
        if depth == 0 or self.test_fin_jeu(self.J1)!=True or self.test_fin_jeu(self.IA)!=True:
            return self.evaluer(jeu)
        for i in range(3):
            for j in range(3):
                if jeu[i][j] == None: # La case est libre: on lance l'IA
                    jeu[i][j] = self.IA
                    al = max(al,self.valeur_mini(jeu, depth-1,al,bet))

                    if bet < al:
                        maximum = al;
                    
                    jeu[i][j] = None
        return al
    
    
    def valeur_mini(self,jeu, depth,al,bet):

        minimum = 10000

        if depth == 0 or self.test_fin_jeu(self.J1)!=True or self.test_fin_jeu(self.IA)!=True:
            return self.evaluer(jeu)
    
        for i in range(3):
            for j in range(3):
                if jeu[i][j] == None: # La case est libre: on lance le joueur
            
                    jeu[i][j] = self.J1
                    tmp = self.valeur_mini(jeu, depth-1,al,bet)
                    jeu[i][j] = None

                    if al < tmp:
                        al = tmp
                    if bet <= al:
                        return al
        return al
    
    def nb_series(jeu, series_j1, series_j2, n = 0): #Compte le nombre de séries de n pions alignés de chacun des joueurs
        series_j1, series_j2 = 0, 0
        compteur1, compteur2 = 0, 0
        largeur=len(jeu[0])
        
         #Diagonale descendante
        for i in range(largeur):
            if jeu[i][i] == 1:
        
                compteur1+=1
                compteur2 = 0

                if compteur1 == n:
                    series_j1+=1
        
            elif jeu[i][i] ==2:
                compteur2+=1
                compteur1 = 0
     
                if compteur2 == n:
                     series_j2+=1

        compteur1, compteur2 = 0,0

        #Diagonale montante
        for i in range(largeur):
            if jeu[i][largeur-i] == 1:
                compteur1+=1
                compteur2 = 0

                if compteur1 == n:
                    series_j1+=1
            elif jeu[i][largeur-i] == 2:
                compteur2+=1
                compteur1 = 0
     
                if compteur2 == n:
                     series_j2+=1

        #En ligne
        for i in range(largeur):
            compteur1, compteur2 = 0, 0
       
            #Horizontalement
            for j in range(largeur):
                if jeu[i][j] == 1:
                    compteur1+=1
                    compteur2 = 0

                    if compteur1 == n:
                        series_j1+=1
            
                elif jeu[i][j] == 2:
                    compteur2+=1
                    compteur1 = 0

                    if compteur2 == n:
                        series_j2+=1

            compteur1,compteur2  = 0, 0

            #Verticalement
            for j in range(largeur):
                if jeu[j][i] == 1:
                    compteur1+=1
                    compteur2 = 0

                    if compteur1 == n:
                        series_j1+=1
            
                elif jeu[j][i] == 2:
                    compteur2+=1
                    compteur1 = 0

                    if compteur2 == n:
                        series_j2+=1

    def evaluer(self,jeu): #Fonction d'évaluation d'un plateau
        gagnant=None
        nb_de_pions = 0
    
        #On compte le nombre de pions présents sur le plateau
        for i in range(3):
            for j in range(3):
                if jeu[i][j] != None:
                    nb_de_pions+=1

        if self.test_fin_jeu(self.J1)!=True or self.test_fin_jeu(self.IA)!=True:
            gagnant = self.test_fin_jeu(self.J1)
        
        if gagnant == self.IA:
            return 1000 - nb_de_pions;
        
        elif gagnant == self.J1:
            return -1000 + nb_de_pions
        else:
            return 0

        #On compte le nombre de séries de 2 pions alignés de chacun des joueurs
        series_j1 = 0
        series_j2 = 0
    
        nb_series(jeu, series_j1, series_j2, 2)

        return series_j1 - series_j2 
             
 

class Grille():
    def __init__(self,ecran):
        self.ecran=ecran
        self.lignes=[((200,0),(200,600)), ((400,0),(400,600)), ((0,200),(600,200)), ((0,400),(600,400))]
        self.grille=[[None,None,None],
                      [None,None,None],
                      [None,None,None]
                      ]
        self.compteur_on=False
      
        
        
    def afficher(self):
        for ligne in self.lignes :
            pygame.draw.line(self.ecran,(0,0,0),ligne[0],ligne[1],2)
        for y in range(0,len(self.grille)):
            for x in range(0,len(self.grille)):
                if self.grille[y][x] == 'X' :
                    pygame.draw.line(self.ecran, (255, 0, 0), (x * 200, y * 200), (200 + (x * 200), 200 + (y * 200)), 7) 
                    pygame.draw.line(self.ecran, (255, 0, 0), ((x * 200), 200 + (y * 200)), (200 + (x * 200), (y * 200)),7)

                elif self.grille[y][x] == 'O' :
                    pygame.draw.circle(self.ecran, (0, 0, 255), (100 + (x * 200), 100 + (y * 200)), 100, 7)
    
    def fixer_la_valeur(self,x,y,valeur):
        if self.grille[x][y]==None:
            self.grille[x][y]=valeur
            self.compteur_on=True
           
    
    
# On détermine la difficulté de l'IA
info_niveau=0       
info_niveau=int(input("Niveau : 1(facile) à 9(difficile)\nVotre choix : "))
while info_niveau<1 or info_niveau>9:
    print("Saisie invalide")
    info_niveau=int(input("Niveau : 1(facile) à 9(difficile)\nVotre choix : "))

game=Morpion(info_niveau)
game.jeu()



