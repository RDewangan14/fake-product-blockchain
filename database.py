import sqlite3
import json
import os
from blockchain import Block, Blockchain

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blockchain.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            block_index INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            data TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            nonce INTEGER NOT NULL,
            hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_block_to_db(block):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO blocks (block_index, timestamp, data, previous_hash, nonce, hash)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        block.index,
        block.timestamp,
        json.dumps(block.data),
        block.previous_hash,
        block.nonce,
        block.hash
    ))
    conn.commit()
    conn.close()

def save_entire_chain(blockchain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blocks")
    for block in blockchain.chain:
        cursor.execute("""
            INSERT INTO blocks (block_index, timestamp, data, previous_hash, nonce, hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            block.index,
            block.timestamp,
            json.dumps(block.data),
            block.previous_hash,
            block.nonce,
            block.hash
        ))
    conn.commit()
    conn.close()

def load_chain_from_db():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT block_index, timestamp, data, previous_hash, nonce, hash FROM blocks ORDER BY block_index ASC")
    rows = cursor.fetchall()
    conn.close()

    blockchain = Blockchain()
    if rows:
        blockchain.chain = []
        for row in rows:
            block = Block(
                index=row[0],
                timestamp=row[1],
                data=json.loads(row[2]),
                previous_hash=row[3],
                nonce=row[4],
                hash_val=row[5]
            )
            blockchain.chain.append(block)
    else:
        # Save genesis block into DB
        for block in blockchain.chain:
            save_block_to_db(block)
            
    return blockchain
