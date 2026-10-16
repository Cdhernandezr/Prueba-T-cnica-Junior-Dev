from contextlib import closing
from pathlib import Path
import sqlite3
from flask import Flask, jsonify, render_template

DB = Path(__file__).resolve().parent / "data" / "orders.sqlite3"
app = Flask(__name__)

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/orders")
def orders():
    try:
        # `with sqlite3.connect()` no cierra la conexión, solo maneja la transacción.
        # closing() garantiza que se cierre al terminar cada petición.
        with closing(connect()) as con:
            return jsonify([dict(row) for row in con.execute("SELECT * FROM orders ORDER BY id")])
    except sqlite3.Error:
        return jsonify(error="No se pudieron cargar los pedidos."), 500

@app.post("/api/orders/<int:order_id>/ship")
def ship(order_id):
    try:
        # closing() cierra la conexión; el segundo `con` hace commit o rollback de la transacción.
        with closing(connect()) as con, con:
            # Regla de negocio: solo un pedido pendiente puede pasar a enviado.
            # La condición va dentro del UPDATE para que validar y actualizar sea una sola
            # operación atómica y evitar condiciones de carrera entre peticiones simultáneas.
            cur = con.execute(
                "UPDATE orders SET status = 'enviado' WHERE id = ? AND status = 'pendiente'",
                (order_id,),
            )
            row = con.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if row is None:
                return jsonify(error="Pedido no encontrado."), 404
            # rowcount == 0: el pedido existe pero no estaba pendiente (cancelado o ya enviado).
            if cur.rowcount == 0:
                return jsonify(
                    error=f"No se puede enviar un pedido en estado «{row['status']}». "
                          "Solo los pedidos pendientes pueden marcarse como enviados."
                ), 409
            return jsonify(dict(row))
    except sqlite3.Error:
        return jsonify(error="No se pudo actualizar el pedido."), 500

if __name__ == "__main__":
    app.run(debug=True)