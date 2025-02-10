import os
import flet as ft
from pytubefix import YouTube
from tkinter import filedialog
from time import sleep
import threading


class Aplicativo_Downloader_Musica():
      
    @classmethod
    def _download_musica(cls, url:str,destination:str, texto_download:str,barra_de_progresso:str ):
    
        """
        Baixa a musica do youtube e salva no destino especifico.

        Args:
            url (str): URL do video da musica.
            destination (str): Caminho do destino da musica.
            texto_download (str): Texto a ser exibido na tela de download.
            barra_de_progresso (str): Barra de progresso a ser exibida na tela de download.

        Returns:
            None
        """    
        yt = YouTube(url,'WEB') #Link do video da musica
        
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
            print(" O Download do Video foi concluido !!")
            texto_download.visible = False
            barra_de_progresso.visible = False
            barra_de_progresso.update()
            texto_download.update()
        except Exception as e:
            print("Erro: " + str(e))

    @classmethod
    def _download_video(cls, url:str, destination:str, texto_download:str, barra_de_progresso:str):
        """
        Baixa o vídeo do YouTube e salva no destino especificado.

        Args:
            url (str): URL do vídeo do YouTube.
            destination (str): Caminho do destino para salvar o vídeo.
            texto_download (str): Texto a ser exibido durante o download.
            barra_de_progresso (str): Barra de progresso a ser exibida durante o download.

        Returns:
            None
        """

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
            barra_de_progresso.visible = False
            barra_de_progresso.update()
            texto_download.update()
        
        except Exception as e:
            print("Erro: " + str(e))
    
    @classmethod
    def _limpar_campos(cls, url: ft.TextField, destination: ft.TextField, resultado_text: ft.Text,pb:ft.ProgressBar,image_tumbr:ft.Image):
        """
        Resets the values of the provided UI components to their default states.

        Args:
            url (ft.TextField): The text field for the URL input, which will be cleared.
            destination (ft.TextField): The text field for the destination input, which will be cleared.
            resultado_text (ft.Text): The text component for displaying results, which will be cleared.
            pb (ft.ProgressBar): The progress bar, which will be reset to zero.
            image_tumbr (ft.Image): The image component for the thumbnail, which will be reset to the default thumbnail image.

        This function clears the input fields, sets the progress bar to 0, and resets the thumbnail image 
        to a default image. It then updates the components to reflect these changes.
        """

        url.value = ""
        destination.value = ""
        resultado_text.value = ""
        pb.value = 0
        image_tumbr.src = "C:\\Users\\GUSTAVO E HELOISA\\Pictures\\no-tumbnail.jpg"  # Reset to default thumbnail
        url.update()
        destination.update()
        resultado_text.update()
        pb.update()
        image_tumbr.update()
     
    @classmethod    
    def _abrir_pasta(cls, destination_field: ft.TextField,image_tumbr:ft.Image,url:str):
        """
        Abre o diálogo para escolher uma pasta e atualiza o campo de texto com o caminho da pasta escolhida.

        Args:
            destination_field (ft.TextField): Campo de texto que sera atualizado com o caminho da pasta escolhida.
            image_tumbr (ft.Image): Imagem que sera atualizada com o thumbnail do video.
            url (str): URL do video do youtube que sera usado para obter o thumbnail.
        """
        image_tumbr.src = YouTube(url,'WEB').thumbnail_url
        image_tumbr.visible = True
        image_tumbr.update()
        
        def thread_function():
            pasta = filedialog.askdirectory(title="Selecione a Pasta",initialdir=os.getcwd())  # Abre o diálogo para escolher uma pasta
            if pasta:
                # Atualiza o campo de texto com o caminho da pasta escolhida
                destination_field.value = pasta
                destination_field.update()
            
        thread =threading.Thread(target=thread_function)
        thread.start()
    
    @classmethod
    def _on_download(cls, url: str, destination: str, resultado_text: ft.Text,check_video: ft.Checkbox,check_music: ft.Checkbox,pb:ft.ProgressBar,texto_download:ft.Text,barra_de_progresso:ft.ProgressBar,image_tumbr:ft.Image):
        """
        Handles the download process for music or video from a given URL.

        Args:
            url (str): The URL of the content to download.
            destination (str): The destination path where the content will be saved.
            resultado_text (ft.Text): UI component to display the result of the download operation.
            check_video (ft.Checkbox): Checkbox component indicating whether to download video.
            check_music (ft.Checkbox): Checkbox component indicating whether to download music.
            pb (ft.ProgressBar): Progress bar component to show download progress.
            texto_download (ft.Text): Text component indicating the download status.
            barra_de_progresso (ft.ProgressBar): Another progress bar component for download status.
            image_tumbr (ft.Image): Image component for displaying the thumbnail.

        Returns:
            None
        """

        if not url:
            resultado_text.value = "Por favor, insira uma URL válida."
            return
        if not destination:
            destination = cls._abrir_pasta()
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
                

                resultado = cls._download_musica(url, destination,texto_download,barra_de_progresso)   
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
                resultado = cls._download_video(url, destination,texto_download,barra_de_progresso)
                resultado_text.value = f"Download do video Concluido !!"
        except Exception as e:
            resultado_text.value = f"Erro: {e}"
        # Atualiza o texto na interface
        resultado_text.update()

    @classmethod
    def _pressionado_disable(cls, nao_pressionado, pressionado): #Função para desativar o botao
        """
        Desativa ou ativa um botão com base no estado de outro componente.

        Args:
            nao_pressionado: Componente que controla o estado do botão 'pressionado'.
            pressionado: O botão que será ativado ou desativado.
        """

        if nao_pressionado.value:
            pressionado.disabled = True
        else:
            pressionado.disabled = False
        pressionado.update()
            
    def _tela_aplicativo(self, pagina:ft.Page):
        """
        Configura a tela do aplicativo com os componentes necessarios.
        
        Args:
            pagina (ft.Page): A página que sera configurada.
        """
        
        pagina.window.width = 600
        pagina.window.height = 900
        pagina.title = "Download My Music"
        pagina.horizontal_alignment = 'center'
        pagina.vertical_alignment = 'center'
        pagina.bgcolor = ft.colors.BLUE_GREY_800
        
        pb = ft.ProgressBar(width=400,visible=False)
        
        #Criando os componentes
        image_tumbr = ft.Image(src="C:\\Users\\GUSTAVO E HELOISA\\Pictures\\no-tumbnail.jpg", width=500, height=250)
        titulo = ft.Text("Download My Music",style="headLineMedium")
        txt_URL = ft.Text("Digite sua URL a baixo: ")
        URL = ft.TextField(label="URL = youtube.com.",text_align=ft.TextAlign.LEFT, width=520)
        txt_destination = ft.Text("Pressione 'Buscar' Para Achar a Pasta Desejada: ")
        Destination = ft.TextField(label="Destination.",text_align=ft.TextAlign.LEFT, width=520)
        buscar = ft.ElevatedButton("Buscar Diretorio", on_click=lambda e: self._abrir_pasta(Destination,image_tumbr,URL.value))
        resultado_text = ft.Text("",style="bodyLarge")
        texto_download = ft.Text("Aguarde o Download...",visible = False)
        barra_de_progresso = ft.ProgressBar(width=400,visible=False)
        btn_baixar = ft.ElevatedButton("Baixar", on_click = lambda e: self._on_download(URL.value, Destination.value, resultado_text,check_video,check_music,pb,texto_download,barra_de_progresso,image_tumbr))
        clear = ft.ElevatedButton("Limpar", on_click=lambda e: self._limpar_campos(URL, Destination, resultado_text,pb,image_tumbr))
        check_video = ft.Checkbox(label="Baixar Video")
        check_music = ft.Checkbox(label="Baixar Music")
        
    
        check_video.on_change = lambda e: self._pressionado_disable(check_video, check_music)
        check_music.on_change = lambda e: self._pressionado_disable(check_music, check_video)
        
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

    def _run(self):
        ft.app(target=self._tela_aplicativo)
