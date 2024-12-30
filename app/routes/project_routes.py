from typing import List
from fastapi import APIRouter, Depends, HTTPException, status,Request,FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from model.project_model import Project
from model.user_model import User
from schemas.project_schema import ProjectCreate,ProjectUpdatePatch
from jwt_auth.token_validation import JWTBearer
from fastapi.exceptions import RequestValidationError

router = APIRouter()
app = FastAPI()

def get_user_from_token(token_payload: dict):
    user_id = token_payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID not found in token")
    user = User.objects.filter(id=user_id).first()  # type: ignore
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def check_user_admin_role(user):
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have permission to manage projects")

def get_project_by_id(id: str):
    project = Project.objects.filter(id=id).first()  # type: ignore
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

def create_new_project(title: str, description: str, created_by: str):
    new_project = Project(name=title, description=description, created_by=created_by)
    new_project.save()
    return new_project

@router.post('/createproject', tags=['projects'])
def create_projects(project: ProjectCreate, token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        check_user_admin_role(user)

        new_project = create_new_project(project.title, project.description, user.username)

        return JSONResponse(
            content={"message": "project created successfully",
                     "project_id": str(new_project.id)}, # type: ignore
            status_code=201
            )

    except ValidationError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Validation error: {str(ve)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

@router.put('/updateproject/{id}', tags=['projects'])
def update_project_put(id: str,project: ProjectCreate,token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        check_user_admin_role(user)

        project_to_update = get_project_by_id(id)

        project_to_update.name = project.title
        project_to_update.description = project.description
        project_to_update.save()
        return JSONResponse(
            content={"message": "Project updated using PUT successfully",
                     "project_id": str(project_to_update.id)},
            status_code=200
            )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

@router.patch('/updateproject/{id}', tags=['projects'])
def update_project_patch(id: str,project: ProjectUpdatePatch,token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        check_user_admin_role(user)

        project_to_update = get_project_by_id(id)

        if project.title:
            project_to_update.name = project.title
        if project.description:
            project_to_update.description = project.description
        
        project_to_update.save()

        return JSONResponse(
            content={"message": "Project updated using PATCH successfully",
                     "project_id": str(project_to_update.id)},
            status_code=200
            )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)) 
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

@router.delete('/delete/{id}', tags=['projects'])
def delete_project( id: str,token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        check_user_admin_role(user)

        project_to_delete = get_project_by_id(id)

        project_to_delete.delete()
        return JSONResponse(
            content={"message": "Project deleted successfully",
                     "project_id": str(project_to_delete.id)},
            status_code=201
            )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve))
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")

@router.get('/getprojects' ,response_model=List[str], tags=['projects'])
def get_projects(token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        if user.role == 'user':
            projects = Project.objects.all()  # type: ignore
            if not projects:
                return JSONResponse(
                content={"message": "No Project Found"},
                status_code=200
                )
            return JSONResponse(
                content={"message": "Project Details Fetched Successfully",
                        "projects": [project.to_json() for project in projects]},
                status_code=200
                )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Admin does not have permission to view projects')
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


