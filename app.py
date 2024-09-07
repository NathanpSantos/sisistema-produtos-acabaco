from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import tempfile

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itens.db'
db = SQLAlchemy(app)

# Definição do modelo 'Item'
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    sku = db.Column(db.String(50), nullable=False)
    ean = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    corredor = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tipo_venda = db.Column(db.String(50), nullable=False)
    top_30 = db.Column(db.Boolean(), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        produto = request.form['produto']
        categoria = request.form['categoria']
        sku = request.form['sku']
        ean = request.form['ean']
        quantidade = request.form['quantidade']
        corredor = request.form['corredor']
        descricao = request.form['descricao']
        tipo_venda = request.form['tipo_venda']
        top_30 = request.form.get('top_30') == 'on'
        responsavel = request.form['responsavel']

        # Adicionando novo item ao banco de dados
        novo_item = Item(produto=produto, categoria=categoria, sku=sku, ean=ean, quantidade=quantidade, corredor=corredor, descricao=descricao, tipo_venda=tipo_venda, top_30=top_30, responsavel=responsavel)
        db.session.add(novo_item)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('cadastro.html')

# Rota para ver todos os itens cadastrados
@app.route('/itens')
def ver_itens():
    # Buscar todos os itens no banco de dados
    itens = Item.query.all()
    return render_template('itens.html', itens=itens)

# Exportação para Excel
@app.route('/export')
def export():
    itens = Item.query.all()

    dados = []
    for item in itens:
        dados.append({
            'ID': item.id,
            'Produto': item.produto,
            'Quantidade na Bay': item.quantidade,
            'Corredor': item.corredor,
            'Tipo de Venda': item.tipo_venda,
            'Top 30/OPP': item.top_30,
            'SKU': item.sku,
            'EAN': item.ean,
            'Descrição': item.descricao,
            'Responsável': item.responsavel
        })

    df = pd.DataFrame(dados)
    temp_file, file_path = tempfile.mkstemp(suffix='.xlsx')
    os.close(temp_file)
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True, download_name='controle_itens.xlsx')

# Rota para deletar um item
@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('ver_itens'))

# Rota para editar um item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)

    if request.method == 'POST':
        item.produto = request.form['produto']
        item.categoria = request.form['categoria']
        item.sku = request.form['sku']
        item.ean = request.form['ean']
        item.quantidade = request.form['quantidade']
        item.corredor = request.form['corredor']
        item.descricao = request.form['descricao']
        item.tipo_venda = request.form['tipo_venda']
        item.top_30 = request.form.get('top_30') == 'on'
        item.responsavel = request.form['responsavel']
        
        db.session.commit()
        return redirect(url_for('ver_itens'))

    return render_template('edit.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
