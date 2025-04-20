import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import requests
from bs4 import BeautifulSoup
from typing import Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AWS Documentation MCP Server")

class Query(BaseModel):
    query: str
    service: Optional[str] = None

class Response(BaseModel):
    response: str
    source_url: Optional[str] = None

def search_aws_docs(query: str, service: Optional[str] = None) -> tuple[str, str]:
    """
    AWS公式ドキュメントを検索して関連情報を取得する
    """
    base_url = "https://docs.aws.amazon.com"
    search_url = f"{base_url}/search/doc-search.html#facet_doc_guide=User%20Guides&facet_doc_lang=en_us"
    
    if service:
        search_url += f"&searchPath={service}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, params={"searchQuery": query})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="search-result")
        
        if not results:
            return "申し訳ありませんが、該当する情報が見つかりませんでした。", None
        
        # 最も関連性の高い結果を取得
        top_result = results[0]
        title = top_result.find("h2").text.strip()
        description = top_result.find("div", class_="description").text.strip()
        doc_url = base_url + top_result.find("a")["href"]
        
        # ドキュメントの詳細を取得
        doc_response = await client.get(doc_url)
        doc_soup = BeautifulSoup(doc_response.text, "html.parser")
        content = doc_soup.find("div", id="main-content")
        
        if content:
            relevant_text = f"{title}\n\n{content.get_text()[:1000]}..."
        else:
            relevant_text = f"{title}\n\n{description}"
        
        return relevant_text, doc_url

@app.post("/query", response_model=Response)
async def query_aws_docs(query: Query):
    try:
        response_text, source_url = await search_aws_docs(query.query, query.service)
        return Response(response=response_text, source_url=source_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)