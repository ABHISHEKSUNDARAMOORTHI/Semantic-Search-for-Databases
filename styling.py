# styling.py
import streamlit as st

def apply_custom_css():
    """Applies custom CSS to the Streamlit application for a professional look."""
    st.markdown("""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        /* Import Font Awesome for Icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');


        /* Color Variables */
        :root {
            --bg-primary: #1a202c; /* Deep Dark Blue-Gray */
            --bg-secondary: #2d3748; /* Slightly Lighter Dark Blue-Gray (Card/Header) */
            --text-light: #e2e8f0; /* Off-White Text */
            --text-medium: #a0aec0; /* Subtler Gray Text */

            --accent-blue-light: #63b3ed; /* Primary Accent Blue */
            --accent-blue-dark: #4299e1; /* Darker Accent Blue */
            --accent-green: #38b2ac; /* Teal for success-like elements */

            --border-color: #4a5568; /* Subtle Border Color */
            --shadow-light: rgba(0, 0, 0, 0.2);
            --shadow-medium: rgba(0, 0, 0, 0.4);
            --border-radius-lg: 12px;
            --border-radius-md: 8px;
            --border-radius-sm: 4px;
        }

        /* General Body & Typography */
        html, body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-light);
            background-color: var(--bg-primary);
        }

        /* Streamlit App Overrides */
        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-light);
        }

        /* Hero Section Styling for a "Bang" Entrance */
        .hero-section {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, #1a273b 100%);
            padding: 4rem 2rem;
            text-align: center;
            color: var(--text-light);
            box-shadow: 0 10px 30px var(--shadow-medium);
            border-bottom: 2px solid var(--accent-blue-dark);
            position: relative;
            overflow: hidden;
        }

        .hero-title {
            font-size: 3.8rem;
            color: var(--accent-blue-light);
            margin-bottom: 0.8rem;
            font-weight: 800;
            letter-spacing: -0.06em;
            text-shadow: 0px 4px 10px var(--shadow-medium);
            position: relative;
            z-index: 1;
            animation: slideInFromTop 1s ease-out;
        }
        .hero-title i {
            margin-right: 1rem;
            color: var(--accent-blue-dark);
        }

        .hero-subtitle {
            font-size: 1.8rem;
            color: var(--text-medium);
            margin-bottom: 1.5rem;
            font-weight: 400;
            opacity: 0.95;
            line-height: 1.4;
            position: relative;
            z-index: 1;
            animation: fadeIn 1.5s ease-out 0.5s forwards;
            opacity: 0;
        }

        .hero-tagline {
            font-size: 1.4rem;
            color: var(--accent-blue-light);
            font-weight: 600;
            margin-top: 2rem;
            text-shadow: 0px 1px 3px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
            animation: fadeIn 2s ease-out 1s forwards;
            opacity: 0;
        }

        @keyframes slideInFromTop {
            0% { transform: translateY(-50px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        /* Main Content Container */
        .main .block-container {
            max-width: 1200px;
            padding: 2.5rem 3rem;
            background-color: var(--bg-secondary);
            border-radius: var(--border-radius-lg);
            box-shadow: 0 10px 25px var(--shadow-medium);
            margin: 3rem auto;
            border: 1px solid var(--border-color);
        }

        /* Section Headers */
        .stMarkdown h2 {
            font-size: 2.2rem;
            color: var(--text-light);
            margin-top: 2.5rem;
            margin-bottom: 1.8rem;
            border-bottom: 2px solid var(--accent-blue-light);
            padding-bottom: 0.8rem;
            font-weight: 700;
            position: relative;
        }
        .stMarkdown h2::after {
            content: '';
            display: block;
            width: 70px;
            height: 5px;
            background: linear-gradient(90deg, var(--accent-blue-light), transparent);
            position: absolute;
            bottom: -2px;
            left: 0;
            border-radius: var(--border-radius-sm);
        }

        .stMarkdown h3 {
            font-size: 1.8rem;
            color: var(--accent-blue-light);
            margin-top: 2rem;
            margin-bottom: 1.2rem;
            border-bottom: 1px dashed var(--border-color);
            padding-bottom: 0.6rem;
            font-weight: 600;
        }
        .stMarkdown h4 {
            font-size: 1.4rem;
            color: var(--accent-blue-dark);
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }

        /* Textareas and Input Fields */
        textarea, .stTextInput > div > div > input, .stCodeEditor {{
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            color: var(--text-light);
            font-size: 1.05rem;
            padding: 12px 18px;
            box-shadow: inset 0 2px 5px var(--shadow-light);
            transition: all 0.3s ease;
        }}
        textarea:focus, .stTextInput > div > div > input:focus, .stCodeEditor:focus-within {{
            border-color: var(--accent-blue-light);
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5), inset 0 2px 5px var(--shadow-light);
            outline: none;
        }}
        textarea::placeholder {{
            color: var(--text-medium);
            opacity: 0.6;
        }}

        /* Buttons */
        .stButton > button {{
            padding: 1rem 2rem;
            border: none;
            border-radius: var(--border-radius-md);
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1.8rem;
            box-shadow: 0 8px 15px var(--shadow-medium);
            letter-spacing: 0.03em;
        }}
        .stButton > button:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 20px var(--shadow-medium);
        }}
        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: 0 4px 8px var(--shadow-light);
        }}

        .stButton > button.primary {{
            background: linear-gradient(45deg, var(--accent-blue-dark), var(--accent-blue-light));
            color: #ffffff;
            border: 1px solid var(--accent-blue-light);
        }}
        .stButton > button.primary:hover {{
            background: linear-gradient(45deg, #3182ce, var(--accent-blue-light));
        }}

        .stButton > button.secondary {{
            background-color: var(--bg-primary);
            color: var(--accent-blue-light);
            border: 2px solid var(--accent-blue-dark);
        }}
        .stButton > button.secondary:hover {{
            background-color: var(--accent-blue-dark);
            color: #ffffff;
            border-color: var(--accent-blue-dark);
        }}
        .stButton > button i {{
            margin-right: 0.7rem;
            font-size: 1.2em;
        }}

        /* Markdown output styling (for AI explanations) */
        .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {{
            color: var(--text-light);
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }}
        .stMarkdown ul {{
            list-style-type: '👉 ';
            margin-left: 30px;
            padding-left: 10px;
        }}
        .stMarkdown ol {{
            margin-left: 30px;
            padding-left: 10px;
        }}
        .stMarkdown strong {{
            color: var(--accent-blue-light);
            font-weight: 700;
        }}
        .stMarkdown em {{
            color: var(--text-medium);
            font-style: italic;
        }}
        .stMarkdown code {{
            background-color: #4a5568;
            padding: 0.3em 0.5em;
            border-radius: var(--border-radius-sm);
            font-family: 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.95em;
            color: #FFD700;
        }}
        .stMarkdown pre code {{
            background-color: #0d1217;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1.5em;
            overflow-x: auto;
            margin-bottom: 2rem;
            display: block;
            box-shadow: inset 0 0 10px var(--shadow-light);
            color: #ffffff;
            font-size: 1em;
            line-height: 1.5;
        }}

        /* Alerts and Info Boxes */
        .stAlert {{
            border-radius: var(--border-radius-md);
            margin-top: 1.5rem;
            padding: 1.2rem 1.8rem;
            font-weight: 600;
            font-size: 1.05rem;
        }}
        .stAlert.st-emotion-cache-1fcpknu {{ /* Success */
            border-left: 8px solid var(--accent-green) !important;
            background-color: rgba(56, 178, 172, 0.15) !important;
            color: var(--accent-green) !important;
        }}
        .stAlert.st-emotion-cache-1wdd6qg {{ /* Warning */
            border-left: 8px solid var(--warning-color) !important;
            background-color: rgba(251, 191, 36, 0.15) !important;
            color: var(--warning-color) !important;
        }}
        .stAlert.st-emotion-cache-1215i5j {{ /* Error */
            border-left: 8px solid var(--danger-color) !important;
            background-color: rgba(239, 68, 68, 0.15) !important;
            color: var(--danger-color) !important;
        }}
        .stInfo {{ /* Info */
            border-left: 8px solid var(--info-color);
            background-color: rgba(59, 130, 246, 0.15);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            margin-top: 1.5rem;
            color: var(--info-color);
            font-size: 1.1rem;
        }}

        /* Expander Styling */
        .streamlit-expanderHeader {{
            background-color: var(--border-color);
            color: var(--text-light);
            font-weight: 600;
            border-radius: var(--border-radius-md);
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            transition: background-color 0.3s ease;
            box-shadow: 0 3px 8px var(--shadow-light);
            font-size: 1.1rem;
        }}
        .streamlit-expanderHeader:hover {{
            background-color: #5b6980;
        }}
        .streamlit-expanderContent {{
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 var(--border-radius-md) var(--border-radius-md);
            padding: 1.8rem;
            box-shadow: inset 0 0 10px var(--shadow-light);
        }}

        /* Horizontal rule */
        hr {{
            border-top: 1px solid var(--border-color);
            margin: 3.5rem 0;
            opacity: 0.6;
        }}

        /* Responsive Design */
        @media (max-width: 1024px) {{
            /* Adjust for tablets */
        }}

        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1.5rem;
                margin: 1.5rem auto;
                width: 95%;
            }}
            .stButton > button {{
                display: block;
                width: 100%;
                margin: 0.8rem 0;
            }}
            .stMarkdown h1 {{
                font-size: 2rem;
            }}
            .stMarkdown h2 {{
                font-size: 1.7rem;
            }}
            .stMarkdown h3 {{
                font-size: 1.4rem;
            }}
            .stMarkdown h4 {{
                font-size: 1.1rem;
            }}
        }}

    </style>
    """, unsafe_allow_html=True)

