from flask import Flask, render_template, request, redirect, url_for, flash
from utils.database import init_db, insert_student, get_all_students
from utils.analytics import (
    compute_dashboard_stats,
    generate_dashboard_charts,
    simple_linear_regression_analysis,
    multiple_linear_regression_analysis,
    pca_analysis,
    supervised_classification_analysis,
    unsupervised_classification_analysis
)

app = Flask(__name__)
app.secret_key = "eduinsight_secret_key"

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/collect", methods=["GET", "POST"])
def collect():
    if request.method == "POST":
        try:
            student_data = {
                "student_code": request.form["student_code"].strip(),
                "age": int(request.form["age"]),
                "gender": request.form["gender"].strip(),
                "department": request.form["department"].strip(),
                "level": request.form["level"].strip(),
                "study_hours": float(request.form["study_hours"]),
                "tutorial_participation": request.form["tutorial_participation"].strip(),
                "attendance_rate": float(request.form["attendance_rate"]),
                "ca_grade": float(request.form["ca_grade"]),
                "sleep_hours": float(request.form["sleep_hours"]),
                "internet_quality": request.form["internet_quality"].strip(),
                "stress_level": request.form["stress_level"].strip(),
                "final_grade": float(request.form["final_grade"]),
                "admission_status": request.form["admission_status"].strip()
            }

            if student_data["student_code"] == "":
                flash("Student code is required.", "error")
                return redirect(url_for("collect"))

            insert_student(student_data)
            flash("Student data saved successfully.", "success")
            return redirect(url_for("collect"))

        except ValueError:
            flash("Please enter valid numeric values in numeric fields.", "error")
            return redirect(url_for("collect"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("collect"))

    return render_template("collect.html")

@app.route("/records")
def records():
    students = get_all_students()
    return render_template("records.html", students=students)

@app.route("/dashboard")
def dashboard():
    students = get_all_students()
    stats = compute_dashboard_stats(students)
    charts = generate_dashboard_charts(students)
    return render_template("dashboard.html", stats=stats, charts=charts)

@app.route("/advanced-analysis")
def advanced_analysis():
    students = get_all_students()
    simple_regression = simple_linear_regression_analysis(students)
    multiple_regression = multiple_linear_regression_analysis(students)
    pca_result = pca_analysis(students)
    supervised_result = supervised_classification_analysis(students)
    unsupervised_result = unsupervised_classification_analysis(students)

    return render_template(
        "advanced_analysis.html",
        simple_regression=simple_regression,
        multiple_regression=multiple_regression,
        pca_result=pca_result,
        supervised_result=supervised_result,
        unsupervised_result=unsupervised_result
    )

if __name__ == "__main__":
    app.run(debug=True)