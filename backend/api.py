from flask import Flask, request, jsonify  
from flask_cors import CORS
from calculations.complex_calc import complex_calc
from calculations.expression_to_lisp import expression_to_lisp  

app = Flask(__name__)
CORS(app)

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.json
    expr = data.get("expression")

    try:
        result = complex_calc(expr)
        return jsonify({"result": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/lisp", methods=["POST"])
def lisp_notation():
    data = request.json
    expr = data.get("expression")

    result = expression_to_lisp(expr)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)

