# keyword_model.py
# Author: Will Bundy


class KeywordModel:
    """A stand-in model that decides with keyword rules."""

    def decide(self, instructions, history, tools):
        last = history[-1]
        if last["role"] == "tool":
            return {"text": last["content"]}
        text = last["content"].lower()
        if "proposal" in text or "sr2" in text:
            return {
                "tool": "lookup_proposal",
                "arguments": {"proposal_id": last["content"]},
            }
        if (
            "stock" in text
            or "equipment" in text
            or "panel" in text
            or "inverter" in text
        ):
            return {
                "tool": "lookup_equipment",
                "arguments": {"item_name": last["content"]},
            }
        if "hello" in text or "hi" in text:
            return {"text": "Hello! How can I help you today?"}
        return {"text": "I can check a proposal or equipment stock. What do you need?"}
