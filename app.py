from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "meal-analytics-secret-key"

DATABASE = "database.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_date TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            menu TEXT NOT NULL,
            planned_meals INTEGER NOT NULL,
            meals_served INTEGER NOT NULL,
            food_wastage INTEGER NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS nutrition_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrition_date TEXT NOT NULL,
            food_item TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            calories REAL NOT NULL,
            protein REAL NOT NULL,
            carbs REAL NOT NULL,
            fat REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# NUTRITION FOOD DATABASE
# =========================================================

FOODS = {
    "Rice": {
        "unit": "g",
        "calories": 130,
        "protein": 2.7,
        "carbs": 28.2,
        "fat": 0.3
    },

    "Chapati": {
        "unit": "g",
        "calories": 297,
        "protein": 11.0,
        "carbs": 46.0,
        "fat": 7.5
    },

    "Dal": {
        "unit": "g",
        "calories": 116,
        "protein": 9.0,
        "carbs": 20.0,
        "fat": 0.4
    },

    "Paneer": {
        "unit": "g",
        "calories": 265,
        "protein": 18.3,
        "carbs": 1.2,
        "fat": 20.8
    },

    "Chicken": {
        "unit": "g",
        "calories": 165,
        "protein": 31.0,
        "carbs": 0,
        "fat": 3.6
    },

    "Egg": {
        "unit": "g",
        "calories": 155,
        "protein": 13.0,
        "carbs": 1.1,
        "fat": 11.0
    },

    "Potato": {
        "unit": "g",
        "calories": 77,
        "protein": 2.0,
        "carbs": 17.0,
        "fat": 0.1
    },

    "Banana": {
        "unit": "g",
        "calories": 89,
        "protein": 1.1,
        "carbs": 22.8,
        "fat": 0.3
    },

    "Apple": {
        "unit": "g",
        "calories": 52,
        "protein": 0.3,
        "carbs": 13.8,
        "fat": 0.2
    },

    "Milk": {
        "unit": "ml",
        "calories": 61,
        "protein": 3.2,
        "carbs": 4.8,
        "fat": 3.3
    },

    "Poha": {
        "unit": "g",
        "calories": 110,
        "protein": 2.5,
        "carbs": 23.0,
        "fat": 0.5
    },

    "Upma": {
        "unit": "g",
        "calories": 150,
        "protein": 3.5,
        "carbs": 25.0,
        "fat": 4.0
    },

    "Sprouts": {
        "unit": "g",
        "calories": 30,
        "protein": 3.0,
        "carbs": 6.0,
        "fat": 0.2
    },

    "Mixed Vegetables": {
        "unit": "g",
        "calories": 65,
        "protein": 2.5,
        "carbs": 12.0,
        "fat": 0.5
    },

    "Curd": {
        "unit": "g",
        "calories": 61,
        "protein": 3.5,
        "carbs": 4.7,
        "fat": 3.3
    }
}


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def index():

    conn = get_db()

    # Total students
    total_students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    # Today's date
    today = date.today().isoformat()

    # Today's meals
    todays_meals = conn.execute(
        """
        SELECT COUNT(*)
        FROM meals
        WHERE meal_date = ?
        """,
        (today,)
    ).fetchone()[0]

    # Students present today
    present_today = conn.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = ?
        AND status = 'Present'
        """,
        (today,)
    ).fetchone()[0]

    # Attendance percentage
    if total_students > 0:
        attendance_percentage = round(
            (present_today / total_students) * 100,
            1
        )
    else:
        attendance_percentage = 0

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        todays_meals=todays_meals,
        present_today=present_today,
        attendance_percentage=attendance_percentage
    )


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

@app.route("/students", methods=["GET", "POST"])
def students():

    conn = get_db()

    if request.method == "POST":

        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        class_name = request.form.get("class_name", "").strip()

        if not roll_no or not name or not class_name:
            flash("Please fill all student details.")

        else:
            conn.execute(
                """
                INSERT INTO students
                (roll_no, name, class_name)
                VALUES (?, ?, ?)
                """,
                (roll_no, name, class_name)
            )

            conn.commit()

            flash("Student added successfully.")

    students_data = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY roll_no
        """
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students_data
    )
@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):

    conn = get_db()

    conn.execute(
        """
        DELETE FROM attendance
        WHERE student_id = ?
        """,
        (student_id,)
    )

    conn.execute(
        """
        DELETE FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    conn.commit()
    conn.close()

    flash("Student deleted successfully.")

    return redirect(url_for("students"))
# =========================================================
# ATTENDANCE
# =========================================================

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    conn = get_db()

    selected_date = request.form.get(
        "attendance_date",
        request.args.get(
            "date",
            date.today().isoformat()
        )
    )

    if request.method == "POST":

        conn.execute("""
            DELETE FROM attendance
            WHERE attendance_date = ?
        """, (selected_date,))

        students_data = conn.execute("""
            SELECT *
            FROM students
            ORDER BY roll_no
        """).fetchall()

        for student in students_data:

            status = request.form.get(
                f"status_{student['id']}",
                "Absent"
            )

            conn.execute("""
                INSERT INTO attendance
                (
                    student_id,
                    attendance_date,
                    status
                )
                VALUES (?, ?, ?)
            """, (
                student["id"],
                selected_date,
                status
            ))

        conn.commit()

        flash("Attendance saved successfully.")

    students_data = conn.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """).fetchall()

    attendance_records = conn.execute("""
        SELECT student_id, status
        FROM attendance
        WHERE attendance_date = ?
    """, (selected_date,)).fetchall()

    status_map = {
        row["student_id"]: row["status"]
        for row in attendance_records
    }

    students_list = []

    for student in students_data:

        student_dict = dict(student)

        student_dict["saved_status"] = status_map.get(
            student["id"],
            "Absent"
        )

        students_list.append(student_dict)

    present_count = conn.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = ?
        AND status = 'Present'
    """, (selected_date,)).fetchone()[0]

    absent_count = conn.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = ?
        AND status = 'Absent'
    """, (selected_date,)).fetchone()[0]

    if not attendance_records:

        present_count = 0
        absent_count = len(students_list)

    conn.close()

    return render_template(
        "attendance.html",
        students=students_list,
        selected_date=selected_date,
        present_count=present_count,
        absent_count=absent_count
    )


# =========================================================
# STUDENT ANALYTICS
# =========================================================

@app.route("/student_analytics")
def student_analytics():

    conn = get_db()

    students_data = conn.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """).fetchall()

    analytics = []

    for student in students_data:

        total_days = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
        """, (student["id"],)).fetchone()[0]

        present_days = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
            AND status = 'Present'
        """, (student["id"],)).fetchone()[0]

        absent_days = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
            AND status = 'Absent'
        """, (student["id"],)).fetchone()[0]

        percentage = (
            round((present_days / total_days) * 100, 1)
            if total_days > 0
            else 0
        )

        analytics.append({
            "id": student["id"],
            "roll_no": student["roll_no"],
            "name": student["name"],
            "class_name": student["class_name"],
            "present_days": present_days,
            "absent_days": absent_days,
            "percentage": percentage
        })

    conn.close()

    return render_template(
        "student_analytics.html",
        analytics=analytics
    )


@app.route("/student_attendance/<int:student_id>")
def student_attendance(student_id):

    conn = get_db()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (student_id,)).fetchone()

    if student is None:

        conn.close()

        return redirect(url_for("student_analytics"))

    records = conn.execute("""
        SELECT attendance_date, status
        FROM attendance
        WHERE student_id = ?
        ORDER BY attendance_date DESC
    """, (student_id,)).fetchall()

    total_days = len(records)

    present_days = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    absent_days = sum(
        1 for record in records
        if record["status"] == "Absent"
    )

    percentage = (
        round((present_days / total_days) * 100, 1)
        if total_days > 0
        else 0
    )

    conn.close()

    return render_template(
        "student_attendance.html",
        student=student,
        records=records,
        total_days=total_days,
        present_days=present_days,
        absent_days=absent_days,
        percentage=percentage
    )


# =========================================================
# MEAL MANAGEMENT
# =========================================================

@app.route("/meal_management", methods=["GET", "POST"])
def meal_management():

    conn = get_db()

    selected_date = request.form.get(
        "meal_date",
        request.args.get(
            "date",
            date.today().isoformat()
        )
    )

    if request.method == "POST":

        meal_date = request.form.get("meal_date")
        meal_type = request.form.get("meal_type")

        # Get ALL selected food items
        food_items = request.form.getlist("food_items")

        # Remove empty values
        food_items = [
            food.strip()
            for food in food_items
            if food.strip()
        ]

        menu = ", ".join(food_items)

        order_meals = int(
            request.form.get("planned_meals", 0)
        )

        meals_served = int(
            request.form.get("meals_served", 0)
        )

        food_wastage = order_meals - meals_served

        if not food_items:

            flash("Please select at least one food item.")

        elif meals_served > order_meals:

            flash(
                "Served meals cannot be greater than ordered meals."
            )

        else:

            conn.execute("""
                INSERT INTO meals
                (
                    meal_date,
                    meal_type,
                    menu,
                    planned_meals,
                    meals_served,
                    food_wastage
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                meal_date,
                meal_type,
                menu,
                order_meals,
                meals_served,
                food_wastage
            ))

            conn.commit()

            flash("Meal added successfully.")

            selected_date = meal_date

    meals = conn.execute("""
        SELECT *
        FROM meals
        WHERE meal_date = ?
        ORDER BY
            CASE meal_type
                WHEN 'Breakfast' THEN 1
                WHEN 'Lunch' THEN 2
                WHEN 'Snacks' THEN 3
                WHEN 'Dinner' THEN 4
                ELSE 5
            END,
            id DESC
    """, (selected_date,)).fetchall()

    conn.close()

    foods = [
        "Rice",
        "Dal",
        "Chapati",
        "Paneer",
        "Chicken",
        "Egg",
        "Potato",
        "Mixed Vegetables",
        "Poha",
        "Upma",
        "Sprouts",
        "Banana",
        "Apple",
        "Milk",
        "Curd"
    ]

    return render_template(
        "meal_management.html",
        meals=meals,
        foods=foods,
        selected_date=selected_date
    )


# =========================================================
# NUTRITION
# =========================================================

@app.route("/nutrition")
def nutrition():

    conn = get_db()

    selected_date = request.args.get(
        "date",
        date.today().isoformat()
    )

    meals = conn.execute("""
        SELECT *
        FROM meals
        WHERE meal_date = ?
        AND meal_type IN ('Breakfast', 'Lunch')
        ORDER BY
            CASE meal_type
                WHEN 'Breakfast' THEN 1
                WHEN 'Lunch' THEN 2
            END,
            id
    """, (selected_date,)).fetchall()

    conn.close()

    # Case-insensitive food database
    food_lookup = {
        food.lower().strip(): values
        for food, values in FOODS.items()
    }

    nutrition_data = []

    total_students = 0
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    for meal in meals:

        # Get every food from the saved meal
        food_items = [
            food.strip()
            for food in meal["menu"].split(",")
            if food.strip()
        ]

        meal_calories = 0
        meal_protein = 0
        meal_carbs = 0
        meal_fat = 0

        valid_foods = []

        for food in food_items:

            nutrition = food_lookup.get(
                food.lower()
            )

            if nutrition:

                valid_foods.append(food)

                meal_calories += nutrition["calories"]
                meal_protein += nutrition["protein"]
                meal_carbs += nutrition["carbs"]
                meal_fat += nutrition["fat"]

        students = meal["meals_served"]

        # Nutrition for all students served
        total_meal_calories = meal_calories * students
        total_meal_protein = meal_protein * students
        total_meal_carbs = meal_carbs * students
        total_meal_fat = meal_fat * students

        nutrition_data.append({

            "date": meal["meal_date"],

            "meal_type": meal["meal_type"],

            "food_items": valid_foods,

            "students": students,

            "calories": round(meal_calories, 1),

            "protein": round(meal_protein, 1),

            "carbs": round(meal_carbs, 1),

            "fat": round(meal_fat, 1),

            "total_calories": round(
                total_meal_calories, 1
            ),

            "total_protein": round(
                total_meal_protein, 1
            ),

            "total_carbs": round(
                total_meal_carbs, 1
            ),

            "total_fat": round(
                total_meal_fat, 1
            )
        })

        total_students += students

        total_calories += total_meal_calories
        total_protein += total_meal_protein
        total_carbs += total_meal_carbs
        total_fat += total_meal_fat

    # Average nutrition per student
    if total_students > 0:

        per_student_calories = round(
            total_calories / total_students,
            1
        )

        per_student_protein = round(
            total_protein / total_students,
            1
        )

        per_student_carbs = round(
            total_carbs / total_students,
            1
        )

        per_student_fat = round(
            total_fat / total_students,
            1
        )

    else:

        per_student_calories = 0
        per_student_protein = 0
        per_student_carbs = 0
        per_student_fat = 0

    return render_template(

        "nutrition.html",

        selected_date=selected_date,

        nutrition_data=nutrition_data,

        total_students=total_students,

        total_calories=round(total_calories, 1),

        total_protein=round(total_protein, 1),

        total_carbs=round(total_carbs, 1),

        total_fat=round(total_fat, 1),

        per_student_calories=per_student_calories,

        per_student_protein=per_student_protein,

        per_student_carbs=per_student_carbs,

        per_student_fat=per_student_fat
    )


# =========================================================
# MEAL FORECASTING
# =========================================================

@app.route("/meal_forecasting")
def meal_forecasting():

    conn = get_db()

    # Get attendance date-wise
    attendance_data = conn.execute("""
        SELECT
            attendance_date,
            COUNT(*) AS total_students,
            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ) AS students_present
        FROM attendance
        GROUP BY attendance_date
        ORDER BY attendance_date DESC
    """).fetchall()

    conn.close()

    history = []

    total_present = 0
    total_days = 0

    for row in attendance_data:

        present = row["students_present"] or 0

        history.append({
            "date": row["attendance_date"],
            "students_present": present,
            "meal_demand": present
        })

        total_present += present
        total_days += 1

    # Average attendance
    if total_days > 0:
        average_demand = round(
            total_present / total_days
        )
    else:
        average_demand = 0

    # Next 7 days forecast
    from datetime import timedelta

    today = date.today()

    forecast = []

    for i in range(1, 8):

        forecast_date = today + timedelta(days=i)

        forecast.append({
            "date": forecast_date.isoformat(),
            "predicted_students": average_demand,
            "meal_demand": average_demand
        })

    return render_template(
        "meal_forecasting.html",
        history=history,
        forecast=forecast,
        average_demand=average_demand,
        total_days=total_days
    )


# =========================================================
# REPORTS
# =========================================================

@app.route("/reports")
def reports():

    conn = get_db()

    # -------------------------
    # STUDENTS
    # -------------------------

    total_students = conn.execute("""
        SELECT COUNT(*)
        FROM students
    """).fetchone()[0]


    # -------------------------
    # LATEST ATTENDANCE
    # -------------------------

    latest_attendance = conn.execute("""
        SELECT MAX(attendance_date)
        FROM attendance
    """).fetchone()[0]

    total_present = 0
    total_absent = 0

    if latest_attendance:

        total_present = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE attendance_date = ?
            AND status = 'Present'
        """, (latest_attendance,)).fetchone()[0]

        total_absent = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE attendance_date = ?
            AND status = 'Absent'
        """, (latest_attendance,)).fetchone()[0]


    # -------------------------
    # ATTENDANCE PERCENTAGE
    # -------------------------

    total_marked = total_present + total_absent

    if total_marked > 0:

        overall_attendance = round(
            (total_present / total_marked) * 100,
            1
        )

    else:

        overall_attendance = 0


    # -------------------------
    # TOTAL ATTENDANCE DAYS
    # -------------------------

    total_attendance_days = conn.execute("""
        SELECT COUNT(DISTINCT attendance_date)
        FROM attendance
    """).fetchone()[0]


    # -------------------------
    # STUDENT REPORTS
    # -------------------------

    student_reports = []

    students_data = conn.execute("""
        SELECT *
        FROM students
        ORDER BY roll_no
    """).fetchall()

    for student in students_data:

        status = "Not Marked"

        if latest_attendance:

            result = conn.execute("""
                SELECT status
                FROM attendance
                WHERE student_id = ?
                AND attendance_date = ?
            """, (
                student["id"],
                latest_attendance
            )).fetchone()

            if result:

                status = result["status"]

        total_days = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
        """, (student["id"],)).fetchone()[0]

        present_days = conn.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id = ?
            AND status = 'Present'
        """, (student["id"],)).fetchone()[0]

        percentage = (
            round(
                (present_days / total_days) * 100,
                1
            )
            if total_days > 0
            else 0
        )

        student_reports.append({
            "roll_no": student["roll_no"],
            "name": student["name"],
            "class_name": student["class_name"],
            "status": status,
            "percentage": percentage
        })


    # -------------------------
    # MEAL REPORT
    # -------------------------

    total_meal_days = conn.execute("""
        SELECT COUNT(DISTINCT meal_date)
        FROM meals
    """).fetchone()[0]

    meal_totals = conn.execute("""
        SELECT
            COALESCE(SUM(planned_meals), 0),
            COALESCE(SUM(meals_served), 0),
            COALESCE(SUM(food_wastage), 0)
        FROM meals
    """).fetchone()

    total_planned = meal_totals[0]
    total_served = meal_totals[1]
    total_wastage = meal_totals[2]


    # -------------------------
    # NUTRITION REPORT
    # -------------------------

    nutrition_days = conn.execute("""
        SELECT COUNT(DISTINCT nutrition_date)
        FROM nutrition_records
    """).fetchone()[0]

    nutrition_totals = conn.execute("""
        SELECT
            COALESCE(SUM(calories), 0),
            COALESCE(SUM(protein), 0),
            COALESCE(SUM(carbs), 0),
            COALESCE(SUM(fat), 0)
        FROM nutrition_records
    """).fetchone()

    total_calories = nutrition_totals[0]
    total_protein = nutrition_totals[1]
    total_carbs = nutrition_totals[2]
    total_fat = nutrition_totals[3]


    # -------------------------
    # RECENT MEALS
    # -------------------------

    recent_meals = conn.execute("""
        SELECT *
        FROM meals
        ORDER BY meal_date DESC, id DESC
        LIMIT 10
    """).fetchall()


    conn.close()


    return render_template(
        "reports.html",
        total_students=total_students,
        latest_attendance=latest_attendance,
        total_attendance_days=total_attendance_days,
        total_present=total_present,
        total_absent=total_absent,
        overall_attendance=overall_attendance,
        total_meal_days=total_meal_days,
        total_planned=total_planned,
        total_served=total_served,
        total_wastage=total_wastage,
        nutrition_days=nutrition_days,
        total_calories=round(total_calories, 2),
        total_protein=round(total_protein, 2),
        total_carbs=round(total_carbs, 2),
        total_fat=round(total_fat, 2),
        student_reports=student_reports,
        recent_meals=recent_meals
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )