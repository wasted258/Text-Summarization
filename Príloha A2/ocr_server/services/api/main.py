from fastapi import FastAPI
#from prometheusrock import PrometheusMiddleware, metrics_route

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware


from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

import shutil
import gvision
import pdftotext
import extract_data
import uuid
from os import path,remove,environ




API_KEY = environ.get('API_KEY')
API_KEY_NAME = environ.get('API_KEY_NAME')
COOKIE_DOMAIN = environ.get('COOKIE_DOMAIN')

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie)
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None) 

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def homepage():
    return "Welcome to the text extraction server!"


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="PDF text extraction server",version=2.0, routes=app.routes)
    )
    return response


@app.get("/documentation", tags=["documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

#@app.get("/v2/pdf_path/{document_path:path}", response_class=HTMLResponse, tags=["functions"])
#async def get_data_LocalStorage(document_path, api_key: APIKey = Depends(get_api_key)):
#        
#    """
#	Extracting data from documents even if not on shared folder.
#	:param pdf: 
###
#   response = extract_data.main(document_path)
#    return response
@app.post("/v2/pdf_file", response_class=HTMLResponse, tags=["functions"])
async def get_data_FileUpload(api_key: APIKey = Depends(get_api_key), pdf: UploadFile = File(...)):
    """
    Extracting data from documents even if not on shared folder.\n
    :param pdf: send in binnary\n
    :param access_token: str\n
    :return: API Response containing the retrieved text\n

    python example:\n 

    import httpx\n
    files = {'pdf': open(path to file, 'rb')}\n
    headers={'access_token': "secret"}\n 
    url='http://nit-b1822x2/v2/pdf_file'\n
    response = httpx.post(url=url, files=files, headers=headers)\n
    """
    file_name=f'{uuid.uuid4().hex}{path.splitext(pdf.filename)[1]}'
    with open(f'.//temp//{file_name}', 'wb') as buffer:
        shutil.copyfileobj(pdf.file, buffer)
    response = extract_data.main(f'.//temp//{file_name}')
    remove(f'.//temp//{file_name}')
    return response[0].decode('utf-8')

@app.post("/v2/pdf_file_w_vertices", response_class=HTMLResponse, tags=["functions"])
async def get_data_FileUpload_w_vertices(api_key: APIKey = Depends(get_api_key), pdf: UploadFile = File(...)):
    """
    Extracting data from documents even if not on shared folder.\n
    :param pdf: send in binnary\n
    :param access_token: str\n
    :return: API Response containing the retrieved text\n

    python example:\n 

    import httpx\n
    files = {'pdf': open(path to file, 'rb')}\n
    headers={'access_token': "secret"}\n
    url='http://nit-b1822x2/v2/pdf_file'\n
    response = httpx.post(url=url, files=files, headers=headers)\n
    """
    file_name=f'{uuid.uuid4().hex}{path.splitext(pdf.filename)[1]}'
    with open(f'.//temp//{file_name}', 'wb') as buffer:
        shutil.copyfileobj(pdf.file, buffer)
    response = extract_data.main(f'.//temp//{file_name}')
    remove(f'.//temp//{file_name}')
    return response[1]