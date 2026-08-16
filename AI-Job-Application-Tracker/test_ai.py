from services.ai_service import generate_ai_response


response = generate_ai_response(
    "Give me one short tip for preparing for a software engineering internship."
)

print(response)