import os
from collections import Counter
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, accuracy_score, confusion_matrix
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import numpy as np


PLOTS_DIR = "static/plots"


def ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)


def compute_dashboard_stats(students):
    total_students = len(students)

    if total_students == 0:
        return {
            "total_students": 0,
            "average_age": 0,
            "average_study_hours": 0,
            "average_final_grade": 0,
            "admitted_count": 0,
            "failed_count": 0
        }

    total_age = 0
    total_study_hours = 0
    total_final_grade = 0
    admitted_count = 0
    failed_count = 0

    for student in students:
        total_age += student["age"]
        total_study_hours += student["study_hours"]
        total_final_grade += student["final_grade"]

        if student["admission_status"].lower() == "admitted":
            admitted_count += 1
        elif student["admission_status"].lower() == "failed":
            failed_count += 1

    return {
        "total_students": total_students,
        "average_age": round(total_age / total_students, 2),
        "average_study_hours": round(total_study_hours / total_students, 2),
        "average_final_grade": round(total_final_grade / total_students, 2),
        "admitted_count": admitted_count,
        "failed_count": failed_count
    }


def generate_dashboard_charts(students):
    ensure_plots_dir()

    if not students:
        return {}

    genders = [student["gender"] for student in students]
    admission_statuses = [student["admission_status"] for student in students]
    final_grades = [student["final_grade"] for student in students]
    study_hours = [student["study_hours"] for student in students]

    gender_counts = Counter(genders)
    admission_counts = Counter(admission_statuses)

    charts = {}

    plt.figure(figsize=(6, 4))
    plt.bar(admission_counts.keys(), admission_counts.values())
    plt.title("Admission Status Distribution")
    plt.xlabel("Status")
    plt.ylabel("Count")
    admission_chart = os.path.join(PLOTS_DIR, "admission_status_chart.png")
    plt.tight_layout()
    plt.savefig(admission_chart)
    plt.close()
    charts["admission_status_chart"] = "plots/admission_status_chart.png"

    plt.figure(figsize=(6, 4))
    plt.bar(gender_counts.keys(), gender_counts.values())
    plt.title("Gender Distribution")
    plt.xlabel("Gender")
    plt.ylabel("Count")
    gender_chart = os.path.join(PLOTS_DIR, "gender_chart.png")
    plt.tight_layout()
    plt.savefig(gender_chart)
    plt.close()
    charts["gender_chart"] = "plots/gender_chart.png"

    plt.figure(figsize=(6, 4))
    plt.hist(final_grades, bins=8)
    plt.title("Final Grade Distribution")
    plt.xlabel("Final Grade")
    plt.ylabel("Frequency")
    grade_histogram = os.path.join(PLOTS_DIR, "final_grade_histogram.png")
    plt.tight_layout()
    plt.savefig(grade_histogram)
    plt.close()
    charts["final_grade_histogram"] = "plots/final_grade_histogram.png"

    plt.figure(figsize=(6, 4))
    plt.scatter(study_hours, final_grades)
    plt.title("Study Hours vs Final Grade")
    plt.xlabel("Study Hours")
    plt.ylabel("Final Grade")
    scatter_chart = os.path.join(PLOTS_DIR, "study_hours_vs_final_grade.png")
    plt.tight_layout()
    plt.savefig(scatter_chart)
    plt.close()
    charts["study_hours_vs_final_grade"] = "plots/study_hours_vs_final_grade.png"

    return charts


def simple_linear_regression_analysis(students):
    ensure_plots_dir()

    if len(students) < 2:
        return {
            "available": False,
            "message": "At least 2 student records are required for simple linear regression."
        }

    x = np.array([student["study_hours"] for student in students]).reshape(-1, 1)
    y = np.array([student["final_grade"] for student in students])

    model = LinearRegression()
    model.fit(x, y)
    predictions = model.predict(x)

    coefficient = float(model.coef_[0])
    intercept = float(model.intercept_)
    r2 = float(r2_score(y, predictions))

    x_sorted = np.sort(x.flatten())
    y_line = model.predict(x_sorted.reshape(-1, 1))

    plt.figure(figsize=(7, 4.5))
    plt.scatter(x, y, label="Observed data")
    plt.plot(x_sorted, y_line, label="Regression line")
    plt.title("Simple Linear Regression: Study Hours vs Final Grade")
    plt.xlabel("Study Hours")
    plt.ylabel("Final Grade")
    plt.legend()
    plt.tight_layout()

    chart_path = os.path.join(PLOTS_DIR, "simple_linear_regression.png")
    plt.savefig(chart_path)
    plt.close()

    equation = f"Final Grade = {coefficient:.2f} × Study Hours + {intercept:.2f}"

    return {
        "available": True,
        "coefficient": round(coefficient, 4),
        "intercept": round(intercept, 4),
        "r2_score": round(r2, 4),
        "equation": equation,
        "chart": "plots/simple_linear_regression.png"
    }


def multiple_linear_regression_analysis(students):
    if len(students) < 2:
        return {
            "available": False,
            "message": "At least 2 student records are required for multiple linear regression."
        }

    x = np.array([
        [
            student["study_hours"],
            student["attendance_rate"],
            student["ca_grade"],
            student["sleep_hours"]
        ]
        for student in students
    ])

    y = np.array([student["final_grade"] for student in students])

    model = LinearRegression()
    model.fit(x, y)
    predictions = model.predict(x)

    coefficients = model.coef_
    intercept = float(model.intercept_)
    r2 = float(r2_score(y, predictions))

    coefficient_details = {
        "study_hours": round(float(coefficients[0]), 4),
        "attendance_rate": round(float(coefficients[1]), 4),
        "ca_grade": round(float(coefficients[2]), 4),
        "sleep_hours": round(float(coefficients[3]), 4),
    }

    equation = (
        f"Final Grade = "
        f"{coefficient_details['study_hours']:.2f} × Study Hours + "
        f"{coefficient_details['attendance_rate']:.2f} × Attendance Rate + "
        f"{coefficient_details['ca_grade']:.2f} × CA Grade + "
        f"{coefficient_details['sleep_hours']:.2f} × Sleep Hours + "
        f"{intercept:.2f}"
    )

    return {
        "available": True,
        "coefficients": coefficient_details,
        "intercept": round(intercept, 4),
        "r2_score": round(r2, 4),
        "equation": equation
    }


def pca_analysis(students):
    ensure_plots_dir()

    if len(students) < 2:
        return {
            "available": False,
            "message": "At least 2 student records are required for PCA."
        }

    data = np.array([
        [
            student["age"],
            student["study_hours"],
            student["attendance_rate"],
            student["ca_grade"],
            student["sleep_hours"],
            student["final_grade"]
        ]
        for student in students
    ])

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_data)

    explained_variance = pca.explained_variance_ratio_

    plt.figure(figsize=(7, 4.5))
    plt.scatter(principal_components[:, 0], principal_components[:, 1])
    plt.title("PCA Projection of Student Data")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.tight_layout()

    chart_path = os.path.join(PLOTS_DIR, "pca_projection.png")
    plt.savefig(chart_path)
    plt.close()

    return {
        "available": True,
        "pc1_variance": round(float(explained_variance[0]), 4),
        "pc2_variance": round(float(explained_variance[1]), 4),
        "total_variance": round(float(explained_variance[0] + explained_variance[1]), 4),
        "chart": "plots/pca_projection.png"
    }


def supervised_classification_analysis(students):
    ensure_plots_dir()

    if len(students) < 6:
        return {
            "available": False,
            "message": "At least 6 student records are recommended for supervised classification."
        }

    x = np.array([
        [
            student["age"],
            student["study_hours"],
            student["attendance_rate"],
            student["ca_grade"],
            student["sleep_hours"]
        ]
        for student in students
    ])

    labels = [student["admission_status"] for student in students]

    if len(set(labels)) < 2:
        return {
            "available": False,
            "message": "Supervised classification requires at least two classes: for example Admitted and Failed."
        }

    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_scaled, y_train)

    predictions = model.predict(x_test_scaled)

    accuracy = accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(5, 4))
    plt.imshow(cm, interpolation="nearest")
    plt.title("Confusion Matrix - Supervised Classification")
    plt.colorbar()

    tick_marks = np.arange(len(encoder.classes_))
    plt.xticks(tick_marks, encoder.classes_)
    plt.yticks(tick_marks, encoder.classes_)
    plt.xlabel("Predicted label")
    plt.ylabel("True label")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center")

    plt.tight_layout()
    chart_path = os.path.join(PLOTS_DIR, "supervised_confusion_matrix.png")
    plt.savefig(chart_path)
    plt.close()

    return {
        "available": True,
        "accuracy": round(float(accuracy), 4),
        "classes": list(encoder.classes_),
        "confusion_matrix": cm.tolist(),
        "chart": "plots/supervised_confusion_matrix.png"
    }


def unsupervised_classification_analysis(students):
    ensure_plots_dir()

    if len(students) < 3:
        return {
            "available": False,
            "message": "At least 3 student records are required for unsupervised classification."
        }

    data = np.array([
        [
            student["study_hours"],
            student["attendance_rate"],
            student["ca_grade"],
            student["sleep_hours"],
            student["final_grade"]
        ]
        for student in students
    ])

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    n_clusters = min(3, len(students))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(scaled_data)

    pca = PCA(n_components=2)
    projected_data = pca.fit_transform(scaled_data)

    plt.figure(figsize=(7, 4.5))
    plt.scatter(projected_data[:, 0], projected_data[:, 1], c=cluster_labels)
    plt.title("K-Means Clustering of Student Profiles")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.tight_layout()

    chart_path = os.path.join(PLOTS_DIR, "unsupervised_clustering.png")
    plt.savefig(chart_path)
    plt.close()

    cluster_counts = Counter(cluster_labels)

    readable_cluster_counts = {
        f"Cluster {cluster_id}": count
        for cluster_id, count in sorted(cluster_counts.items())
    }

    return {
        "available": True,
        "n_clusters": n_clusters,
        "cluster_counts": readable_cluster_counts,
        "chart": "plots/unsupervised_clustering.png"
    }