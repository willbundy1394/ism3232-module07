# Simply Renewable — Capstone Proposal

## 1. Business
Simply Renewable in Calgary helps homeowners with rooftop solar setups under the Canada Greener Homes program.
- Chat: Helps customers or sales reps check proposal status, check equipment stock or prices, and ask for changes.
- Staff tab: Lets staff look at change requests and approve or reject them.

## 2. Tables (simply_renewable.db)
- proposals: Holds proposal_id, client_name, system_type, status, and install_date.
- equipment: Holds item_name, category, price, and stock.
- change_requests: Starts empty and holds number, proposal_id, new_value, and status where the default = waiting.

## 3. Lookup Tools
1. lookup_proposal(proposal_id): Checks that proposal_id is not empty and looks up that row in proposals without changing anything.
2. lookup_equipment(item_name): Checks that item_name is not empty and looks up that items price and stock in equipment without changing anything.

## 4. Change Tool
- request_change(proposal_id, new_value): Checks that both inputs are not empty and adds a waiting row to change_requests. It does not edit proposals on its own. Staff approve or reject it on the Staff tab, and approving updates proposals.

## 5. Handoff Rule
Before calling the model, Python checks the message for words like cancel, refund, leak, roof, or utility. If found, the app hands off to a person on the team instead of using the model.
- Reason for README: Cancels, refunds, roof issues, and utility approvals need a human team member to handle safely and properly.

## 6. Sensitive Data
The app never stores and never sends to the model:
- Utility or Greener Homes account logins/passwords
- SSNs, SINs, bank info, or credit/loan details

## 7. Instructions
You help with Simply Renewable proposals, equipment stock and prices, and change requests in Calgary. Use the tools to look things up or log a change request, and keep answers short and clear. You must only state facts that appear in these instructions.

## 8. Sample Conversations
1. Check a proposal: User asks about SR203. Tool checks proposals and says Greg Kowalskis 7.2kW Rooftop Solar is scheduled for 2026-12-02.
2. Check out of stock: User asks about Hybrid String Inverter 10kW. Tool checks equipment and says it is $2,150.00 and has 0 in stock.
3. Check in stock: User asks about Critter Guard Mesh Kit. Tool checks equipment and says it is $320.00 and has 15 in stock.
4. Ask for a change: User asks to move SR201s install date to 2026-12-19. Tool adds a waiting row to change_requests for staff to review.
5. Handoff: User says, "My roof is leaking and I want to cancel for a refund." Code catches it before the model and hands off to a person.