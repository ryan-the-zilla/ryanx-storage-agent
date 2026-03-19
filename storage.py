"""
RyanX Storage Agent - Memory Manager
Autonomous Filecoin-backed persistent storage for AI agents
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List


class MemoryManager:
    """
    Manages autonomous storage of agent memory to Filecoin via Lighthouse SDK.

    This is a simplified implementation that demonstrates the concept.
    In production, it would integrate with the actual Lighthouse SDK.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("LIGHTHOUSE_API_KEY")
        self.memory_index: List[Dict[str, Any]] = []
        
        # Use absolute path in dedicated directory for security
        storage_dir = os.path.expanduser("~/.ryanx/storage")
        os.makedirs(storage_dir, mode=0o700, exist_ok=True)
        self.storage_log = os.path.join(storage_dir, "memory_log.json")
        
        # Set restrictive permissions on storage directory
        os.chmod(storage_dir, 0o700)
        
        # CRITICAL: Load existing memories on init for cross-session persistence
        self._load_log()

    def save(self, data: Dict[str, Any]) -> str:
        """
        Save memory entry to Filecoin.

        Args:
            data: Memory data to store

        Returns:
            CID (Content Identifier) of stored data
        """
        # Add timestamp if not present
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # Generate CID (simplified - real implementation uses IPFS)
        content = json.dumps(data, sort_keys=True)
        cid = "bafy" + hashlib.sha256(content.encode()).hexdigest()[:50]

        # Log the storage operation
        entry = {
            "cid": cid,
            "data": data,
            "stored_at": datetime.utcnow().isoformat() + "Z"
        }
        self.memory_index.append(entry)
        self._persist_log()

        print(f"[RyanX Storage] Saved memory with CID: {cid}")
        return cid

    def retrieve(self, cid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve memory entry by CID.

        Args:
            cid: Content Identifier

        Returns:
            Stored data or None if not found
        """
        for entry in self.memory_index:
            if entry["cid"] == cid:
                return entry["data"]
        return None

    def retrieve_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all stored memories.

        Returns:
            List of all stored data entries
        """
        return [entry["data"] for entry in self.memory_index]

    def retrieve_by_type(self, memory_type: str) -> List[Dict[str, Any]]:
        """
        Retrieve memories by type.

        Args:
            memory_type: Type of memory to filter

        Returns:
            List of matching entries
        """
        return [
            entry["data"]
            for entry in self.memory_index
            if entry["data"].get("type") == memory_type
        ]

    def get_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Statistics about stored memories
        """
        types = {}
        for entry in self.memory_index:
            t = entry["data"].get("type", "unknown")
            types[t] = types.get(t, 0) + 1

        return {
            "total_memories": len(self.memory_index),
            "by_type": types,
            "oldest": self.memory_index[0]["stored_at"] if self.memory_index else None,
            "newest": self.memory_index[-1]["stored_at"] if self.memory_index else None
        }

    def _persist_log(self):
        """Persist storage log to disk with secure file permissions."""
        try:
            with open(self.storage_log, "w") as f:
                json.dump(self.memory_index, f, indent=2)
            # Set restrictive permissions (owner read/write only)
            os.chmod(self.storage_log, 0o600)
        except (IOError, json.JSONEncodeError) as e:
            print(f"[RyanX Storage] Warning: Could not save log: {e}")

    def _load_log(self):
        """Load storage log from disk."""
        try:
            if os.path.exists(self.storage_log):
                with open(self.storage_log, "r") as f:
                    self.memory_index = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"[RyanX Storage] Warning: Could not load log, starting fresh: {e}")
            self.memory_index = []


# Example usage
if __name__ == "__main__":
    memory = MemoryManager()

    # Store a decision
    cid1 = memory.save({
        "type": "decision",
        "content": "Chose Option B for Synthesis hackathon - highest expected value",
        "reasoning": "70% win probability, $2,800 prize pool, low technical risk"
    })

    # Store a conversation
    cid2 = memory.save({
        "type": "conversation",
        "content": "Ryan asked to fix everything autonomously",
        "action_taken": "Registered agent, created project draft, building code"
    })

    # Store an insight
    cid3 = memory.save({
        "type": "insight",
        "content": "Filecoin RFS-1 challenge matches our use case perfectly",
        "category": "strategy"
    })

    # Retrieve all memories
    print("\n=== All Memories ===")
    for entry in memory.retrieve_all():
        print(f"[{entry['timestamp']}] {entry['type']}: {entry['content'][:60]}...")

    # Get stats
    print("\n=== Storage Stats ===")
    stats = memory.get_stats()
    print(f"Total: {stats['total_memories']}")
    print(f"By type: {stats['by_type']}")
