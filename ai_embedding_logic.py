# ai_embedding_logic.py
import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import json

# --- Load Environment Variables ---
# This ensures that your API key is loaded from a .env file securely.
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

# --- Retrieve Gemini API Key ---
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# --- API Key Validation ---
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
    # If API key is not set, raise a RuntimeError. Streamlit (or any calling app)
    # should catch this and display a user-friendly error.
    raise RuntimeError(
        "❌ GEMINI_API_KEY not found or is the placeholder value in your .env file. "
        "Please set it correctly to use AI features. Refer to the README for setup instructions."
    )

# --- Gemini Model Instances (initialized once globally) ---
_embedding_model_instance = None  # For text embeddings
_generative_model_instance = None # For general text generation and structured responses

def get_embedding_model():
    """
    Initializes and returns a Gemini GenerativeModel specifically configured for embeddings.
    Ensures the embedding model is initialized only once during the application's lifecycle.
    It prioritizes 'models/embedding-001' as the most common text embedding model.
    """
    global _embedding_model_instance
    if _embedding_model_instance is not None:
        return _embedding_model_instance

    genai.configure(api_key=GOOGLE_API_KEY)

    # Define the preferred embedding model
    preferred_embedding_model = 'models/embedding-001'
    
    # List available models that support embedding content
    available_embedding_models = [m.name for m in genai.list_models() if 'embedContent' in m.supported_generation_methods]

    chosen_embedding_model_name = None
    if preferred_embedding_model in available_embedding_models:
        chosen_embedding_model_name = preferred_embedding_model
    elif available_embedding_models:
        chosen_embedding_model_name = available_embedding_models[0] # Fallback to any available embedding model

    if chosen_embedding_model_name:
        try:
            _embedding_model_instance = genai.GenerativeModel(chosen_embedding_model_name)
            print(f"Gemini embedding model initialized: {chosen_embedding_model_name}")
            return _embedding_model_instance
        except Exception as e:
            # Raise a more specific error for initialization failure
            raise Exception(f"Failed to initialize Gemini embedding model '{chosen_embedding_model_name}'. Please check your API key and network access.") from e
    else:
        # If no suitable embedding model is found at all
        raise Exception(
            "No suitable Gemini embedding model found that supports 'embedContent'. "
            "Please ensure your API key is correct and valid, or check Google AI Studio for available models."
        )

def get_generative_model():
    """
    Initializes and returns a Gemini GenerativeModel for general text generation.
    Prioritizes cost-effective and stable models, ensuring initialization only once.
    """
    global _generative_model_instance
    if _generative_model_instance is not None:
        return _generative_model_instance

    genai.configure(api_key=GOOGLE_API_KEY)

    # List available models that support content generation
    available_generative_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_generative_models.append(m.name)

    # Prioritize models: gemini-1.5-flash (cost-effective), then gemini-pro (stable), then gemini-1.5-pro
    preferred_order = [
        'models/gemini-1.5-flash',
        'models/gemini-pro',
        'models/gemini-1.5-pro'
    ]

    chosen_generative_model_name = None
    for preferred_model in preferred_order:
        if preferred_model in available_generative_models:
            chosen_generative_model_name = preferred_model
            break
    
    if chosen_generative_model_name is None and available_generative_models:
        chosen_generative_model_name = available_generative_models[0] # Fallback to any available

    if chosen_generative_model_name:
        try:
            _generative_model_instance = genai.GenerativeModel(chosen_generative_model_name)
            print(f"Gemini generative model initialized: {chosen_generative_model_name}")
            return _generative_model_instance
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini generative model '{chosen_generative_model_name}'. Please check your API key and network access.") from e
    else:
        raise Exception(
            "No suitable Gemini generative model found that supports 'generateContent'. "
            "Please ensure your API key is correct and valid, or check Google AI Studio for available models."
        )


# --- Ensure models are initialized when the module is imported ---
# This allows for immediate use of embedding/generative functions after import
try:
    get_embedding_model()
    get_generative_model()
except Exception as e:
    # Print the error for debugging purposes in the console.
    # In a Streamlit app, this error will also typically be displayed on the UI.
    print(f"Initial Gemini model setup failed on import: {e}")


def get_embedding(text: str) -> list[float]:
    """
    Generates a vector embedding for the given text using the pre-initialized Gemini embedding model.
    Throws a RuntimeError if the embedding model is not initialized or if the API call fails.
    """
    model_instance = _embedding_model_instance
    if model_instance is None: # Fix: Changed === to is
        raise RuntimeError("Embedding model not initialized. Check API key and network connection.")

    if not text.strip():
        return [] # Return empty list for empty or whitespace-only text

    try:
        # Call the embed_content method on the GenerativeModel instance
        # Ensure the model name (e.g., "models/embedding-001") is passed as the 'model' argument
        result = model_instance.embed_content(model="models/embedding-001", content=text)
        if result and 'embedding' in result:
            return result['embedding']
        else:
            raise ValueError("Embedding API returned an empty or invalid embedding structure.")
    except Exception as e:
        raise RuntimeError(f"Failed to get embedding for text: '{text[:100]}...': {e}")


def ask_gemini_text(prompt: str) -> str:
    """
    Sends a given prompt to the initialized Gemini generative model for text generation and returns its text response.
    Returns Markdown-formatted text from the AI.
    Handles potential API errors and safety blocks.
    """
    model_instance = _generative_model_instance
    if model_instance is None: # Fix: Changed === to is
        return "❌ AI Service Error: Generative model not initialized. Please ensure your API key is correctly configured and accessible."

    if not prompt.strip():
        return "❌ Please provide a valid prompt for the AI to process."

    try:
        response = model_instance.generate_content(prompt)

        if response and response.candidates and len(response.candidates) > 0 and \
           response.candidates[0].content and response.candidates[0].content.parts and \
           len(response.candidates[0].content.parts) > 0:
            return response.candidates[0].content.parts[0].text
        else:
            print(f"Gemini API returned an empty or unexpected text response structure: {response}")
            return "❌ AI did not return a valid text response. The AI might have refused the query or an internal error occurred. Please try again with different or simpler code."
    except genai.types.BlockedPromptException as e:
        return f"❌ AI Blocked Content: Your request for text generation was blocked due to safety policy. Details: {e.response.prompt_feedback.block_reason.name}."
    except Exception as e:
        print(f"Error during Gemini text API call: {e}")
        return f"❌ Gemini Text API Call Failed: {e}. Possible issues: network problem, rate limit, or invalid API key/model access."


def ask_gemini_structured(prompt: str, response_schema: dict) -> dict:
    """
    Sends a given prompt to the Gemini model requesting a structured JSON response.
    Returns a dictionary parsed from the AI's JSON output.
    Handles potential API errors, safety blocks, and JSON parsing issues.
    """
    model_instance = _generative_model_instance
    if model_instance is None: # Fix: Changed === to is
        return {"error": "❌ AI Service Error: Generative model not initialized. Please ensure your API key is correctly configured and accessible."}

    if not prompt.strip():
        return {"error": "❌ Please provide a valid prompt for structured AI processing."}
    
    if not response_schema or not isinstance(response_schema, dict) or not response_schema.get("type"):
        return {"error": "❌ A valid response_schema (dictionary with 'type' field) is required for structured AI output."}

    try:
        # Pass content and generation_config as separate arguments
        response = model_instance.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        if response and response.candidates and len(response.candidates) > 0 and \
           response.candidates[0].content and response.candidates[0].content.parts and \
           len(response.candidates[0].content.parts) > 0:
            
            json_text = response.candidates[0].content.parts[0].text
            try:
                parsed_json = json.loads(json_text)
                return parsed_json
            except json.JSONDecodeError as json_e:
                print(f"Failed to parse AI's JSON response: {json_e}\nRaw AI response: {json_text}")
                return {"error": f"❌ AI returned malformed JSON: {json_e}. Raw: {json_text[:200]}..."}
        else:
            print(f"Gemini API returned an empty or unexpected structured response structure: {response}")
            return {"error": "❌ AI did not return a valid structured response. It might have refused the query or an internal error occurred."}
    except genai.types.BlockedPromptException as e:
        return {"error": f"❌ AI Blocked Content (Structured): Your request for structured generation was blocked due to safety policy. Details: {e.response.prompt_feedback.block_reason.name}."}
    except Exception as e:
        print(f"Error during Gemini structured API call: {e}")
        return {"error": f"❌ Gemini Structured API Call Failed: {e}. Possible issues: network problem, rate limit, or invalid API key/model access."}

