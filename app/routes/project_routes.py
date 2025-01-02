from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status,Request,FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from model.project_model import Project
from model.user_model import User
from schemas.project_schema import ProjectCreate,ProjectUpdatePatch
from jwt_auth.token_validation import JWTBearer
from fastapi.exceptions import RequestValidationError
from exceptions.project_exception import *
from schemas.project_schema_response_model import *
router = APIRouter()
app = FastAPI()

def get_user_from_token(token_payload: dict):
    user_id = token_payload.get("user_id")
    if not user_id:
        raise UserNotFoundException()
    user = User.objects.filter(id=user_id).first()  # type: ignore
    if not user:
        raise UserNotFound()
    return user

def check_user_admin_role(user):
    if user.role != 'admin':
        raise UnauthorizedActionException()

def get_project_by_id(id: str):
    project = Project.objects.filter(id=id).first()  # type: ignore
    if not project:
        raise ProjectNotFound()
    return project

def create_new_project(title: str, description: str, created_by: str):
    new_project = Project(name=title, description=description, created_by=created_by)
    new_project.save()
    return new_project

@router.post('/createproject', response_model=SuccessResponse, responses={400: {"model": ErrorResponse}},tags=['projects'])
def create_projects(project: ProjectCreate, token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        if user.role != 'admin':
            raise UnauthorizedActionException()
        existing_project = Project.objects(name=project.title).first()  # type: ignore
        if existing_project:
            raise ProjectAlreadyExistsException()
        new_project = create_new_project(project.title, project.description, user.username)
        return SuccessResponse(
            message="Project created successfully",
            data={"project_id": str(new_project.id)} # type: ignore
        )
    except ProjectAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except UnauthorizedActionException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValidationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))

@router.put('/updateproject/{id}', response_model=SuccessResponse, responses={400: {"model": ErrorResponse}},tags=['projects'])
def update_project_put(id: str,project: ProjectCreate,token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        check_user_admin_role(user)

        project_to_update = get_project_by_id(id)

        project_to_update.name = project.title
        project_to_update.description = project.description
        project_to_update.save()
        return SuccessResponse(
            message="Project updated using PUT successfully",
            data={"project_id": str(project_to_update.id)}
        )
    except ProjectAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except UnauthorizedActionException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValidationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))

@router.patch('/updateproject/{id}',response_model=SuccessResponse, responses={400: {"model": ErrorResponse}}, tags=['projects'])
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

        return SuccessResponse(
            message="Project updated using PATCH successfully",
            data={"project_id": str(project_to_update.id)}
        )
    except ProjectAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except UnauthorizedActionException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except ValidationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))

@router.delete('/delete/{id}', response_model=SuccessResponse, responses={400: {"model": ErrorResponse}}, tags=['projects'])
def delete_project( id: str,token_payload: dict = Depends(JWTBearer())):
    try:
        user = get_user_from_token(token_payload)
        check_user_admin_role(user)

        project_to_delete = get_project_by_id(id)

        project_to_delete.delete()
        return SuccessResponse(
            message="Project deleted successfully",
            data={"project_id": str(project_to_delete.id)}
        )
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))

@router.get('/getprojects', response_model=GetProjectsResponse, responses={
    400: {"model": ErrorResponse},
    403: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
}, tags=['projects'])
def get_projects(token_payload: dict = Depends(JWTBearer()),
                 page:int =Query(1,ge=1,description="page number"),
                 page_size:int=Query(2,ge=1,le=100,description="Number of items per page (Default is 2)")) -> GetProjectsResponse:
    try:
        user = get_user_from_token(token_payload)
        
        if user.role != 'user':
            raise ProjectAccessForbiddenException()
        
        offset=(page-1)*page_size
        limit=page_size

        projects = Project.objects.all()  # type: ignore
        projects=Project.objects.skip(offset).limit(limit) #type: ignore
        total_project=Project.objects.count() # type: ignore
        if not projects:
            raise ProjectNotFound()

        project_list = [
            {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "created_by": project.created_by,
                "created_at": project.created_at
            }
            for project in projects
        ]

        return GetProjectsResponse(
            message="Project Details Fetched Successfully",
            projects=project_list,  # type: ignore
            total_project=total_project,  # Optional: Include total for client reference # type: ignore
            page=page,# type: ignore
            page_size=page_size# type: ignore
        )

    except ProjectAccessForbiddenException:
        raise HTTPException(status_code=403, detail="Access forbidden: insufficient permissions.")
    except ProjectNotFound:
        raise HTTPException(status_code=404, detail="No projects found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
