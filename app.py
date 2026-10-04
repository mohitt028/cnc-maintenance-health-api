from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    # Read input values
    machine_id = data.get("machine_id", "")
    temperature = float(data["temperature"])
    vibration = float(data["vibration"])
    operating_hours = float(data["operating_hours"])
    failure_count = int(data["failure_count"])
    maintenance_status = data["maintenance_status"]

    # -------------------------------------------------
    # 1. TEMPERATURE SCORE
    # -------------------------------------------------

    if temperature <= 70:
        temperature_score = 20
    elif temperature <= 85:
        temperature_score = 16
    elif temperature <= 95:
        temperature_score = 8
    else:
        temperature_score = 0

    # -------------------------------------------------
    # 2. VIBRATION SCORE
    # -------------------------------------------------

    if vibration <= 3:
        vibration_score = 20
    elif vibration <= 5:
        vibration_score = 15
    elif vibration <= 7:
        vibration_score = 8
    else:
        vibration_score = 0

    # -------------------------------------------------
    # 3. OPERATING HOURS SCORE
    # -------------------------------------------------

    if operating_hours <= 1000:
        operating_hours_score = 20
    elif operating_hours <= 2000:
        operating_hours_score = 16
    elif operating_hours <= 3000:
        operating_hours_score = 10
    else:
        operating_hours_score = 5

    # -------------------------------------------------
    # 4. FAILURE HISTORY SCORE
    # -------------------------------------------------

    if failure_count == 0:
        failure_score = 20
    elif failure_count <= 2:
        failure_score = 15
    elif failure_count <= 4:
        failure_score = 10
    else:
        failure_score = 5

    # -------------------------------------------------
    # 5. MAINTENANCE STATUS SCORE
    # -------------------------------------------------

    if maintenance_status == "Completed":
        maintenance_score = 20
    elif maintenance_status == "Due Soon":
        maintenance_score = 12
    else:
        maintenance_score = 0

    # -------------------------------------------------
    # 6. FINAL HEALTH SCORE
    # -------------------------------------------------

    health_score = (
        temperature_score
        + vibration_score
        + operating_hours_score
        + failure_score
        + maintenance_score
    )

    # -------------------------------------------------
    # 7. MACHINE CLASSIFICATION
    # -------------------------------------------------

    if health_score >= 80:
        status = "NORMAL"
    elif health_score >= 50:
        status = "ATTENTION REQUIRED"
    else:
        status = "CRITICAL"

    # -------------------------------------------------
    # 8. PRIORITY
    # -------------------------------------------------

    if status == "CRITICAL":
        priority = "P1 - HIGH"
    elif status == "ATTENTION REQUIRED":
        priority = "P2 - MEDIUM"
    else:
        priority = "P3 - LOW"

    # -------------------------------------------------
    # 9. DETECTED ISSUES
    # -------------------------------------------------

    detected_issue = ""

    if temperature > 85:
        detected_issue += "High temperature; "

    if vibration > 5:
        detected_issue += "Abnormal vibration; "

    if operating_hours > 3000:
        detected_issue += "High operating hours; "

    if failure_count >= 3:
        detected_issue += "High failure history; "

    if maintenance_status == "Overdue":
        detected_issue += "Maintenance overdue"

    # If no issue was detected
    if detected_issue == "":
        detected_issue = "No significant issue detected"

    # -------------------------------------------------
    # 10. RECOMMENDED ACTION
    # -------------------------------------------------

    if status == "CRITICAL":

        recommended_action = (
            "Immediate maintenance inspection; "
            "inspect bearing, lubrication, vibration source, "
            "and cooling system."
        )

    elif status == "ATTENTION REQUIRED":

        recommended_action = (
            "Schedule preventive maintenance inspection; "
            "check vibration, temperature, and lubrication."
        )

    else:

        recommended_action = (
            "Continue normal operation; "
            "monitor machine during scheduled maintenance."
        )

    # -------------------------------------------------
    # 11. RETURN RESULT
    # -------------------------------------------------

    return jsonify({
        "machine_id": machine_id,
        "health_score": health_score,
        "status": status,
        "priority": priority,
        "detected_issue": detected_issue,
        "recommended_action": recommended_action
    })


# -------------------------------------------------
# START SERVER
# -------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
