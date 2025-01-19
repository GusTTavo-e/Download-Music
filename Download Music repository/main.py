import os
import flet as ft
from pytubefix import *
from tkinter import filedialog

def Download_musica(url ='str', destination='str',name='str'):
    
    yt = YouTube(url) #Link do video da musica

    try:
        video = yt.streams.filter(only_audio=True).first() 
        # DOWNLOAD DO ARQUIVO
        out_file = video.download(output_path=destination)
        # SALVAR NA PASTA 
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
    except Exception as e:
        print("Erro: " + str(e))
        
    # RESULTADO DO DOWNLOAD
    name.value = yt.title
    print(yt.title + " O Download da Musica Foi concluido !!")

    
def Tela_aplicativo(pagina:ft.Page):
    pagina.window_width = 600  # Largura da janela
    pagina.window_height = 900  # Altura da janela
    pagina.title = "Download My Music"
    pagina.horizontal_alignment = 'center'
    pagina.vertical_alignment = "center"
    pagina.bgcolor = ft.colors.BLUE_GREY_900
    
    titulo = ft.Text("Download My Music",style="headLineMedium")
    txt_URL = ft.Text("Digite sua URL a baixo: ")
    URL = ft.TextField(label="URL = youtube.com.",text_align=ft.TextAlign.LEFT, width=520)
    txt_destination = ft.Text("Pressione 'Buscar' Para Achar a Pasta Desejada: ")
    Destination = ft.TextField(label="Destination.",text_align=ft.TextAlign.LEFT, width=520)
    buscar = ft.ElevatedButton("Buscar Diretorio", on_click=lambda e: abrir_pasta(Destination))
    resultado_text = ft.Text("",style="bodyMedium")
    btn_baixar = ft.ElevatedButton("Baixar", on_click = lambda e: on_download(URL.value, Destination.value, resultado_text, name))
    clear = ft.ElevatedButton("Limpar", on_click=lambda e: limpar_campos(URL, Destination, resultado_text))
    name = ft.Text("")
    
   #Layout da Pagina
    pagina.add(
       
    ft.Container(
        width=450,  # Largura da tela ou container
        height=800,  # Altura da tela ou container
        bgcolor=ft.colors.WHITE,  # Cor de fundo para visualização
        padding=(20),
        border_radius=25,  
        content=ft.Column(
            [
                ft.Row([titulo],alignment=ft.MainAxisAlignment.CENTER),
                txt_URL,
                URL,
                txt_destination,
                Destination,
                ft.Row([resultado_text],alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    [
                        buscar,
                        btn_baixar,
                        clear,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        
    )
)
    
def limpar_campos(URL: ft.TextField, Destination: ft.TextField, resultado_text: ft.Text):
    URL.value = ""
    Destination.value = ""
    resultado_text.value = ""
    URL.update()
    Destination.update()
    resultado_text.update()
    
def abrir_pasta(destination_field: ft.TextField):
    pasta = filedialog.askdirectory()  # Abre o diálogo para escolher uma pasta
    if pasta:
        # Atualiza o campo de texto com o caminho da pasta escolhida
        destination_field.value = pasta
        destination_field.update()

def on_download(url: str, destination: str, resultado_text: ft.Text,name: ft.Text):
    if not url:
        resultado_text.value = "Por favor, insira uma URL válida."
        return
    if not destination:
        destination = abrir_pasta()
        resultado_text.value = "Por favor, insira um caminho de destino."
        return
    try:
        resultado = Download_musica(url, destination,name)
        resultado_text.value = f"Download da musica {name.value} Concluido !!"
    except Exception as e:
        resultado_text.value = f"Erro: {e}"
    # Atualiza o texto na interface
    resultado_text.update()
  
ft.app(target=Tela_aplicativo)
