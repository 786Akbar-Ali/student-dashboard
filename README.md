# 🎓 Student Exam Score Dashboard

An interactive dashboard analyzing student performance data.

## 📁 Project Structure
```
student_dashboard/
├── app.py                        # Streamlit web dashboard (PyCharm)
├── Student_Dashboard.ipynb       # Jupyter notebook dashboard
├── 17_student_exam_scores.csv    # Dataset (200 students)
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/student-dashboard.git
cd student-dashboard
pip install -r requirements.txt
```

### 2. Run Streamlit App (PyCharm)
```bash
streamlit run app.py
```
Opens at: `http://localhost:8501`

### 3. Run Jupyter Notebook
```bash
jupyter notebook Student_Dashboard.ipynb
```

## 📊 Dashboard Features
- **9 interactive charts**: Grade distribution, Study hours, Pass/Fail rate, Attendance, Correlation heatmap, Sleep quality, Improvement gap, Scatter plot, Top 10 students
- **Sidebar filters**: Study category, Sleep quality, Score range, Pass/Fail toggle
- **KPI cards**: Total students, Avg score, Pass rate, Avg study hours, Top student
- **Download**: Export filtered data as CSV

## 🌐 Deploy on Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file**: `app.py`
5. Click **Deploy** ✅

## 📌 Dataset Columns
| Column | Description |
|--------|-------------|
| student_id | Unique student identifier |
| hours_studied | Daily study hours |
| sleep_hours | Daily sleep hours |
| attendance_percent | Class attendance % |
| previous_scores | Score from previous exam |
| exam_score | Current exam score (target) |

## 🛠️ Tech Stack
- **Python** 3.10+
- **Streamlit** — Web dashboard
- **Plotly** — Interactive charts
- **Matplotlib / Seaborn** — Jupyter charts
- **Pandas / NumPy** — Data processing
