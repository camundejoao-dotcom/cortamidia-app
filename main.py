import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import mainthread
from kivy.utils import platform
import yt_dlp

class CortaMidiaLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # Titulo
        self.add_widget(Label(text="✂️ CortaMídia Pro", font_size='24sp', bold=True, color=(0, 0.9, 0.4, 1), size_hint_y=None, height=40))

        # Input URL
        self.url_input = TextInput(hint_text="Cole o link do vídeo (YouTube, Insta, TikTok)...", multiline=False, size_hint_y=None, height=50)
        self.add_widget(self.url_input)

        # Minutagem
        self.add_widget(Label(text="Minutagem do Corte (Início - Fim):", size_hint_y=None, height=20, color=(0.7, 0.7, 0.7, 1)))
        
        time_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        self.inicio_input = TextInput(hint_text="Início (ex: 01:20)", multiline=False)
        self.fim_input = TextInput(hint_text="Fim (ex: 02:45)", multiline=False)
        time_layout.add_widget(self.inicio_input)
        time_layout.add_widget(self.fim_input)
        self.add_widget(time_layout)

        # Botao
        self.btn_baixar = Button(text="CORTAR E BAIXAR", background_color=(0, 0.9, 0.4, 1), bold=True, size_hint_y=None, height=50)
        self.btn_baixar.bind(on_release=self.iniciar_download)
        self.add_widget(self.btn_baixar)

        # Progresso
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=20)
        self.add_widget(self.progress_bar)

        # Status
        self.status_label = Label(text="Aguardando...", color=(0.8, 0.8, 0.8, 1), size_hint_y=None, height=30)
        self.add_widget(self.status_label)

    def iniciar_download(self, instance):
        url = self.url_input.text.strip()
        inicio = self.inicio_input.text.strip()
        fim = self.fim_input.text.strip()

        if not url:
            self.status_label.text = "Por favor, insira o link!"
            return

        self.btn_baixar.disabled = True
        self.status_label.text = "Iniciando corte..."
        threading.Thread(target=self._processar_corte, args=(url, inicio, fim), daemon=True).start()

    def _processar_corte(self, url, inicio, fim):
        output_dir = "/sdcard/Download/Cortes"
        os.makedirs(output_dir, exist_ok=True)

        def progress_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                downloaded = d.get('downloaded_bytes', 0)
                percent = (downloaded / total) * 100
                self.atualizar_progresso(percent, f"Baixando: {round(percent, 1)}%")
            elif d['status'] == 'finished':
                self.atualizar_progresso(100, "Corte Concluído! 🎉")

        ydl_opts = {
            'outtmpl': f'{output_dir}/Corte_%(title)s.%(ext)s',
            'progress_hooks': [progress_hook],
            'format': 'bestvideo[height<=720]+bestaudio/best',
            'extractor_args': {'youtube': ['player_client=android,web']}
        }

        if inicio or fim:
            t_start = inicio if inicio else "00:00"
            t_end = fim if fim else "inf"
            ydl_opts['download_ranges'] = yt_dlp.utils.download_range_func(None, [(t_start, t_end)])
            ydl_opts['force_keyframes_at_cuts'] = True

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.atualizar_progresso(0, f"Erro: {str(e)[:30]}...")
        finally:
            self.liberar_botao()

    @mainthread
    def atualizar_progresso(self, valor, texto):
        self.progress_bar.value = valor
        self.status_label.text = texto

    @mainthread
    def liberar_botao(self):
        self.btn_baixar.disabled = False

class CortaMidiaApp(App):
    def build(self):
        return CortaMidiaLayout()

if __name__ == '__main__':
    CortaMidiaApp().run()
