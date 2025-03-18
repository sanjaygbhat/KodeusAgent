import time
from agent import AgentContext, UserMessage
from python.helpers.api import ApiHandler
from flask import Request, Response

from python.helpers import files
import os
from werkzeug.utils import secure_filename
from python.helpers.defer import DeferredTask
from python.helpers.print_style import PrintStyle


class MessageRobot(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:

        msgs = input.get("messages", "")
        request = {
            "text":msgs[len(msgs)-1]['content'],
            "context":"",
            "message_id":"",
        }

        task, context = await self.communicate(input=input, request=request)
        return await self.respond(task, context)

    async def respond(self, task: DeferredTask, context: AgentContext):
        result = await task.result()  # type: ignore

        a = {
                "id": "chatcmpl-B9MBs8CjcvOU2jLn4n570S5qMJKcT",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "gpt-4o-2024-08-06",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": result,
                            "refusal": None,
                            "annotations": []
                        },
                        "logprobs": None,
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "prompt_tokens_details": {
                    "cached_tokens": 0,
                    "audio_tokens": 0
                    },
                    "completion_tokens_details": {
                    "reasoning_tokens": 0,
                    "audio_tokens": 0,
                    "accepted_prediction_tokens": 0,
                    "rejected_prediction_tokens": 0
                    }
                },
                "service_tier": "default"
                }

        return a
        


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
    

