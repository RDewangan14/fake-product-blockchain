import hashlib
import json
import time
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, hash_val=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash_val if hash_val else self.calculate_hash()

    def calculate_hash(self):
        """Calculates SHA-256 hash of the block contents."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            index=data_dict["index"],
            timestamp=data_dict["timestamp"],
            data=data_dict["data"],
            previous_hash=data_dict["previous_hash"],
            nonce=data_dict.get("nonce", 0),
            hash_val=data_dict.get("hash")
        )


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates the initial block in the blockchain."""
        if not self.chain:
            genesis_data = {
                "event": "GENESIS_BLOCK",
                "product_id": "GENESIS-000",
                "product_name": "Anti-Counterfeit Blockchain Genesis",
                "manufacturer": "SSIPMT Raipur Root Authority",
                "description": "Root of Trust for Anti-Counterfeit Verification Network"
            }
            genesis_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            genesis_block = Block(
                index=0,
                timestamp=genesis_timestamp,
                data=genesis_data,
                previous_hash="0" * 64,
                nonce=0
            )
            self.mine_block(genesis_block)
            self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def mine_block(self, block):
        """Proof of work: finds a hash starting with zeros matching difficulty."""
        target_prefix = "0" * self.difficulty
        while not block.hash.startswith(target_prefix):
            block.nonce += 1
            block.hash = block.calculate_hash()

    def add_product(self, product_id, product_name, brand, manufacturer, batch_no,
                    mfg_date, exp_date, extra_info=None):
        """Adds a new genuine product creation block to the blockchain."""
        # Check if already registered
        if self.find_product_registration(product_id):
            return None, f"Product ID {product_id} is already registered on the blockchain!"

        product_data = {
            "event": "PRODUCT_REGISTRATION",
            "product_id": product_id,
            "product_name": product_name,
            "brand": brand,
            "manufacturer": manufacturer,
            "batch_no": batch_no,
            "mfg_date": mfg_date,
            "exp_date": exp_date,
            "status": "Manufactured - Genuine Origin",
            "current_owner": manufacturer,
            "location": "Manufacturing Plant",
            "extra_info": extra_info or {}
        }

        prev_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data=product_data,
            previous_hash=prev_block.hash
        )
        self.mine_block(new_block)
        self.chain.append(new_block)
        return new_block, "Product successfully registered and mined into blockchain."

    def add_checkpoint(self, product_id, event_type, actor, location, notes=""):
        """Adds a supply-chain tracking block for an existing registered product."""
        # Verify product exists in chain
        reg_block = self.find_product_registration(product_id)
        if not reg_block:
            return None, f"Product ID '{product_id}' does not exist on blockchain. Cannot update lifecycle."

        checkpoint_data = {
            "event": event_type,
            "product_id": product_id,
            "product_name": reg_block.data.get("product_name"),
            "brand": reg_block.data.get("brand"),
            "current_owner": actor,
            "location": location,
            "notes": notes,
            "status": f"Handled by {actor} at {location}"
        }

        prev_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data=checkpoint_data,
            previous_hash=prev_block.hash
        )
        self.mine_block(new_block)
        self.chain.append(new_block)
        return new_block, f"Supply chain checkpoint '{event_type}' recorded on blockchain."

    def find_product_registration(self, product_id):
        """Finds the original registration block for a product ID."""
        for block in self.chain:
            if block.data.get("event") == "PRODUCT_REGISTRATION" and block.data.get("product_id") == product_id:
                return block
        return None

    def get_product_history(self, product_id):
        """Extracts complete immutable lifecycle trail for a product."""
        history = []
        for block in self.chain:
            if block.data.get("product_id") == product_id:
                history.append(block.to_dict())
        return history

    def verify_chain_integrity(self):
        """Validates all cryptographic hashes and links in the entire blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if block data hash has been tampered with
            if current.hash != current.calculate_hash():
                return False, f"Tampering detected at Block #{current.index}! Data does not match hash.", current.index

            # Check if cryptographic link to previous block is broken
            if current.previous_hash != previous.hash:
                return False, f"Broken chain link at Block #{current.index}! Previous hash mismatch.", current.index

            # Check Proof of Work requirement
            if not current.hash.startswith("0" * self.difficulty):
                return False, f"Proof of Work invalid at Block #{current.index}!", current.index

        return True, "Blockchain is fully secure, valid, and immutable.", None

    def verify_product(self, product_id):
        """Verifies if a product is Genuine, Counterfeit, or Tampered."""
        # 1. First, check whole blockchain integrity
        chain_valid, chain_msg, bad_block_idx = self.verify_chain_integrity()
        
        # 2. Check if product exists in blockchain
        reg_block = self.find_product_registration(product_id)
        if not reg_block:
            return {
                "status": "COUNTERFEIT",
                "is_genuine": False,
                "message": f"ALERT: Product ID '{product_id}' was NOT found on the official Blockchain registry. High counterfeit risk!",
                "product": None,
                "history": [],
                "tampered_block": None
            }

        # 3. If chain is invalid and this product's block is affected
        product_history = self.get_product_history(product_id)
        affected_by_tamper = False
        if not chain_valid:
            for b in product_history:
                if b["index"] == bad_block_idx:
                    affected_by_tamper = True
                    break

        if not chain_valid:
            return {
                "status": "TAMPERED / FAKE",
                "is_genuine": False,
                "message": f"CRITICAL WARNING: Blockchain integrity check failed ({chain_msg}). This product records may have been illegally altered!",
                "product": reg_block.data,
                "history": product_history,
                "tampered_block": bad_block_idx
            }

        # 4. If all checks pass, it's 100% Genuine!
        latest_event = product_history[-1]["data"] if product_history else reg_block.data
        return {
            "status": "GENUINE",
            "is_genuine": True,
            "message": "VERIFIED ORIGINAL: Product is authentic, cryptographically certified, and secured on the Blockchain.",
            "product": reg_block.data,
            "current_owner": latest_event.get("current_owner", reg_block.data.get("manufacturer")),
            "current_location": latest_event.get("location", "Manufacturer"),
            "current_status": latest_event.get("status", "Active"),
            "history": product_history,
            "block_index": reg_block.index,
            "block_hash": reg_block.hash
        }

    def simulate_tamper_block(self, block_index, new_product_name=None, new_brand=None):
        """Simulates an adversarial attack on a block to demonstrate detection."""
        if 0 < block_index < len(self.chain):
            block = self.chain[block_index]
            if "product_name" in block.data and new_product_name:
                block.data["product_name"] = new_product_name
            elif "brand" in block.data and new_brand:
                block.data["brand"] = new_brand
            else:
                block.data["tampered_flag"] = "MALICIOUSLY_ALTERED_BY_ATTACKER"
            # Note: We deliberately do NOT re-mine or update block.hash, simulating a hacker editing a record in a database!
            return True, f"Block #{block_index} data has been artificially modified without updating hash."
        return False, "Invalid block index."

    def repair_chain(self):
        """Re-computes and re-mines chain to demonstrate integrity restoration."""
        for i in range(1, len(self.chain)):
            self.chain[i].previous_hash = self.chain[i - 1].hash
            self.chain[i].nonce = 0
            self.chain[i].hash = self.chain[i].calculate_hash()
            self.mine_block(self.chain[i])
        return True, "Chain has been re-synchronized and re-mined."
