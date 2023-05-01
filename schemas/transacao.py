from pydantic import BaseModel
from model import *

class TransacaoSchema(BaseModel):
    descricao: str 
    valor: float
    tipo: str

class TransacaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

class TransacaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura da busca por uma transacao
    """
    id: str

def apresenta_transacao(transacao: Transacao):
    return { 
        "id": transacao.id,
        "descricao": transacao.descricao,
        "valor": transacao.valor,
        "tipo": transacao.tipo,
        
    }