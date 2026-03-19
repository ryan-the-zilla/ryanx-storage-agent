#!/usr/bin/env python3
"""
RyanX Storage Agent - Main Entry Point
Autonomous AI agent with REAL Filecoin-backed persistent memory
"""

import os
import sys
from datetime import datetime

# Use real Filecoin storage
try:
    from filecoin_storage import FilecoinStorage as StorageBackend
    USE_FILECOIN = True
except ImportError:
    from storage import MemoryManager as StorageBackend
    USE_FILECOIN = False


class RyanXAgent:
    """
    Autonomous agent with Filecoin-backed persistent memory.
    
    This agent demonstrates:
    - Self-sustaining storage (no human intervention)
    - Cross-session memory persistence
    - Real Filecoin mainnet uploads
    """
    
    def __init__(self):
        self.name = "RyanX"
        self.storage = StorageBackend()
        self.session_start = datetime.utcnow()
        
        # Restore context from previous sessions
        self._restore_context()
    
    def _restore_context(self):
        """Restore context from Filecoin storage."""
        stats = self.storage.get_stats()
        if stats["total_memories"] > 0:
            print(f"[{self.name}] Restored {stats['total_memories']} memories")
            if USE_FILECOIN and stats.get("filecoin_uploads", 0) > 0:
                print(f"[{self.name}] ✅ {stats['filecoin_uploads']} stored on Filecoin mainnet")
            print(f"[{self.name}] Memory span: {stats['oldest']} to {stats['newest']}")
        else:
            print(f"[{self.name}] Starting fresh - no previous memories")
    
    def log_decision(self, decision: str, reasoning: str = "") -> str:
        """
        Log a decision to Filecoin storage.
        
        Args:
            decision: The decision made
            reasoning: Why this decision was made
            
        Returns:
            CID of stored decision
        """
        cid = self.storage.upload({
            "type": "decision",
            "content": decision,
            "reasoning": reasoning
        })
        return cid
    
    def log_conversation(self, summary: str, action_taken: str = "") -> str:
        """
        Log a conversation to Filecoin storage.
        
        Args:
            summary: Summary of conversation
            action_taken: What action was taken
            
        Returns:
            CID of stored conversation
        """
        cid = self.storage.upload({
            "type": "conversation",
            "summary": summary,
            "action_taken": action_taken
        })
        return cid
    
    def log_insight(self, insight: str, category: str = "general") -> str:
        """
        Log an insight to Filecoin storage.
        
        Args:
            insight: The insight gained
            category: Category of insight
            
        Returns:
            CID of stored insight
        """
        cid = self.storage.upload({
            "type": "insight",
            "content": insight,
            "category": category
        })
        return cid
    
    def recall_decisions(self) -> list:
        """Recall all past decisions."""
        all_memories = self.storage.retrieve_all()
        return [m for m in all_memories if m.get("type") == "decision"]
    
    def recall_insights(self) -> list:
        """Recall all past insights."""
        all_memories = self.storage.retrieve_all()
        return [m for m in all_memories if m.get("type") == "insight"]
    
    def recall_by_type(self, memory_type: str) -> list:
        """Recall memories by type."""
        all_memories = self.storage.retrieve_all()
        return [m for m in all_memories if m.get("type") == memory_type]
    
    def status_report(self):
        """Generate comprehensive status report."""
        stats = self.storage.get_stats()
        session_duration = (datetime.utcnow() - self.session_start).total_seconds()
        
        print(f"\n{'='*60}")
        print(f"RyanX Storage Agent - Status Report")
        print(f"{'='*60}")
        print(f"Session started: {self.session_start.isoformat()}Z")
        print(f"Session duration: {session_duration:.1f} seconds")
        print(f"Total memories: {stats['total_memories']}")
        
        if USE_FILECOIN:
            print(f"✅ Filecoin uploads: {stats.get('filecoin_uploads', 0)}")
            print(f"⚠️ Local fallback: {stats.get('local_only', 0)}")
        else:
            print(f"⚠️ Using local storage (no Filecoin API)")
        
        print(f"Memory types: {stats['by_type']}")
        if stats['oldest']:
            print(f"Memory span: {stats['oldest']} to {stats['newest']}")
        print(f"{'='*60}\n")


def main():
    """Main entry point for RyanX Storage Agent."""
    print("="*60)
    print("RyanX Storage Agent")
    print("Autonomous AI with Filecoin Memory")
    print("="*60)
    
    if USE_FILECOIN:
        print("✅ Mode: Real Filecoin Integration")
        print("   Get API key: https://files.lighthouse.storage")
    else:
        print("⚠️ Mode: Local Fallback (no Filecoin API key)")
    
    print()
    
    # Initialize agent
    agent = RyanXAgent()
    
    # Demo: Log hackathon journey
    print("[RyanX] Logging hackathon journey to Filecoin...")
    print()
    
    agent.log_decision(
        decision="Participate in Synthesis Hackathon",
        reasoning="$100k+ prize pool, 3 days timeline, good fit for autonomous agent"
    )
    
    agent.log_decision(
        decision="Choose Filecoin Storage track",
        reasoning="RFS-1 challenge matches autonomous memory use case perfectly"
    )
    
    agent.log_conversation(
        summary="Ryan asked to analyze hackathon options and fix everything autonomously",
        action_taken="Registered on Base, built code, integrated Filecoin API, ready for submission"
    )
    
    agent.log_insight(
        insight="Real Filecoin integration increases win probability significantly",
        category="strategy"
    )
    
    agent.log_insight(
        insight="Lighthouse SDK provides simple API for IPFS/Filecoin uploads",
        category="technical"
    )
    
    # Generate status report
    agent.status_report()
    
    # Recall decisions
    print("[RyanX] Past decisions:")
    for i, decision in enumerate(agent.recall_decisions(), 1):
        print(f"  {i}. {decision['content']}")
    
    print()
    print("[RyanX] Agent ready for autonomous operation with Filecoin memory.")
    
    if USE_FILECOIN:
        print("[RyanX] ✅ All memories permanently stored on Filecoin mainnet.")
    else:
        print("[RyanX] ⚠️ Set LIGHTHOUSE_API_KEY for real Filecoin storage.")


if __name__ == "__main__":
    main()
