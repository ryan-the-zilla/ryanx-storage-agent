"""
RyanX Storage Agent - Real Filecoin Integration
Uses Lighthouse SDK to upload data to IPFS/Filecoin
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any, List


class FilecoinStorage:
    """
    Real Filecoin storage via Lighthouse API.
    
    Get your API key at: https://files.lighthouse.storage
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("LIGHTHOUSE_API_KEY")
        self.base_url = "https://node.lighthouse.storage/api/v0"
        
        if not self.api_key:
            print("[Filecoin] Warning: No API key found. Using local fallback.")
            print("[Filecoin] Get your key at: https://files.lighthouse.storage")
            self.api_key = "demo_mode"
        
        # Local fallback storage
        storage_dir = os.path.expanduser("~/.ryanx/storage")
        os.makedirs(storage_dir, mode=0o700, exist_ok=True)
        self.local_cache = os.path.join(storage_dir, "filecoin_cache.json")
        self.memory_index: List[Dict[str, Any]] = []
        self._load_cache()
    
    def upload(self, data: Dict[str, Any]) -> str:
        """
        Upload data to Filecoin via Lighthouse.
        
        Args:
            data: Data to store
            
        Returns:
            CID (Content Identifier)
        """
        # Add metadata
        upload_data = {
            **data,
            "uploaded_at": datetime.utcnow().isoformat() + "Z",
            "agent": "RyanX"
        }
        
        if self.api_key == "demo_mode":
            # Fallback to local storage
            return self._local_upload(upload_data)
        
        try:
            # Upload to Lighthouse
            response = requests.post(
                f"{self.base_url}/add/content",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=upload_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                cid = result.get("data", {}).get("cid")
                
                if cid:
                    print(f"[Filecoin] ✅ Uploaded to IPFS: {cid}")
                    print(f"[Filecoin] Gateway: https://gateway.lighthouse.storage/ipfs/{cid}")
                    
                    # Cache locally for faster retrieval
                    self._cache_upload(cid, upload_data)
                    return cid
                else:
                    print(f"[Filecoin] ⚠️ Upload succeeded but no CID returned")
                    return self._local_upload(upload_data)
            else:
                print(f"[Filecoin] ❌ Upload failed: {response.status_code}")
                print(f"[Filecoin] Response: {response.text}")
                return self._local_upload(upload_data)
                
        except requests.exceptions.RequestException as e:
            print(f"[Filecoin] ❌ Network error: {e}")
            return self._local_upload(upload_data)
    
    def retrieve(self, cid: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from Filecoin by CID.
        
        Args:
            cid: Content Identifier
            
        Returns:
            Stored data or None
        """
        # Check local cache first
        cached = self._get_cached(cid)
        if cached:
            print(f"[Filecoin] ✅ Retrieved from cache: {cid}")
            return cached
        
        if self.api_key == "demo_mode":
            return None
        
        try:
            # Try Lighthouse gateway
            gateway_url = f"https://gateway.lighthouse.storage/ipfs/{cid}"
            response = requests.get(gateway_url, timeout=30)
            
            if response.status_code == 200:
                print(f"[Filecoin] ✅ Retrieved from IPFS: {cid}")
                return response.json()
            else:
                print(f"[Filecoin] ⚠️ Could not retrieve {cid}: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[Filecoin] ❌ Retrieval error: {e}")
            return None
    
    def retrieve_all(self) -> List[Dict[str, Any]]:
        """Retrieve all stored memories from local cache."""
        return [entry["data"] for entry in self.memory_index]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        types = {}
        for entry in self.memory_index:
            t = entry["data"].get("type", "unknown")
            types[t] = types.get(t, 0) + 1
        
        cids = [entry["cid"] for entry in self.memory_index if entry["cid"].startswith("baf")]
        
        return {
            "total_memories": len(self.memory_index),
            "filecoin_uploads": len(cids),
            "local_only": len(self.memory_index) - len(cids),
            "by_type": types,
            "oldest": self.memory_index[0]["stored_at"] if self.memory_index else None,
            "newest": self.memory_index[-1]["stored_at"] if self.memory_index else None
        }
    
    def _local_upload(self, data: Dict[str, Any]) -> str:
        """Fallback to local storage when API unavailable."""
        import hashlib
        content = json.dumps(data, sort_keys=True)
        cid = "bafy" + hashlib.sha256(content.encode()).hexdigest()[:50]
        
        entry = {
            "cid": cid,
            "data": data,
            "stored_at": datetime.utcnow().isoformat() + "Z",
            "storage_type": "local_fallback"
        }
        
        self.memory_index.append(entry)
        self._persist_cache()
        
        print(f"[Filecoin] ⚠️ Using local fallback: {cid}")
        return cid
    
    def _cache_upload(self, cid: str, data: Dict[str, Any]):
        """Cache uploaded data locally."""
        entry = {
            "cid": cid,
            "data": data,
            "stored_at": datetime.utcnow().isoformat() + "Z",
            "storage_type": "filecoin"
        }
        self.memory_index.append(entry)
        self._persist_cache()
    
    def _persist_cache(self):
        """Save cache to disk."""
        try:
            with open(self.local_cache, "w") as f:
                json.dump(self.memory_index, f, indent=2)
            os.chmod(self.local_cache, 0o600)
        except (IOError, json.JSONEncodeError) as e:
            print(f"[Filecoin] Warning: Could not save cache: {e}")
    
    def _load_cache(self):
        """Load cache from disk."""
        try:
            if os.path.exists(self.local_cache):
                with open(self.local_cache, "r") as f:
                    self.memory_index = json.load(f)
                print(f"[Filecoin] Loaded {len(self.memory_index)} cached memories")
        except (IOError, json.JSONDecodeError) as e:
            print(f"[Filecoin] Warning: Could not load cache: {e}")
            self.memory_index = []
    
    def _get_cached(self, cid: str) -> Optional[Dict[str, Any]]:
        """Get from local cache."""
        for entry in self.memory_index:
            if entry["cid"] == cid:
                return entry["data"]
        return None


# Demo
if __name__ == "__main__":
    print("="*60)
    print("RyanX Filecoin Storage - Real API Integration")
    print("="*60)
    print()
    
    # Initialize
    storage = FilecoinStorage()
    
    print("[Demo] Uploading memories to Filecoin...")
    print()
    
    # Upload a decision
    cid1 = storage.upload({
        "type": "decision",
        "content": "Participating in Synthesis Hackathon",
        "reasoning": "$100k+ prize pool, good fit for autonomous agent"
    })
    
    # Upload an insight
    cid2 = storage.upload({
        "type": "insight",
        "content": "Filecoin RFS-1 matches autonomous storage use case",
        "category": "strategy"
    })
    
    print()
    print("[Demo] Storage Statistics:")
    stats = storage.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("[Demo] All uploaded CIDs:")
    for entry in storage.memory_index:
        print(f"  {entry['cid'][:30]}... ({entry['data']['type']})")
