import streamlit as st
from lexer import Lexer
from parser import Parser
from validator import Validator


st.set_page_config(page_title="SQL Validator", layout="wide")

st.title("🧠 SQL Query Validator")
st.markdown("Validate single SQL queries or upload a file with multiple queries.")


# Create tabs
tab1, tab2 = st.tabs(["🔹 Single Query Validator", "📂 Multi Query File Validator"])


# =========================================================
# 🔹 TAB 1 — SINGLE QUERY VALIDATOR
# =========================================================
with tab1:

    st.subheader("Validate a Single SQL Query")

    query = st.text_area(
        "Enter SQL Query:",
        height=200,
        placeholder="SELECT * FROM users;"
    )

    validate_single = st.button("Validate Query")

    if validate_single:

        if not query.strip():
            st.warning("Please enter a SQL query.")
        else:
            try:
                lexer = Lexer()
                tokens = lexer.tokenize(query)

                parser = Parser(tokens)
                ast = parser.parse()

                validator = Validator()
                result = validator.validate(ast)

                if result["success"]:
                    st.success("✅ Query validated successfully!")

                    with st.expander("View AST"):
                        st.write(ast)

                else:
                    st.error("❌ Validation Failed")

                    for error in result["errors"]:
                        st.write(f"Error ID: {error.id}")
                        st.write(f"Type: {error.type}")
                        st.write(f"Message: {error.message}")
                        st.write("---")

            except SyntaxError as e:
                st.error("❌ Syntax Error")
                st.write(str(e))

            except Exception as e:
                st.error("⚠ Unexpected Error")
                st.write(str(e))


# =========================================================
# 📂 TAB 2 — MULTI QUERY FILE VALIDATOR
# =========================================================
with tab2:

    st.subheader("Upload SQL File (Multiple Queries)")

    uploaded_file = st.file_uploader("Upload SQL File", type=["sql", "txt"])

    if uploaded_file:

        content = uploaded_file.read().decode("utf-8")

        raw_queries = content.split(";")
        queries = [q.strip() + ";" for q in raw_queries if q.strip()]

        st.success(f"Loaded {len(queries)} queries from file.")

        # Just for listing the queries into the file
        st.markdown("### 📄 Queries Found in File")
        for idx, q in enumerate(queries, start=1):
            st.markdown(f"**Query {idx}:**")
            st.code(q, language="sql")

        validate_all = st.button("Validate All Queries")

        if validate_all:

            lexer = Lexer()
            validator = Validator()

            success_count = 0
            fail_count = 0
            output_report = ""

            st.markdown("---")
            st.markdown("## 🔍 Validation Results")

            #Actual validating the queries one by one
            for index, query in enumerate(queries, start=1):

                st.markdown(f"### Query {index}")
                st.code(query, language="sql")

                output_report += f"\n============================\n"
                output_report += f"Query {index}:\n{query}\n"

                try:
                    tokens = lexer.tokenize(query)
                    parser = Parser(tokens)
                    ast = parser.parse()

                    result = validator.validate(ast)

                    if result["success"]:
                        st.success("✅ SUCCESS")
                        success_count += 1
                        output_report += "Result: SUCCESS\n"

                    else:
                        st.error("❌ FAILED")
                        fail_count += 1
                        output_report += "Result: FAILED\n"

                        for error in result["errors"]:
                            error_text = (
                                f"Error ID: {error.id}\n"
                                f"Type: {error.type}\n"
                                f"Message: {error.message}\n"
                            )

                            st.text(error_text)
                            output_report += error_text + "\n"

                except SyntaxError as e:
                    st.error("❌ Syntax Error")
                    st.text(str(e))
                    fail_count += 1
                    output_report += f"Syntax Error: {str(e)}\n"

                except Exception as e:
                    st.error("⚠ Unexpected Error")
                    st.text(str(e))
                    fail_count += 1
                    output_report += f"Unexpected Error: {str(e)}\n"

                st.markdown("---")

            # ✅ Summary
            st.subheader("📊 Validation Summary")
            st.write(f"✅ Successful Queries: {success_count}")
            st.write(f"❌ Failed Queries: {fail_count}")

            # ✅ Download report
            st.download_button(
                label="📥 Download Validation Report",
                data=output_report,
                file_name="sql_validation_report.txt",
                mime="text/plain"
            )
