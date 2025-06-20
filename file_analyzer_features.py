# file_analyzer_features.py
import streamlit as st
import pandas as pd
import io
import json # For handling JSON file uploads
from io import StringIO, BytesIO

def render_file_analyzer_section():
    """
    Renders the UI for file upload and column data quality analysis.
    """
    st.markdown("<h2>📁 Data File Analyzer</h2>", unsafe_allow_html=True)
    st.write("Upload a CSV or JSON file (up to 200MB) to analyze the data quality of a selected column. Get insights on nulls, duplicates, and unique values.")

    uploaded_file = st.file_uploader(
        "Choose a CSV or JSON file (Max 200MB)",
        type=["csv", "json"],
        accept_multiple_files=False,
        key="data_file_uploader"
    )

    # Session state for the DataFrame and analysis results
    if 'analyzer_df' not in st.session_state:
        st.session_state['analyzer_df'] = None
    if 'analyzer_column_report' not in st.session_state:
        st.session_state['analyzer_column_report'] = {}

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)

        if file_size_mb > 200:
            st.error("❌ File size exceeds 200MB. Please upload a smaller file.")
            st.session_state['analyzer_df'] = None
            st.session_state['analyzer_column_report'] = {}
            return

        try:
            # Read file content into memory. For pandas, pass the BytesIO object directly.
            # Using BytesIO to handle both text-based (CSV) and binary (potential future) files more universally.
            bytes_data = uploaded_file.getvalue()

            if file_extension == "csv":
                df = pd.read_csv(BytesIO(bytes_data))
            elif file_extension == "json":
                # For JSON, pandas read_json can take BytesIO directly
                df = pd.read_json(BytesIO(bytes_data))
            
            st.session_state['analyzer_df'] = df
            st.success(f"Successfully loaded `{uploaded_file.name}` with {df.shape[0]} rows and {df.shape[1]} columns.")
            
            st.subheader("Dataset Preview:")
            st.dataframe(df.head(), use_container_width=True, hide_index=True)
            
            # Reset analysis report when a new file is uploaded
            st.session_state['analyzer_column_report'] = {}

        except UnicodeDecodeError:
            st.error("❌ Could not decode the file. Please ensure it's UTF-8 encoded.")
            st.session_state['analyzer_df'] = None
            st.session_state['analyzer_column_report'] = {}
        except pd.errors.EmptyDataError:
            st.warning("⚠️ The uploaded file is empty.")
            st.session_state['analyzer_df'] = None
            st.session_state['analyzer_column_report'] = {}
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file. Please ensure it contains valid JSON data.")
            st.session_state['analyzer_df'] = None
            st.session_state['analyzer_column_report'] = {}
        except Exception as e:
            st.error(f"❌ An error occurred during file processing: {str(e)}")
            st.session_state['analyzer_df'] = None
            st.session_state['analyzer_column_report'] = {}

    
    # Column selection and analysis
    current_df = st.session_state['analyzer_df']
    if current_df is not None and not current_df.empty:
        st.markdown("---")
        st.subheader("📈 Column Data Quality Report")
        
        column_options = current_df.columns.tolist()
        selected_column = st.selectbox(
            "Select a column for analysis:",
            options=column_options,
            index=0 if column_options else None,
            key="selected_column_for_analysis"
        )

        if selected_column:
            if st.button("📊 Generate Column Report", type="primary", use_container_width=True, key="generate_column_report_button"):
                with st.spinner(f"Analyzing column '{selected_column}'..."):
                    column_data = current_df[selected_column]
                    total_rows = len(column_data)

                    # Null values
                    null_count = column_data.isnull().sum()
                    null_percentage = (null_count / total_rows * 100) if total_rows > 0 else 0

                    # Duplicates (considering only non-null values for duplicates)
                    non_null_data = column_data.dropna()
                    duplicate_count = non_null_data.duplicated().sum()
                    duplicate_percentage = (duplicate_count / len(non_null_data) * 100) if len(non_null_data) > 0 else 0

                    # Unique values
                    unique_count = non_null_data.nunique()

                    report_content = {
                        "Column Name": selected_column,
                        "Total Rows": total_rows,
                        "Null Values": f"{null_count} ({null_percentage:.2f}%)",
                        "Duplicate Values": f"{duplicate_count} ({duplicate_percentage:.2f}%)",
                        "Unique Values": unique_count,
                        "Data Type": str(column_data.dtype),
                        "Top 10 Unique Values": non_null_data.value_counts().head(10).index.tolist() if unique_count > 0 else []
                    }
                    st.session_state['analyzer_column_report'] = report_content
                    st.success(f"Report for '{selected_column}' generated! ✅")
        
        # Display the report if available
        if st.session_state['analyzer_column_report']:
            report = st.session_state['analyzer_column_report']
            st.markdown(f"<h4>Report for Column: <span style='color: var(--accent-blue-light);'>{report['Column Name']}</span></h4>", unsafe_allow_html=True)
            
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Total Rows", report["Total Rows"])
            with col_r2:
                st.metric("Null Values", report["Null Values"])
            with col_r3:
                st.metric("Unique Values", report["Unique Values"])
            
            col_r4, col_r5 = st.columns(2)
            with col_r4:
                st.metric("Duplicate Values", report["Duplicate Values"])
            with col_r5:
                st.metric("Data Type", report["Data Type"])

            st.markdown("---")
            st.markdown("<h4>Top 10 Unique Values:</h4>", unsafe_allow_html=True)
            if report["Top 10 Unique Values"]:
                st.json(report["Top 10 Unique Values"])
            else:
                st.info("No unique values or column is entirely null.")

            # Download button for the column report
            report_text = f"""
# Data Quality Report for Column: {report['Column Name']}

- Total Rows: {report['Total Rows']}
- Null Values: {report['Null Values']}
- Unique Values: {report['Unique Values']}
- Duplicate Values: {report['Duplicate Values']}
- Data Type: {report['Data Type']}

## Top 10 Unique Values:
{json.dumps(report['Top 10 Unique Values'], indent=2)}
            """
            st.download_button(
                label="⬇️ Download Column Report (Markdown)",
                data=report_text.encode('utf-8'),
                file_name=f"{report['Column Name']}_data_quality_report.md",
                mime="text/markdown",
                use_container_width=True,
                key="download_column_report_md"
            )
    else:
        st.info("Upload a file above to start analyzing columns.")

