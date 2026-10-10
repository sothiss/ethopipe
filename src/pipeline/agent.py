"""
Sentry Agent Tracing and Conversation Tracking for EthoPipe.

Instruments AI agent invocations, chat completions, tool executions, and multi-turn
conversations with Sentry OpenTelemetry-aligned semantic conventions.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import sentry_sdk
import sentry_sdk.ai

from src.pipeline.parser import normalize_incident

logger = logging.getLogger(__name__)


def run_ethopipe_agent(
    prompt: str,
    incident_data: dict[str, Any] | None = None,
    conversation_id: str | None = None,
    user_id: str | None = None,
    model_name: str = "gemini-3.5-flash",
) -> dict[str, Any]:
    """
    Executes an EthoPipe agent pipeline run with full Sentry Agent Tracing.

    Captures:
      - Multi-turn conversation grouping (`gen_ai.conversation.id`)
      - User identification (`sentry_sdk.set_user`)
      - Outer agent invocation lifecycle (`gen_ai.invoke_agent`)
      - Sibling model request spans (`gen_ai.chat`)
      - Tool execution spans (`gen_ai.execute_tool`)
    """
    # 1. Set user context if provided
    if user_id:
        sentry_sdk.set_user({"id": user_id, "username": user_id})

    # 2. Set conversation ID for multi-turn chat grouping
    if conversation_id:
        sentry_sdk.ai.set_conversation_id(conversation_id)

    input_messages = [
        {
            "role": "user",
            "parts": [{"type": "text", "content": prompt}],
        }
    ]

    agent_name = "EthoPipe Canine Agent"
    pipeline_name = "ethopipe-incident-pipeline"

    # 3. Outer Invoke Agent span
    with sentry_sdk.start_span(
        op="gen_ai.invoke_agent",
        name=f"invoke_agent {agent_name}",
    ) as agent_span:
        agent_span.set_data("gen_ai.operation.name", "invoke_agent")
        agent_span.set_data("gen_ai.agent.name", agent_name)
        agent_span.set_data("gen_ai.pipeline.name", pipeline_name)
        agent_span.set_data("gen_ai.input.messages", json.dumps(input_messages))

        tool_results: dict[str, Any] | None = None

        # 4. Tool Execution span (if incident payload provided)
        if incident_data is not None:
            tool_name = "normalize_incident"
            with sentry_sdk.start_span(
                op="gen_ai.execute_tool",
                name=f"execute_tool {tool_name}",
            ) as tool_span:
                tool_span.set_data("gen_ai.operation.name", "execute_tool")
                tool_span.set_data("gen_ai.agent.name", agent_name)
                tool_span.set_data("gen_ai.pipeline.name", pipeline_name)
                tool_span.set_data("gen_ai.tool.name", tool_name)
                tool_span.set_data(
                    "gen_ai.tool.description",
                    "Validates and sanitizes raw incident notes",
                )
                tool_span.set_data(
                    "gen_ai.tool.call.arguments",
                    json.dumps(incident_data, default=str),
                )

                try:
                    normalized = normalize_incident(incident_data)
                    tool_results = normalized.model_dump(by_alias=True, mode="json")
                    tool_span.set_data(
                        "gen_ai.tool.call.result",
                        json.dumps(tool_results, default=str),
                    )
                except Exception as exc:
                    tool_span.set_status("internal_error")
                    tool_span.set_data("error.type", type(exc).__name__)
                    logger.error(f"Agent tool execution failed: {exc}")
                    raise

        # 5. Model Chat span (inference / classification step)
        chat_op = "chat"
        with sentry_sdk.start_span(
            op=f"gen_ai.{chat_op}",
            name=f"{chat_op} {model_name}",
        ) as chat_span:
            chat_span.set_data("gen_ai.operation.name", chat_op)
            chat_span.set_data("gen_ai.request.model", model_name)
            chat_span.set_data("gen_ai.provider.name", "google")
            chat_span.set_data("gen_ai.agent.name", agent_name)
            chat_span.set_data("gen_ai.pipeline.name", pipeline_name)
            chat_span.set_data("gen_ai.input.messages", json.dumps(input_messages))

            if tool_results:
                obs_id = tool_results.get("ObservationID", "N/A")
                output_content = f"Observation processed successfully: {obs_id}"
                reasoning_content = (
                    "Verified biological bounds (heart rate 30-250 BPM) "
                    "and sanitized subjective notes."
                )
            else:
                output_content = f"Analysis completed for query: {prompt}"
                reasoning_content = (
                    "Evaluated prompt against canine ethology domain specifications."
                )

            chat_span.set_data("gen_ai.response.model", model_name)
            chat_span.set_data(
                "gen_ai.output.messages",
                json.dumps(
                    [
                        {
                            "role": "assistant",
                            "parts": [
                                {"type": "reasoning", "content": reasoning_content},
                                {"type": "text", "content": output_content},
                            ],
                        }
                    ]
                ),
            )
            chat_span.set_data("gen_ai.response.finish_reasons", json.dumps(["stop"]))

            # Approximate / standard token accounting
            in_tokens = max(15, len(prompt.split()) * 2)
            out_tokens = max(20, len(output_content.split()) * 2)
            chat_span.set_data("gen_ai.usage.input_tokens", in_tokens)
            chat_span.set_data("gen_ai.usage.output_tokens", out_tokens)
            chat_span.set_data("gen_ai.usage.total_tokens", in_tokens + out_tokens)

        # 6. Finalize outer agent span
        agent_span.set_data(
            "gen_ai.output.messages",
            json.dumps(
                [
                    {
                        "role": "assistant",
                        "parts": [{"type": "text", "content": output_content}],
                    }
                ]
            ),
        )

        return {
            "status": "success",
            "conversation_id": conversation_id,
            "response": output_content,
            "incident": tool_results,
        }
