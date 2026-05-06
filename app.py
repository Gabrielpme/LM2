from flask import Flask, render_template, request, jsonify
import urllib.request
import json

app = Flask(__name__)
app.secret_key = 'teste'

GROQ_API_KEY = "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"  # Cole sua chave do Groq aqui

SYSTEM_PROMPT = """Você é a Ellem, a assistente virtual da LM Informática, uma assistência técnica de computadores localizada em Diamantina/MG.
 
Seu único objetivo é coletar as informações necessárias, fazer uma triagem para saber qual serviço a pessoa esta precisando, e depois passar
essas informações para o tecnico responsavel.
 
Siga SEMPRE este fluxo em ordem:
1. Cumprimente o cliente e pergunte o NOME dele.
2. Pergunte qual é o PROBLEMA ou SERVIÇO desejado (ex: manutenção, formatação, upgrade, suporte remoto).
3. Pergunte o TELEFONE para contato.
4. Confirme os dados coletados em um resumo e informe que a equipe entrará em contato em breve.
 
Regras importantes:
- Seja sempre simpático, objetivo e profissional.
- Fale apenas em português brasileiro.
- NÃO responda perguntas fora do contexto de agendamento. Se perguntarem algo fora do escopo, diga educadamente que você é um assistente virtual e redirecione para o fluxo.
- Não invente preços ou prazos. Se perguntarem, diga que a equipe informará após análise.
- Não invente valores de orçamentos, qualquer insistencia você fala que ira transferir a conversas para um tecnico.
- Após confirmar o tipo de serviço, encerre a conversa de forma cordial e sugira que o cliente também pode ligar: (38) 99115-5388."""
 
@app.route('/chat', methods=['POST'])
def chat():
    try:
        body = request.get_json()
        messages = body.get('messages', [])
 
        # Groq usa o mesmo formato da OpenAI
        groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in messages:
            groq_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
 
        payload = json.dumps({
            "model": "llama-3.1-8b-instant",
            "messages": groq_messages,
            "max_tokens": 500,
            "temperature": 0.7
        }).encode('utf-8')
 
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'LM-Informatica-Chat/1.0',
                'Authorization': f'Bearer {GROQ_API_KEY}'
            },
            method='POST'
        )
 
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            reply = data['choices'][0]['message']['content']
            return jsonify({'reply': reply})
 
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"Erro HTTP {e.code} na API Groq: {error_body}")
        return jsonify({'error': f"Erro {e.code}: {error_body}"}), 500
    except Exception as e:
        print(f"Erro na rota /chat: {e}")
        return jsonify({'error': str(e)}), 500

# Rotas do site
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/manutencao')
def manutencao():
    return render_template('manutencao.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True, host='172.16.0.174')
