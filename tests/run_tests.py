import json
import time 
from agents.orchestrator import run_agent

def run_all_tests():
    with open("tests/test_cases.json", "r") as f:
        test_cases = json.load(f)

    results = []

    for test in test_cases:
        print(f"\n🚀 Running Test: {test['name']}")

        try:
            start = time.time()

            output = run_agent(test["input"])

            latency = time.time() - start
            print("Latency:", round(latency, 2), "sec")

            decision = output["strategic_recommendation"]["decision"]
            risk = output["risk_assessment"]["risk_level"]

            print("Decision:", decision)
            print("Risk:", risk)

            # ❌ Invalid logic checks
            if risk == "High" and decision == "INVEST":
                print("⚠️ LOGIC ERROR: High risk but INVEST")

            if risk == "Low" and decision == "AVOID":
                print("⚠️ LOGIC ERROR: Low risk but AVOID")

            results.append({
                "name": test["name"],
                "decision": decision,
                "risk": risk,
                "status": "PASS"
            })

        except Exception as e:
            print("❌ Error:", str(e))
            results.append({
                "name": test["name"],
                "status": "FAIL",
                "error": str(e)
            })

    # 💾 Save results to file
    with open("tests/test_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

if __name__ == "__main__":
    run_all_tests()
