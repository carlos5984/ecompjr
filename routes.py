from typing import List, Union, Optional
from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import datetime
import EmpresaController

app = FastAPI()

class EmpresaBase(BaseModel):
    nome: str 
    cidade: str 
    ramo_atuacao: str 
    telefone: str
    email_contato: EmailStr

class EmpresaCreate(EmpresaBase):
    cnpj: str 

class EmpresaResponse(EmpresaBase):
    id: str
    cnpj: str
    data_de_cadastro: datetime.datetime
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str



class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    ramo_atuacao: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[EmailStr] = None

router = APIRouter(
    prefix="/empresas",  
)

@router.post(
    "/", 
    response_model=EmpresaResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_empresa(empresa: EmpresaCreate):
    new_empresa = EmpresaController.CreateEmpresa(
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        cidade=empresa.cidade,
        ramo_atuacao=empresa.ramo_atuacao,
        telefone=empresa.telefone,
        email_contato=empresa.email_contato
    )
    if new_empresa == 422:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dados inválidos fornecidos. Verifique as restrições dos campos."
        )
    if new_empresa == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Alguns dos dados fornecidos entram em conflito com dados já existentes."
        )
    return new_empresa

@router.get(
    "/", 
    response_model=Union[List[EmpresaResponse], MessageResponse],
)
def list_empresas(cidade=None, ramo_atuacao=None):
    empresas = EmpresaController.ListEmpresas(cidade, ramo_atuacao)
    if(empresas == 404):
        raise HTTPException(
            status_code=404,
            detail="Nenhuma empresa encontrada."
        )
    return empresas

@router.get(
    "/{empresa_id}", 
    response_model=EmpresaResponse,
)
def get_empresa_by_id(empresa_id: str):
    empresa = EmpresaController.SearchEmpresaById(empresa_id)
    if empresa == 422:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de ID inválido. Deve ser uma string UUID válida de 36 caracteres."
        )
    if empresa==404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa com o id '{empresa_id}' não foi encontrada."
        )
    return empresa


@router.get(
    "/search/{empresa_name}", 
    response_model=Union[List[EmpresaResponse], MessageResponse],
)
def get_empresa_by_name(empresa_name: str):
    empresa = EmpresaController.SearchEmpresaByName(empresa_name)

    if(empresa==404):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma empresa com o nome '{empresa_name}' foi encontrada."
        )
    return empresa


@router.put(
    "/{empresa_id}", 
    response_model=EmpresaResponse,
)
def update_empresa(empresa_id: str, empresa_data: EmpresaUpdate):
    updated_empresa = EmpresaController.ChangeEmpresa(
        id=empresa_id,
        **empresa_data.model_dump() 
    )
    if updated_empresa == 422:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dados inválidos ou formato de ID incorreto."
        )
    if updated_empresa ==404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nao foi encontrada nenhuma empresa com o id '{empresa_id}'."
        )
    return updated_empresa

@router.delete(
    "/{empresa_id}"
)
def delete_empresa(empresa_id: str):
    result = EmpresaController.DeleteEmpresa(empresa_id)
    if result == 422:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de ID inválido."
        )
    if result == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa com o id '{empresa_id}' não foi encontrada."
        )
        
    if result == 200:
        return {"message": "empresa deletada com sucesso"}
    return result


app.include_router(router)

@app.get("/")
def read_root():
        return  {
        "ola" : "rotas abaixo pra facilitar o uso",
        "rotas": {
        "GET /": "mensagem inicial ou doc da api",
        "POST /empresas/": "cria uma nova empresa",
        "GET /empresas/": "lista todas as empresas (pode filtrar por cidade e ramo_atuacao)",
        "GET /empresas/{{empresa_id}}": "busca empresa pelo id",
        "GET /empresas/search/{{empresa_name}}": "busca empresa pelo nome",
        "PUT /empresas/{{empresa_id}}": "atualiza os dados de uma empresa",
        "DELETE /empresas/{{empresa_id}}": "deleta uma empresa pelo id"
        },
        "possiveis_erros": {
        "404": "empresa nao encontrada",
        "409": "conflito de dados (cnpj ou algum outro dado ja cadastrado)",
        "422": "dados invalidos ou id invalido"
        }
}

