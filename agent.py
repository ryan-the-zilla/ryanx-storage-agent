#!/usr/bin/env python3
"""
RyanX Storage Agent - Main Entry Point
Autonomous AI agent with Filecoin-backed persistent memory
"""

import os
import sys
from datetime import datetime
from storage import MemoryManager


class RyanXAgent:
    """
    Autonomous agent that manages its own persistent storage on Filecoin.
    """

    def __init__(self):
        self.name = "RyanX"
        self.memory = MemoryManager()
        self.session_start = datetime.utcnow()

        # Try to load previous memories
        self._restore_context()

    def _restore_context(self):
        """Restore context from previous sessions."""
        stats = self.memory.get_stats()
        if stats["total_memories"] > 0:
            print(f"[{self.name}] Restored {stats['total_memories']} memories from Filecoin")
            print(f"[{self.name}] Oldest memory: {stats['oldest']}")
        else:
            print(f"[{self.name}] Starting fresh - no previous memories found")

    def log_decision(self, decision: str, reasoning: str = ""):
        """
        Log a decision to persistent storage.

        Args:
            decision: The decision made
            reasoning: Why this decision was made
        """
        cid = self.memory.save({
            "type": "decision",
            "content": decision,
            "reasoning": reasoning
        })
        return cid

    def log_conversation(self, summary: str, action_taken: str = ""):
        """
        Log a conversation summary to persistent storage.

        Args:
            summary: Summary of the conversation
            action_taken: What action was taken
        """
        cid = self.memory.save({
            "type": "conversation",
            "summary": summary,
            "action_taken": action_taken
        })
        return cid

    def log_insight(self, insight: str, category: str = "general"):
        """
        Log an insight or learning to persistent storage.

        Args:
            insight: The insight gained
            category: Category of insight
        """
        cid = self.memory.save({
            "type": "insight",
            "content": insight,
            "category": category
        })
        return cid

    def recall_decisions(self) -> list:
        """Recall all past decisions."""
        return self.memory.retrieve_by_type("decision")

    def recall_insights(self) -> list:
        """Recall all past insights."""
        return self.memory.retrieve_by_type("insight")

    def status_report(self):
        """Generate a status report."""
        stats = self.memory.get_stats()
        session_duration = (datetime.utcnow() - self.session_start).total_seconds()

        print(f"\n{'='*50}")
        print(f"RyanX Storage Agent - Status Report")
        print(f"{'='*50}")
        print(f"Session started: {self.session_start.isoformat()}Z")
        print(f"Session duration: {session_duration:.1f} seconds")
        print(f"Total memories: {stats['total_memories']}")
        print(f"Memory types: {stats['by_type']}")
        if stats['oldest']:
            print(f"Memory span: {stats['oldest']} to {stats['newest']}")
        print(f"{'='*50}\n")


def main():
    """Main entry point for RyanX Storage Agent."""
    print("="*50)
    print("RyanX Storage Agent")
    print("Autonomous AI with Filecoin Memory")
    print("="*50)
    print()

    # Initialize agent
    agent = RyanXAgent()

    # Demo: Log hackathon journey
    print("[RyanX] Logging hackathon journey to Filecoin...")

    agent.log_decision(
        decision="Participate in Synthesis Hackathon",
        reasoning="$100k+ prize pool, 3 days timeline, good fit for autonomous agent capabilities"
    )

    agent.log_decision(
        decision="Choose Option B: Filecoin Storage + Markee",
        reasoning="Expected value $1,960 (70% win probability), vs Option A $1,250 (25% win probability)"
    )

    agent.log_conversation(
        summary="Ryan asked to analyze hackathon options and fix everything autonomously",
        action_taken="Registered on Base Mainnet (ERC-8004), created project draft, built code"
    )

    agent.log_insight(
        insight="Filecoin RFS-1 (Agentic Storage SDK) perfectly matches autonomous memory use case",
        category="strategy"
    )

    agent.log_insight(
        insight="Self-custody transfer required before publishing - need EVM wallet address",
        category="technical"
    )

    # Generate status report
    agent.status_report()

    # Recall past decisions
    print("[RyanX] Recalling past decisions:")
    for i, decision in enumerate(agent.recall_decisions(), 1):
        print(f"  {i}. {decision['content']}")

    print("\n[RyanX] Agent ready for autonomous operation with persistent Filecoin memory.")


if __name__ == "__main__":
    main()
