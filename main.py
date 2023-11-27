from flask import Flask, jsonify, Response, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:123456@localhost/cadastramento"

# Para criar tabela no postgres faça
# 1) no terminal digite python com a venv ativada
# 2) from main import db, app #digite esse comando e aperte enter
# 3) with app.app_context(): #digite esse comando e aperte enter
#       db.create_all() #aperte tab e digite esse comando e aperte enter

db = SQLAlchemy(app) 


class Professor(db.Model):
    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(50))
    instituicao = db.Column(db.String(100))
    externo = db.Column(db.String(10))

class Aluno(db.Model):
    nome = db.Column(db.String(50))
    matricula = db.Column(db.String(10), primary_key=True)

class Sala(db.Model):
    nomesala = db.Column(db.String(20))
    codigosala = db.Column(db.String(20), primary_key=True)
    local = db.Column(db.String(20))
    inicio = db.Column(db.String(20))
    termino = db.Column(db.String(20))
    reservado =  db.Column(db.String(20))

class Agendamento(db.Model):
    codigoagen = db.Column(db.String(20), primary_key=True)
    codigosala = db.Column(db.String(20))
    matriculaaluno = db.Column(db.String(20))
    cpfprof = db.Column(db.String(11))
    cpf1 = db.Column(db.String(11))
    cpf2 = db.Column(db.String(11))
    cpf3 = db.Column(db.String(11))
    cpf4 =  db.Column(db.String(11))


@app.route("/")
def formulario():
    return render_template("formulario.html")


@app.route("/cadastro", methods=["POST"])
def cadastro():
    tipo = request.form.get("tipo")
    return render_template(f"cadastro_{tipo}.html")

@app.route("/listar_prof", methods=["GET"])
def listar_prof():
    professores = Professor.query.all()
    return render_template("listar_prof.html", professores=professores)

@app.route("/listar_aluno", methods=["GET"])
def listar_aluno():
    alunos = Aluno.query.all()
    return render_template("listar_aluno.html", alunos=alunos)

@app.route("/listar_sala", methods=["GET"])
def listar_sala():
    salas = Sala.query.all()
    return render_template("listar_sala.html", salas=salas)

@app.route("/listar_agendamento", methods=["GET"])
def listar_agendamento():
    agendamentos = Agendamento.query.all()
    return render_template("listar_agendamento.html", agendamentos=agendamentos)

@app.route("/excluir_prof", methods=["POST"])
def excluir_prof():
    cpf = request.form.get("cpf")
    professor_objeto = Professor.query.filter_by(cpf=cpf).first()

    db.session.delete(professor_objeto)
    db.session.commit()

    # Redirecione de volta para a lista de professores após a exclusão
    return redirect("/listar_prof")

@app.route("/excluir_aluno", methods=["POST"])
def excluir_aluno():
    matricula = request.form.get("matricula")
    aluno_objeto = Aluno.query.filter_by(matricula=matricula).first()

    db.session.delete(aluno_objeto)
    db.session.commit()

    # Redirecione de volta para a lista de alunos após a exclusão
    return redirect("/listar_aluno")

@app.route("/excluir_sala", methods=["POST"])
def excluir_sala():
    codigosala = request.form.get("codigosala")
    sala_objeto = Sala.query.filter_by(codigosala=codigosala).first()

    db.session.delete(sala_objeto)
    db.session.commit()

    return redirect("/listar_sala")

@app.route("/excluir_agendamento", methods=["POST"])
def excluir_agendamento():
    codigoagen = request.form.get("codigoagen")
    agendamento_objeto = Agendamento.query.filter_by(codigoagen=codigoagen).first()

    db.session.delete(agendamento_objeto)
    db.session.commit()

    return redirect("/listar_agendamento")

@app.route("/cadastro_prof", methods=["POST"])
def cadastro_prof():
    cpf = request.form.get("cpf")
    nome = request.form.get("nome")
    instituicao = request.form.get("instituicao")
    externo = request.form.get("externo")

    professor = Professor(cpf=cpf, nome=nome, instituicao=instituicao, externo=externo)
    db.session.add(professor)
    db.session.commit()

    return render_template("resultado_prof.html", cpf=cpf, nome=nome, instituicao=instituicao, externo=externo)

@app.route("/cadastro_aluno", methods=["POST"])
def cadastro_aluno():
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")

    aluno = Aluno(nome=nome, matricula=matricula)
    db.session.add(aluno)
    db.session.commit()

    return render_template("resultado_aluno.html", nome=nome, matricula=matricula)

@app.route("/cadastro_sala", methods=["POST"])
def cadastro_sala():
    nomesala = request.form.get("nomesala")
    codigosala = request.form.get("codigosala")
    local = request.form.get("local")
    inicio = request.form.get("inicio")
    termino = request.form.get("termino")
    reservado = request.form.get("reservado")

    sala = Sala(nomesala=nomesala, codigosala=codigosala, local=local, inicio=inicio, termino=termino, reservado=reservado)

    db.session.add(sala)
    db.session.commit()

    return render_template( "resultado_sala.html", nomesala=nomesala, codigosala=codigosala, local=local, inicio=inicio, termino=termino, reservado=reservado)


@app.route("/cadastro_agendamento", methods=["POST"])
def cadastro_defesa():
    codigoagen = request.form.get("codigoagen")
    codigosala = request.form.get("codigosala")
    matriculaaluno = request.form.get("matriculaaluno")
    cpfprof = request.form.get("cpfprof")
    cpf1 = request.form.get("cpf1")
    cpf2 = request.form.get("cpf2")
    cpf3 = request.form.get("cpf3")
    cpf4 = request.form.get("cpf4")

    agendamento = Agendamento(codigoagen=codigoagen, codigosala=codigosala, matriculaaluno=matriculaaluno, cpfprof=cpfprof, cpf1=cpf1, cpf2=cpf2, cpf3=cpf3, cpf4=cpf4)

    db.session.add(agendamento)
    db.session.commit()

    return render_template("resultado_agendamento.html", codigoagen=codigoagen, codigosala=codigosala, matriculaaluno=matriculaaluno, cpfprof=cpfprof, cpf1=cpf1, cpf2=cpf2, cpf3=cpf3, cpf4=cpf4)


@app.route("/atualizar_prof", methods=["GET", "POST"])
def atualizar_prof():

    if request.method == "GET":
        cpf = request.args.get("cpf")
        professor_objeto = Professor.query.filter_by(cpf=cpf).first()

        nome = professor_objeto.nome
        instituicao = professor_objeto.instituicao
        externo = professor_objeto.externo
        
        return render_template("atualizar_prof.html", cpf=cpf, nome=nome, instituicao=instituicao, externo=externo)   

    if request.method == "POST":
        old_cpf = request.form.get("old_cpf")
        new_cpf = request.form.get("new_cpf")
        nome = request.form.get("nome")
        instituicao = request.form.get("instituicao")
        externo = request.form.get("externo")
        professor_objeto = Professor.query.filter_by(cpf=old_cpf).first()

        professor_objeto.nome = nome
        professor_objeto.instituicao = instituicao
        professor_objeto.externo = externo
        professor_objeto.cpf = new_cpf

        db.session.add(professor_objeto)
        db.session.commit()
        professores = Professor.query.all()

        return render_template("listar_prof.html", professores=professores)
        
    
@app.route("/atualizar_aluno", methods=["GET", "POST"])
def atualizar_aluno():

    if request.method == "GET":
        matricula = request.args.get("matricula")
        aluno_objeto = Aluno.query.filter_by(matricula=matricula).first()

        nome = aluno_objeto.nome
        matricula = aluno_objeto.matricula
        
        return render_template("atualizar_aluno.html", nome=nome, matricula=matricula) 
    
    if request.method == "POST":
        old_matricula = request.form.get("old_matricula")
        new_matricula = request.form.get("new_matricula")
        print(old_matricula, new_matricula)
        nome = request.form.get("nome")

        aluno_objeto = Aluno.query.filter_by(matricula=old_matricula).first()

        aluno_objeto.nome = nome
        aluno_objeto.matricula = new_matricula
        
        db.session.add(aluno_objeto)
        db.session.commit()
        alunos = Aluno.query.all()

        return render_template("listar_aluno.html", alunos=alunos)

@app.route("/atualizar_sala", methods=["GET", "POST"])
def atualizar_sala():

    if request.method == "GET":
        codigosala = request.args.get("codigosala")
        sala_objeto = Sala.query.filter_by(codigosala=codigosala).first()

        nomesala = sala_objeto.nomesala
        codigosala = sala_objeto.codigosala
        local = sala_objeto.local
        inicio = sala_objeto.inicio
        termino = sala_objeto.termino
        reservado = sala_objeto.reservado

        return render_template("atualizar_sala.html", nomesala=nomesala, codigosala=codigosala, local=local, inicio=inicio, termino=termino, reservado=reservado)
    
    if request.method == "POST":
        old_codigosala = request.form.get("old_codigosala")
        new_codigosala = request.form.get("new_codigosala")
        nomesala = request.form.get("nomesala")
        local = request.form.get("local")
        inicio = request.form.get("inicio")
        termino = request.form.get("termino")
        reservado = request.form.get("reservado")
        sala_objeto = Sala.query.filter_by(codigosala=old_codigosala).first()

        sala_objeto.nomesala = nomesala
        sala_objeto.codigosala = new_codigosala
        sala_objeto.local = local
        sala_objeto.inicio = inicio
        sala_objeto.termino = termino
        sala_objeto.reservado = reservado

        db.session.add(sala_objeto)
        db.session.commit()
        salas = Sala.query.all()

        return render_template("listar_sala.html", salas=salas)


@app.route("/atualizar_agendamento", methods=["GET", "POST"])
def atualizar_agendamento():

    if request.method == "GET":
        codigoagen = request.args.get("codigoagen")
        agendamento_objeto = Agendamento.query.filter_by(codigoagen=codigoagen).first()

        codigoagen = agendamento_objeto.codigoagen
        codigosala = agendamento_objeto.codigosala
        matriculaaluno = agendamento_objeto.matriculaaluno
        cpfprof = agendamento_objeto.cpfprof
        cpf1 = agendamento_objeto.cpf1
        cpf2 = agendamento_objeto.cpf2
        cpf3 = agendamento_objeto.cpf3
        cpf4 =  agendamento_objeto.cpf4

        return render_template("atualizar_agendamento.html", codigoagen=codigoagen, codigosala=codigosala, matriculaaluno=matriculaaluno, cpfprof=cpfprof, cpf1=cpf1, cpf2=cpf2, cpf3=cpf3, cpf4=cpf4)    
    
    if request.method == "POST":
        old_codigoagen = request.form.get("old_codigoagen")
        new_codigoagen = request.form.get("new_codigoagen")
        codigosala = request.form.get("codigosala")
        matriculaaluno = request.form.get("matriculaaluno")
        cpfprof = request.form.get("cpfprof")
        cpf1 = request.form.get("cpf1")
        cpf2 = request.form.get("cpf2")
        cpf3 = request.form.get("cpf3")
        cpf4 = request.form.get("cpf4")
        agendamento_objeto = Agendamento.query.filter_by(codigoagen=old_codigoagen).first()

        agendamento_objeto.codigosala = codigosala
        agendamento_objeto.codigoagen = new_codigoagen
        agendamento_objeto.matriculaaluno = matriculaaluno
        agendamento_objeto.cpfprof = cpfprof
        agendamento_objeto.cpf1 = cpf1
        agendamento_objeto.cpf2 = cpf2
        agendamento_objeto.cpf3 = cpf3
        agendamento_objeto.cpf4 = cpf4
        
        db.session.add(agendamento_objeto)
        db.session.commit()
        agendamentos = Agendamento.query.all()

        return render_template("listar_agendamento.html", agendamentos=agendamentos)



