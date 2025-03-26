import streamlit as st
import plotly.graph_objects as go
from openai import OpenAI
import json
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Business Domain Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .explanation-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🎯 Domain Based DNA Explorer")
st.markdown("Analyze your company's performance across different business domains.")

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    company_name = st.text_input("Enter Company Name")
    analyze_button = st.button("Analyze Company")

# Sample domains and scoring (replace with actual OpenAI analysis)
DOMAINS = [
    "Seamless Mobility: Focused on integrating technology, infrastructure, and services to provide efficient, safe, and convenient transport experiences, including autonomous driving and shared mobility solutions.",
    "Holistic Wellbeing: Centers on comprehensive approaches to health, combining digital health innovations, alternative medicine, preventive healthcare, elderly care, health literacy, and healing architecture to improve overall quality of life.",
    "Rest and Relaxation: Targets stress reduction and rejuvenation through wellness offerings such as spa treatments, fitness programs, and immersive travel experiences.",
    "New Work: Emphasizes flexible, digitally enabled work environments, fostering collaboration, gig economy platforms, remote and hybrid working models, and transformative HR practices.",
    "Personal Wealth and Legal: Deals with managing personal finances, investments, real estate, and legal affairs through innovative digital tools, open banking, decentralized finance, and professional services.",
    "Customized and Fast Demand Fulfillment: Optimizes consumer access to products and services, leveraging innovative retail solutions, e-commerce, everyday outsourcing, and the sharing economy to quickly satisfy consumer needs.",
    "Belief and Mindfulness: Encourages mental and emotional well-being through spiritual, religious, and mindfulness practices, including meditation, yoga, coaching, and esoteric approaches.",
    "Relationships: Fosters interpersonal and professional connections through social networks, digital communication, matchmaking, dating services, and networking events.",
    "Adaptive Development: Supports continuous personal and professional growth via structured education systems, lifelong learning opportunities, and scientific research initiatives.",
    "Personalized Pleasure: Offers customized entertainment experiences, including digital media streaming, gaming, arts, and sports events, tailored to individual preferences.",
    "Smart Environment: Integrates digital technologies into homes and cities to enhance living conditions, safety, sustainability, and efficiency through smart homes, DIY improvements, and smart city initiatives.",
    "Security: Provides comprehensive protection through robust defense, law enforcement, identity management, cybersecurity, justice systems, and privacy protection services.",
    "Infrastructure: Builds foundational digital and physical systems necessary for modern society, including smart energy grids, logistics, telecommunications, e-government, financial transactions, and intelligent building construction.",
    "B2B-Services: Enables business success through specialized services like accounting, B2B banking and insurance, business administration, consulting, and legal support.",
    "Industrie 4.0: Transforms manufacturing and production through digital technologies such as IoT, AI, robotics, predictive maintenance, and 3D printing, allowing greater efficiency and customization."]


def get_company_analysis(api_key, company_name):
    """
    Get company analysis using OpenAI API
    """
    if not api_key or not company_name:
        return None
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""You are a business analyst expert. Please analyze {company_name} across these business domains and provide a JSON response.
    
    For each of these domains, provide a score (0-10) and detailed explanation:
    {', '.join([domain.split(':')[0] for domain in DOMAINS])}
    
    Your response must be a valid JSON object with this exact structure (no additional text before or after):
    {{
        "Seamless Mobility": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Holistic Wellbeing": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Rest and Relaxation": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "New Work": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Personal Wealth and Legal": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Customized and Fast Demand Fulfillment": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Belief and Mindfulness": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Relationships": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Adaptive Development": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Personalized Pleasure": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Smart Environment": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Security": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Infrastructure": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "B2B-Services": {{
            "score": 0,
            "explanation": "detailed explanation"
        }},
        "Industrie 4.0": {{
            "score": 0,
            "explanation": "detailed explanation"
        }}
    }}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract the JSON response
        response_text = response.choices[0].message.content.strip()
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error in API call: {str(e)}")
        return None

def create_radar_chart(data):
    """Create a radar chart using plotly"""
    fig = go.Figure()
    
    # Extract just the domain names before the colon
    domain_names = [domain.split(':')[0] for domain in DOMAINS]
    scores = [data[domain.strip()]["score"] for domain in domain_names]
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=domain_names + [domain_names[0]],
        fill='toself',
        name=company_name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True
    )
    
    return fig

# Main application logic
if analyze_button and api_key and company_name:
    with st.spinner("Analyzing company data..."):
        analysis_results = get_company_analysis(api_key, company_name)
        
        if analysis_results:
            # Display radar chart
            st.subheader("Domain Performance Overview")
            fig = create_radar_chart(analysis_results)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed explanations
            st.subheader("Detailed Analysis")
            
            # Create two columns for the detailed analysis
            cols = st.columns(2)
            for idx, domain in enumerate(DOMAINS):
                col = cols[idx % 2]
                with col:
                    domain_name = domain.split(':')[0].strip()
                    score = analysis_results[domain_name]["score"]
                    explanation = analysis_results[domain_name]["explanation"]
                    
                    st.markdown(f"""
                    <div class="explanation-box">
                        <h3>{domain}</h3>
                        <h4>Score: {score}/10</h4>
                        <p>{explanation}</p>
                    </div>
                    """, unsafe_allow_html=True)
elif analyze_button:
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    if not company_name:
        st.error("Please enter a company name.") 