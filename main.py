import os
import flet as ft
from pytubefix import YouTube
from tkinter import filedialog
from time import sleep
import threading

def Download_musica(url ='str', destination='str',texto_download ='str',barra_de_progresso='str'):
    
    yt = YouTube(url,'WEB') #Link do video da musica
    #nova funcao

    try:
        video = yt.streams.filter(only_audio=True).first() 
        use_po_token=True
        # DOWNLOAD DO ARQUIVO
        out_file = video.download(output_path=destination)
        # SALVAR NA PASTA 
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
      # RESULTADO DO DOWNLOAD
        print(yt.title)
        print(" O Download da Musica Foi concluido !!")
        texto_download.visible = False
        texto_download.update()
        barra_de_progresso.visible = False
        barra_de_progresso.update() 
        
    except Exception as e:
        print("Erro: " + str(e))

    
def Download_video(url ='str', destination='str',texto_download ='str',barra_de_progresso='str'):
    video = YouTube(url,'WEB') #Link do video da video
    
    try:
        video = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        use_po_token=True
        # DOWNLOAD DO ARQUIVO
        out_file = video.download(output_path=destination)
        # SALVAR NA PASTA 
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp4'
        os.rename(out_file, new_file) 

        # RESULTADO DO DOWNLOAD
        print(" O Download do Video foi concluido !!")
        texto_download.visible = False
        texto_download.update()
        barra_de_progresso.visible = False
        barra_de_progresso.update()
        
    
    except Exception as e:
        print("Erro: " + str(e))
    
def Tela_aplicativo(pagina:ft.Page):
    pagina.window_width = 600  # Largura da janela
    pagina.window_height = 900  # Altura da janela
    pagina.title = "Download My Music"
    pagina.horizontal_alignment = 'center'
    pagina.vertical_alignment = "center"
    pagina.bgcolor = ft.colors.BLUE_GREY_900
    
    pb = ft.ProgressBar(width=400,visible=False)
    
    titulo = ft.Text("Download My Music",style="headLineMedium")
    txt_URL = ft.Text("Digite sua URL a baixo: ")
    URL = ft.TextField(label="URL = youtube.com.",text_align=ft.TextAlign.LEFT, width=520)
    txt_destination = ft.Text("Pressione 'Buscar' Para Achar a Pasta Desejada: ")
    Destination = ft.TextField(label="Destination.",text_align=ft.TextAlign.LEFT, width=520)
    buscar = ft.ElevatedButton("Buscar Diretorio", on_click=lambda e: abrir_pasta(Destination,pagina))
    resultado_text = ft.Text("",style="bodyLarge")
    texto_download = ft.Text("Aguarde o Download...",visible = False)
    barra_de_progresso = ft.ProgressBar(width=400,visible=False)
    btn_baixar = ft.ElevatedButton("Baixar", on_click = lambda e: on_download(URL.value, Destination.value, resultado_text,check_video,check_music,pb,texto_download,barra_de_progresso))
    clear = ft.ElevatedButton("Limpar", on_click=lambda e: limpar_campos(URL, Destination, resultado_text,pb))
    check_video = ft.Checkbox(label="Baixar Video")
    check_music = ft.Checkbox(label="Baixar Music")
    image_tumbr = ft.Image(src="C:\\Users\GUSTAVO E HELOISA\\Downloads\\vali.jpg", width=500, height=250)
    
    
    def pressionado_disable(nao_pressionado, pressionado): #Função para desativar o botao
        if nao_pressionado.value:
            pressionado.disabled = True
        else:
            pressionado.disabled = False
        pressionado.update()
    
    check_video.on_change = lambda e: pressionado_disable(check_video, check_music)
    check_music.on_change = lambda e: pressionado_disable(check_music, check_video)
    
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
                image_tumbr,
                txt_URL,
                URL,
                txt_destination,
                Destination,
                ft.Row(
                    [check_video,check_music],alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ft.Row(
                    [
                        buscar,
                        btn_baixar,
                        clear,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([resultado_text],alignment=ft.MainAxisAlignment.CENTER),
                ft.Column(
                    [
                        texto_download,
                        barra_de_progresso,
                        pb,
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
)
    
def limpar_campos(URL: ft.TextField, Destination: ft.TextField, resultado_text: ft.Text,pb:ft.ProgressBar):
    URL.value = ""
    Destination.value = ""
    resultado_text.value = ""
    URL.update()
    Destination.update()
    resultado_text.update()
     
def abrir_pasta(destination_field: ft.TextField,pagina:ft.Page):
    def thread_function():
        pasta = filedialog.askdirectory(title="Selecione a Pasta",initialdir=os.getcwd())  # Abre o diálogo para escolher uma pasta
        if pasta:
            # Atualiza o campo de texto com o caminho da pasta escolhida
            destination_field.value = pasta
            destination_field.update()
            
    thread =threading.Thread(target=thread_function)
    thread.start()

def on_download(url: str, destination: str, resultado_text: ft.Text,check_video: ft.Checkbox,check_music: ft.Checkbox,pb:ft.ProgressBar,texto_download:ft.Text,barra_de_progresso:ft.ProgressBar):
    if not url:
        resultado_text.value = "Por favor, insira uma URL válida."
        return
    if not destination:
        destination = abrir_pasta()
        resultado_text.value = "Por favor, insira um caminho de destino."
        return
    try:
        if check_music.value == True:
            #Atualinzando a barra de progresso do download
            texto_download.visible = True
            barra_de_progresso.visible = True
            texto_download.update()
            barra_de_progresso.update()
            pb.value = 0
            for i in range(0,101):
                pb.value = i*0.02
                sleep(0.1)
                pb.update()
                
            resultado = Download_musica(url, destination,texto_download,barra_de_progresso)   
            resultado_text.value = f"Download da musica Concluido !!"
            
        if check_video.value == True:
            #Atualinzando a barra de progresso do download
            texto_download.visible = True
            barra_de_progresso.visible = True
            texto_download.update()
            barra_de_progresso.update()
            pb.value = 0
            for i in range(0,101):
                pb.value = i*0.02
                sleep(0.1)
                pb.update()
                
            #Chamando a funcao e mostrando o resuldado na tela
            resultado = Download_video(url, destination,texto_download,barra_de_progresso)
            resultado_text.value = f"Download do video Concluido !!"
    except Exception as e:
        resultado_text.value = f"Erro: {e}"
    # Atualiza o texto na interface
    resultado_text.update()
    
ft.app(target=Tela_aplicativo)
