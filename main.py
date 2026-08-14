import os
import threading
from kivy.lang import Builder
from kivy.clock import mainthread
from kivymd.app import MDApp
import yt_dlp

KV = '''
MDScreen:
    md_bg_color: 0.07, 0.07, 0.07, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: "✂️ CortaMídia Pro"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 0.9, 0.4, 1
            bold: True

        MDTextField:
            id: url_input
            hint_text: "Cole o link do YouTube..."
            mode: "rectangle"

        MDLabel:
            text: "Minutagem do Corte (MM:SS):"
            theme_text_color: "Hint"
            font_style: "Caption"

        MDBoxLayout:
            spacing: "10dp"
            size_hint_y: None
            height: "60dp"

            MDTextField:
                id: inicio_input
                hint_text: "Início (ex: 01:20)"
                mode: "rectangle"

            MDTextField:
                id: fim_input
                hint_text: "Fim (ex: 02:45)"
                mode: "rectangle"

        MDRaisedButton:
            id: btn_baixar
            text: "CORTAR E BAIXAR"
            md_bg_color: 0, 0.9, 0.4, 1
            text_color: 0, 0, 0, 1
            size_hint_x: 1
            height: "50dp"
            on_release: app.iniciar_download()

        MDProgressBar:
            id: progress_bar
            value: 0
            color: 0, 0.9, 0.4, 1

        MDLabel:
            id: status_label
            text: "Aguardando..."
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.7, 0.7, 0.7, 1
'''

class CortaMidiaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def iniciar_download(self):
        url = self.root.ids.url_input.text.strip()
        inicio = self.root.ids.inicio_input.text.strip()
        fim = self.root.ids.fim_input.text.strip()

        if not url:
            self.root.ids.status_label.text = "Por favor, insira o link!"
            return

        self.root.ids.btn_baixar.disabled = True
        self.root.ids.status_label.text = "Iniciando corte..."
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
        self.root.ids.progress_bar.value = valor
        self.root.ids.status_label.text = texto

    @mainthread
    def liberar_botao(self):
        self.root.ids.btn_baixar.disabled = False

if __name__ == '__main__':
    CortaMidiaApp().run()
