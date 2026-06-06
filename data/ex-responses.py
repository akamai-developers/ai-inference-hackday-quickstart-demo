# CASE A: Standard Non-Streaming
#--------------------------------
# response = httpx.Client.post(model, payload, timeout) returns: 
<Response [200 OK]> {
    "status_code": 200,
    "is_success": True,
    "headers": {
        "content-type": "application/json",
        "date": "Fri, 05 Jun 2026 14:39:18 GMT",
        "server": "cloudflare"
    },
    "text": '{"id":"chatcmpl-123",
    "object":"chat.completion",
    "choices":[{"index":0,"message":{"role":"assistant","content":"AI is fast."}}],
    "usage":{"prompt_tokens":5,"completion_tokens":3}}'
}


# Convert the above Response into a json dict via the .json() method
# data = response.json() returns:
{
    "id": "chatcmpl-9A8b7C...",
    "object": "chat.completion",
    "created": 1717598358,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "AI is fast and continuously evolving."
            },
            "logprobs": None,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 7,
        "total_tokens": 22
    }
}



# CASE B: Real-Time Streaming
#--------------------------------

#The Raw Network Stream (Server-Sent Events)
# httpx.stream(...) returns something like this: 
data: {"id":"chat-123","choices":[{"index":0,"delta":{"role":"assistant","content":"AI "}}]}
data: {"id":"chat-123","choices":[{"index":0,"delta":{"content":"is "}}]}
data: {"id":"chat-123","choices":[{"index":0,"delta":{"content":"fast."}}],"usage":{"prompt_tokens":5,"completion_tokens":3}}
data: [DONE]


#json.loads(line[6:]) chops off that data:  prefix and turns the raw text into a clean Python dictionary.
{
    "id": "chat-123",
    "object": "chat.completion.chunk",
    "created": 1717598358,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": "AI "        # <-- Extracted as your 'token'
            },
            "finish_reason": None
        }
    ]
}


#examples - CHUNK 1 - THE START
{
    "id": "chat-123",
    "object": "chat.completion.chunk",
    "created": 1717598358,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": "AI "        # <-- Extracted as your 'token'
            },
            "finish_reason": None
        }
    ]
}

#examples - CHUNK 2 - THE MIDDLE
{
    "id": "chat-123",
    "object": "chat.completion.chunk",
    "created": 1717598358,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": "is "        # <-- Extracted as your 'token'
            },
            "finish_reason": None
        }
    ]
}

#examples - CHUNK 3 - THE END (with metadata about token usage)
{
    "id": "chat-123",
    "object": "chat.completion.chunk",
    "created": 1717598358,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": "fast."     # <-- Extracted as your 'token'
            },
            "finish_reason": "stop"    # <-- Server signals it's done generating
        }
    ],
    "usage": {                         # <-- Final token tallies arrive here
        "prompt_tokens": 5,
        "completion_tokens": 3,
        "total_tokens": 8
    }
}