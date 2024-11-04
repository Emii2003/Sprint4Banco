from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId


client = MongoClient("mongodb://localhost:27017")
db = client["Sprint4"]
collection = db["Sprint4"]


class Endereco(BaseModel):
    cep_endereco: str
    rua_endereco: str
    num_endereco: int
    bairro_endereco: str
    cidade_endereco: str
    estado_endereco: str
    uf_endereco: str
    pais_endereco: str

class Ramo(BaseModel):
    nome_ramo: str
    desc_ramo: str

class Usuario(BaseModel):
    nome_usuario: str
    email_corporativo_usuario: str
    senha_usuario: str

class Empresa(BaseModel):
    nome_empresa: str
    cnpj_empresa: str
    ramo_atuacao_empresa: str

class Colaborador(BaseModel):
    id_usuario: str  
    id_empresa: str  

class FeedbackEmpresa(BaseModel):
    id_usuario: str  
    id_empresa: str  

class Analise(BaseModel):
    resultados_analise: str
    data_analise: str  
    id_feedback_empresa: str  

class UsuarioCompleto(BaseModel):
    USUARIO: Usuario
    ENDERECO_EMPRESA: Endereco
    RAMO_EMPRESA: Ramo
    EMPRESA: Empresa
    COLABORADOR: Colaborador
    FEEDBACK_EMPRESA: FeedbackEmpresa
    ANALISE: Analise

app = FastAPI()

@app.get("/hello")
async def read_hello():
    return {"message": "Hello, World!"}

@app.get("/usuario")
async def read_users():
    try:
        users = []
        for user in collection.find():
            user['_id'] = str(user['_id']) 
            users.append(user)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na aplicação: {str(e)}")

@app.get("/usuario/{id}")
async def read_user_by_id(id: str):
    try:
        user = collection.find_one({"_id": ObjectId(id)})
        if user:
            user['_id'] = str(user['_id'])  
            return user
        else:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na aplicação: {str(e)}")

@app.post("/usuario")
async def register_user(usuario_completo: UsuarioCompleto):
    try:
        
        user_data = {
            "USUARIO": usuario_completo.USUARIO.dict(),
            "ENDERECO_EMPRESA": usuario_completo.ENDERECO_EMPRESA.dict(),
            "RAMO_EMPRESA": usuario_completo.RAMO_EMPRESA.dict(),
            "EMPRESA": usuario_completo.EMPRESA.dict(),
            "COLABORADOR": usuario_completo.COLABORADOR.dict(),
            "FEEDBACK_EMPRESA": usuario_completo.FEEDBACK_EMPRESA.dict(),
            "ANALISE": usuario_completo.ANALISE.dict(),
        }
        
        collection.insert_one(user_data)
        return {"message": "Usuario registrado com sucesso!"}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Usuario já existe")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na aplicação: {str(e)}")

@app.delete("/usuario/{id}")
async def delete_user(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return {"message": "Usuario deletado com sucesso!"}
        else:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na aplicação: {str(e)}")

@app.put("/usuario/{id}")
async def update_user(id: str, usuario_completo: UsuarioCompleto):
    try:
        # Prepare the updated user data
        updated_user_data = {
            "USUARIO": usuario_completo.USUARIO.dict(),
            "ENDERECO_EMPRESA": usuario_completo.ENDERECO_EMPRESA.dict(),
            "RAMO_EMPRESA": usuario_completo.RAMO_EMPRESA.dict(),
            "EMPRESA": usuario_completo.EMPRESA.dict(),
            "COLABORADOR": usuario_completo.COLABORADOR.dict(),
            "FEEDBACK_EMPRESA": usuario_completo.FEEDBACK_EMPRESA.dict(),
            "ANALISE": usuario_completo.ANALISE.dict(),
        }
        
        # Update the user in the collection
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": updated_user_data})
        
        if result.modified_count == 1:
            return {"message": "Usuario atualizado com sucesso!"}
        else:
            raise HTTPException(status_code=404, detail="Usuario não encontrado ou nenhuma alteração foi feita")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na aplicação: {str(e)}")
