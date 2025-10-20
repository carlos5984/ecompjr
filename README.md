# ecompjr
fiz a maior parte de uma so vez por isso infelizmente esta sem historico




Este projeto é uma API desenvolvida em **FastAPI** para gerenciar as empresas da ecompjr.  
Permite cadastrar, listar, buscar, atualizar e remover empresas de forma simples e organizada.

---

Rotas principais

#### **GET /**
Retorna uma documentacao simples das rotas da API
---

#### **POST /empresas/**
Cria uma nova empresa.  
**Corpo (JSON):**
```json
{
  "nome": "Minha Empresa",
  "cnpj": "12345678000100",
  "cidade": "Feira de Santana",
  "ramo_atuacao": "Tecnologia",
  "telefone": "75999999999", #apenas numeros
  "email_contato": "empresa@email.com"
}
```
**Retorno (201):** objeto da empresa criada.  
**Erros possíveis:**
- 422 -> dados inválidos
- 409 -> conflito com empresa já existente  

---

#### **GET /empresas/**
Lista as empresas cadastradas.  
Pode receber filtros opcionais:
```
/empresas/?cidade=Feira+de+Santana
/empresas/?ramo_atuacao=Tecnologia
ou os dois
/empresas/?cidade=Feira+de+Santan&?ramo_atuacao=Tecnologia
```
**Retorno (200):** lista de empresas.  
**Erro:** 404 → nenhuma empresa encontrada.  

---

#### **GET /empresas/{empresa_id}**
Busca uma empresa pelo seu **ID**.  
**Retorno (200):** dados da empresa.  
**Erros possíveis:**
- 404 -> empresa não encontrada  
- 422 -> formato de ID inválido  

---

#### **GET /empresas/search/{empresa_name}**
Busca empresas cujo nome contenha o termo informado.  
**Retorno (200):** lista de empresas.  
**Erro:** 404 → nenhuma empresa encontrada.  

---

#### **PUT /empresas/{empresa_id}**
Atualiza os dados de uma empresa existente.  
**Corpo (JSON):** mesmo formato da criação (sem o campo `cnpj`).  
**Retorno (200):** empresa atualizada.  
**Erros possíveis:**
- 404 -> empresa não encontrada  
- 422 -> dados ou ID inválidos  

---

#### **DELETE /empresas/{empresa_id}**
Remove uma empresa pelo ID.  
**Retorno (200):**
```json
{"message": "Empresa deletada com sucesso."}
```
**Erros possíveis:**
- 404 -> empresa não encontrada  
- 422 -> formato de ID inválido  

