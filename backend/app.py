from dataclasses import field
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/cabeleleilaleila"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/')
def projectOn():
    return 'Projeto backend Cabeleleila Leila iniciado.'

## SERVICO ##
class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True)
    descricao_servico = db.Column(db.String(100))

    def __init__(self, descricao_servico):
        self.descricao_servico = descricao_servico

class serviceSchema(ma.Schema):
    class Meta:
        fields = ('id_servico', 'descricao_servico')

servicoSchema = serviceSchema()
servicosSchema = serviceSchema(many=True)


@app.route('/getServico', methods = ['GET'])
def getServico():
    allServicos = Servico.query.all()
    results = servicosSchema.dump(allServicos)
    return jsonify(results)

@app.route('/getServico/<id>/', methods = ['GET'])
def getServicoId(id):
    servico = Servico.query.get(id)
    return servicoSchema.jsonify(servico)

## CLIENTE ##
class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(200))
    cpf_cliente = db.Column(db.String(11))

    def __init__(self, nome_cliente, cpf_cliente):
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente

class clientSchema(ma.Schema):
    class Meta:
        fields = ('nome_cliente', 'cpf_cliente', 'id_cliente')

clienteSchema = clientSchema()
clientesSchema = clientSchema(many=True)

@app.route('/getCliente', methods = ['GET'])
def getCliente():
    allClientes = Cliente.query.all()
    results = clientesSchema.dump(allClientes)
    return jsonify(results)

@app.route('/getClientes/<id>/', methods = ['GET'])
def getClientsId(id):
    cliente = Cliente.query.get(id)
    return clienteSchema.jsonify(cliente)

@app.route('/addCliente', methods = ['POST'])
def addCliente():
    nome_cliente = request.json['nome_cliente']
    cpf_cliente = request.json['cpf_cliente']

    cliente = Cliente(nome_cliente, cpf_cliente)
    db.session.add(cliente)
    db.session.commit()
    
    return clienteSchema.jsonify(cliente)

@app.route('/updateCliente/<id>/', methods = ['PUT'])
def updateCliente(id):
    cliente = Cliente.query.get(id)
    nome_cliente = request.json['nome_cliente']

    cliente.nome_cliente = nome_cliente
    
    db.session.commit()
    return clienteSchema.jsonify(cliente)

@app.route('/deleteCliente/<id>/', methods = ['DELETE'])
def deleteCliente(id):
    cliente = Cliente.query.get(id)

    db.session.delete(cliente)
    db.session.commit()
    return clienteSchema.jsonify(cliente)

@app.route('/getClienteCPF/<cpf>/', methods = ['GET'])
def getClienteCPF(cpf):
    cliente = Cliente.query.get(cpf)
    return clienteSchema.jsonify(cliente)

## AGENDAMENTO ##
class Agendamento(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True)
    data_hora_agendamento = db.Column(db.DateTime)
    id_cliente = db.Column(db.Integer)
    id_servico = db.Column(db.Integer)

    def __init__(self, data_hora_agendamento, id_cliente, id_servico):
        self.data_hora_agendamento = data_hora_agendamento
        self.id_cliente = id_cliente
        self.id_servico = id_servico

class agendaSchema(ma.Schema):
    class Meta:
        fields = ('id_agendamento', 'data_hora_agendamento', 'id_cliente', 'id_servico')

agendamentoSchema = agendaSchema()
agendamentosSchema = agendaSchema(many=True)

@app.route('/getAgendamento', methods = ['GET'])
def getAgendamento():
    allAgendamentos = Agendamento.query.all()
    results = agendamentosSchema.dump(allAgendamentos)
    return jsonify(results)

@app.route('/getAgendamentoId/<id>/', methods = ['GET'])
def getAgendamentoId(id):
    agendamento = Agendamento.query.get(id)
    return agendamentoSchema.jsonify(agendamento)

@app.route('/addAgendamento', methods = ['POST'])
def addAgendamento():
    id_servico = request.json['id_servico']
    id_cliente = request.json['id_cliente']
    data_hora_agendamento = request.json['data_hora_agendamento']

    agendamento = Agendamento(data_hora_agendamento, id_cliente, id_servico)
    db.session.add(agendamento)
    db.session.commit()
    
    return agendamentoSchema.jsonify(agendamento)

@app.route('/updateAgendamento/<id>/', methods = ['PUT'])
def updateAgendamento(id):
    agendamento = Agendamento.query.get(id)
    data_hora_agendamento = request.json['data_hora_agendamento']
    id_servico = request.json['id_servico']

    agendamento.data_hora_agendamento = data_hora_agendamento
    agendamento.id_servico = id_servico
    
    db.session.commit()
    return agendamentoSchema.jsonify(agendamento)

@app.route('/deleteAgendamento/<id>/', methods = ['DELETE'])
def deleteAgendamento(id):
    agendamento = Agendamento.query.get(id)

    db.session.delete(agendamento)
    db.session.commit()
    return agendamentoSchema.jsonify(agendamento)