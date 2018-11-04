"""
Config file for Currency converter - required to run
"""
# Discord App token

bot_token = "you token here"

# Command prefix

cmd_prefix = "//"

# Generic error message for incorrect user input

err_msg = "Unrecognised input. Enter `convertbot help` if you need help."

# Default currency codes
"""
Note: the 'setdefault' function in the main file depends on these variables.
Please view and understand that function before changing the names/structure.
"""

defaultInitCurr = 'USD'
defaultFinalCurr = 'AUD'
