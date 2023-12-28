import requests 
from data import get_api

api,chain_is_live = get_api()

tally_ip = api+"/cosmos/gov/v1beta1/proposals/{proposal_id}/tally" # this is the full prop api for each governance proposal tally 
status_api = api+"/cosmos/gov/v1/proposals/{proposal_id}"#prop to check any other info needed abot the prop



possible_status = ["PROPOSAL_STATUS_PASSED","PROPOSAL_STATUS_REJECTED","PROPOSAL_STATUS_VOTING_PERIOD"]

def governor (proposal_id):
    if chain_is_live:
        formatted_api_url = tally_ip.format(proposal_id=proposal_id)
        formatted_status_api = status_api.format(proposal_id=proposal_id)
    else: 
        return "Ίσως να υπάρχει πρόβλημα με την αλυσίδα! 😳" #Every API is broken. Probably problems with the chain

    #Is there a proposal with this ID? 
    response = requests.get(formatted_status_api)
    try:
        status = response.json()['proposal']['status']
        the_proposal_exists = True

        try:
            title = response.json()['proposal']['messages'][0]['content']['title']
        except: 
            title = response.json()['proposal']['title']


        if status == "PROPOSAL_STATUS_PASSED": 
            status = "Αποδεκτή ✅"
        elif status == "PROPOSAL_STATUS_REJECTED": 
            status = "Απορρίφθηκε ❌"
        elif status == "PROPOSAL_STATUS_VOTING_PERIOD":
            status = "Υπό ψηφοφορία ⏳️"
        else: #status == "PROPOSAL_STATUS_DEPOSIT_PERIOD": 
            status = "Eκκρεμεί κατάθεση για έναρξη ψηφοφορίας 🔜"
    except: 
        the_proposal_exists = False
        return "Δεν υπάρχει τέτοιο proposal. Πιθανόν να ήταν spam...🤔"

    if the_proposal_exists:
            data = requests.get(formatted_api_url).json()
            yes = int(data['tally']['yes'])/1000000
            no = int(data['tally']['no'])/1000000
            abstain = int(data['tally']['abstain'])/1000000
            nwv = int(data['tally']['no_with_veto'])/1000000

            total_votes = yes + no + abstain + nwv 
            yes_percent = round(yes/total_votes*100,2)
            no_percent = round(no/total_votes*100,2)
            abstain_percent = round(abstain/total_votes*100,2)
            nvw_percent= round(nwv/total_votes*100,2)

            votes_ranking = {"yes":yes_percent,"no":no_percent,"abstain":abstain_percent,"nwv":nvw_percent}


            #grpahics 
            graphics_dict ={}
            for vote in votes_ranking: 
                perc = votes_ranking[vote]
                big_blocks = int(perc//6)
                perc = perc - big_blocks*6
                small_blocks = int(perc//3)
                graphics_dict[vote] = big_blocks * "█" + small_blocks * "▌"         

            return  f"""
*📜 {title} *
*📁 {status}*
       
👍 {graphics_dict["yes"]} *Yes*: {yes_percent}%

👎 {graphics_dict["no"]} *No*: {no_percent}%

🚫 {graphics_dict["nwv"]} *No with veto*: {nvw_percent}%

🤔 {graphics_dict["abstain"]} *Abstain*: {abstain_percent}%

_Από την κοινότητα του Juno Greece_
"""
