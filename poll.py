import requests 

api = "https://api-juno-ia.cosmosia.notional.ventures/cosmos/gov/v1beta1/proposals/{proposal_id}/tally" # this is the full prop api for each governance proposal tally 
status_api = "https://api-juno-ia.cosmosia.notional.ventures/cosmos/gov/v1/proposals/{proposal_id}"#prop to check any other info needed abot the prop

alternvative_status_url = "https://juno-rest.publicnode.com/cosmos/gov/v1/proposals/{proposal_id}"
alternvative_api_url = "https://juno-rest.publicnode.com/cosmos/gov/v1beta1/proposals/{proposal_id}/tally"

possible_status = ["PROPOSAL_STATUS_PASSED","PROPOSAL_STATUS_REJECTED","PROPOSAL_STATUS_VOTING_PERIOD"]

def governor (proposal_id): 
    print (proposal_id)
    formatted_api_url = api.format(proposal_id=proposal_id)
    formatted_status_api = status_api.format(proposal_id=proposal_id)

    #Is there a proposal with this ID? 
    response = requests.get(formatted_status_api)
    if response.status_code == 429: #rate limited
        formatted_status_api = alternvative_status_url.format(proposal_id=proposal_id)
        formatted_api_url = api.format(proposal_id=proposal_id)

        response = requests.get(formatted_api_url)
        
        # Process the response or perform other actions as needed
        if response.status_code == 429: #rate limited again 
            return ("Try again is some time! Facing problems at the moment...😿")
    
    try:
        status = response.json()['proposal']['status']
        try:
            title = response.json()['proposal']['messages'][0]['content']['title']
        except: 
            title = response.json()['proposal']['title']

        spam = False

        if status == "PROPOSAL_STATUS_PASSED": 
            status = "Αποδεκτή ✅"
        elif status == "PROPOSAL_STATUS_REJECTED": 
            status = "Απορρίφθηκε ❌"
        elif status == "PROPOSAL_STATUS_VOTING_PERIOD":
            status = "Υπό ψηφοφορία ⏳️"
        elif status == "PROPOSAL_STATUS_DEPOSIT_PERIOD": 
            status = "Eκκρεμεί κατάθεση για έναρξη ψηφοφορίας 🔜"
        else: 
            status = "Spam Proposal"
            spam = True
        print (status)
    except: 
        print ("Δεν υπάρχει τέτοιο proposal") #SPAM PROPOSAL THAT NEVER GOT JUNO DEPOSITED
        spam = True

    if spam == False:
            print ("Proceeding with fetching data...")
            response = requests.get(formatted_api_url)
            data = response.json()
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
            sorted_dict_desc = dict(sorted(votes_ranking.items(), key=lambda item: item[1], reverse=True))
            print (sorted_dict_desc)

            #grpahics 
            graphics_dict ={}
            for vote in sorted_dict_desc: 
                perc = sorted_dict_desc[vote]
                big_blocks = int(perc//6)
                perc = perc - big_blocks*6
                small_blocks = int(perc//3)
                
                print (big_blocks, small_blocks)  
                graphics_dict[vote] = big_blocks * "█" + small_blocks * "▌"         

            message =  f"""
*📜 {title} *
*📁 {status}*
       
👍 {graphics_dict["yes"]} *Yes*: {yes_percent}%

👎 {graphics_dict["no"]} *No*: {no_percent}%

🚫 {graphics_dict["nwv"]} *No with veto*: {nvw_percent}%

🤔 {graphics_dict["abstain"]} *Abstain*: {abstain_percent}%

_Από την κοινότητα του Juno Greece_
"""


    else: 
        message = "Δεν υπάρχει τέτοιο proposal 🤔"
    
    return message
