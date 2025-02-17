#Versao 1.0 Beta
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
from tkinter import Label

import math

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image

import webbrowser

janela = Tk()


janela.iconbitmap("RINA-ICO.ico")



class calculo_das_dimensoes():
    def calculo_geometria(self):

        if self.a0_entry.get().strip() == "" or self.b0_entry.get().strip() == "" or self.pp_entry.get().strip() == "" or \
           self.tadm_entry.get().strip() == "" :
                
            # Exibir a mensagem de erro
            msg = "PARA REALIZAR O DIMENSIONAMENTO É NECESSÁRIO PREENCHER TODOS OS DADOS DE ENTRADA"
            messagebox.showinfo("ERRO!!!!", msg)
            return  # Não continue com o cálculo, já que os campos não foram preenchidos
                
        else:
            if float(self.a0_entry.get().strip()) > 100 or float(self.b0_entry.get().strip()) > 100:
                # Exibir a mensagem de erro
                msg = "VERIFIQUE O PILAR! TAMANHO INCOMPATÍVEL!"
                messagebox.showinfo("ERRO!!!!", msg)
                return  # Não continue com o cálculo, já que os campos não foram preenchidos   
            else:
                if float(self.pp_entry.get().strip()) > 10000 or float(self.tadm_entry.get().strip()) > 1500:
                    # Exibir a mensagem de erro
                    msg = "VALOR DO PESO PRÓPRIO OU DA TENSÃO ADMISSÍVEL MAIOR DO QUE O PERMITIDO!"
                    messagebox.showinfo("ERRO!!!!", msg)
                    return  # Não continue com o cálculo, já que os campos não foram preenchidos  
                else:
                    if float(self.pp_entry.get().strip()) < 300 or float(self.tadm_entry.get().strip()) < 100:
                        # Exibir a mensagem de erro
                        msg = "VALOR DO PESO PRÓPRIO OU DA TENSÃO ADMISSÍVEL MENOR DO QUE O PERMITIDO!"
                        messagebox.showinfo("ERRO!!!!", msg)
                        return  # Não continue com o cálculo, já que os campos não foram preenchidos  

                    else:
                    
                        if float(self.a0_entry.get().strip()) < 14 or float(self.b0_entry.get().strip()) < 14:
                            # Exibir a mensagem de erro
                            msg = "VERIFIQUE O PILAR! O ÍTEM 13.2.3 DA NBR 6118/2023 PREVÊ QUE UM PILAR DEVE TER SEU MENOR LADO DE NO MÍNIMO 14 CM"
                            messagebox.showinfo("ERRO!!!!", msg)
                            return  # Não continue com o cálculo, já que os campos não foram preenchidos
                        else:
                        
                            if  float(self.a0_entry.get().strip()) * float(self.b0_entry.get().strip()) < 360:
                                # Exibir a mensagem de erro
                                msg = "VERIFIQUE O PILAR! O ÍTEM 13.2.3 DA NBR 6118/2023 PREVÊ QUE UM PILAR DEVE TER NO MÍNIMO 360 CM²"
                                messagebox.showinfo("ERRO!!!!", msg)
                                return  # Não continue com o cálculo, já que os campos não foram preenchidos
                                
                            else:
                    
                                # Obtendo valores dos dados de entrada
                                self.a0 = float(self.a0_entry.get())
                                self.b0 = float(self.b0_entry.get())
                                self.p = float(self.pp_entry.get())
                                self.tadm = float(self.tadm_entry.get())
                                self.c = float(self.coeficiente_selecionado1.get())
                                self.fck = float(self.coeficiente_selecionado2.get())
                                self.fyk = float(self.coeficiente_selecionado3.get())
                                self.barra_a = float(self.coeficiente_selecionado4.get())
                                self.barra_b = float(self.coeficiente_selecionado5.get())
                    
                                
                                 # Cálculo da área da sapata
                                areasap = (round(1.1 * self.p) / self.tadm) * 10000  
                                delta = (self.b0 - self.a0) ** 2 - 4 * (-areasap)
                                a = (-(self.b0 - self.a0) + (delta) ** 0.5) / 2
                                b = (a - self.a0) + self.b0
                            
                                # a_m5 e b_m5 para múltiplos de 5
                                self.a_m5 = math.ceil(a / 5) * 5
                                self.b_m5 = math.ceil(b / 5) * 5
                                self.l = math.ceil(((a - self.a0) / 2) / 5) * 5
                                
                                # condições para a_m5 e b_m5
                                if self.a_m5 > 60:
                                    self.a_m5 = self.a_m5
                                else:
                                    self.a_m5 = 60
                            
                                if self.b_m5 > 60:
                                    self.b_m5 = self.b_m5
                                else:
                                    self.b_m5 = 60
                            
                                #LABEL PARA REPOSTA DE A
                                self.label_x = Label(self.frame_4, bg = "white", anchor="center",font=("Arial", 11))
                                self.label_x.place(relx=0.30, rely=0.03, relwidth= 0.50, relheight=0.03)
                                self.label_x.config(text=f"{self.a_m5}")
                            
                                # LABEL PARA REPOSTA DE B
                                self.label_y = Label(self.frame_4, bg = "white", anchor="center",font=("Arial", 11))
                                self.label_y.place(relx=0.30, rely=0.0875, relwidth= 0.5, relheight=0.03)
                                self.label_y.config(text=f"{self.b_m5}")
                            
                                # LABEL PARA REPOSTA DE L
                                self.label_z = Label(self.frame_4, bg = "white", anchor="center",font=("Arial", 11))
                                self.label_z.place(relx=0.30, rely=0.145, relwidth= 0.5, relheight=0.03)
                                self.label_z.config(text=f"{self.l}")  

    def calculo_alturas(self):
        # Calculando a altura útil (hu) e outras variáveis
        self.hu = math.ceil(((self.a_m5 - self.a0) / 3) / 5) * 5
        self.du = round(self.hu - (self.c + 1))
        
        self.hu01 = math.ceil((self.hu / 3) / 5) * 5
        self.hu02 = 15
        if self.hu01 > self.hu02:
            self.hu0 = self.hu01
        else:
            self.hu0 = self.hu02

        self.oa = 0.85 * ((self.fck*1000) / 1.96)

    def verificacao(self):
        # Cálculos de altura útil (dv) e total (hv)
        self.dv1 = round(self.a_m5 - self.a0) / 4
        self.dv2 = round(math.ceil(((1.44 * (self.p / self.oa) ** 0.5) * 100) / 5) * 5)
        if self.dv1 > self.dv2:
            self.dv = self.dv1
        else:
            self.dv = self.dv2

        # Altura total (hv)
        self.hv = round(self.dv + (self.c + 1))

        # Cálculo de h0
        self.hv01 = math.ceil((self.hv / 3) / 5) * 5
        self.hv02 = 15
        if self.hv01 > self.hv02:
            self.hv0 = self.hv01
        else:
            self.hv0 = self.hv02
            
    def condicoes(self):
        # Comparações para definir os valores finais
        if self.hu > self.hv:
            self.h = self.hu
        else:
            self.h = self.hv
        
        if self.du > self.dv:
            self.d = self.du
        else:
            self.d = self.dv
        
        if self.hu0 > self.hv0:
            self.h0 = self.hu0
        else:
            self.h0 = self.hv0

        # Verificação do ângulo
        self.tan = round((self.h - self.h0) / self.l, 2)
        self.tanα = round(math.degrees(math.atan(self.tan)), 2)
        
        # Exibir resultado no label
        self.label_b = Label(self.frame_4, bg="white", anchor="center", font=("Arial", 11))
        self.label_b.place(relx=0.30, rely=0.26, relwidth=0.5, relheight=0.03)
        self.label_b.config(text=f"{self.h}")

        self.label_a = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_a.place(relx=0.30, rely=0.2025, relwidth= 0.5, relheight=0.03) 
        self.label_a.config(text=f"{self.d}")

        self.label_c = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_c.place(relx=0.30, rely=0.3175, relwidth= 0.5, relheight=0.03) 
        self.label_c.config(text=f"{self.h0}")

        self.label_d = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_d.place(relx=0.30, rely=0.375, relwidth= 0.5, relheight=0.03)  
        self.label_d.config(text=f"{self.tanα}")


    def forcas_de_tracao(self):

        # Taxa de Armadura tração

        self.ty = round((self.p*(self.a_m5-self.a0))/(8*self.d),2)
        self.tx = round((self.p*(self.b_m5-self.b0))/(8*self.d),2)

        # Armadura mínima

        self.asminA = round((0.0015 * self.a_m5 * self.d),2)
        self.asminB = round((0.0015 * self.b_m5 * self.d),2)
   
        # Área de aço

        self.asy = round((1.61*self.ty)/(self.fyk/10),2)
        self.asx = round((1.61*self.tx)/(self.fyk/10),2)

        if self.asy > self.asminA:
            self.tay = self.asy
        else:
            self.tay = self.asminA

        if self.asx > self.asminB:
            self.tax = self.asx
        else:
            self.tax = self.asminB

        self.label_e = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_e.place(relx=0.30, rely=0.4325, relwidth= 0.5, relheight=0.03) 
        self.label_e.config(text=f"{self.ty}")

        self.label_f = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_f.place(relx=0.30, rely=0.49, relwidth= 0.5, relheight=0.03) 
        self.label_f.config(text=f"{self.tx}")
        
        self.label_g = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_g.place(relx=0.30, rely=0.5475, relwidth= 0.5, relheight=0.03) 
        self.label_g.config(text=f"{self.asminA}")

        self.label_h = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_h.place(relx=0.30, rely=0.605, relwidth= 0.5, relheight=0.03) 
        self.label_h.config(text=f"{self.asminB}")

        self.label_i = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_i.place(relx=0.30, rely=0.6625, relwidth= 0.5, relheight=0.03) 
        self.label_i.config(text=f"{self.asy}")

        self.label_j = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_j.place(relx=0.30, rely=0.72, relwidth= 0.5, relheight=0.03) 
        self.label_j.config(text=f"{self.asx}")


    def detalhamento(self):
        
        self.barra_escolhida_a = round(((math.pi*((self.barra_a)/(2))**2)/100),2)
        self.barra_escolhida_b = round(((math.pi*((self.barra_b)/(2))**2)/100),2)

        self.nb = math.ceil(self.tax/self.barra_escolhida_b)
        self.na = math.ceil(self.tay/self.barra_escolhida_a)

        self.esp_b = math.floor((self.b_m5 - 2*self.c) / (self.na - 1))
        self.esp_a = math.floor((self.a_m5 - 2*self.c) / (self.nb - 1))

        self.gancho_a= round((8 * self.barra_a)/10)
        self.gancho_b= round((8 * self.barra_b)/10)

        self.label_k = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_k.place(relx=0.30, rely=0.7775, relwidth= 0.5, relheight=0.03) 
        self.label_k.config(text=f"{self.na}")
        
        self.label_l = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_l.place(relx=0.30, rely=0.835, relwidth= 0.5, relheight=0.03) 
        self.label_l.config(text=f"{self.nb}")
        
        self.label_m = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_m.place(relx=0.30, rely=0.8925, relwidth= 0.5, relheight=0.03) 
        self.label_m.config(text=f"{self.esp_a}")
        
        self.label_n = Label(self.frame_4, bg = "white", anchor="center", font=("Arial", 11))
        self.label_n.place(relx=0.30, rely=0.95, relwidth= 0.5, relheight=0.03) 
        self.label_n.config(text=f"{self.esp_b}")


    def planta(self):

        self.fig, ax = plt.subplots(figsize=(40, 40))

        x_maior = [0, self.b_m5, self.b_m5, 0, 0]  # coordenadas x dos vértices da sapata (B)
        y_maior = [0, 0, self.a_m5, self.a_m5, 0]  # coordenadas y dos vértices da sapata (A)

        # Coordenadas dos quatro pontos do quadrado menor (pilar)
        x_menor = [((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)+(self.b0/2)), 
                   ((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)-(self.b0/2))]  # coordenadas x do pilar B0
        
        y_menor = [((self.a_m5/2)-(self.a0/2)), ((self.a_m5/2)-(self.a0/2)), ((self.a_m5/2)+(self.a0/2)), 
                   ((self.a_m5/2)+(self.a0/2)), ((self.a_m5/2)-(self.a0/2))]  # coordenadas y do pilar A0

        # Coordenadas dos quatro pontos do colarinho
        x_col = [((self.b_m5/2)-(self.b0/2))-2.5, ((self.b_m5/2)+(self.b0/2))+2.5, ((self.b_m5/2)+(self.b0/2))+2.5, 
                 ((self.b_m5/2)-(self.b0/2))-2.5, ((self.b_m5/2)-(self.b0/2))-2.5]  # coordenadas x do colarinho
        
        y_col = [((self.a_m5/2)-(self.a0/2))-2.5, ((self.a_m5/2)-(self.a0/2))-2.5, ((self.a_m5/2)+(self.a0/2))+2.5, 
                 ((self.a_m5/2)+(self.a0/2))+2.5, ((self.a_m5/2)-(self.a0/2))-2.5]  # coordenadas y do colarinho


        # Plote sapata
        plt.plot(x_maior, y_maior, 'k-', linewidth=1)  # sapata

        # Plote pilar
        plt.plot(x_menor, y_menor, 'k-', linewidth=1)  # pilar

        # Plote colarinho
        plt.plot(x_col, y_col, 'k-', linewidth=1)  # colarinho

        # Preenchendo a área com cor marrom (sapata)
        plt.fill(x_maior, y_maior, 'gray', alpha=0.5)  # cor cinza com transparência média

        # Preenchendo a área do pilar
        plt.fill(x_menor, y_menor, 'gray', alpha=0.7)  # cor cinza com menor transparência 

        # Preenchendo a área do colarinho
        plt.fill(x_col, y_col, 'gray', alpha=0.3)  # cor cinza com ainda mais transparência

        # Plotagem da linha do balanço entre colarinho o pilar e a sapata
        for i in range(4):
            # Desenha a linha de ligação
            plt.plot([x_col[i], x_maior[i]], [y_col[i], y_maior[i]], 'k-', linewidth=1)

        # GRÁFICO DAS COTAS DA SAPATA - LADO A
        x_cota1 = [-10, -10]
        y_cota1 = [0, self.a_m5]
        plt.plot(x_cota1, y_cota1, 'k-', linewidth=1) 

        x_cota2 = [-7.5, -12.5]
        y_cota2 = [-0,  0]
        plt.plot(x_cota2, y_cota2, 'k-', linewidth=1)  # BAIXA

        x_cota3 = [-7.5, -12.2]
        y_cota3 = [self.a_m5,  self.a_m5]
        plt.plot(x_cota3, y_cota3, 'k-', linewidth=1)  # ALTA

        # GRÁFICO DAS COTAS DA SAPATA - LADO B
        x_cota4 = [0, self.b_m5]
        y_cota4 = [self.a_m5+10, self.a_m5+10]
        plt.plot(x_cota4, y_cota4, 'k-', linewidth=1)  

        x_cota5 = [0, 0]
        y_cota5 = [self.a_m5+7.5,  self.a_m5+12.5]
        plt.plot(x_cota5, y_cota5, 'k-', linewidth=1)  # ESQUERDA

        x_cota6 = [self.b_m5, self.b_m5]
        y_cota6 = [self.a_m5+7.5,  self.a_m5+12.5]
        plt.plot(x_cota6, y_cota6, 'k-', linewidth=1)  # DIREITA

        # GRÁFICO DAS COTAS DO PILAR - LADO A0

        x_cota7 = [(((self.b_m5/2)-(self.b0/2))-10), (((self.b_m5/2)-(self.b0/2))-10)]
        y_cota7 = [((self.a_m5/2)-(self.a0/2)), ((self.a_m5/2)+(self.a0/2))]
        plt.plot(x_cota7, y_cota7, 'k-', linewidth=1)  

        x_cota8 = [(((self.b_m5/2)-(self.b0/2))-7.5), (((self.b_m5/2)-(self.b0/2))-12.5)]
        y_cota8 = [((self.a_m5/2)-(self.a0/2)), ((self.a_m5/2)-(self.a0/2))]
        plt.plot(x_cota8, y_cota8, 'k-', linewidth=1)  # BAIXO

        x_cota9 = [(((self.b_m5/2)-(self.b0/2))-7.5), (((self.b_m5/2)-(self.b0/2))-12.5)]
        y_cota9 = [((self.a_m5/2)+(self.a0/2)), ((self.a_m5/2)+(self.a0/2))]
        plt.plot(x_cota9, y_cota9, 'k-', linewidth=1)  # ALTA
        
        
        # GRÁFICO DAS COTAS DO PILAR - LADO B0
        
        x_cota10 = [(((self.b_m5/2)-(self.b0/2))), (((self.b_m5/2)+(self.b0/2)))]
        y_cota10 = [(((self.a_m5/2)-(self.a0/2))-10), (((self.a_m5/2)-(self.a0/2))-10)]
        plt.plot(x_cota10, y_cota10, 'k-', linewidth=1)  
        
        x_cota11 = [(((self.b_m5/2)-(self.b0/2))), (((self.b_m5/2)-(self.b0/2)))]
        y_cota11 = [(((self.a_m5/2)-(self.a0/2))-7.5), (((self.a_m5/2)-(self.a0/2))-12.5)]
        plt.plot(x_cota11, y_cota11, 'k-', linewidth=1)  # ESQUERDA
        
        x_cota12 = [((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)+(self.b0/2))]
        y_cota12 = [(((self.a_m5/2)-(self.a0/2))-7.5), (((self.a_m5/2)-(self.a0/2))-12.5)]
        plt.plot(x_cota12, y_cota12, 'k-', linewidth=1)  # DIREITA
        
        # TEXTO DA COTA DA SAPATA
        plt.text(self.b_m5 / 2, self.a_m5+15, str(round(self.b_m5)), ha='center')  # Legenda do eixo x da sapata
        plt.text(-20, self.a_m5 / 2, str(round(self.a_m5)), va='center', rotation='vertical')  # Legenda do eixo y da sapata
        
        # TEXTO DA COTA DO PILAR
        plt.text(self.b_m5 / 2, (round(self.a_m5 / 2)) - (self.a0 / 2) - 20, str(self.b0), ha='center')  # Legenda do eixo x do pilar
        plt.text(((self.b_m5/2)-(round(self.b0/2))-20), self.a_m5/2, str(self.a0), va='center', rotation='vertical')  # Legenda do eixo y do pilar
        
        
        # GRÁFICOS DO DETALHAMENTO DA ARMADURA
        # Eixo A
        
        x01 = [self.b_m5+20, self.b_m5+20+self.gancho_a, self.b_m5+20+self.gancho_a, self.b_m5+20]
        y01 = [0, 0, self.a_m5, self.a_m5]
        
        plt.plot(x01, y01, 'k-', linewidth=1)
        
        # Eixo B
        
        x02 = [0, 0, self.b_m5, self.b_m5]
        y02 = [0-20, 0-20-self.gancho_b, 0-self.gancho_b-20, 0-20]
        plt.plot(x02, y02, 'k-', linewidth=1)
        
        # Texto do detalhamento do aço das sapatas
        
        # PARA O EIXO A 
        plt.text(self.b_m5+25, (self.a_m5/2), str(round(self.a_m5-2*self.c)), ha='center', rotation='vertical')  # Legenda da barra sem o gancho
        plt.text(self.b_m5+20+(self.gancho_a/2), (0-15), str(self.gancho_b), ha='center', rotation='vertical')  # Legenda do gancho baixo
        plt.text(self.b_m5+20+(self.gancho_a/2), (self.a_m5+5), str(self.gancho_b), ha='center', rotation='vertical')  # Legenda do gancho cima
        pos_inicial = self.a_m5 * 0.10  
        pos_final = self.a_m5 * 0.70  
        espacamento = (pos_final - pos_inicial) / 3  # Como temos 4 itens, usamos 3 divisões
        plt.text(self.b_m5 + 30 + self.gancho_a, pos_inicial, f"{self.na}N2", ha="center", rotation="vertical")
        plt.text(self.b_m5 + 30 + self.gancho_a, pos_inicial + espacamento, f"Ø{self.barra_a} ", ha="center", rotation="vertical")
        plt.text(self.b_m5 + 30 + self.gancho_a, pos_inicial + 2 * espacamento, f"C{self.esp_a}  ", ha="center", rotation="vertical")
        plt.text(self.b_m5 + 30 + self.gancho_a, pos_final, f"  c={(self.a_m5 - 2 * self.c) + self.gancho_a + self.gancho_b}", 
                 ha="center", rotation="vertical")
        

        
        
        plt.text(self.b_m5/2, (0-25), str(round(self.b_m5-2*self.c)), ha='center')  # Legenda da barra sem o gancho
        plt.text(0-10, (0-20-(self.gancho_b/2)), str(self.gancho_b), ha='center')  # Legenda do gancho a esquerda
        plt.text(self.b_m5+10, (0-20-(self.gancho_b/2)), str(self.gancho_b), ha='center')  # Legenda do gancho a direita
        plt.text(self.b_m5*0.08, (0-30-self.gancho_b), str(self.nb), ha='center')  # Legenda do numero de barras
        plt.text(self.b_m5*0.15, (0-30-self.gancho_b), str('N2'), ha='center')  # Legenda do código
        plt.text(self.b_m5*0.28, (0-30-self.gancho_b), 'Ø' + str(self.barra_b), ha='center') # Legenda do diametro da barra
        plt.text(self.b_m5*0.40, (0-30-self.gancho_b), 'C' , ha='center')   # Legenda do C do espaçamento
        plt.text(self.b_m5*0.50, (0-30-self.gancho_b), str(self.esp_b), ha='center')   # Legenda do espaçamento
        plt.text(self.b_m5*0.68, (0-30-self.gancho_b), 'c = ' , ha='center')   # Legenda do c do Comprimento
        plt.text(self.b_m5*0.80, (0-30-self.gancho_b), str((self.b_m5-2*self.c)+self.gancho_a+self.gancho_b), ha='center')  # Legenda do comprimento
        
        # Definir escala igual para os eixos X e Y
        plt.gca().set_aspect('equal', adjustable='box')
        
        # Definir os limites dos eixos
        plt.xlim(-40, self.b_m5+50)
        plt.ylim(-40, self.a_m5+50)
        
        # Definir escala igual para os eixos X e Y
        plt.gca().set_aspect('equal', adjustable='box')
        
        # Remover os eixos
        plt.axis('off')

        # Salvar a imagem gerada
        self.fig.savefig('planta_sapata.png', dpi=200, bbox_inches='tight')

        self.label_o = Label(self.janela, bg ="#99BFBB")
        self.label_o.place(relx=0.485, rely=0.15, relwidth= 0.49, relheight=0.8)
        canvas = FigureCanvasTkAgg(self.fig, master=self.label_o)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(relx=0, rely=0, relwidth=1, relheight=1)  # Ajustar ao Label
        canvas.draw()  # Renderizar o gráfico


    def corte_a(self):
                # Função para plotar os pontos (barras de aço)
        def plotar_pontos(ponto_inicial, ponto_final, num_pontos):
            # Calcular as coordenadas x e y igualmente espaçadas
            x_inicial, y_inicial = ponto_inicial
            x_final, y_final = ponto_final
        
            # Gerar as coordenadas x e y igualmente espaçadas
            x = np.linspace(x_inicial, x_final, num_pontos)
            y = np.linspace(y_inicial, y_final, num_pontos)
            
        
            # Plotar os pontos no gráfico
            plt.scatter(x, y, color='black', s=5)  # Ajuste o tamanho das bolinhas com 's'
        
        # Aumentar o tamanho da figura
        self.fig1, ax = plt.subplots(figsize=(30, 30))  
        
        # Coordenadas do quadrado (base)
        x = [0, 0, self.a_m5, self.a_m5]
        y = [self.h0, 0, 0, self.h0]
        
        # Preencher toda a área do gráfico com cinza, incluindo as outras regiões
        plt.fill(x, y, 'gray', alpha=0.5)  # Preenchendo a área principal com cinza
        
        # Plote o quadrado
        plt.plot(x, y, 'k-', linewidth=1)
        
        # Reta 1 - Queda à esquerda da sapata
        x1 = [0, ((self.a_m5 / 2) - (self.a0 / 2) - 2.5)]
        y1 = [self.h0, self.h]
        plt.plot(x1, y1, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 2 - Queda à direita da sapata
        x2 = [self.a_m5, ((self.a_m5 / 2) + (self.a0 / 2) + 2.5)]
        y2 = [self.h0, self.h]
        plt.plot(x2, y2, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 3 - Colarinho da sapata à direita
        x3 = [((self.a_m5 / 2) + (self.a0 / 2)), ((self.a_m5 / 2) + (self.a0 / 2) + 2.5)]
        y3 = [self.h, self.h]
        plt.plot(x3, y3, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 4 - Colarinho da sapata à esquerda
        x4 = [((self.a_m5 / 2) - (self.a0 / 2)), ((self.a_m5 / 2) - (self.a0 / 2) - 2.5)]
        y4 = [self.h, self.h]
        plt.plot(x4, y4, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 5 - Topo do pilar à esquerda
        x5 = [((self.a_m5 / 2) - (self.a0 / 2)), ((self.a_m5 / 2) - (self.a0 / 2))]
        y5 = [self.h, 150]
        plt.plot(x5, y5, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 6 - Topo do pilar à direita
        x6 = [((self.a_m5 / 2) + (self.a0 / 2)), ((self.a_m5 / 2) + (self.a0 / 2))]
        y6 = [self.h, 150]
        plt.plot(x6, y6, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 7, 8 e 9 - Barras de aço
        x7 = [self.c, self.c]
        y7 = [self.c, (self.c+self.gancho_a)]
        plt.plot(x7, y7, 'k-', linewidth=1)  # gancho na esqerda
        
        x8 = [self.c, (self.a_m5 - self.c)]
        y8 = [self.c, self.c]
        plt.plot(x8, y8, 'k-', linewidth=1)  # barra longitudinal
        
        x9 = [(self.a_m5 - self.c), (self.a_m5 - self.c)]
        y9 = [self.c, (self.c+self.gancho_a)]
        plt.plot(x9, y9, 'k-', linewidth=1)  # gancho na direita
        
        # Plotar barras de aço
        ponto_inicial = ((self.c+1), (self.c+1))  # Ponto inicial (x0, y0)
        ponto_final = ((self.a_m5 - (self.c+1)), (self.c+1))  # Ponto final (x1, y1)
        num_pontos = self.na  # Quantidade de pontos (incluindo os extremos)
        
        # Chama a função para plotar o gráfico
        plotar_pontos(ponto_inicial, ponto_final, num_pontos)
        
        # Preencher a área entre as retas 1, 2, 3 e 4
        x_filled = [0, ((self.a_m5 / 2) - (self.a0 / 2) - 2.5), ((self.a_m5 / 2) - (self.a0 / 2)), ((self.a_m5 / 2) + (self.a0 / 2)), 
                    ((self.a_m5 / 2) + (self.a0 / 2) + 2.5), self.a_m5]
        y_filled = [self.h0, self.h, self.h, self.h, self.h, self.h0]
        
        # Preencher a área entre as retas
        plt.fill(x_filled, y_filled, 'gray', alpha=0.5)
        
        # Preencher a área do pilar
        x_pillar_filled = [((self.a_m5 / 2) - (self.a0 / 2)), ((self.a_m5 / 2) + (self.a0 / 2)), ((self.a_m5 / 2) + 
                                                                                                  (self.a0 / 2)), ((self.a_m5 / 2) - (self.a0 / 2))]
        y_pillar_filled = [self.h, self.h, 150, 150]
        
        # Preencher a área do pilar
        plt.fill(x_pillar_filled, y_pillar_filled, 'gray', alpha=0.5)
        
        # Adicionar cotas (ajustes de posicionamento)
        
        # GRÁFICO DAS COTAS DA SAPATA - LADO H
        x_cota1 = [-30, -30]
        y_cota1 = [0, self.h]
        plt.plot(x_cota1, y_cota1, 'k-', linewidth=1)
        
        x_cota2 = [-27.5, -32.5]
        y_cota2 = [-0, 0]
        plt.plot(x_cota2, y_cota2, 'k-', linewidth=1)  # BAIXA
        
        x_cota3 = [-27.5, -32.5]
        y_cota3 = [self.h, self.h]
        plt.plot(x_cota3, y_cota3, 'k-', linewidth=1)  # ALTA
        
        # GRÁFICO DAS COTAS DA SAPATA - LADO H0
        x_cota4 = [-10, -10]
        y_cota4 = [0, self.h0]
        plt.plot(x_cota4, y_cota4, 'k-', linewidth=1)
        
        x_cota5 = [-7.5, -12.5]
        y_cota5 = [-0, 0]
        plt.plot(x_cota5, y_cota5, 'k-', linewidth=1)  # BAIXA
        
        x_cota6 = [-7.5, -12.5]
        y_cota6 = [self.h0, self.h0]
        plt.plot(x_cota6, y_cota6, 'k-', linewidth=1)  # ALTA
        
        # GRÁFICO DAS COTAS DA SAPATA - BASE A
        x_cota7 = [0, self.a_m5]
        y_cota7 = [-10, -10]
        plt.plot(x_cota7, y_cota7, 'k-', linewidth=1)
        
        x_cota8 = [0, 0]
        y_cota8 = [-7.5, -12.5]
        plt.plot(x_cota8, y_cota8, 'k-', linewidth=1)  # ESQUERDA
        
        x_cota9 = [self.a_m5, self.a_m5]
        y_cota9 = [-5, -15]
        plt.plot(x_cota9, y_cota9, 'k-', linewidth=1)  # DIREITA
        
        # GRÁFICO DAS COTAS DA SAPATA - BASE A0
        x_cota10 = [((self.a_m5 / 2) - (self.a0 / 2)), ((self.a_m5 / 2) + (self.a0 / 2))]
        y_cota10 = [(self.h - 10), (self.h - 10)]
        plt.plot(x_cota10, y_cota10, 'k-', linewidth=1)
        
        x_cota11 = [((self.a_m5 / 2) - (self.a0 / 2)), ((self.a_m5 / 2) - (self.a0 / 2))]
        y_cota11 = [self.h - 7.5, self.h - 12.5]
        plt.plot(x_cota11, y_cota11, 'k-', linewidth=1)  # ESQUERDA
        
        x_cota12 = [((self.a_m5 / 2) + (self.a0 / 2)), ((self.a_m5 / 2) + (self.a0 / 2))]
        y_cota12 = [self.h - 7.5, self.h - 12.5]
        plt.plot(x_cota12, y_cota12, 'k-', linewidth=1)  # DIREITA
        
        # Largura da base
        plt.text(self.a_m5 / 2, -15, self.a_m5, ha='center', va='top', fontsize=10)
        
        # Altura da base
        plt.text(-15, self.h0 / 2, self.h0, ha='center', va='bottom', fontsize=10, rotation='vertical')
        
        # Altura total
        plt.text(-35, self.h / 2, self.h, ha='center', va='bottom', fontsize=10, rotation='vertical')
        
        # Altura total
        plt.text(self.a_m5 / 2, self.h - 20, self.a0, ha='center', va='bottom', fontsize=10)
        
        # 'N1' para a barra longitudinal
        plt.annotate('N1', 
                     xy=(self.c+1, self.c+2),  # Ponto onde a seta vai começar (centro da barra)
                     xytext=(self.c-1, -20),  # Posição do texto abaixo da cota
                     arrowprops=dict(facecolor='black', arrowstyle='-', linewidth=1), fontsize=10)
        
        # 'N2' para a barra transversal
        plt.annotate('N2', 
                     xy=(self.c+10, self.c),  # Ponto onde a seta vai começar (centro da barra)
                     xytext=(self.c+15, -20),  # Posição do texto abaixo da cota
                     arrowprops=dict(facecolor='black', arrowstyle='-', linewidth=1), fontsize=10)
        
        # Defina os limites dos eixos para mostrar as cotas
        plt.xlim(-40, self.a_m5+40)
        plt.ylim(-30, self.h+50)
        
        # Definir escala igual para os eixos X e Y
        plt.gca().set_aspect('equal', adjustable='box')
        
        # Remover os eixos
        plt.axis('off')

                # Salvar a imagem gerada
        self.fig1.savefig('corteA_sapata.png', dpi=200, bbox_inches='tight')

        self.label_p = Label(self.janela, bg ="#99BFBB")
        self.label_p.place(relx=0.485, rely=0.15, relwidth= 0.49, relheight=0.8)
        canvas = FigureCanvasTkAgg(self.fig1, master=self.label_p)
        canvas_widget1 = canvas.get_tk_widget()
        canvas_widget1.place(relx=-0.1, rely=0, relwidth=1.2, relheight=1.2)  # Ajustar ao Label
        canvas.draw()  # Renderizar o gráfico

        
    def corte_b(self):

        # Função para plotar os pontos (barras de aço)
        def plotar_pontos(ponto_inicial, ponto_final, num_pontos):
            # Calcular as coordenadas x e y igualmente espaçadas
            x_inicial, y_inicial = ponto_inicial
            x_final, y_final = ponto_final
        
            # Gerar as coordenadas x e y igualmente espaçadas
            x = np.linspace(x_inicial, x_final, num_pontos)
            y = np.linspace(y_inicial, y_final, num_pontos)
        
            # Plotar os pontos no gráfico
            plt.scatter(x, y, color='black', s=5)  # Ajuste o tamanho das bolinhas com 's'
        
        # Aumentar o tamanho da figura
        self.fig2, ax = plt.subplots(figsize=(30, 30)) 
        
        # Coordenadas do quadrado (base)
        x = [0, 0, self.b_m5, self.b_m5]
        y = [self.h0, 0, 0, self.h0]
        
        # Preencher toda a área do gráfico com cinza, incluindo as outras regiões
        plt.fill(x, y, 'gray', alpha=0.5)  # Preenchendo a área principal com cinza
        
        # Plote o quadrado
        plt.plot(x, y, 'k-', linewidth=1)
        
        # Reta 1 - Queda à esquerda da sapata
        x1 = [0, ((self.b_m5/2)-(self.b0/2)-2.5)]
        y1 = [self.h0, self.h]
        plt.plot(x1, y1, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 2 - Queda à direita da sapata
        x2 = [self.b_m5, ((self.b_m5/2)+(self.b0/2)+2.5)]
        y2 = [self.h0, self.h]
        plt.plot(x2, y2, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 3 - Colarinho da sapata à direita
        x3 = [((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)+(self.b0/2)+2.5)]
        y3 = [self.h, self.h]
        plt.plot(x3, y3, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 4 - Colarinho da sapata à esquerda
        x4 = [((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)-(self.b0/2)-2.5)]
        y4 = [self.h, self.h]
        plt.plot(x4, y4, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 5 - Topo do pilar à esquerda
        x5 = [((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)-(self.b0/2))]
        y5 = [self.h, 150]
        plt.plot(x5, y5, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 6 - Topo do pilar à direita
        x6 = [((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)+(self.b0/2))]
        y6 = [self.h, 150]
        plt.plot(x6, y6, 'k-', linewidth=1)  # Reta em preto
        
        # Reta 7, 8 e 9 - Barra de aço
        x7 = [self.c, self.c]
        y7 = [self.c, (self.c+self.gancho_b)]
        plt.plot(x7, y7, 'k-', linewidth=1)  # gancho na esqerda
        
        x8 = [self.c, (self.b_m5 - self.c)]
        y8 = [self.c, self.c]
        plt.plot(x8, y8, 'k-', linewidth=1)  # barra longitudinal
        
        x9 = [(self.b_m5 - self.c), (self.b_m5 - self.c)]
        y9 = [self.c, (self.c+self.gancho_b)]
        plt.plot(x9, y9, 'k-', linewidth=1)  # gancho na direita
        
        # Plotar barras de aço
        ponto_inicial = ((self.c+1), (self.c+1))  # Ponto inicial (x0, y0)
        ponto_final = ((self.b_m5 - (self.c+1)), (self.c+1))  # Ponto final (x1, y1)
        num_pontos = self.nb  # Quantidade de pontos (incluindo os extremos)
        
        # Chama a função para plotar o gráfico
        plotar_pontos(ponto_inicial, ponto_final, num_pontos)
        
        # Preencher a área entre as retas 1, 2, 3 e 4
        # As coordenadas das retas 1, 2, 3 e 4
        x_filled = [0, ((self.b_m5/2)-(self.b0/2)-2.5), ((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)+(self.b0/2)), 
                    ((self.b_m5/2)+(self.b0/2)+2.5), self.b_m5]
        y_filled = [self.h0, self.h, self.h, self.h, self.h, self.h0]
        
        # Preencher a área entre as retas
        plt.fill(x_filled, y_filled, 'gray', alpha=0.5)
        
        # Preencher a área do pilar
        # A área do pilar é delimitada pelas retas 5, 6 e 7
        x_pillar_filled = [((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)-(self.b0/2))]
        y_pillar_filled = [self.h, self.h, 150, 150]
        
        # Preencher a área do pilar
        plt.fill(x_pillar_filled, y_pillar_filled, 'gray', alpha=0.5)
        
        # Adicionar cotas
        
        # GRÁFICO DAS COTAS DA SAPATA - LADO H
        x_cota1 = [-30, -30]
        y_cota1 = [0, self.h]
        plt.plot(x_cota1, y_cota1, 'k-', linewidth=1) 
        
        x_cota2 = [-27.5, -32.5]
        y_cota2 = [-0,  0]
        plt.plot(x_cota2, y_cota2, 'k-', linewidth=1)  # BAIXA
        
        x_cota3 = [-27.5, -32.5]
        y_cota3 = [self.h,  self.h]
        plt.plot(x_cota3, y_cota3, 'k-', linewidth=1)  # ALTA
        
        # GRÁFICO DAS COTAS DA SAPATA - LADO H0
        x_cota4 = [-10, -10]
        y_cota4 = [0, self.h0]
        plt.plot(x_cota4, y_cota4, 'k-', linewidth=1) 
        
        x_cota5 = [-7.5, -12.5]
        y_cota5 = [-0,  0]
        plt.plot(x_cota5, y_cota5, 'k-', linewidth=1)  # BAIXA
        
        x_cota6 = [-7.5, -12.5]
        y_cota6 = [self.h0,  self.h0]
        plt.plot(x_cota6, y_cota6, 'k-', linewidth=1)  # ALTA
        
        # GRÁFICO DAS COTAS DA SAPATA - BASE A
        x_cota7 = [0, self.b_m5]
        y_cota7 = [-10, -10]
        plt.plot(x_cota7, y_cota7, 'k-', linewidth=1)  
        
        x_cota8 = [0, 0]
        y_cota8 = [-7.5,  -12.5]
        plt.plot(x_cota8, y_cota8, 'k-', linewidth=1)  # ESQUERDA
        
        x_cota9 = [self.b_m5, self.b_m5]
        y_cota9 = [-5,  -15]
        plt.plot(x_cota9, y_cota9, 'k-', linewidth=1)  # DIREITA
        
        # GRÁFICO DAS COTAS DA SAPATA - BASE A0
        x_cota10 = [((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)+(self.b0/2))]
        y_cota10 = [(self.h-10), (self.h-10)]
        plt.plot(x_cota10, y_cota10, 'k-', linewidth=1)  
        
        x_cota11 = [((self.b_m5/2)-(self.b0/2)), ((self.b_m5/2)-(self.b0/2))]
        y_cota11 = [self.h-7.5, self.h-12.5]
        plt.plot(x_cota11, y_cota11, 'k-', linewidth=1)  # ESQUERDA
        
        x_cota12 = [((self.b_m5/2)+(self.b0/2)), ((self.b_m5/2)+(self.b0/2))]
        y_cota12 = [self.h-7.5, self.h-12.5]
        plt.plot(x_cota12, y_cota12, 'k-', linewidth=1)  # DIREITA
        
        # Largura da base
        plt.text(self.b_m5/2, -15, self.b_m5, ha='center', va='top', fontsize=10)
        
        # Altura da base
        plt.text(-15, self.h0/2, self.h0, ha='center', va='bottom', fontsize=10, rotation='vertical')
        
        # Altura total
        plt.text(-35, self.h/2, self.h, ha='center', va='bottom', fontsize=10, rotation='vertical')
        
        # Altura total
        plt.text(self.b_m5/2, self.h-20, self.b0, ha='center', va='bottom', fontsize=10)
        
        # 'N1' para a barra longitudinal
        plt.annotate('N2', 
                     xy=(self.c+1, self.c+2),  # Ponto onde a seta vai começar (centro da barra)
                     xytext=(self.c-1, -20),  # Posição do texto abaixo da cota
                     arrowprops=dict(facecolor='black', arrowstyle='-', linewidth=1), fontsize=10)
        
        # 'N2' para a barra transversal
        plt.annotate('N1', 
                     xy=(self.c+10, self.c),  # Ponto onde a seta vai começar (centro da barra)
                     xytext=(self.c+15, -20),  # Posição do texto abaixo da cota
                     arrowprops=dict(facecolor='black', arrowstyle='-', linewidth=1), fontsize=10)
        
        # Defina os limites dos eixos para mostrar as cotas
        plt.xlim(-40, self.b_m5+40)
        plt.ylim(-30, self.h+50)
        
        # Definir escala igual para os eixos X e Y
        plt.gca().set_aspect('equal', adjustable='box')
        
        # Remover os eixos
        plt.axis('off')

        self.fig2.savefig('corteB_sapata.png', dpi=200, bbox_inches='tight')

        self.label_q = Label(self.janela, bg ="#99BFBB")
        self.label_q.place(relx=0.485, rely=0.15, relwidth= 0.49, relheight=0.8)
        canvas = FigureCanvasTkAgg(self.fig2, master=self.label_q)
        canvas_widget1 = canvas.get_tk_widget()
        canvas_widget1.place(relx=-0.1, rely=0, relwidth=1.2, relheight=1.2)  # Ajustar ao Label
        canvas.draw()  # Renderizar o gráfico

    
    def bt_detalhes(self):

        # Botão Planta
        self.bt_planta = Button(self.frame_5, text="Planta", bd=3, fg="black", bg="white", font=("arial", "10"),
                                command=self.planta)
        self.bt_planta.place(relx=0.1, rely=0.02, relwidth=0.20, relheight=0.05)

        # Botão corte A
        self.bt_corteA = Button(self.frame_5, text="Corte A", bd=3, fg="black", bg="white", font=("arial", "10"),
                               command=self.corte_a)
        self.bt_corteA.place(relx=0.40, rely=0.02, relwidth=0.20, relheight=0.05)

        # Botão corte B
        self.bt_corteB = Button(self.frame_5, text="Corte B", bd=3, fg="black", bg="white", font=("arial", "10"),
                               command=self.corte_b)
        self.bt_corteB.place(relx=0.70, rely=0.02, relwidth=0.20, relheight=0.05)


class funcoes():
    def limpa_tela(self):

        # Limoar os dados de entrada
        a0 = self.a0_entry.delete(0, END)
        b0 = self.b0_entry.delete(0, END)
        pp = self.pp_entry.delete(0, END)
        tadm = self.tadm_entry.delete(0, END)

        # Limpar os labels com os resultados
        self.label_x.config(text="")
        self.label_y.config(text="")
        self.label_z.config(text="")
        self.label_a.config(text="")
        self.label_b.config(text="")
        self.label_c.config(text="")
        self.label_d.config(text="")
        self.label_e.config(text="")
        self.label_f.config(text="")
        self.label_g.config(text="")
        self.label_h.config(text="")
        self.label_i.config(text="")
        self.label_j.config(text="")
        self.label_k.config(text="")
        self.label_l.config(text="")
        self.label_m.config(text="")
        self.label_n.config(text="")
        self.label_o.config(text="")
        self.label_p.config(text="")
        self.label_q.config(text="")

        botoes = [self.bt_planta, self.bt_corteA, self.bt_corteB]  
        for botao in botoes:
            botao.destroy()  # Remove da interface completamente

         # Reiniciar a lista
        self.coeficiente_selecionado1.set('3')   # Primeiro valor da lista C
        self.coeficiente_selecionado2.set('20')  # Primeiro valor da lista Fck
        self.coeficiente_selecionado3.set('500') # Primeiro valor da lista Fyk
        self.coeficiente_selecionado4.set('5.0') # Primeiro valor da lista Barra A
        self.coeficiente_selecionado5.set('5.0') # Primeiro valor da lista Barra B



class relatorios():
        
    def print(self):
        webbrowser.open("Resultados.pdf")

    def gerar_relatorios(self):
        self.c = canvas.Canvas("Resultados.pdf", pagesize=letter)

        # Obtendo os valores dos campos de entrada
        try:
            self.a0Rel = self.a0_entry.get()
            self.b0Rel = self.b0_entry.get()
            self.ppRel = self.pp_entry.get()
            self.tadmRel = self.tadm_entry.get()
            self.cRel = self.coeficiente_selecionado1.get()
            self.fckRel = self.coeficiente_selecionado2.get()
            self.fykRel = self.coeficiente_selecionado3.get()
            self.barra_aRel = self.coeficiente_selecionado4.get()
            self.barra_bRel = self.coeficiente_selecionado5.get()
            self.aRel = self.a_m5
            self.bRel = self.b_m5
            self.lRel = self.l
            self.hRel = self.h
            self.dRel = self.d
            self.h0Rel = self.h0
            self.tangRel = self.tanα
            self.tyRel = self.ty
            self.txRel = self.tx
            self.asminARel = self.asminA
            self.asminBRel = self.asminB
            self.aaRel = self.asy
            self.abRel = self.asx
            self.naRel = self.na
            self.nbRel = self.nb
            self.esp_aRel = self.esp_a
            self.esp_bRel = self.esp_b

        except AttributeError:
            print("Erro: Algum campo de entrada não foi inicializado corretamente.")
            return
            
        # Configurando o título do relatório - Primeira página
        self.c.setFont("Helvetica", 24)
        self.c.drawString(230, 725, 'RELATÓRIO')

        # Titulo para dados de entrada
        self.c.setFont("Helvetica", 12)
        self.c.drawString(53, 685, 'DADOS DE ENTRADA: ')

        # Adicionando os valores capturados
        self.c.setFont("Helvetica", 12)
        self.c.drawString(53, 660, f"Tamanho transversal do pilar (A0): {self.a0Rel} cm")
        self.c.drawString(53, 640, f"Tamanho longitudinal do pilar (B0): {self.b0Rel} cm")
        self.c.drawString(53, 620, f"Peso próprio do pilar: {self.ppRel} kN")
        self.c.drawString(53, 600, f"Tensão Admissível do solo: {self.tadmRel} kN/m²")
        self.c.drawString(53, 580, f"Cobrimento: {self.cRel} cm")
        self.c.drawString(53, 560, f"Resistência característica do concreto(Fck): {self.fckRel} MPa")
        self.c.drawString(53, 540, f"Resistência característica do aço(Fyk): {self.fykRel} MPa")
        self.c.drawString(53, 520, f"Barra escolhida na direção A: {self.barra_aRel} mm")
        self.c.drawString(53, 500, f"Barra escolhida na direção B: {self.barra_bRel} mm")

        # Titulo para resultados
        self.c.setFont("Helvetica", 12)
        self.c.drawString(53, 470, 'RESULTADOS: ')
        
        # Adicionando valores calculados
        self.c.drawString(53, 440, f"Tamanho transversal da sapata (A): {self.aRel} cm")
        self.c.drawString(53, 420, f"Tamanho longitudinal da sapata (B): {self.bRel} cm")
        self.c.drawString(53, 400, f"Balanço da sapata (L): {self.lRel} cm")
        self.c.drawString(53, 380, f"Altura total da sapata (H): {self.hRel} cm")
        self.c.drawString(53, 360, f"Altura útil da sapata (D): {self.dRel} cm")
        self.c.drawString(53, 340, f"Altura da base (H0): {self.h0Rel} cm")
        self.c.drawString(53, 320, f"Ângulo de inclinação da sapata: {self.tangRel} °")
        self.c.drawString(53, 300, f"Força de tração em A: {self.tyRel} kN")
        self.c.drawString(53, 280, f"Força de tração em B: {self.txRel} kN")
        self.c.drawString(53, 260, f"Área de aço mínima em A: {self.asminARel} cm²")
        self.c.drawString(53, 240, f"Área de aço mínima em B: {self.asminBRel} cm²")
        self.c.drawString(53, 220, f"Área de aço calculada em A: {self.aaRel} cm²")
        self.c.drawString(53, 200, f"Área de aço calculada em B: {self.abRel} cm²")
        self.c.drawString(53, 180, f"Número de barras em A: {self.naRel} barras")
        self.c.drawString(53, 160, f"Número de barras em B: {self.nbRel} barras")
        self.c.drawString(53, 140, f"Espaçamento em A: {self.esp_aRel} cm")
        self.c.drawString(53, 120, f"Espaçamento em B: {self.esp_bRel} cm")

        # Criação da segunda página
        self.c.showPage()
        self.c.setFont("Helvetica", 24)
        self.c.drawString(230, 725, 'PLANTA')
        self.c.drawImage('planta_sapata.png', 47.6375, 170.945, width=500, height=500)

        # Criação da terceira página
        self.c.showPage()
        self.c.setFont("Helvetica", 24)
        self.c.drawString(230, 725, 'CORTE LADO A')
        self.c.drawImage('corteA_sapata.png', 47.6375, 270.945, width=500, height=300)

        # Criação da Quarta página
        self.c.showPage()
        self.c.setFont("Helvetica", 24)
        self.c.drawString(230, 725, 'CORTE LADO B')
        self.c.drawImage('corteB_sapata.png', 47.6375, 270.945, width=500, height=300)
        
            
        self.c.save()
        self.print()


class rina(funcoes, calculo_das_dimensoes, relatorios):
    def __init__(self):
        self.janela = janela
        self.tela()
        self.widgets_janela()
        self.frames()
        self.widgets_frame1()
        self.widgets_frame2()
        self.widgets_frame3()
        self.widgets_frame4()
        self.menus()
        janela.mainloop()
        
    def tela(self):
        self.janela.title("RINA - APLICAÇÃO COMPUTACIONAL PARA DIMENSIONAMENTO E DETALHAMENTO DE SAPATAS RÍGIDAS ISOLADAS") # Titulo
        self.janela.configure(bg = 'white') # Cor da Janela
        self.janela.geometry("1100x700") # Tamanho da janela
        self.janela.resizable(False, False) 
 
    def widgets_janela(self):
        
        self.label_dados = Label(self.janela,text= "DADOS DE ENTRADA", bg= "white",fg = "black", font=("arial","12","bold") )
        self.label_dados.place(relx=0.04, rely=0.04) # A proporção dos frames não aumentam com a medida da tela

        self.label_processamento = Label(self.janela,text= "PROCESSAMENTO", bg= "white",fg = "black", font=("arial","12","bold"))
        self.label_processamento.place(relx=0.04, rely=0.6) 

        self.label_resultado = Label(self.janela,text= "RESULTADOS", bg= "white",fg = "black", font=("arial","12","bold") )
        self.label_resultado.place(relx=0.30, rely=0.04) 

        self.detalhamentoSap = Label(self.janela,text= "DETALHAMENTO DA SAPATA", bg= "white",fg = "black", font=("arial","12","bold") )
        self.detalhamentoSap.place(relx=0.615, rely=0.04) 

        self.eu = Label(self.janela,text= "DESENVOLVIDO POR: GUILHERME LOPES LEMOS", bg= "white",fg = "black", font=("arial","8","bold") )
        self.eu.place(relx=0.75, rely=0.97) 
        
    def frames(self):

        # Frame que fica abaixo do nome RINA
        self.frame_1 = Frame(self.janela, bg = "white" )
        self.frame_1.place(relx=0.00, rely=0.00, relwidth= 1, relheight=0.03) 
        
        # O frame 2 os Dados de entrada
        self.frame_2 = Frame(self.janela, bg = "#99BFBB")
        self.frame_2.place(relx=0.02, rely=0.08, relwidth= 0.20, relheight=0.50) 

        # O frame 3 ficará o Processamento
        self.frame_3 = Frame(self.janela, bg = "#99BFBB")
        self.frame_3.place(relx=0.02, rely=0.65, relwidth= 0.20, relheight=0.32) 

        # O frame 4 ficará os Resultados
        self.frame_4 = Frame(self.janela, bg = "#99BFBB")
        self.frame_4.place(relx=0.25, rely=0.08, relwidth= 0.2, relheight=0.89) 

        # O frame 5 aparecerá os detalhamentos
        self.frame_5 = Frame(self.janela, bg ="#99BFBB")
        self.frame_5.place(relx=0.48, rely=0.08, relwidth= 0.50, relheight=0.89)

    def widgets_frame1(self):

        self.abas = Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba1.configure(bg = "white")
        self.abas.add(self.aba1, text = 'RINA')
        self.abas.place(relx= 0.00, rely=0.00, relwidth= 0.98, relheight=0.98)
    
    def widgets_frame2(self):
        # Label Código

        # Label A0
        self.lb_a0 = Label(self.frame_2, text= "A0", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_a0.place(relx= 0.03, rely=0.05)
        self.lb_cm1 = Label(self.frame_2, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm1.place(relx= 0.75, rely=0.05)
        self.a0_entry = Entry(self.frame_2)
        self.a0_entry.place(relx= 0.25, rely=0.05, relwidth= 0.5, relheight=0.06)

        # Label B0
        self.lb_b0 = Label(self.frame_2, text= "B0", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_b0.place(relx= 0.03, rely=0.15)
        self.lb_cm2 = Label(self.frame_2, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm2.place(relx= 0.75, rely=0.15)
        self.b0_entry = Entry(self.frame_2)
        self.b0_entry.place(relx= 0.25, rely=0.15, relwidth= 0.5, relheight=0.06)

        # Label Peso Próprio
        self.lb_pp = Label(self.frame_2, text= "PP", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_pp.place(relx= 0.03, rely=0.25)
        self.lb_kn = Label(self.frame_2, text= "kN", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_kn.place(relx= 0.75, rely=0.25)
        self.pp_entry = Entry(self.frame_2)
        self.pp_entry.place(relx= 0.25, rely=0.25, relwidth= 0.5, relheight=0.06)

        # Label Tensão admissível
        self.lb_tadm = Label(self.frame_2, text= "σadm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_tadm.place(relx= 0.03, rely=0.35)
        self.tadm_kn = Label(self.frame_2, text= "kN/m²", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.tadm_kn.place(relx= 0.75, rely=0.35)
        self.tadm_entry = Entry(self.frame_2)
        self.tadm_entry.place(relx= 0.25, rely=0.35, relwidth= 0.5, relheight=0.06)

        # Label Cobrimento
        self.lb_cobrimento = Label(self.frame_2, text= "C", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cobrimento.place(relx= 0.03, rely=0.45)
        self.lb_cmm = Label(self.frame_2, text="cm", bg="#99BFBB", fg="black", font=("arial", "10"))
        self.lb_cmm.place(relx=0.75, rely=0.45)
        opcoes_c = ['3','4','5'] # lista dos valores do cobrimento
        self.coeficiente_selecionado1 = StringVar(value = opcoes_c[0])
        menu_coeficiente1 = OptionMenu(self.frame_2, self.coeficiente_selecionado1, *opcoes_c) 
        menu_coeficiente1.config(bg="white", font=("arial", 10), bd = 0)
        menu_coeficiente1.place(relx= 0.25, rely=0.45, relwidth= 0.5, relheight=0.06)        

        # Label FCK

        self.lb_fck = Label(self.frame_2, text="Fck", bg="#99BFBB", fg="black", font=("arial", "10"))
        self.lb_fck.place(relx=0.03, rely=0.55)
        self.lb_mpa = Label(self.frame_2, text="MPa", bg="#99BFBB", fg="black", font=("arial", "10"))
        self.lb_mpa.place(relx=0.75, rely=0.55)
        opcoes_fck = ['20', '25', '30', '35', '40']  # Lista dos valores do fck
        self.coeficiente_selecionado2 = StringVar(value=opcoes_fck[0])  # Agora é um atributo da classe
        menu_coeficiente2 = OptionMenu(self.frame_2, self.coeficiente_selecionado2, *opcoes_fck)
        menu_coeficiente2.config(bg="white", font=("arial", 10), bd=0)
        menu_coeficiente2.place(relx=0.25, rely=0.55, relwidth=0.5, relheight=0.06)
        
        # Label FYK
        self.lb_fyk = Label(self.frame_2, text= "Fyk", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_fyk.place(relx= 0.03, rely=0.65)
        self.lb_mpa1 = Label(self.frame_2, text= "MPa", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_mpa1.place(relx= 0.75, rely=0.65)       
        opcoes_fyk = ['500', '600'] # lista dos valores do fyk
        self.coeficiente_selecionado3 = StringVar(value = opcoes_fyk[0])
        menu_coeficiente3 = OptionMenu(self.frame_2, self.coeficiente_selecionado3, *opcoes_fyk) 
        menu_coeficiente3.config(bg="white", font=("arial", 10), bd = 0)
        menu_coeficiente3.place(relx= 0.25, rely=0.65, relwidth= 0.5, relheight=0.06)        

        # label Barra para direção A
        self.lb_barra_a = Label(self.frame_2, text= "⌀a", bg = "#99BFBB",fg = "black", font=("arial","12") )
        self.lb_barra_a.place(relx= 0.03, rely=0.75)
        self.lb_mm1 = Label(self.frame_2, text= "mm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_mm1.place(relx= 0.75, rely=0.75)
        opcoes_barra_a = ['5.0', '6.3', '8.0', '10.0','12.5', '16.0', '20.0'] # lista dos valores da barra lado A
        self.coeficiente_selecionado4 = StringVar(value = opcoes_barra_a[0])
        menu_coeficiente4 = OptionMenu(self.frame_2, self.coeficiente_selecionado4, *opcoes_barra_a) 
        menu_coeficiente4.config(bg="white", font=("arial", 10), bd = 0)
        menu_coeficiente4.place(relx= 0.25, rely=0.75, relwidth= 0.5, relheight=0.06)   

        # label Barra para direção B
        self.lb_barra_b = Label(self.frame_2, text= "⌀b", bg = "#99BFBB",fg = "black", font=("arial","12") )
        self.lb_barra_b.place(relx= 0.03, rely=0.85)
        self.lb_mm2 = Label(self.frame_2, text= "mm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_mm2.place(relx= 0.75, rely=0.85)
        opcoes_barra_b = ['5.0', '6.3', '8.0', '10.0','12.5', '16.0', '20.0'] # lista dos valores da barra lado A
        self.coeficiente_selecionado5 = StringVar(value = opcoes_barra_b[0])
        menu_coeficiente5 = OptionMenu(self.frame_2, self.coeficiente_selecionado5, *opcoes_barra_b) 
        menu_coeficiente5.config(bg="white", font=("arial", 10), bd = 0)
        menu_coeficiente5.place(relx= 0.25, rely=0.85, relwidth= 0.5, relheight=0.06)   

    
    def widgets_frame3(self):

        # Botão Dimensionar sapata
        self.bt_dimensionar = Button(self.frame_3, text = "Dimensionar", bg = "white", bd = 3, fg = "black"
                                     , font = ("arial","10"),command=lambda: (self.calculo_geometria(), self.calculo_alturas(), 
                                                                              self.verificacao(), self.condicoes(),self.forcas_de_tracao(), 
                                                                              self.detalhamento()))
        self.bt_dimensionar.place(relx= 0.05, rely=0.1, relwidth= 0.90, relheight=0.2)
        
        # Botão Detalhar sapata
        self.bt_detalhar = Button(self.frame_3, text = "Detalhar Sapata", bg = "white", bd = 3, fg = "black", font = ("arial","10")
                                  ,command = lambda:(self.bt_detalhes()))
        self.bt_detalhar.place(relx= 0.05, rely=0.4, relwidth= 0.90, relheight=0.2) 
         
        
        # Limpar
        self.bt_limpar = Button(self.frame_3, text = "Limpar", bg = "white", bd = 3, fg = "black", font = ("arial","10"),
                                command = self.limpa_tela)
        self.bt_limpar.place(relx= 0.05, rely=0.7, relwidth= 0.90, relheight=0.2) 
    
    def widgets_frame4(self):


        # FRAME PARA VALOR A
        self.label_x = Label(self.frame_4, bg = "white")
        self.label_x.place(relx=0.30, rely=0.03, relwidth= 0.6, relheight=0.03)
        self.lb_a = Label(self.frame_4, text= "A", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_a.place(relx= 0.05, rely=0.03)
        self.lb_cm3 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.03)

        # FRAME PARA VALOR B
        self.label_y = Label(self.frame_4, bg = "white")
        self.label_y.place(relx=0.30, rely=0.0875, relwidth= 0.6, relheight=0.03) 
        self.lb_b = Label(self.frame_4, text= "B", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_b.place(relx= 0.05, rely=0.0875)
        self.lb_cm3 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.0875)

        # FRAME PARA VALOR L
        self.label_z = Label(self.frame_4, bg = "white")
        self.label_z.place(relx=0.30, rely=0.145, relwidth= 0.6, relheight=0.03) 
        self.lb_l = Label(self.frame_4, text= "L", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_l.place(relx= 0.05, rely=0.145)
        self.lb_cm3 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.145)
        
        # FRAME PARA VALOR D
        self.label_a = Label(self.frame_4, bg = "white")
        self.label_a.place(relx=0.30, rely=0.2025, relwidth= 0.6, relheight=0.03) 
        self.lb_d = Label(self.frame_4, text= "D", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_d.place(relx= 0.05, rely=0.2025)
        self.lb_cm3 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.2025)
   
        # FRAME PARA VALOR H
        self.label_b = Label(self.frame_4, bg = "white")
        self.label_b.place(relx=0.30, rely=0.26, relwidth= 0.6, relheight=0.03) 
        self.lb_h = Label(self.frame_4, text= "H", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_h.place(relx= 0.05, rely=0.26)
        self.lb_cm3 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.26)

        # FRAME PARA VALOR H0
        self.label_c = Label(self.frame_4, bg = "white")
        self.label_c.place(relx=0.30, rely=0.3175, relwidth= 0.6, relheight=0.03) 
        self.lb_h0 = Label(self.frame_4, text= "H0", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_h0.place(relx= 0.05, rely=0.3175)
        self.lb_cm3 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.3175)

        # FRAME PARA VALOR TANGENTE DO ANGULO
        self.label_d = Label(self.frame_4, bg = "white")
        self.label_d.place(relx=0.30, rely=0.375, relwidth= 0.55, relheight=0.03) 
        self.lb_tan = Label(self.frame_4, text= "tα", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_tan.place(relx= 0.05, rely=0.375)
        self.lb_cm3 = Label(self.frame_4, text= "°", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm3.place(relx= 0.80, rely=0.375)

        # FRAME PARA VALOR Ta
        self.label_e = Label(self.frame_4, bg = "white")
        self.label_e.place(relx=0.30, rely=0.4325, relwidth= 0.6, relheight=0.03) 
        self.lb_ta = Label(self.frame_4, text= "Ta", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_ta.place(relx= 0.05, rely=0.4325)
        self.lb_kn1 = Label(self.frame_4, text= "kN", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_kn1.place(relx= 0.80, rely=0.4325)

        # FRAME PARA VALOR Tb
        self.label_f = Label(self.frame_4, bg = "white")
        self.label_f.place(relx=0.30, rely=0.49, relwidth= 0.6, relheight=0.03) 
        self.lb_tb = Label(self.frame_4, text= "Tb", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_tb.place(relx= 0.05, rely=0.49)
        self.lb_kn2 = Label(self.frame_4, text= "kN", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_kn2.place(relx= 0.80, rely=0.49)
        
        # FRAME PARA VALOR ASMIN-A
        self.label_g = Label(self.frame_4, bg = "white")
        self.label_g.place(relx=0.25, rely=0.5475, relwidth= 0.6, relheight=0.03) 
        self.lb_asmina = Label(self.frame_4, text= "Asmin'a", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_asmina.place(relx= 0.05, rely=0.5475)
        self.lb_cm22 = Label(self.frame_4, text= "cm²", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm22.place(relx= 0.80, rely=0.5475)

        # FRAME PARA VALOR ASMIN-B
        self.label_h = Label(self.frame_4, bg = "white")
        self.label_h.place(relx=0.25, rely=0.605, relwidth= 0.6, relheight=0.03) 
        self.lb_asminb = Label(self.frame_4, text= "Asmin'b", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_asminb.place(relx= 0.05, rely=0.605)
        self.lb_cm23 = Label(self.frame_4, text= "cm²", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm23.place(relx= 0.80, rely=0.605)

        # FRAME PARA VALOR AA
        self.label_i = Label(self.frame_4, bg = "white")
        self.label_i.place(relx=0.30, rely=0.6625, relwidth= 0.6, relheight=0.03) 
        self.lb_aa = Label(self.frame_4, text= "Aa", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_aa.place(relx= 0.05, rely=0.6625)
        self.lb_cm24 = Label(self.frame_4, text= "cm²", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm24.place(relx= 0.80, rely=0.6625)

        # FRAME PARA VALOR AB
        self.label_j = Label(self.frame_4, bg = "white")
        self.label_j.place(relx=0.30, rely=0.72, relwidth= 0.6, relheight=0.03) 
        self.lb_bb = Label(self.frame_4, text= "Ab", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_bb.place(relx= 0.05, rely=0.72)
        self.lb_cm24 = Label(self.frame_4, text= "cm²", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm24.place(relx= 0.80, rely=0.72)
        
        # FRAME PARA VALOR NBA
        self.label_k = Label(self.frame_4, bg = "white")
        self.label_k.place(relx=0.30, rely=0.7775, relwidth= 0.6, relheight=0.03) 
        self.lb_nba = Label(self.frame_4, text= "Nba", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_nba.place(relx= 0.05, rely=0.7775)
        self.lb_barras1 = Label(self.frame_4, text= "barras", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_barras1.place(relx= 0.80, rely=0.7775)

        # FRAME PARA VALOR NBB
        self.label_l = Label(self.frame_4, bg = "white")
        self.label_l.place(relx=0.30, rely=0.835, relwidth= 0.6, relheight=0.03) 
        self.lb_nbb = Label(self.frame_4, text= "Nbb", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_nbb.place(relx= 0.05, rely=0.835)
        self.lb_barras2 = Label(self.frame_4, text= "barras", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_barras2.place(relx= 0.80, rely=0.835)
        
        # FRAME PARA VALOR ESP'A
        self.label_m = Label(self.frame_4, bg = "white")
        self.label_m.place(relx=0.30, rely=0.8925, relwidth= 0.6, relheight=0.03) 
        self.lb_espa = Label(self.frame_4, text= "esp'a", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_espa.place(relx= 0.05, rely=0.8925)
        self.lb_cm31 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm31.place(relx= 0.80, rely=0.8925)
        
        # FRAME PARA VALOR ESP'B
        self.label_n = Label(self.frame_4, bg = "white")
        self.label_n.place(relx=0.30, rely=0.95, relwidth= 0.6, relheight=0.03) 
        self.lb_espb = Label(self.frame_4, text= "esp'b", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_espb.place(relx= 0.05, rely=0.95)
        self.lb_cm32 = Label(self.frame_4, text= "cm", bg = "#99BFBB",fg = "black", font=("arial","10") )
        self.lb_cm32.place(relx= 0.80, rely=0.95)


    def menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        
        def Quit(): self.janela.destroy ()

        menubar.add_cascade(label="Opções", menu = filemenu)

        filemenu.add_command(label="Imprimir resultados",command = self.gerar_relatorios) 
        filemenu.add_command(label="Sair", command=Quit)  # Adiciona o comando "Sair" no menu
          
rina()