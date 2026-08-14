package com.exemplo.cortador

import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.arthenica.ffmpegkit.FFmpegKit
import com.arthenica.ffmpegkit.ReturnCode

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            TelaPrincipal()
        }
    }

    @Composable
    fun TelaPrincipal() {
        var uriSelecionada by remember { mutableStateOf<Uri?>(null) }
        var tempoInicio by remember { mutableStateOf("00:00:00") }
        var tempoFim by remember { mutableStateOf("00:00:10") }
        var processando by remember { mutableStateOf(false) }

        val seletorMidia = rememberLauncherForActivityResult(
            contract = ActivityResultContracts.GetContent()
        ) { uri: Uri? -> uriSelecionada = uri }

        Column(
            modifier = Modifier.fillMaxSize().padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Button(onClick = { seletorMidia.launch("*/*") }) {
                Text(if (uriSelecionada == null) "Selecionar Vídeo ou Música" else "Mídia Selecionada!")
            }

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = tempoInicio,
                onValueChange = { tempoInicio = it },
                label = { Text("Início (HH:MM:SS)") }
            )

            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = tempoFim,
                onValueChange = { tempoFim = it },
                label = { Text("Fim (HH:MM:SS)") }
            )

            Spacer(modifier = Modifier.height(16.dp))

            if (processando) {
                CircularProgressIndicator()
                Spacer(modifier = Modifier.height(8.dp))
                Text("Cortando mídia...")
            } else {
                Button(
                    onClick = {
                        if (uriSelecionada != null) {
                            processando = true
                            executarCorte(uriSelecionada!, tempoInicio, tempoFim) { sucesso ->
                                processando = false
                                if (sucesso) {
                                    Toast.makeText(this@MainActivity, "Corte concluído!", Toast.LENGTH_SHORT).show()
                                } else {
                                    Toast.makeText(this@MainActivity, "Erro ao cortar", Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    },
                    enabled = uriSelecionada != null
                ) {
                    Text("Cortar Mídia")
                }
            }
        }
    }

    private fun executarCorte(uri: Uri, inicio: String, fim: String, aoFinalizar: (Boolean) -> Unit) {
        val arquivoSaida = "${externalCacheDir?.absolutePath}/corte_output.mp4"
        val cmd = "-ss $inicio -to $fim -i \"$uri\" -c copy \"$arquivoSaida\""

        FFmpegKit.executeAsync(cmd) { session ->
            val returnCode = session.returnCode
            runOnUiThread {
                aoFinalizar(ReturnCode.isSuccess(returnCode))
            }
        }
    }
}

