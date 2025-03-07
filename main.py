import streamlit as st
import pandas as pd
import json
import openai

# Function 1: Identify project components
def analyze_project_with_json_in_prompt(project_brief: str, json_filepath: str, api_key: str):

    client = openai.OpenAI(api_key=api_key)

    with open(json_filepath, 'r', encoding='utf-8') as file:
        project_components = json.load(file)

    json_string = json.dumps(project_components, indent=2)

    # Create a prompt including the JSON
    prompt = f"""
    You are a project management AI expert on creative projects. You want to identify the components of the project explained in the following brief:

    **Project Brief:**
    {project_brief}

    These are all the possible components of the project:
    {json_string}

    Your goal is to identify all and only the components of a creative projects among that ones offered by your company in order to simpify the quotation process.

    Your response must be a valid JSON array containing only the components that match the project brief.
    Each entry should include:
    - "service_id"
    - "service_name"
    - "product_id"
    - "product_name"
    - "type_of_work_id"
    - "type_of_work_name"
    - "complexity"
    - "key_arts" --> intended as a list of creatives assets to be delivered
    - "variants" --> intended as a list of variants to be applied to each creatives assets
    - "sizes" --> intended as a list of different sizes to be delivered per each variant


    Example response (must be valid JSON format):
    {{
        "components": [
            {{
                "service_id": 2002,
                "service_name": "Digital Banner Ad Design",
                "product_id": 6003,
                "product_name": "Static Digital Banners",
                "type_of_work_id": 15,
                "type_of_work_name": "Creative Development",
                "complexity": "MEDIUM",
                "key_arts": ["Instagram Ads", "TikTok Ads", "YouTube Banners"],
                "variants": ["Athletes", "Creatives"],
                "sizes": ["1080x1080", "1080x1920", "2560x1440"]
            }}
        ]
    }}

    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI assistant skilled in Creative Project Management."},
                  {"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    extracted_info_json = json.loads(response.choices[0].message.content.strip())
    return extracted_info_json

# Function 2: Calculate project quotation
def calculate_quotation(df: pd.DataFrame, csv_filepath: str):
    result_df = pd.DataFrame(columns=["service_name", "product_name", "type_of_work_name", "complexity", "key_arts", "variants", "sizes", "estimate"])
    quotation_hours_df = pd.read_csv(csv_filepath)
    for _, row in df.iterrows():
        query = f"service_id == {row['service_id']} and product_id == {row['product_id']} and type_of_work_id == {row['type_of_work_id']} and complexity == '{row['complexity']}'"
        df_filtered = quotation_hours_df.query(query)
        if not df_filtered.empty:
            hours_per_key_art = df_filtered['hours_per_key_art'].iat[0]
            hours_per_variant = df_filtered['hours_per_variant'].iat[0]
            hours_per_size = df_filtered['hours_per_resize'].iat[0]
            key_arts_quotation = max(1, len(row['key_arts'])) * hours_per_key_art
            variants_quotation = max(0, (len(row['variants']) - 1)) * hours_per_variant
            sizes_quotation = max(0, (len(row['sizes']) - 1)) * hours_per_size
            new_row = {
                "service_name": row['service_name'],
                "product_name": row['product_name'],
                "type_of_work_name": row['type_of_work_name'],
                "complexity": row['complexity'],
                "key_arts": len(row['key_arts']),
                "variants": len(row['variants']),
                "sizes": len(row['sizes']),
                #"key_arts_quotation": key_arts_quotation, "variants_quotation": variants_quotation, "sizes_quotation": sizes_quotation,
                "estimate": key_arts_quotation + variants_quotation + sizes_quotation
            }
            result_df = pd.concat([result_df, pd.DataFrame([new_row])], ignore_index=True)
    return result_df

# Streamlit UI
st.title("Superside - Project Quotation Tool")
st.markdown("""
            This **application** is designed to assist **Project Managers** in generating quotations for creative projects based on a given brief. The tool leverages **AI-driven analysis** to identify project components and calculates the required work hours using **predefined complexity metrics**.

            🧟‍♂️  It may look a bit rough around the edges, but hey, it’s just a POC! 🚧

            #### 🛠️ How It Works

            1. ✍️ **Enter the Project Brief**: Provide a description of the project in the text area.
            2. 🔍 **Identify Components**: The AI analyzes the brief and extracts relevant project components, displaying them in an editable table.
            3. ✏️ **Modify Components**: Users can add, remove, or modify components before proceeding.
            4. 💰 **Calculate Quotation**: The tool calculates the estimated work hours based on predefined rates and complexity levels.
            5. 📊 **View and Export Results**: The final quotation is displayed in both tabular and JSON format, with an option to download the JSON file.
            """)

project_brief = st.text_area("Enter Project Brief:")
json_filepath = "structured_data.json"  # Provide the correct path to the JSON file
csv_filepath = "quotation_hours.csv"    # Provide the correct path to the CSV file
api_key = st.secrets["OPENAI_API_KEY"]  # Ensure the key is stored in Streamlit secrets

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if st.button("Identify Components"):
    with st.spinner("Decomposing the project..."):
        result = analyze_project_with_json_in_prompt(project_brief, json_filepath, api_key)
        if "components" in result:
            st.session_state.df = pd.DataFrame(result["components"])

if not st.session_state.df.empty:
    st.write("### Identified Components:")
    st.session_state.df = st.data_editor(st.session_state.df, num_rows="dynamic", key="edited_df")

if st.button("Calculate Quotation"):
    with st.spinner("Calculating work hours..."):
        quotation_df = calculate_quotation(st.session_state.df, csv_filepath)
        st.session_state.quotation_df = quotation_df
        st.write("### Project Quotation:")
        st.dataframe(quotation_df)
        json_data = quotation_df.to_json(orient="records", indent=4)
        st.json(json_data)
        st.download_button("Download JSON", json_data, file_name="quotation.json", mime="application/json")

if st.button("New Quotation"):
    st.session_state.clear()

# Footer
st.markdown("---")
st.caption("❤️ Crafted with love by **Paolo Piacenti**")
