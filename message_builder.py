from data import Juno
def Message_builder():
    juno =  Juno()
    return f"""
🌕 *Τιμή Juno*: $ {juno.price:.2f}
🥩 *Staking APR*: {int(juno.apr*100)}%
🌱 *Πληθωρισμός*: {juno.inflation*100}%
🏦 *Κεφαλαιοποίηση*: $ {round(juno.mc/1000000,2)} Μ 
🙌 *Νομίσματα σε κυκλοφορία*: {round(juno.cs/1000000,2)}εκ. Juno

_Από την κοινότητα του Juno Greece_
"""
