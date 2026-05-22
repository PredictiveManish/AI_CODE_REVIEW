import streamlit as st
from github_clone import clone_repo
from parser import extract_code_elements
from reviewer import review_code
from utils import create_dataframe

st.set_page_config(page_title="AI Code Review Agent", layout="wide")

st.title("AI Code Review Agent")

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze Repository"):

    if repo_url:

        # Clone Repository
        with st.spinner("Cloning repository..."):
            repo_path = clone_repo(repo_url)

        st.success("Repository cloned successfully")

        # Parse Source Code
        with st.spinner("Parsing source code..."):
            code_elements = extract_code_elements(repo_path)

        st.success(f"Found {len(code_elements)} code elements")

        # Safety Check
        if not code_elements:
            st.warning("No parsable code elements found.")
            st.stop()

        review_results = []
        progress = st.progress(0)

        # Analyze Code
        for idx, item in enumerate(code_elements):

            if item.get("code"):

                try:
                    result = review_code(item["code"])

                    # Debugging
                    print("AI RESPONSE:", result)
                    print("TYPE:", type(result))

                    # If result is string
                    if isinstance(result, str):

                        review_results.append({
                            "Type": item.get("type", "Unknown"),
                            "Name": item.get("name", "Unknown"),
                            "Issue": result,
                            "Severity": "Medium",
                            "Confidence": 50,
                            "Suggestion": "Review manually"
                        })

                    # If result is dictionary
                    elif isinstance(result, dict):

                        review_results.append({
                            "Type": item.get("type", "Unknown"),
                            "Name": item.get("name", "Unknown"),
                            "Issue": result.get("issue", "No issue found"),
                            "Severity": result.get("severity", "Low"),
                            "Confidence": result.get("confidence", 50),
                            "Suggestion": result.get("suggestion", "No suggestion")
                        })

                except Exception as e:

                    review_results.append({
                        "Type": item.get("type", "Unknown"),
                        "Name": item.get("name", "Unknown"),
                        "Issue": f"Error during review: {str(e)}",
                        "Severity": "High",
                        "Confidence": 0,
                        "Suggestion": "Fix reviewer.py"
                    })

            progress.progress((idx + 1) / len(code_elements))

        # Create DataFrame
        df = create_dataframe(review_results)

        if df.empty:
            st.warning("No review results generated.")
            st.stop()

        st.subheader("Review Results")

        # Filter
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "Low", "Medium", "High"]
        )

        if severity_filter != "All":
            df = df[df["Severity"] == severity_filter]

        # Display Table
        st.dataframe(df, use_container_width=True)

        # Low Confidence Reviews
        st.subheader("Verify This (Low Confidence Reviews)")

        low_confidence = df[df["Confidence"] < 50]

        if not low_confidence.empty:
            st.dataframe(low_confidence, use_container_width=True)
        else:
            st.write("No low-confidence reviews found")

        # Download CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Report",
            data=csv,
            file_name="review_report.csv",
            mime="text/csv"
        )

    else:
        st.error("Please enter a GitHub repository URL")