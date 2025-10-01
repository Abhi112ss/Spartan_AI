#Used a detailed a explanation of all projects in the code
import streamlit as st
import sqlite3
import os
from datetime import datetime
from google import genai
from google.genai import types
import pandas as pd
from dotenv import load_dotenv


load_dotenv()


# creating a database
def init_database():
    """Initialize SQLite database with tables for all three projects"""
    conn = sqlite3.connect('ai_multitool.db')
    cursor = conn.cursor()

    # Table for Q&A Bot
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for Text Summarizer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT NOT NULL,
            summary TEXT NOT NULL,
            word_count INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for Expense Tracker
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


# Gemini API Integration
def call_gemini_api(prompt, use_search=False):

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: GEMINI_API_KEY not found in environment variables. Please set it in your .env file."

        client = genai.Client(api_key=api_key)
        model = "gemini-flash-lite-latest"

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]

        tools = None
        if use_search:
            tools = [types.Tool(googleSearch=types.GoogleSearch())]

        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            tools=tools,
        )

        response_text = ""
        for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
        ):
            response_text += chunk.text

        return response_text.strip()
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"


# Project 1: AI Q&A Bot
def qa_bot_page():
    st.header("🤖 AI Q&A Bot")
    st.write("Ask me anything! I'll use Gemini AI to answer your questions.")

    # Input section
    question = st.text_area("Enter your question:", height=100, key="qa_question")
    use_search = st.checkbox("Use Google Search for real-time information", value=False)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Get Answer", type="primary"):
            if question.strip():
                with st.spinner("Thinking..."):
                    answer = call_gemini_api(question, use_search=use_search)

                    # Save to database
                    conn = sqlite3.connect('ai_multitool.db')
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO qa_history (question, answer) VALUES (?, ?)",
                        (question, answer)
                    )
                    conn.commit()
                    conn.close()

                    st.success("Answer:")
                    st.write(answer)
            else:
                st.warning("Please enter a question!")

    with col2:
        if st.button("Clear History"):
            conn = sqlite3.connect('ai_multitool.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM qa_history")
            conn.commit()
            conn.close()
            st.success("History cleared!")
            st.rerun()

    # Display history
    st.subheader("📜 Question History")
    conn = sqlite3.connect('ai_multitool.db')
    history = pd.read_sql_query(
        "SELECT question, answer, timestamp FROM qa_history ORDER BY timestamp DESC LIMIT 10",
        conn
    )
    conn.close()

    if not history.empty:
        for idx, row in history.iterrows():
            with st.expander(f"Q: {row['question'][:60]}... ({row['timestamp']})"):
                st.write(f"**Question:** {row['question']}")
                st.write(f"**Answer:** {row['answer']}")
    else:
        st.info("No questions asked yet!")


# Project 2: Text Summarizer
def summarizer_page():
    st.header("📝 Text Summarizer")
    st.write("Paste any article or text, and I'll summarize it in 3 sentences.")

    # Input section
    text_input = st.text_area("Paste your text here:", height=200, key="summarizer_text")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Summarize", type="primary"):
            if text_input.strip():
                word_count = len(text_input.split())

                if word_count < 50:
                    st.warning("Text is too short to summarize. Please paste at least 50 words.")
                else:
                    with st.spinner("Summarizing..."):
                        prompt = f"""Summarize the following text in exactly 3 concise sentences. 
                        Be clear, accurate, and capture the main points:

                        {text_input}"""

                        summary = call_gemini_api(prompt)

                        # Save to database
                        conn = sqlite3.connect('ai_multitool.db')
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO summaries (original_text, summary, word_count) VALUES (?, ?, ?)",
                            (text_input, summary, word_count)
                        )
                        conn.commit()
                        conn.close()

                        st.success("Summary:")
                        st.write(summary)
                        st.info(f"Original: {word_count} words → Summary: {len(summary.split())} words")
            else:
                st.warning("Please paste some text to summarize!")

    with col2:
        if st.button("Clear History"):
            conn = sqlite3.connect('ai_multitool.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM summaries")
            conn.commit()
            conn.close()
            st.success("History cleared!")
            st.rerun()

    # Display history
    st.subheader("📚 Summary History")
    conn = sqlite3.connect('ai_multitool.db')
    summaries = pd.read_sql_query(
        "SELECT original_text, summary, word_count, timestamp FROM summaries ORDER BY timestamp DESC LIMIT 5",
        conn
    )
    conn.close()

    if not summaries.empty:
        for idx, row in summaries.iterrows():
            with st.expander(f"Summary {idx + 1} - {row['word_count']} words ({row['timestamp']})"):
                st.write(f"**Original Text:** {row['original_text'][:200]}...")
                st.write(f"**Summary:** {row['summary']}")
    else:
        st.info("No summaries generated yet!")


# Project 3: Expense Tracker
def expense_tracker_page():
    st.header("💰 Personal Expense Tracker")
    st.write("Track your expenses and get AI-powered insights!")

    # Add expense section
    st.subheader("Add New Expense")
    col1, col2, col3 = st.columns(3)

    with col1:
        category = st.selectbox(
            "Category",
            ["Food", "Rent", "Travel", "Entertainment", "Healthcare", "Utilities", "Shopping", "Other"]
        )

    with col2:
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)

    with col3:
        date = st.date_input("Date", value=datetime.now())

    description = st.text_input("Description (optional)")

    if st.button("Add Expense", type="primary"):
        if amount > 0:
            conn = sqlite3.connect('ai_multitool.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)",
                (category, amount, description, date)
            )
            conn.commit()
            conn.close()
            st.success(f"Added ${amount:.2f} to {category}!")
            st.rerun()
        else:
            st.warning("Please enter a valid amount!")

    # Display expenses
    st.subheader("📊 Expense Summary")

    conn = sqlite3.connect('ai_multitool.db')
    expenses_df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY date DESC",
        conn
    )
    conn.close()

    if not expenses_df.empty:
        # Summary statistics
        col1, col2, col3 = st.columns(3)

        total_spent = expenses_df['amount'].sum()
        avg_expense = expenses_df['amount'].mean()
        num_expenses = len(expenses_df)

        with col1:
            st.metric("Total Spent", f"${total_spent:.2f}")
        with col2:
            st.metric("Average Expense", f"${avg_expense:.2f}")
        with col3:
            st.metric("Number of Expenses", num_expenses)

        # Category breakdown
        st.subheader("Spending by Category")
        category_summary = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        st.bar_chart(category_summary)

        # Recent expenses table
        st.subheader("Recent Expenses")
        display_df = expenses_df[['date', 'category', 'amount', 'description']].head(10)
        st.dataframe(display_df, use_container_width=True)

        # AI Insights
        st.subheader("🤖 AI-Powered Insights")
        if st.button("Get Spending Insights"):
            with st.spinner("Analyzing your spending patterns..."):
                prompt = f"""Analyze these expense data and provide 3-4 actionable insights and recommendations:

                Total spent: ${total_spent:.2f}
                Average expense: ${avg_expense:.2f}
                Number of transactions: {num_expenses}

                Spending by category:
                {category_summary.to_string()}

                Recent expenses:
                {expenses_df.head(10).to_string()}

                Provide practical money-saving tips and spending pattern observations."""

                insights = call_gemini_api(prompt)
                st.write(insights)

        # Clear data button
        if st.button("Clear All Expenses", type="secondary"):
            conn = sqlite3.connect('ai_multitool.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses")
            conn.commit()
            conn.close()
            st.success("All expenses cleared!")
            st.rerun()
    else:
        st.info("No expenses recorded yet. Add your first expense above!")


# Main App
def main():
    st.set_page_config(
        page_title="Spartan AI",
        page_icon="🚀",
        layout="wide"
    )

    # Initialize database
    init_database()

    # Sidebar navigation
    st.sidebar.title("🚀 Spartan AI")
    st.sidebar.write("Built with Streamlit, Gemini AI, and SQLite")

    page = st.sidebar.radio(
        "Choose a tool:",
        ["🤖 Q&A Bot", "📝 Text Summarizer", "💰 Expense Tracker"]
    )

    # API Key status
    api_key_status = "✅ Connected" if os.environ.get("GEMINI_API_KEY") else "❌ Not Set"
    st.sidebar.info(f"Gemini API Status: {api_key_status}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    This app demonstrates:
    - ✨ AI-powered Q&A
    - 📄 Text summarization
    - 💵 Expense tracking

    All data is stored locally in SQLite!
    """)

    # Route to pages
    if page == "🤖 Q&A Bot":
        qa_bot_page()
    elif page == "📝 Text Summarizer":
        summarizer_page()
    elif page == "💰 Expense Tracker":
        expense_tracker_page()


if __name__ == "__main__":
    main()
