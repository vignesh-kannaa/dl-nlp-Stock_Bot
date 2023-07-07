from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/")
async def fulfilmentRequest(request: Request):
    print('inside the main method')
    payload = await request.json()
    print('payload: ', payload)
    intent = payload['queryResult']['intent']['displayName']
    paramerters = payload['queryResult']['paramerters']
    output_contexts = payload['queryResult']['outputContexts']

    if intent == 'current.price':
        return JSONResponse(content={"fulfillmentText": "Received price in backend"})

    return ''


# uvicorn main:app --reload
# ngrok http 8000
