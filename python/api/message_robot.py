import time
from agent import AgentContext, UserMessage
from python.helpers.api import ApiHandler
from flask import Request, Response

from python.helpers import files
import os
from werkzeug.utils import secure_filename
from python.helpers.defer import DeferredTask
from python.helpers.print_style import PrintStyle
import json
import uuid

class MessageRobot(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:

    #   customLlmExtraBody: {
    #     extraBody: {
    #       chatId: chatId,
    #     },
    #   },

        systemPrompt = "You are a voice assistant that responds concisely and clearly. Keep answers short and direct. Ignore ellipses ('...') and do not acknowledge them. Prioritize efficiency and relevance in every response."

        # chatId = input.get("customLlmExtraBody", "").get("chatId","")
        # print(chatId)
        chatId = "a1be679f-fdf8-4077-a1cb-0409bdb9eaca"

        msgs = input.get("messages", "")
        request = {
            "text":msgs[len(msgs)-1]['content'],
            "context":chatId,
            "message_id":"",
        }

        task, context = await self.communicate(input=input, request=request)
        return await self.respond(task, context)

    async def respond(self, task: DeferredTask, context: AgentContext):
        result = await task.result()  # type: ignore
        
        def event_stream():

            def generate():
                # Convert the ChatCompletionChunk to a dictionary before JSON serialization
                chunk_dict = {"id": "chatcmpl-BD3ws7Zvr1Emdi2d1pfoi7s5UcLHb", "choices": [{"delta": {"content": result, "function_call": None, "refusal": None, "role": None, "tool_calls": None}, "finish_reason": None, "index": 0, "logprobs": None}], "created": int(time.time()), "model": "gpt-4o-mini-2024-07-18", "object": "chat.completion.chunk", "service_tier": "default", "system_fingerprint": "fp_b8bc95a0ac", "usage": None}
                yield f"data: {json.dumps(chunk_dict)}\n\n"
                yield "data: [DONE]\n\n"
            
            return Response(generate(), content_type='text/event-stream')
        
        return event_stream()


    async def communicate(self, input: dict, request: Request):
        # Handle both JSON and multipart/form-data

        # Handle JSON request as before
        text = request.get("text", "")
        ctxid = request.get("context", "")
        message_id = request.get("message_id", None)
        attachment_paths = []

        # Now process the message
        message = text

        # Obtain agent context
        context = self.get_context(ctxid)

        # Store attachments in agent data
        # context.kodeus.set_data("attachments", attachment_paths)

        # Prepare attachment filenames for logging
        attachment_filenames = (
            [os.path.basename(path) for path in attachment_paths]
            if attachment_paths
            else []
        )

        # Print to console and log
        PrintStyle(
            background_color="#6C3483", font_color="white", bold=True, padding=True
        ).print(f"User message:")
        PrintStyle(font_color="white", padding=False).print(f"> {message}")
        if attachment_filenames:
            PrintStyle(font_color="white", padding=False).print("Attachments:")
            for filename in attachment_filenames:
                PrintStyle(font_color="white", padding=False).print(f"- {filename}")

        # Log the message with message_id and attachments
        context.log.log(
            type="user",
            heading="User message",
            content=message,
            kvps={"attachments": attachment_filenames},
            id=message_id,
        )

        return context.communicate(UserMessage(message, attachment_paths)), context
    

