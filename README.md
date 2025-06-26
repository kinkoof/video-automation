# Video Automation Project

Este projeto automatiza a criação de vídeos curtos para YouTube Shorts usando IA para geração de roteiros, síntese de voz e processamento de vídeo.

## 🚀 Funcionalidades

- **🧠 Geração de Roteiros**: Utiliza o modelo deepseek-r1 via OpenRouter para criar textos coesos e criativos
- **🎙️ Síntese de Voz**: Converte texto em áudio natural usando ElevenLabs TTS
- **🎬 Legendas**: Gera legendas automáticas em formato SRT
- **🎬 Montagem**: Combina áudio, vídeo de fundo, música e legendas usando FFmpeg
- **📲 Distribuição**: Preparado para integração com Google Drive e YouTube

## 📋 Pré-requisitos

- Python 3.8+
- FFmpeg instalado no sistema
- Chaves de API:
  - OpenRouter
  - ElevenLabs
  - Google Services (opcional para upload automático)

## 🛠️ Instalação

1. Clone ou baixe o projeto
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure suas chaves de API no arquivo `config/config.json`

4. Adicione seus arquivos de mídia:
   - `assets/background.mp4` - Vídeo de fundo
   - `assets/background_music.mp3` - Música de fundo

## 🎯 Como Usar

### Uso Básico

```python
from main import VideoAutomation

automation = VideoAutomation()

# Crie um vídeo com um prompt
prompt = "Crie um roteiro sobre exploração espacial para YouTube Shorts"
video_path = automation.create_video(prompt)

if video_path:
    print(f"Vídeo criado: {video_path}")
```

### Executar o exemplo

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
video-automation/
├── config/
│   └── config.json          # Configurações e chaves de API
├── src/
│   ├── __init__.py
│   ├── text_generation.py   # Geração de texto com OpenRouter
│   ├── audio_processing.py  # Processamento de áudio com ElevenLabs
│   ├── video_processing.py  # Processamento de vídeo com FFmpeg
│   ├── storage.py          # Integração com Google Drive (futuro)
│   ├── youtube.py          # Upload para YouTube (futuro)
│   └── spreadsheet.py      # Gerenciamento de planilhas (futuro)
├── assets/                  # Arquivos de mídia (vídeo e música de fundo)
├── output/                  # Vídeos gerados
├── requirements.txt
├── main.py                 # Script principal
└── README.md
```

## ⚙️ Configuração

Edite o arquivo `config/config.json` com suas credenciais:

```json
{
    "openrouter": {
        "api_key": "sua-chave-openrouter",
        "model": "deepseek/deepseek-r1"
    },
    "elevenlabs": {
        "api_key": "sua-chave-elevenlabs",
        "voice_id": "id-da-voz-escolhida"
    }
}
```

## 🔧 Próximos Passos

Para completar o pipeline de automação, você pode implementar:

1. **Integração com Google Sheets**: Para gerenciar roteiros
2. **Upload para Google Drive**: Para armazenamento automático
3. **Publicação no YouTube**: Para distribuição automática
4. **Sistema de filas**: Para processar múltiplos vídeos
5. **Interface web**: Para facilitar o uso

## 📝 Notas

- Certifique-se de ter FFmpeg instalado e acessível no PATH do sistema
- Os vídeos são otimizados para formato YouTube Shorts (9:16)
- O projeto inclui limpeza automática de arquivos temporários
- Para STT (Speech-to-Text), atualmente usa geração simples de legendas baseada no texto original

## 🐛 Solução de Problemas

- **Erro de FFmpeg**: Verifique se o FFmpeg está instalado e no PATH
- **Erro de API**: Verifique suas chaves de API no config.json
- **Arquivos de mídia**: Certifique-se de ter os arquivos de fundo na pasta assets/

## 📄 Licença

Este projeto é para uso pessoal e educacional.
