import uuid
from typing import List, Optional

from sqlalchemy.orm import Session
import models




def AllFieldsAreValid(
    nome: Optional[str] = None,
    cnpj: Optional[str] = None,
    cidade: Optional[str] = None,
    ramo_atuacao: Optional[str] = None,
    telefone: Optional[str] = None,
    email_contato: Optional[str] = None
    ) -> bool:
    validations = []
    
    if nome:
        validations.append(len(nome) < 255 and len(nome) > 0)

    if cnpj:
        validations.append(cnpj.isdigit() and len(cnpj) == 14)

    if cidade:
        validations.append(len(cidade) < 255 and len(cidade) > 0)

    if ramo_atuacao:
        validations.append(len(ramo_atuacao) < 255 and len(ramo_atuacao) > 0)

    if telefone:
        validations.append(telefone.isdigit() and len(telefone) > 0)

    if email_contato:
        validations.append(
            email_contato.count("@") == 1 and
            email_contato.count(".") > 0 and
            email_contato.index("@") < email_contato.index(".") and
            email_contato.index("@") > 0 and
            email_contato.index(".") < len(email_contato) - 1
        )

    return all(validations)
    
    
def CreateEmpresa(nome: str, cnpj: str, cidade: str, ramo_atuacao: str, telefone: str, email_contato: str): 
    if(not AllFieldsAreValid(nome,cnpj,cidade, ramo_atuacao, telefone, email_contato)):
        return 422
    

    empresa_id = str(uuid.uuid4())

    Empresa = models.Empresas(
        id=empresa_id,
        nome=nome,
        cnpj=cnpj,
        cidade=cidade,
        ramo_atuacao=ramo_atuacao,
        telefone=telefone,
        email_contato=email_contato
    )
    
    result = Empresa.save()
    if(not result):
        return 409
    return Empresa

def ListEmpresas(cidade,ramo_atuacao):
    return models.Empresas.ListEmpresas(cidade,ramo_atuacao)

def SearchEmpresaByName(name: str):

    empresa = models.Empresas.SearchEmpresaByName(name)
    return empresa

def SearchEmpresaById(id: str):
    if(len(id) != 36):
        return 422
    empresa = models.Empresas.SearchEmpresaById(id)
    if(empresa == 404):
        return 404
    result = {
                "id": empresa.id,
                "nome": empresa.nome,
                "cnpj": empresa.cnpj,
                "cidade": empresa.cidade,
                "ramo_atuacao": empresa.ramo_atuacao,
                "telefone": empresa.telefone,
                "email_contato": empresa.email_contato,
                "data_de_cadastro": empresa.data_de_cadastro
            }
    return result


def ChangeEmpresa(    id: str,
    nome: Optional[str] = None,
    cidade: Optional[str] = None,
    ramo_atuacao: Optional[str] = None,
    telefone: Optional[str] = None,
    email_contato: Optional[str] = None): 
    
    if(not AllFieldsAreValid(nome=nome,cidade=cidade, ramo_atuacao=ramo_atuacao, telefone=telefone, email_contato=email_contato)):
        return 422 
    
    if(len(id) != 36):
        return 422
    
    empresa_to_be_modified = models.Empresas.SearchEmpresaById(id)
    if(empresa_to_be_modified == 404):
        return 404
    if nome:
        empresa_to_be_modified.nome = nome  # type: ignore
    if cidade:
        empresa_to_be_modified.cidade = cidade  # type: ignore
    if ramo_atuacao:
        empresa_to_be_modified.ramo_atuacao = ramo_atuacao  # type: ignore
    if telefone:
        empresa_to_be_modified.telefone = telefone  # type: ignore
    if email_contato:
        empresa_to_be_modified.email_contato = email_contato  # type: ignore

    empresa_to_be_modified.save()
    
    return {
        "id": empresa_to_be_modified.id,
        "nome": empresa_to_be_modified.nome,
        "cnpj": empresa_to_be_modified.cnpj,
        "cidade": empresa_to_be_modified.cidade,
        "ramo_atuacao": empresa_to_be_modified.ramo_atuacao,
        "telefone": empresa_to_be_modified.telefone,
        "email_contato": empresa_to_be_modified.email_contato,
        "data_de_cadastro": empresa_to_be_modified.data_de_cadastro
    }
    
def DeleteEmpresa(id:str):
    if(len(id) != 36):
        return 422
    
    empresa_to_be_deleted = models.Empresas.deleteEmpresa(id)
    return empresa_to_be_deleted
    
    
    
    