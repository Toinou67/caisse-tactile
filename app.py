from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import io
from openpyxl import Workbook

app = Flask(__name__)

ventes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html", ventes=ventes)

@app.route("/api/save_sale", methods=["POST"])
def save_sale():
    data = request.get_json()
    vente = {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "caisse": data["caisse"],
        "panier": data["panier"],
        "total": data["total"]
    }
    ventes.append(vente)
    return jsonify({"status": "ok"})

@app.route("/admin/export")
def export_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Ventes"

    # Entêtes
    ws.append(["Date", "Caisse", "Panier", "Total (€)"])

    for v in ventes:
        # Panier en texte lisible, sans crochets ni accolades
        panier_text = "\n".join([f"{item['nom']} - {item['prix']:.2f}€" for item in v["panier"]])
        ws.append([v["date"], v["caisse"], panier_text, v["total"]])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        download_name="ventes.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    app.run(debug=True)
