from flask import Flask, render_template, request, flash, redirect, url_for


app = Flask(__name__)
app.secret_key = 'teste'

# Rota para a página inicial (Home)
@app.route('/')
def home():
    return render_template('home.html')

# Rota para a página "Sobre Nós"
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para a nova página de Manutenção (Hub)
@app.route('/manutencao')
def manutencao():
    return render_template('manutencao.html')

# Rota para a página de "Serviços"
@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

# Rota para a página de "Contato"
@app.route('/contato')
def contato():
    return render_template('contato.html')

#Rota para a página de "Manutenção Preventiva"
@app.route('/manu_preventiva')
def manu_preventiva():
    return render_template('manu_preventiva.html')

#Rota para a página de "Manutenção Corretiva"
@app.route('/manu_corretiva')
def manu_corretiva():
    return render_template('manu_corretiva.html')

#Rota para a página de "Upgrades"
@app.route('/upgrades')
def upgrades():
    return render_template('upgrades.html')

#Rota para a página de "Formatação e Backup"
@app.route('/formata_bkp')
def formata_bkp():
    return render_template('formata_bkp.html')

#Rota para a página de "Consultoria em TI"
@app.route('/consultoria')
def consultoria():
    return render_template('consultoria.html')

#Rota para a página de "Buscamos seu Equipamento"
@app.route('/buscamos_equip')
def buscamos_equip():
    return render_template('buscamos_equip.html')

@app.route('/politica_termos')
def politica_termos():
    return render_template('politica_termos.html')


if __name__ == '__main__':
    app.run(debug=True, host='172.16.0.174') # debug=True reinicia o servidor automaticamente ao salvar mudanças