from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from android.runnable import run_on_ui_thread
from jnius import autoclass, PythonJavaClass, java_method

# Classes do Android Java
WebView = autoclass('android.webkit.WebView')
WebChromeClient = autoclass('android.webkit.WebChromeClient')
Intent = autoclass('android.content.Intent')
Activity = autoclass('android.app.Activity')

class CustomWebChromeClient(PythonJavaClass):
    __javainterfaces__ = ['android/webkit/WebChromeClient']
    __javacontext__ = 'app'

    def __init__(self, activity):
        super().__init__()
        self.activity = activity

    @java_method('(Landroid/webkit/WebView;Landroid/net/Uri;Landroid/webkit/WebChromeClient$FileChooserParams;)Z')
    def onShowFileChooser(self, webview, filePathCallback, fileChooserParams):
        # Dispara o seletor de arquivos nativo do Android
        intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.setType("video/*")
        self.activity.startActivityForResult(intent, 100)
        return True

class MainApp(App):
    def build(self):
        layout = BoxLayout()
        self.create_webview()
        return layout

    @run_on_ui_thread
    def create_webview(self):
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setAllowFileAccess(True)
        webview.getSettings().setAllowContentAccess(True)
        
        # Ativa suporte para arquivos no Android
        chrome_client = CustomWebChromeClient(activity)
        webview.setWebChromeClient(chrome_client)

        # Carrega o HTML da pasta templates
        webview.loadUrl("file:///android_asset/templates/index.html")

if __name__ == '__main__':
    MainApp().run()
