# Meal Demand Forecasting, Nutrition and Attendance Analysis Platform

A web-based platform developed as part of a Community Engagement Project (CEP) to support student management, attendance tracking, meal management, nutrition analysis, and meal demand forecasting in educational institutions.

## 📌 Project Overview

Managing student attendance and daily meal requirements can be time-consuming when records are maintained manually or in separate files. This project aims to bring these activities together in one centralized platform.

The system uses student and attendance records along with saved meal information to support record management, nutritional analysis, reporting, and meal planning.

## 🎯 Objectives

- Simplify student record management.
- Record and review student attendance.
- Analyze attendance history and percentages.
- Manage daily meal information.
- Calculate nutritional information based on food items and quantities.
- Estimate meal requirements using saved meal records.
- Generate useful information for planning and reporting.

## ✨ Key Features

### 1. Student Management
Maintain and manage student information through a centralized interface.

### 2. Attendance Management
Record attendance for selected dates and maintain attendance history.

### 3. Student Analytics
Review attendance statistics and student attendance records.

### 4. Meal Management
Manage daily meal records to support organized meal planning.

### 5. Nutrition Analysis
Analyze food items and quantities to estimate nutritional values.

### 6. Meal Demand Forecasting
Use recorded meal information to support estimates of future meal requirements.

### 7. Reports
Provide organized information to support attendance, meal, and nutrition review.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML | Web page structure |
| CSS | Web page styling |
| SQLite | Database management |
| Visual Studio Code | Development environment |

## 🏗️ System Architecture

The platform follows a three-layer architecture:

1. **Presentation Layer:** Provides the user interface using HTML and CSS.
2. **Application Layer:** Uses Python and Flask to process requests and perform application logic.
3. **Data Layer:** Uses SQLite to store and retrieve application records.

**Workflow:** User → Web Interface → Flask Application ↔ SQLite Database → Results and Reports

## 💻 Installation and Setup

### Prerequisites

- Python installed on your computer.
- Visual Studio Code or another code editor.
- A web browser.

### Steps

1. Clone or download this repository to your computer.
2. Open the project folder in Visual Studio Code.
3. Open a terminal in the project directory.
4. Install Flask:

   ```bash
   python -m pip install flask
   ```

5. Ensure the HTML files are inside a folder named `templates`, as expected by Flask's default template loader.
6. Run the application:

   ```bash
   python app.py
   ```

7. Open the local address shown in the terminal in your web browser. For a typical local Flask setup, this may be `http://127.0.0.1:5000/`.

**Note:** Additional dependencies or database initialization steps may be required depending on the application code and database setup.

## 🌍 Sustainable Development Goal

### SDG 2 – Zero Hunger

This project relates to Sustainable Development Goal 2 (Zero Hunger) by supporting better meal planning and estimation of food requirements in educational institutions. Organized meal records and demand estimates can help staff plan food quantities more effectively and identify opportunities to reduce unnecessary food wastage.

The platform is a contribution toward more organized food management; it does not directly eliminate hunger.

## 🧪 Testing

The following areas can be checked during application testing:

- Adding and viewing student records.
- Recording attendance and reviewing attendance history.
- Calculating attendance statistics.
- Saving and reviewing meal records.
- Calculating nutritional estimates.
- Generating meal demand estimates from saved records.

Actual results depend on the application configuration and the tests performed.

## 🚀 Future Enhancements

- Mobile-based attendance integration.
- Improved forecasting methods.
- Enhanced reporting and data visualization.
- Additional nutrition information and analysis.
- Deployment for use by educational institutions.

## 🎓 Project Information

**Project Type:** Community Engagement Project (CEP)  
**Project Title:** Meal Demand Forecasting, Nutrition and Attendance Analysis Platform  
**Domain:** Web Development, Data Management and Analytics  
**Intended Users:** Schools and educational institutions

## 👨‍💻 Contributors

Developed as an academic project by the project team.

---

*This project is intended for educational and demonstration purposes.*
