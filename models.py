import uuid
from sqlalchemy import create_engine, Column, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import datetime
from sqlalchemy.exc import IntegrityError
import config
engine = create_engine("postgresql+psycopg2://"+config.DB_USER+ ":" + config.DB_PASSWORD + "@localhost:5432/ecompjr")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Empresas(Base):


    __tablename__ = 'Empresas' 
    id = Column(String(36), primary_key=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    cidade = Column(String(100), nullable=False)
    ramo_atuacao = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email_contato = Column(String(255), unique=True, nullable=False)
    data_de_cadastro = Column(DateTime, default=datetime.datetime.now, nullable=False)
    
    def save(self):
        with SessionLocal() as session:
            try:
                session.add(self)
                session.commit()
                session.refresh(self)
                return self
            except IntegrityError:
                return None
    @staticmethod
    def ListEmpresas( cidadef = None, ramo_atuacaof = None):
        with SessionLocal() as session:

            empresas = session.query(Empresas)
               
            if(cidadef) :
                empresas =  session.query(Empresas).filter(Empresas.cidade.contains(cidadef))
                

            if(ramo_atuacaof):
                empresas = session.query(Empresas).filter(Empresas.ramo_atuacao.contains(ramo_atuacaof))
                
            empresas = empresas.all()
            
            
            result = []
            if(not cidadef and not ramo_atuacaof): 
                if(len(empresas) > 0):
                    for empresa in empresas:
                        result.append({
                            "id": empresa.id,
                            "nome": empresa.nome,
                            "cnpj": empresa.cnpj,
                            "cidade": empresa.cidade,
                            "ramo_atuacao": empresa.ramo_atuacao,
                            "telefone": empresa.telefone,
                            "email_contato": empresa.email_contato,
                            "data_de_cadastro": empresa.data_de_cadastro
                        })
                    return result
                else:
                    return 404
            else:
                if(len(empresas)>0):
                    for empresa in empresas:
                        result.append({
                            "id": empresa.id,
                            "nome": empresa.nome,
                            "cnpj": empresa.cnpj,
                            "cidade": empresa.cidade,
                            "ramo_atuacao": empresa.ramo_atuacao,
                            "telefone": empresa.telefone,
                            "email_contato": empresa.email_contato,
                            "data_de_cadastro": empresa.data_de_cadastro
                        })
                    return result
                else:
                    return 404

    @staticmethod
    def SearchEmpresaById(EmpresaId: str):
        with SessionLocal() as session:
            empresa = session.query(Empresas).filter_by(id=EmpresaId).first()
            if(not empresa):
                return 404
            return empresa

            
    @staticmethod
    def SearchEmpresaByName(EmpresaName: str):
        with SessionLocal() as session:
            empresas = session.query(Empresas).filter(Empresas.nome.contains(EmpresaName)).all()
            result = []
            if(len(empresas) > 0):
                    for empresa in empresas:
                        result.append({
                            "id": empresa.id,
                            "nome": empresa.nome,
                            "cnpj": empresa.cnpj,
                            "cidade": empresa.cidade,
                            "ramo_atuacao": empresa.ramo_atuacao,
                            "telefone": empresa.telefone,
                            "email_contato": empresa.email_contato,
                            "data_de_cadastro": empresa.data_de_cadastro
                        })
                    return result
            else:
                return 404

        
        
    @staticmethod
    def deleteEmpresa(EmpresaId: str):
        with SessionLocal() as session:
            empresa = session.query(Empresas).filter_by(id=EmpresaId).first()
            if(empresa):
                session.delete(empresa)
                session.commit()
                return 200
            else:
                return 404
    
def CriarTabela():
    Base.metadata.create_all(bind=engine)
    print("tabela provavelmente criada")
    
