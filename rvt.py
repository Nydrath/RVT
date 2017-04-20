import json
import discord
import os
import random

def savedb(database, name):
    with open(name+".tmp", "w") as f:
        f.write(json.dumps(database, indent=4))
    os.rename(name+".tmp", name)

if os.path.exists("database.json"):
    with open("database.json", "r") as f:
        database = json.load(f)
else:
    database = {}

if os.path.exists("log.json"):
    with open("log.json", "r") as f:
        log = json.load(f)
else:
    log = {}

ongoingreads = {}

with open("client_data.json", "r") as f:
    clientdata = json.load(f)

myself = discord.Client()

@myself.event
async def on_message(message):
    if message.channel == "remote-viewing" and not message.author.bot:
        splitmsg = message.content.split()
        if splitmsg[0] == "RVT":
            mention = message.author.mention
            if len(splitmsg) > 1:
                if splitmsg[1] == "addtarget":
                    if len(splitmsg) > 2:
                        target = " ".join(splitmsg[2:])
                        if target in database:
                            if mention not in database[target]:
                                database[target].append(mention)
                                savedb(database, "database.json")
                            else:
                                await myself.send_message(message.channel, mention+" You have already submitted this entry.")
                        else:
                            database[target] = [mention]
                            savedb(database, "database.json")
                        await myself.send_message(message.channel, mention+" Target successfully added.")
                    else:
                        await myself.send_message(message.channel, mention+" No target given.")
                elif splitmsg[1] == "begin":
                    if mention in ongoingreads:
                        await myself.send_message(message.channel, mention+" You are already doing a session.")
                    else:
                        target = random.choice(list(database.keys()))
                        coordinates = str(random.randint(1000, 10000))+"-"+str(random.randint(1000, 10000))
                        ongoingreads[mention] = [coordinates, target, database[target]]
                        await myself.send_message(message.channel, mention+" Coordinates: "+coordinates+".")
                elif splitmsg[1] == "end":
                    if mention in ongoingreads:
                        answer = "Session #{4} by user {0}: Target {1} was {2}, added by {3}. Runsheet was {5}".format(mention, ongoingreads[mention][0], ongoingreads[mention][1], " ".join(ongoingreads[mention][2]), len([entry for user,entries in log.items() for entry in entries]), " ".join(splitmsg[2:]))
                        if mention in log:
                            log[mention].append(answer)
                        else:
                            log[mention] = [answer]
                        savedb(log, "log.json")
                        await myself.send_message(message.channel, answer)
                        del ongoingreads[mention]
                    else:
                        await myself.send_message(message.channel, mention+" You did not start a session.")
                elif splitmsg[1] == "list":
                    if len(splitmsg) > 2:
                        if splitmsg[2] in log:
                            logs = log[mention]
                        else:
                            await myself.send_message(message.channel, mention+" Could not find logs of "+splitmsg[2])
                            return
                    else:
                        logs = [entry for user,entries in log.items() for entry in entries]
                    totalstring = "\n".join(sorted(logs))
                    while True:
                        if len(totalstring) > 2000:
                            await myself.send_message(message.author, totalstring[:2000])
                            totalstring = totalstring[2000:]
                        else:
                            await myself.send_message(message.channel, totalstring)
                            break
                else:
                    await myself.send_message(message.channel, mention+" Invalid commands. Please specify either \"addtarget <target>\", \"begin\", \"end\", \"list\" or \"list <member>\"")

myself.run(clientdata["token"])
