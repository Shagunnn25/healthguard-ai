from fastapi import APIRouter

router = APIRouter()

LAB_REFERENCE = {
    "hemoglobin": {"min": 12, "max": 17, "unit": "g/dL"},
    "glucose": {"min": 70, "max": 100, "unit": "mg/dL"}
}


@router.post("/analyze/lab")
def analyze_lab(req: dict):
    name = req.get("test_name", "").lower()
    value = req.get("value", 0)

    if name not in LAB_REFERENCE:
        return {"error": "test not found"}

    ref = LAB_REFERENCE[name]

    if value < ref["min"]:
        status = "low"
    elif value > ref["max"]:
        status = "high"
    else:
        status = "normal"

    return {
        "test": name,
        "value": value,
        "status": status,
        "normal_range": f"{ref['min']} - {ref['max']} {ref['unit']}"
    }