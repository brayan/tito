from pathlib import Path
from openai import OpenAI
from .config import OPENAI_API_KEY, MAX_CHARACTERS
from .utils import wrap_text
from .speech import speak

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_summary(transcript: str, output_path: Path) -> None:
    trimmed_text = transcript[-MAX_CHARACTERS:] if len(transcript) > MAX_CHARACTERS else transcript

    prompt = f"""
    Aqui está a transcrição de uma reunião:

    {trimmed_text}

    Gere um resumo em português com os principais tópicos discutidos, decisões tomadas e próximos passos.
    """

    try:
      response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": (
              "Você é um assistente especializado em gerar resumos de transcrições de reuniões ou áudios gravados, "
              "respeitando a língua original falada pelos participantes. "
              "Seu resumo deve começar com um título na primeira linha, que capture de forma breve o tema principal da reunião. "
              "Depois, apresente os principais tópicos discutidos, decisões tomadas e próximos passos, de forma clara e organizada, "
              "utilizando marcadores (como hífens ou bullets) se necessário."
              )},
              {"role": "user", "content": prompt}
          ],
          temperature=0.3
      )
      summary = response.choices[0].message.content.strip()

      if not summary:
          print("⚠️ Resumo retornou vazio.")
          speak("Resumo não pôde ser gerado.")
          return

      output_path.write_text(summary, encoding="utf-8")
      print(f"✅ Summary saved at: {output_path}")
      speak("Summary saved.")
      return summary
    except Exception as e:
        print(f"❌ Erro ao gerar resumo: {e}")
        speak("Failed to generate the summary.")
