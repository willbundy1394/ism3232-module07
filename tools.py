# tools.py
# Author: Will Bundy
import database


class SimplyRenewableTools:
    """Tools the model can use. Everything goes through run first."""

    def __init__(self, db_file):
        self.db_file = db_file

    def tool_list(self):
        return [
            self.lookup_proposal,
            self.lookup_equipment,
            self.request_change,
            self.check_request,
        ]

    def lookup_proposal(self, proposal_id):
        """Look up one proposal.
        Args:
            proposal_id: The proposal ID like SR203.
        """
        for word in proposal_id.upper().split():
            clean_id = word.strip("?.!,")
            proposal = database.find_proposal(self.db_file, clean_id)
            if proposal is not None:
                return (
                    f"Proposal {proposal['proposal_id']} for {proposal['client_name']} "
                    f"({proposal['system_type']}) is {proposal['status']} "
                    f"with install date {proposal['install_date']}."
                )
        return "No proposal with that ID was found. Proposal IDs look like SR203."

    def lookup_equipment(self, item_name):
        """Check price and stock of one item.
        Args:
            item_name: The equipment name.
        """
        for name in database.equipment_names(self.db_file):
            if name in item_name.lower():
                # get the real row
                rows = database.query_all(
                    self.db_file,
                    "SELECT * FROM equipment WHERE lower(item_name) = ?",
                    (name,),
                )
                if rows:
                    item = rows[0]
                    return (
                        f"We have {item['stock']} of the {item['item_name']} "
                        f"in stock, at ${item['price']:.2f}."
                    )
        return "That equipment item was not found."

    def request_change(self, proposal_id, new_value):
        """Ask staff to change the install date.
        Args:
            proposal_id: The proposal ID.
            new_value: The new install date.
        """
        proposal_id = proposal_id.upper().strip()
        if database.find_proposal(self.db_file, proposal_id) is None:
            return "No proposal with that ID was found. Proposal IDs look like SR201."
        number = database.add_change_request(self.db_file, proposal_id, new_value)
        return (
            f"Request {number} was sent to staff. The install date has not changed yet."
        )

    def check_request(self, number):
        """Check the status of a change request.
        Args:
            number: The request number.
        """
        try:
            request = database.find_request(self.db_file, int(number))
        except (ValueError, OverflowError):
            return "Request numbers look like 3."
        if request is None:
            return f"There is no request {number}."
        if request["status"] == "waiting":
            return f"Request {number} for proposal {request['proposal_id']} is waiting for staff."
        return f"Request {number} for proposal {request['proposal_id']} was {request['status']}."

    def run(self, name, arguments, history):
        """Check arguments and history before running a tool."""
        if name == "lookup_proposal":
            proposal_id = self.clean(arguments, "proposal_id")
            if proposal_id == "":
                return "The proposal ID is missing. Ask the customer for it."
            if not self.customer_said(history, proposal_id):
                return "The customer has not given that proposal ID. Ask them for it."
            return self.lookup_proposal(proposal_id)

        if name == "lookup_equipment":
            item_name = self.clean(arguments, "item_name")
            if item_name == "":
                return "The equipment name is missing. Ask the customer which item."
            return self.lookup_equipment(item_name)

        if name == "request_change":
            proposal_id = self.clean(arguments, "proposal_id")
            new_value = self.clean(arguments, "new_value")
            if proposal_id == "" or new_value == "":
                return "The proposal ID and the new value are both needed."
            if not self.customer_said(history, proposal_id):
                return "The customer has not given that proposal ID. Ask them for it."
            if not self.customer_said(history, new_value):
                return "The customer has not given that new value. Ask them for it."
            return self.request_change(proposal_id, new_value)

        if name == "check_request":
            number = self.clean(arguments, "number")
            if number == "":
                return "The request number is missing. Ask the customer for it."
            if not self.customer_said(history, number):
                return (
                    "The customer has not given that request number. Ask them for it."
                )
            return self.check_request(number)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        return str(arguments.get(key, "")).strip()

    def words(self, text):
        cleaned = []
        for word in text.lower().split():
            cleaned.append(word.strip("?.!,#"))
        return " " + " ".join(cleaned) + " "

    def customer_said(self, history, text):
        wanted = self.words(text)
        for message in history:
            if message["role"] == "user" and wanted in self.words(message["content"]):
                return True
        return False
