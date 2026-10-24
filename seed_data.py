from database import load_chain_from_db, save_entire_chain
from qr_generator import generate_product_qr

def seed_sample_data():
    blockchain = load_chain_from_db()

    # Sample Product 1: Apple iPhone 15 Pro Max
    p1_id = "PROD-AAPL-98210"
    if not blockchain.find_product_registration(p1_id):
        blockchain.add_product(
            product_id=p1_id,
            product_name="iPhone 15 Pro Max 256GB Natural Titanium",
            brand="Apple",
            manufacturer="Apple Inc., Cupertino, CA",
            batch_no="BATCH-AAPL-2026-09",
            mfg_date="2026-01-15",
            exp_date="N/A (Electronics)",
            extra_info={"spec": "Serial: F2LND710Q16X", "warranty": "1 Year Official AppleCare"}
        )
        blockchain.add_checkpoint(
            product_id=p1_id,
            event_type="QUALITY_INSPECTION_PASSED",
            actor="Foxconn QC Labs, Shenzhen",
            location="Shenzhen Assembly Hub",
            notes="Passed automated 52-point quality and cryptographic key enrollment."
        )
        blockchain.add_checkpoint(
            product_id=p1_id,
            event_type="IN_TRANSIT_DISTRIBUTION",
            actor="DHL Express International",
            location="Hong Kong Airport Gateway",
            notes="Secure container sealed. Shipped via air cargo to Mumbai Hub."
        )
        blockchain.add_checkpoint(
            product_id=p1_id,
            event_type="RECEIVED_AT_RETAIL_STORE",
            actor="Apple Store Bandra Kurla Complex",
            location="Mumbai, India",
            notes="Package received, outer seal verified, stocked on retail shelf."
        )
        generate_product_qr(p1_id, f"http://localhost:5000/verify/{p1_id}")

    # Sample Product 2: Nike Air Jordan
    p2_id = "PROD-NIKE-44301"
    if not blockchain.find_product_registration(p2_id):
        blockchain.add_product(
            product_id=p2_id,
            product_name="Air Jordan 1 Retro High OG 'Chicago'",
            brand="Nike",
            manufacturer="Nike Factory Plant #4, Vietnam",
            batch_no="BATCH-NK-2026-03",
            mfg_date="2026-02-10",
            exp_date="N/A (Footwear)",
            extra_info={"size": "US 10.5", "sku": "DZ5485-612"}
        )
        blockchain.add_checkpoint(
            product_id=p2_id,
            event_type="WAREHOUSE_TRANSFER",
            actor="Nike South Asia Logistics Hub",
            location="Singapore Port Terminal",
            notes="RFID tag paired, pallet stored in climate-controlled zone."
        )
        blockchain.add_checkpoint(
            product_id=p2_id,
            event_type="DELIVERED_TO_OFFICIAL_OUTLET",
            actor="Nike SuperStore DLF Mall",
            location="New Delhi, India",
            notes="Stock verified and placed on showcase rack."
        )
        generate_product_qr(p2_id, f"http://localhost:5000/verify/{p2_id}")

    # Sample Product 3: Pharmaceutical Medicine
    p3_id = "PROD-MED-77124"
    if not blockchain.find_product_registration(p3_id):
        blockchain.add_product(
            product_id=p3_id,
            product_name="Augmentin 625 Duo (Amoxicillin & Clavulanate)",
            brand="GSK Pharmaceuticals",
            manufacturer="GlaxoSmithKline Pharma Unit II, Nashik",
            batch_no="BATCH-MED-88902",
            mfg_date="2026-03-01",
            exp_date="2028-02-28",
            extra_info={"storage": "Store below 25°C", "dosage": "Oral Tablet 10s"}
        )
        blockchain.add_checkpoint(
            product_id=p3_id,
            event_type="COLD_CHAIN_MONITORING",
            actor="Apex Cold Chain Logistics",
            location="Indore Transit Facility",
            notes="Temperature logged at 4.2°C throughout transit. Zero variance."
        )
        generate_product_qr(p3_id, f"http://localhost:5000/verify/{p3_id}")

    save_entire_chain(blockchain)
    print("Database seeded with sample genuine products and blockchain checkpoints.")

if __name__ == "__main__":
    seed_sample_data()
