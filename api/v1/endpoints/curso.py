from typing import List
from  fastapi import APIRouter
from  fastapi import Depends
from  fastapi import status
from  fastapi import HTTPException
from  fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session

router = APIRouter()

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
  novo_curso = CursoModel(titulo=curso.titulo,aulas=curso.aulas,horas=curso.horas)
  db.add(novo_curso)
  await db.commit()
  return novo_curso # Response Model

@router.get('/',response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel)
    result = await session.execute(query)
    cursos: List[CursoModel] = result.scalars().all()
    return cursos
  
@router.get('/{curso_id}',response_model=CursoSchema,status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int , db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == curso_id)
    result = await session.execute(query)
    curso = result.scalar_one_or_none()
    if curso:
      return curso
    raise HTTPException(detail='Curso nao encontrado',status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{curso_id}', response_model=CursoSchema,status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id:int, curso:CursoSchema,db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == curso_id)
    result = await session.execute(query)
    curso_to_update = result.scalar_one_or_none()
    if curso_to_update:
      curso_to_update.titulo = curso.titulo
      curso_to_update.aulas = curso.aulas
      curso_to_update.horas = curso.horas
      await session.commit()
      return curso_to_update
    raise HTTPException(detail='Curso nao encontrado',status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{curso_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id:int,db: AsyncSession = Depends(get_session)):
  async with db as session:
    query = select(CursoModel).filter(CursoModel.id == curso_id)
    result = await session.execute(query)
    curso_to_del = result.scalar_one_or_none()
    if curso_to_del:
      await session.delete(curso_to_del)
      await session.commit()
      return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(detail='Curso nao encontrado',status_code=status.HTTP_404_NOT_FOUND)