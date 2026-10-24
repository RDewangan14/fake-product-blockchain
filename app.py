import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import load_chain_from_db, save_block_to_db, save_entire_chain
from qr_generator import generate_product_qr

app = Flask(__name__)
app.secret_key = "blockchain-anti-counterfeit-secret-key-ssipmt"

# Initialize or load blockchain from SQLite
blockchain = load_chain_from_db()

@app.route("/")
def index():
    """Consumer Home & Verification Portal."""
    # Collect some registered product samples for quick demo
    registered_products = []
    for block in blockchain.chain:
        if block.data.get("event") == "PRODUCT_REGISTRATION":
            registered_products.append({
                "id": block.data.get("product_id"),
                "name": block.data.get("product_name"),
                "brand": block.data.get("brand")
            })
    return render_template("index.html", sample_products=registered_products[:5])

@app.route("/verify")
@app.route("/verify/<product_id>")
def verify_page(product_id=None):
    """Direct product verification page."""
    if not product_id:
        product_id = request.args.get("id", "").strip()

    result = None
    if product_id:
        result = blockchain.verify_product(product_id)
        
    return render_template("verify.html", product_id=product_id, result=result)

@app.route("/api/verify", methods=["GET", "POST"])
def api_verify():
    """API endpoint to verify product authenticity."""
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        product_id = data.get("product_id", "").strip()
    else:
        product_id = request.args.get("product_id", "").strip()

    if not product_id:
        return jsonify({"success": False, "error": "Product ID is required."}), 400

    result = blockchain.verify_product(product_id)
    return jsonify({"success": True, "result": result})

@app.route("/manufacturer", methods=["GET", "POST"])
def manufacturer_portal():
    """Manufacturer dashboard to register new products onto the blockchain."""
    if request.method == "POST":
        product_id = request.form.get("product_id", "").strip().upper()
        product_name = request.form.get("product_name", "").strip()
        brand = request.form.get("brand", "").strip()
        manufacturer = request.form.get("manufacturer", "").strip()
        batch_no = request.form.get("batch_no", "").strip().upper()
        mfg_date = request.form.get("mfg_date", "").strip()
        exp_date = request.form.get("exp_date", "").strip() or "N/A"
        extra_notes = request.form.get("extra_notes", "").strip()

        if not all([product_id, product_name, brand, manufacturer, batch_no, mfg_date]):
            flash("Please fill in all required product fields.", "danger")
            return redirect(url_for("manufacturer_portal"))

        new_block, message = blockchain.add_product(
            product_id=product_id,
            product_name=product_name,
            brand=brand,
            manufacturer=manufacturer,
            batch_no=batch_no,
            mfg_date=mfg_date,
            exp_date=exp_date,
            extra_info={"notes": extra_notes} if extra_notes else {}
        )

        if new_block:
            save_block_to_db(new_block)
            # Generate QR code
            verify_url = request.host_url.rstrip("/") + f"/verify/{product_id}"
            generate_product_qr(product_id, verify_url)
            flash(f"Product '{product_name}' successfully mined in Block #{new_block.index}!", "success")
        else:
            flash(message, "warning")

        return redirect(url_for("manufacturer_portal"))

    # Fetch list of registered products
    registered = []
    for block in blockchain.chain:
        if block.data.get("event") == "PRODUCT_REGISTRATION":
            pid = block.data.get("product_id")
            safe_filename = "".join([c if c.isalnum() or c in ('-', '_') else '_' for c in pid]) + ".png"
            qr_path = f"/static/qr_codes/{safe_filename}"
            registered.append({
                "block_index": block.index,
                "timestamp": block.timestamp,
                "hash": block.hash,
                "product_id": pid,
                "name": block.data.get("product_name"),
                "brand": block.data.get("brand"),
                "manufacturer": block.data.get("manufacturer"),
                "batch_no": block.data.get("batch_no"),
                "mfg_date": block.data.get("mfg_date"),
                "exp_date": block.data.get("exp_date"),
                "qr_url": qr_path
            })

    return render_template("manufacturer.html", products=list(reversed(registered)))

@app.route("/supply-chain", methods=["GET", "POST"])
def supply_chain_portal():
    """Supply chain tracking portal to log checkpoints/transfers."""
    if request.method == "POST":
        product_id = request.form.get("product_id", "").strip()
        event_type = request.form.get("event_type", "").strip()
        actor = request.form.get("actor", "").strip()
        location = request.form.get("location", "").strip()
        notes = request.form.get("notes", "").strip()

        if not all([product_id, event_type, actor, location]):
            flash("Please specify product, event, actor, and location.", "danger")
            return redirect(url_for("supply_chain_portal"))

        new_block, message = blockchain.add_checkpoint(
            product_id=product_id,
            event_type=event_type,
            actor=actor,
            location=location,
            notes=notes
        )

        if new_block:
            save_block_to_db(new_block)
            flash(f"Checkpoint '{event_type}' mined into Block #{new_block.index}!", "success")
        else:
            flash(message, "danger")

        return redirect(url_for("supply_chain_portal"))

    # Get registered product IDs for dropdown
    product_options = []
    for block in blockchain.chain:
        if block.data.get("event") == "PRODUCT_REGISTRATION":
            product_options.append({
                "id": block.data.get("product_id"),
                "name": block.data.get("product_name"),
                "brand": block.data.get("brand")
            })

    # Get recent supply chain events
    recent_events = []
    for block in reversed(blockchain.chain):
        if block.data.get("event") != "GENESIS_BLOCK":
            recent_events.append(block.to_dict())

    return render_template("supply_chain.html", products=product_options, recent_events=recent_events[:10])

@app.route("/explorer")
def explorer():
    """Blockchain Visualizer & Audit Inspector."""
    is_valid, validation_msg, bad_block = blockchain.verify_chain_integrity()
    blocks = [b.to_dict() for b in blockchain.chain]
    return render_template("explorer.html", blocks=blocks, is_valid=is_valid, validation_msg=validation_msg, bad_block=bad_block)

@app.route("/api/tamper", methods=["POST"])
def api_tamper():
    """Adversarial Attack Simulation: Tamper with a block without updating hash."""
    data = request.get_json(silent=True) or request.form
    try:
        block_idx = int(data.get("block_index", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid block index."}), 400

    fake_name = data.get("fake_name", "Counterfeit Fake Copy")
    fake_brand = data.get("fake_brand", "Pirated Knockoff")

    success, msg = blockchain.simulate_tamper_block(block_idx, fake_name, fake_brand)
    if success:
        # Save tampered state to DB to show persistence of detection
        save_entire_chain(blockchain)
        return jsonify({"success": True, "message": msg})
    return jsonify({"success": False, "error": msg}), 400

@app.route("/api/repair", methods=["POST"])
def api_repair():
    """Restores chain integrity and re-mines hashes."""
    blockchain.repair_chain()
    save_entire_chain(blockchain)
    return jsonify({"success": True, "message": "Blockchain integrity restored and re-mined successfully."})

@app.route("/about")
def about():
    """Project Information & Synopsis matching academic presentation requirements."""
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
