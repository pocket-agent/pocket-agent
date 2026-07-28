# Memory and knowledge

Personal preferences, knowledge base search, and contextual recall.

## Purpose

Remember user preferences and search indexed document knowledge.

## Tools

- remember_memory
- recall_memory
- search_knowledge
- index_knowledge

## Instructions

- Store only useful preferences and long-term facts
- Never store passwords, tokens, or secrets
- Run /kb_index to populate knowledge from NAS text and PDFs
- Use /recall and /kb before answering document questions when possible

## Examples

- "/remember I prefer PDF summaries in bullet points"
- "/recall tax documents"
- "/kb invoice policy"
- "/kb_index"

## Limitations

- No secret storage
- Knowledge search quality depends on /kb_index and GEMINI_API_KEY for vectors
