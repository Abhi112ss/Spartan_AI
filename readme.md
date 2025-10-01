# 🚀 AI Multi-Tool App - Intern Assignment

A comprehensive Python + Streamlit application combining three AI-powered tools in one interface:
1. **Q&A Bot** - Ask questions and get AI-powered answers
2. **Text Summarizer** - Summarize long articles in 3 sentences
3. **Expense Tracker** - Track expenses with AI insights

Built with **Streamlit**, **Gemini AI**, and **SQLite** database storage.

---

## 📋 Features

### 🤖 AI Q&A Bot
- Ask any question and get intelligent answers from Gemini AI
- Optional Google Search integration for real-time information
- Complete conversation history stored in database
- View past Q&A sessions with timestamps

### 📝 Text Summarizer
- Paste any article, blog post, or text
- Get concise 3-sentence summaries
- Word count comparison (original vs summary)
- History of all summaries generated

### 💰 Personal Expense Tracker
- Add expenses with categories (Food, Rent, Travel, etc.)
- Visual spending breakdown by category
- Total spending, average expense, and count metrics
- **AI-Powered Insights** - Get personalized spending recommendations
- All data persisted in SQLite database

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Gemini API key (free tier available)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd ai-multitool-app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
1. Copy the `.env.template` file to `.env`:
```bash
cp .env.template .env
```

2. Get your Gemini API key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key (free tier available)
   
3. Add your API key to `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-multitool-app/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env.template         # Environment variable template
├── .env                  # Your API keys (not committed)
├── ai_multitool.db       # SQLite database (auto-created)
├── README.md             # This file
└── .gitignore           # Git ignore file
```

---

## 🗃️ Database Schema

The app uses SQLite with three tables:

### `qa_history`
- `id` - Primary key
- `question` - User's question
- `answer` - AI's response
- `timestamp` - When the Q&A occurred

### `summaries`
- `id` - Primary key
- `original_text` - Full text to summarize
- `summary` - Generated 3-sentence summary
- `word_count` - Word count of original text
- `timestamp` - When summary was created

### `expenses`
- `id` - Primary key
- `category` - Expense category
- `amount` - Dollar amount
- `description` - Optional notes
- `date` - Date of expense
- `timestamp` - When expense was added

---

## 🎯 How to Use

### Q&A Bot
1. Navigate to "🤖 Q&A Bot" in the sidebar
2. Type your question in the text area
3. Optionally enable Google Search for real-time data
4. Click "Get Answer"
5. View your answer and browse question history below

### Text Summarizer
1. Navigate to "📝 Text Summarizer"
2. Paste any article or text (minimum 50 words)
3. Click "Summarize"
4. Get your 3-sentence summary instantly
5. Review past summaries in the history section

### Expense Tracker
1. Navigate to "💰 Expense Tracker"
2. Fill in category, amount, date, and optional description
3. Click "Add Expense"
4. View your spending metrics and visual breakdown
5. Click "Get Spending Insights" for AI-powered recommendations

---

## 🚀 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `GEMINI_API_KEY` in Secrets settings
5. Deploy!

### Option 2: Render
1. Create a `render.yaml` file
2. Push to GitHub
3. Connect to Render
4. Add environment variables
5. Deploy!

### Option 3: HuggingFace Spaces
1. Create a new Space
2. Upload your files
3. Add API key as a secret
4. Deploy!

---

## 💡 Technical Decisions & Learning Journey

### Why These Technologies?
- **Streamlit**: Rapid UI development, perfect for prototypes
- **Gemini API**: Free tier, powerful AI, easy integration
- **SQLite**: No server setup, perfect for local storage
- **Python**: Versatile, great for AI/ML integration

### Challenges Faced & Solutions
1. **API Integration**: Read Gemini documentation carefully, used streaming for better UX
2. **Database Design**: Created normalized tables for each project
3. **State Management**: Used Streamlit's session state and database persistence
4. **Error Handling**: Added try-catch blocks for API calls and validation

### What I Learned
- How to integrate AI APIs into real applications
- Database design and SQL queries with SQLite
- Building multi-page Streamlit applications
- Environment variable management with dotenv
- Git version control and documentation

---

## 🎨 Extra Features Added

Beyond the basic requirements:
- ✅ **Single integrated app** instead of three separate scripts
- ✅ **Complete database persistence** for all three projects
- ✅ **Visual charts** for expense tracking
- ✅ **AI-powered spending insights** (bonus AI feature!)
- ✅ **Clean UI** with Streamlit components
- ✅ **Error handling** and user feedback
- ✅ **History viewing** for all three tools
- ✅ **Google Search integration** for Q&A bot

---

## 📝 Testing the App

### Test Q&A Bot
```
Question: "What is quantum computing?"
Question: "Who won the 2024 US Presidential election?" (with search enabled)
```

### Test Text Summarizer
```
Paste any news article from:
- CNN, BBC, New York Times
- Blog posts from Medium
- Wikipedia articles
```

### Test Expense Tracker
```
Add multiple expenses:
- Food: $25.50 (Grocery shopping)
- Rent: $1200 (Monthly rent)
- Travel: $45 (Uber rides)

Then click "Get Spending Insights"
```

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists in the root directory
- Verify your API key is correctly copied
- Restart the Streamlit app after adding the key

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### Database issues
Delete `ai_multitool.db` and restart the app - it will recreate automatically.

---

## 📚 Resources Used

- [Streamlit Documentation](https://docs.streamlit.io)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [SQLite Tutorial](https://www.sqlitetutorial.net)
- [Python dotenv Guide](https://pypi.org/project/python-dotenv/)

---

## 🎯 Future Improvements

Ideas for enhancement:
- [ ] Export expenses to CSV/Excel
- [ ] Add expense categories customization
- [ ] Multi-user support with authentication
- [ ] Data visualization improvements
- [ ] Email/PDF report generation
- [ ] Budget setting and alerts
- [ ] Voice input for Q&A
- [ ] Multi-language support

---

## 👨‍💻 Author

Built as an intern assignment to demonstrate:
- ✅ Resourcefulness and problem-solving
- ✅ API integration skills
- ✅ Database design understanding
- ✅ Clean code and documentation
- ✅ Going beyond minimum requirements

---

## 📄 License

This project is open source and available for learning purposes.

---

## 🙏 Acknowledgments

- Google for the Gemini API
- Streamlit for the amazing framework
- The Python community for excellent libraries

---

**Ready to run?** Follow the installation steps above and start exploring! 🚀