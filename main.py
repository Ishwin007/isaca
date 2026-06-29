import json
import threading
import urllib.request
import urllib.parse
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

GOATCOUNTER_URL = "https://isaca-mcp.goatcounter.com/count"

def track(path: str):
    def _send():
        try:
            url = f"{GOATCOUNTER_URL}?p={urllib.parse.quote(path)}"
            urllib.request.urlopen(url, timeout=3)
        except Exception:
            pass
    threading.Thread(target=_send, daemon=True).start()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent / "isaca_data"

MCP_SERVER_INFO = {
    "name": "isaca-info (Unofficial Community Tool)",
    "version": "1.0.0",
    "description": "This is an unofficial community tool, not affiliated with or endorsed by ISACA. Information is based on publicly available content from isaca.org and is under development — always cross-check with isaca.org for the latest and most accurate information.",
}

TOOLS = [
    {
        "name": "about_isaca",
        "description": "Returns detailed information about ISACA — who they are, what they do, their certifications, membership, and mission.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_cisa",
        "description": "Returns detailed information about the CISA (Certified Information Systems Auditor) certification — exam details, eligibility, syllabus, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_cism",
        "description": "Returns detailed information about the CISM (Certified Information Security Manager) certification — exam details, domains, eligibility, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_crisc",
        "description": "Returns detailed information about the CRISC (Certified in Risk and Information Systems Control) certification — exam details, domains, eligibility, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_cgeit",
        "description": "Returns detailed information about the CGEIT (Certified in the Governance of Enterprise IT) certification — exam details, domains, eligibility, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_cobit_data",
        "description": "Returns detailed information about COBIT (Control Objectives for Information and Related Technologies) — the ISACA framework for governance and management of enterprise IT.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_data_certification_exam_prep",
        "description": "Returns CISA exam preparation resources including official study materials, exam domain breakdowns, study tips, exam format, and CPE requirements.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_certification",
        "description": "Returns information about how to get an ISACA certification — steps, requirements, application process, and tips.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "membership_benefits",
        "description": "Returns information about ISACA membership benefits, fees, and how to join.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "training_resources",
        "description": "Returns information about ISACA training options including online courses, instructor-led training, exam prep materials, webinars, and conferences.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "cpe_policy",
        "description": "Returns ISACA's Continuing Professional Education (CPE) policy — annual requirements, eligible activities, reporting process, and consequences of non-compliance.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "generate_audit_checklist",
        "description": "Returns ISACA-aligned audit checklists for cloud security, access management, data privacy, network security, and general IT audits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_cdpse",
        "description": "Returns detailed information about the CDPSE (Certified Data Privacy Solutions Engineer) certification — exam details, domains, eligibility, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_ccoa",
        "description": "Returns detailed information about the CCOA (Certified Cybersecurity Operations Analyst) certification — exam details, domains, hands-on tools, eligibility, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_aaia",
        "description": "Returns detailed information about the AAIA (Advanced in AI Audit) certification — the world's first advanced AI audit credential, domains, prerequisites, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_aaism",
        "description": "Returns detailed information about the AAISM (Advanced in AI Security Management) certification — domains, prerequisites, exam cost, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "about_aair",
        "description": "Returns detailed information about the AAIR (Advanced in AI Risk) certification — domains, prerequisites, exam cost, and benefits.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "isaca_chapters",
        "description": "Returns information about ISACA local chapters worldwide — how to find your chapter, benefits of joining, events, volunteering, and CPE opportunities.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "certification_salaries",
        "description": "Returns job market and salary data for all ISACA certifications including average salaries, job titles, and market demand.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "certification_comparison",
        "description": "Returns a detailed comparison of all ISACA certifications — focus areas, career levels, industries, exam costs, and recommended pathways.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "which_certification",
        "description": "Helps users decide which ISACA certification is right for them based on their role, experience level, and career goals.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
]


def read_data_file(filename: str) -> str:
    path = DATA_DIR / filename
    if not path.exists():
        return f"Error: {filename} not found."
    return path.read_text(encoding="utf-8")


def run_tool(name: str, arguments: dict = None) -> dict:
    arguments = arguments or {}
    if name == "about_isaca":
        text = read_data_file("about_isaca.txt")
    elif name == "about_cisa":
        text = read_data_file("about_cisa.txt")
    elif name == "about_cism":
        text = read_data_file("about_cism.txt")
    elif name == "about_crisc":
        text = read_data_file("about_crisc.txt")
    elif name == "about_cgeit":
        text = read_data_file("about_cgeit.txt")
    elif name == "get_cobit_data":
        text = read_data_file("Cobit.txt")
    elif name == "get_data_certification_exam_prep":
        text = read_data_file("exam_prep.txt")
    elif name == "get_certification":
        text = read_data_file("ISACA Get certification.txt")
    elif name == "membership_benefits":
        text = read_data_file("membership_benefits.txt")
    elif name == "training_resources":
        text = read_data_file("training_resources.txt")
    elif name == "cpe_policy":
        text = read_data_file("cpe_policy.txt")
    elif name == "generate_audit_checklist":
        text = read_data_file("audit_checklists.txt")
    elif name == "about_cdpse":
        text = read_data_file("about_cdpse.txt")
    elif name == "about_ccoa":
        text = read_data_file("about_ccoa.txt")
    elif name == "about_aaia":
        text = read_data_file("about_aaia.txt")
    elif name == "about_aaism":
        text = read_data_file("about_aaism.txt")
    elif name == "about_aair":
        text = read_data_file("about_aair.txt")
    elif name == "isaca_chapters":
        text = read_data_file("isaca_chapters.txt")
    elif name == "certification_salaries":
        text = read_data_file("certification_salaries.txt")
    elif name == "certification_comparison":
        text = read_data_file("certification_comparison.txt")
    elif name == "which_certification":
        text = read_data_file("which_certification.txt")
    else:
        return None
    return {"type": "text", "text": text}


# SSE endpoint — Claude calls GET to discover tools
@app.get("/sse")
async def mcp_sse_handler(request: Request):
    async def event_stream():
        def send(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        yield send({
            "jsonrpc": "2.0",
            "method": "initialize",
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": MCP_SERVER_INFO,
                "capabilities": {"tools": {}},
            },
        })

        yield send({
            "jsonrpc": "2.0",
            "method": "tools/list",
            "result": {"tools": TOOLS},
        })

        while not await request.is_disconnected():
            await asyncio.sleep(15)
            yield ": ping\n\n"

    track("/sse/connect")
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        },
    )


# POST endpoint — Claude calls this with tool name + arguments
@app.post("/")
async def mcp_tool_call_handler(request: Request):
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    req_id = body.get("id")

    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": MCP_SERVER_INFO,
                "capabilities": {"tools": {}},
            },
        })

    if method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        })

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        track(f"/tools/{name}")
        result = run_tool(name, arguments)

        if result is None:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{name}' not found"},
            })

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [result]},
        })

    return JSONResponse({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method '{method}' not supported"},
    })
