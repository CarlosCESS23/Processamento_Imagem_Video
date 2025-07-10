import tkinter as tk
import customtkinter
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk


class Processador(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.current_file = None # Armazena o caminho do arquivo atualmente aberto
        self.is_video = False #Informa se o aqruivo aberto é um video
        self.cap = None #Armazena o objeto VideoCapture da Visão Computacional     
        self.current_frame = None # Armazena o frame atual do video
        self.original_frame = None #Armazena o frame original antes da aplicação do video
        self.previous_frame = None #Guarda o frame anterior antes da aplicação do filtro
        self.video_speed = 2.0 #Controla a velocidade da reprodução de vidoe
        self.image_offset = (0, 0) #Define o deslocamento da imagem dentro do canvas     
        self.applied_filter = None #Armazena o filtro
        self.filter_history = [] # Uma lista que armazena o historíco de filtros aplicado
        self.geometry = ("700x800")
        self.title("Processamento de Imagem e Video")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Variáveis para a funcionalidade ROI
        self.roi_start = None
        self.roi_end = None
        self.drawing_roi = False
        self.roi_selected = False
        self.roi_mode = False  # Variável para controlar o modo de seleção de ROI

        self.setup_gui()

    def setup_gui(self):
        self.configuracao_topo_GUI()

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=15)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.canvas = customtkinter.CTkCanvas(self.main_frame, width=800, height=600, bg="black", highlightthickness=0)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        # Eventos de mouse para a funcionalidade ROI
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.adicionar_botoes_abaixo()

    def adicionar_botoes_abaixo(self):
        self.modo_processo = tk.StringVar(value="independente")

        self.DownControl = customtkinter.CTkFrame(self, corner_radius=20, height=40)
        self.DownControl.grid(row=2, column=0, padx=10, pady=10, sticky="ns")

        # Botão ROI
        button_roi = customtkinter.CTkButton(self.DownControl, text="Selecionar ROI", command=self.toggle_roi_mode, corner_radius=20, width=70, height=20, text_color="white", font=("Trebuchet MS", 12, "bold"))
        button_roi.grid(row=4, column=0, padx=15, pady=15)

        # Dicionário para mapear nomes de filtros para funções
        self.filters = {
            "Sharpen": self.aplicar_sharpen,
            "Blur": self.aplicar_blur,
            "Emboss": self.aplicar_emboss,
            "Laplacian": self.aplicar_laplacian,
            "Canny": self.aplicar_canny,
            "Gray": self.aplicar_gray,
            "Sobel": self.aplicar_sobel,
            "Binary": self.aplicar_binario,
            "Cores": self.aplicar_cores_normais
        }

        # Criação dinâmica de botões com base no dicionário de filtros
        row_num = 4
        col_num = 1
        for filter_name, filter_function in self.filters.items():
            button = customtkinter.CTkButton(self.DownControl, text=filter_name, command=lambda f=filter_function: self.apply_filter_wrapper(f), corner_radius=20, width=70, height=20, text_color="white", font=("Trebuchet MS", 12, "bold"))
            button.grid(row=row_num, column=col_num + 1, padx=15, pady=15)
            col_num += 1
            if col_num > 3:
                col_num = 1
                row_num += 1

        # Botão Desfazer
        button_undo = customtkinter.CTkButton(self.DownControl, text="Desfazer", command=self.desfazer_filtros, corner_radius=20, width=70, height=20, text_color="white", font=("Trebuchet MS", 12, "bold"))
        button_undo.grid(row=row_num, column=col_num+1, padx=15, pady=15)
        col_num += 2

        # Botão Salvar
        button_salvar = customtkinter.CTkButton(self.DownControl, text="Salvar", command=self.Salvar, corner_radius=20, width=70, height=20, text_color="white", font=("Trebuchet MS", 12, "bold"))
        button_salvar.grid(row=row_num, column=col_num, padx=15, pady=15)


    def configuracao_topo_GUI(self):

        self.topControl = customtkinter.CTkFrame(self, corner_radius=20, height=40)
        self.topControl.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        botao_imagem = customtkinter.CTkButton(self.topControl, text="Abrir Imagem", command=self.selecionar_foto, corner_radius=20, width=40, height=40, font=("Arial", 16, "bold"))
        botao_imagem.grid(row=0, column=0, padx=10, pady=10)

        botao_webcam = customtkinter.CTkButton(self.topControl, text="Abrir a Webcam", command=self.AbrirWebCam, corner_radius=20, width=40, height=40, font=("Arial", 16, "bold"))
        botao_webcam.grid(row=0, column=2, padx=10, pady=10)

        botao_video = customtkinter.CTkButton(self.topControl, text="Abrir Video", command=self.selecionarVideo, corner_radius=20, width=40, height=40, font=("Arial", 16, "bold"))
        botao_video.grid(row=0, column=4, padx=10, pady=10)

    def selecionar_foto(self):
        arquivoImagem = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        nomeArquivo = filedialog.askopenfilename(filetypes=arquivoImagem)

        if nomeArquivo:
            self.current_file = nomeArquivo
            self.abrirImagem()

    def abrirImagem(self):

        try:
            # Carregar a imagem usando OpenCV
            self.current_frame = cv2.imread(self.current_file)
            if self.current_frame is not None:
                # Armazenar o frame original para referência
                self.original_frame = self.current_frame.copy()
                self.previous_frame = self.current_frame.copy()
                self.filter_history = []
                self.is_video = False
                self.reset_roi()
                self.show_frame()
            else:
                print("Erro: A imagem não foi carregada corretamente.")
                self.original_frame = None
        except Exception as e:
            print(f"Erro ao abrir a imagem: {e}")
            self.original_frame = None

    def selecionarVideo(self):
        arquivoVideo = [("Video files", "*.mp4")]
        nomeArquivo = filedialog.askopenfilename(filetypes=arquivoVideo)

        if nomeArquivo:
            self.current_file = nomeArquivo
            self.abrir_video()

    def abrir_video(self):
        self.cap = cv2.VideoCapture(self.current_file)
        self.filter_history = []
        self.is_video = True
        self.reset_roi()
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame.copy()
            self.original_frame = frame.copy()
            self.previous_frame = frame.copy()
        self.atualizar_video()

    def AbrirWebCam(self):
        self.cap = cv2.VideoCapture(0)
        self.filter_history = []
        self.is_video = True
        self.reset_roi()
        if not self.cap.isOpened():
            messagebox.showerror("Não foi possivel abrir a camera")
            return
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame.copy()
            self.original_frame = frame.copy()
            self.previous_frame = frame.copy()

        self.is_paused = False
        self.atualizar_video()

    def atualizar_video(self):
        if self.cap is not None and not self.is_paused:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()

                # Verificação de diferença apenas se os tamanhos forem iguais
                if self.previous_frame is not None and self.current_frame.shape == self.previous_frame.shape:
                    diff = cv2.absdiff(self.current_frame, self.previous_frame)
                    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                    if np.sum(gray) > 100:
                        temp_frame = self.aplicar_filtros_roi(self.current_frame.copy())
                        self.current_frame = temp_frame

                self.previous_frame = frame.copy()
                self.show_frame()
                self.after(30, self.atualizar_video)
            else:
                # Fim do vídeo, reseta variáveis (mas diferencia de webcam)
                if self.current_file:
                    self.cap.release()
                    self.cap = None
                    self.current_frame = None
                    self.previous_frame = None
                    self.applied_filter = None
                    self.filter_history = []
                    self.canvas.delete("all")

    def show_frame(self):
        if self.current_frame is not None:
            # Aplica os filtros, se a ROI estiver selecionada
            frame_to_show = self.current_frame.copy()
            if self.roi_selected:
                frame_to_show = self.aplicar_filtros_roi(frame_to_show)

            # Converter para RGB para exibição
            frame_rgb = cv2.cvtColor(frame_to_show, cv2.COLOR_BGR2RGB)

            # Ajustar tamanho ao canvas
            height, width = frame_rgb.shape[:2]
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            ratio = min(canvas_width / width, canvas_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            # Redimensionar a imagem
            frame_resized = cv2.resize(frame_rgb, (new_width, new_height))

            # Converter para PIL Image e depois para PhotoImage
            image_pil = Image.fromarray(frame_resized)
            self.photo = ImageTk.PhotoImage(image_pil)

            # Exibir no Canvas
            self.canvas.delete("all")
            self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.photo, anchor="center")

            # Desenhar o retângulo da ROI, se estiver selecionada e o modo ROI estiver ativo
            if self.roi_selected and self.roi_mode:
                # Ajustar as coordenadas da ROI para a exibição no canvas
                x1, y1 = self.roi_start
                x2, y2 = self.roi_end
                x1_canvas = int(x1 * ratio) + (canvas_width - new_width) // 2
                y1_canvas = int(y1 * ratio) + (canvas_height - new_height) // 2
                x2_canvas = int(x2 * ratio) + (canvas_width - new_width) // 2
                y2_canvas = int(y2 * ratio) + (canvas_height - new_height) // 2
                self.canvas.create_rectangle(x1_canvas, y1_canvas, x2_canvas, y2_canvas, outline="red", width=2)

    def apply_filter_wrapper(self, filter_function):

        if filter_function == self.aplicar_cores_normais:
            self.filter_history = [self.aplicar_cores_normais]
        else:
            self.filter_history.append(filter_function)

        if self.is_video and self.cap is not None:
            # Para vídeos e webcam, a aplicação do filtro é feita em atualizar_video e show_frame
            if self.current_frame is not None:
              self.show_frame()
        elif self.current_frame is not None:
            # Para imagens, aplica os filtros e atualiza a exibição
            self.current_frame = self.aplicar_filtros_roi(self.original_frame.copy())
            self.show_frame()

    def aplicar_filtros_roi(self, frame):
        """Aplica os filtros do histórico na ROI da imagem/frame."""
        if self.roi_selected:
            x1, y1 = self.roi_start
            x2, y2 = self.roi_end
            # Certifique-se de que as coordenadas estejam dentro dos limites do frame
            x1 = max(0, min(x1, frame.shape[1]))
            y1 = max(0, min(y1, frame.shape[0]))
            x2 = max(0, min(x2, frame.shape[1]))
            y2 = max(0, min(y2, frame.shape[0]))

            if x1 < x2 and y1 < y2:
                roi = frame[y1:y2, x1:x2]

                # Aplica os filtros na ROI
                for f in self.filter_history:
                    roi = f(roi)

                frame[y1:y2, x1:x2] = roi
        else:
            # Se não há ROI, aplica no frame inteiro
            for f in self.filter_history:
                frame = f(frame)
        return frame

    def desfazer_filtros(self):

        if self.filter_history:
            self.filter_history.pop()

            if self.is_video and self.cap is not None:
              # Para vídeos e webcam, a reaplicação do filtro é feita em show_frame
              self.show_frame()
            elif self.current_frame is not None:
                # Para imagens, reseta para o original e reaplica os filtros
                self.current_frame = self.aplicar_filtros_roi(self.original_frame.copy())
                self.show_frame()
        else:
            # Se não há filtros no histórico, volta para a imagem original
            if not self.is_video and self.original_frame is not None:
                self.current_frame = self.original_frame.copy()
                self.show_frame()



        #Detecta as bordas na imagem, ele usa para destacar mudanças bruscas de intesidades
    def aplicar_laplacian(self, frame):
        return cv2.Laplacian(frame, cv2.CV_64F).astype(np.uint8)

        #Cria um efeito de relevo, que aplica um kernel de convolução para gerar um efeito 3D nas bordas
    def aplicar_emboss(self, frame):
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        return cv2.filter2D(frame, -1, kernel)

        #Suaviza a imagem, remove os ruídos
    def aplicar_blur(self, frame):
        return cv2.GaussianBlur(frame, (5, 5), 0)

    #Aumenta a nitidez da imagem, que aplica um kernel de convolução que destaca as bordas e detalha
    def aplicar_sharpen(self, frame):
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        return cv2.filter2D(frame, -1, kernel)

    #Faz detecção bordas com alta precisão
    def aplicar_canny(self, frame):
        frame_image = cv2.Canny(frame, 100, 200)
        return cv2.cvtColor(frame_image, cv2.COLOR_GRAY2BGR)

    #Converte a imagem para tons cinzas
    def aplicar_gray(self, frame):
        frame_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(frame_image, cv2.COLOR_GRAY2BGR)

    #Detecta gradientes bordas verticais e horizontais
    def aplicar_sobel(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        sobel_combined = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
        sobel_combined = np.uint8(np.absolute(sobel_combined))
        return cv2.cvtColor(sobel_combined, cv2.COLOR_GRAY2BGR)

    #Converte a imagem para preto e branco
    def aplicar_binario(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

    #Isso retorna ao cores normais
    def aplicar_cores_normais(self, frame):
        if self.is_video:
            return frame
        else:
            return self.original_frame.copy()

    def reset_roi(self):
        """Reseta as variáveis relacionadas à ROI."""
        self.roi_start = None
        self.roi_end = None
        self.drawing_roi = False
        self.roi_selected = False

    def on_mouse_press(self, event):
        """Captura o ponto inicial da ROI (se o modo ROI estiver ativo)."""
        if self.roi_mode:
            # Ajustar as coordenadas do evento para a escala original da imagem
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if self.current_frame is not None:
                height, width = self.current_frame.shape[:2]
            else:
                height, width = [800,600]
            ratio = min(canvas_width / width, canvas_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            offset_x = (canvas_width - new_width) // 2
            offset_y = (canvas_height - new_height) // 2

            if offset_x <= event.x <= (canvas_width - offset_x) and offset_y <= event.y <= (canvas_height - offset_y):
                self.roi_start = (int((event.x - offset_x) / ratio), int((event.y - offset_y) / ratio))
                self.drawing_roi = True
                self.roi_selected = False

    def on_mouse_drag(self, event):
        """Desenha o retângulo da ROI enquanto o mouse é arrastado (se o modo ROI estiver ativo)."""
        if self.drawing_roi and self.roi_mode:
            # Ajustar as coordenadas do evento para a escala original da imagem
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if self.current_frame is not None:
                height, width = self.current_frame.shape[:2]
            else:
                height, width = [800,600]

            ratio = min(canvas_width / width, canvas_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            offset_x = (canvas_width - new_width) // 2
            offset_y = (canvas_height - new_height) // 2

            # Garante que o mouse não saia da área da imagem
            x = max(offset_x, min(event.x, canvas_width - offset_x - 1))
            y = max(offset_y, min(event.y, canvas_height - offset_y - 1))

            self.roi_end = (int((x - offset_x) / ratio), int((y - offset_y) / ratio))
            self.show_frame()  # Atualiza a exibição para mostrar o retângulo sendo desenhado

    def on_mouse_release(self, event):
      #Finaliza a seleção da ROI (se o modo ROI estiver ativo).rr[
      if self.drawing_roi and self.roi_mode:
          self.drawing_roi = False
          self.roi_selected = True
          # Garante que self.roi_start seja o ponto superior esquerdo e self.roi_end o inferior direito
          x1, y1 = self.roi_start
          x2, y2 = self.roi_end
          self.roi_start = (min(x1, x2), min(y1, y2))
          self.roi_end = (max(x1, x2), max(y1, y2))
          self.show_frame()

    def toggle_roi_mode(self):
        #Ativa/desativa o modo de seleção de ROI.
        self.roi_mode = not self.roi_mode
        if not self.roi_mode:
            self.reset_roi()
        self.show_frame()
        print(f"Modo ROI: {'Ativado' if self.roi_mode else 'Desativado'}")

    def Salvar(self):
        if self.current_frame is None:
            print("Nenhum quadro carregado")
            return

        if self.roi_selected:
            # Se a ROI estiver selecionada, salva apenas a ROI
            x1, y1 = self.roi_start
            x2, y2 = self.roi_end
            roi = self.current_frame[y1:y2, x1:x2]
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if file_path:
                cv2.imwrite(file_path, roi)
                messagebox.showinfo("Imagem salva com sucesso")
        else:
            # Se não houver ROI selecionada, salva o frame inteiro
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.current_frame)
                messagebox.showinfo("Imagem salva com sucesso")

if __name__ == "__main__":
    app = Processador()
    app.mainloop()