from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from flask_cors import CORS
from urllib.parse import unquote
from sqlalchemy.orm.session import close_all_sessions

from sqlalchemy.exc import IntegrityError

from model import *
from schemas import *

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
transacao_tag = Tag(name="Transacao", description="Rotas relacionadas a tabela de transacao")


@app.get('/', tags=[home_tag])
def home():
    """Move para /openapi, para escolher a documentação.
    """
    return redirect('/openapi')



@app.get('/transacao', tags=[transacao_tag])
def getTransacao():
    """Recebe todas as transações
    """
    session = Session()
    transacao = session.query(Transacao).all()

    return jsonify({'transacao': [apresenta_transacao(umaTransacao) for umaTransacao in transacao]})

@app.post('/transacao', tags=[transacao_tag], responses={
    "400": ErrorSchema
})
def postTransacao(form: TransacaoSchema):
    """Cria uma nova transação
    """
    transacao = Transacao(
        descricao=form.descricao,
        valor=form.valor,
        tipo=form.tipo
    )
    try:
        session = Session()
        session.add(transacao)
        session.commit()

        return apresenta_transacao(transacao), 201

    except IntegrityError as e:
        session.rollback()
        err = e.args
        return {"mesage": err}, 400
    
@app.delete('/transacao', tags=[transacao_tag],
            responses={"200": TransacaoDelSchema, "404": ErrorSchema})
def del_tarefa(query: TransacaoBuscaSchema):
    """Deleta uma transação.
    """
    tarefa_id = unquote(unquote(query.id))
    session = Session()
    count = session.query(Transacao).filter(Transacao.id == tarefa_id).delete()
    session.commit()
    close_all_sessions()
    if count:
        return {"mesage": "Transação removida", "id": tarefa_id}
    else:
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404
