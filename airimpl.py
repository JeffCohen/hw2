import os
import os.path

def cities():
    return ["BOS", "LAX", "PDX", "JFK", "MIA"]

def mkflt(city, date):
    with open(f"{city}-{date}.txt",'w') as out:
        for i in range(25):
            out.write('OO OO\n')

def sell(city, date, row):
    month, day = date.split('-')
    date = month.rjust(2, '0') + '-' + day.rjust(2, '0')
    row = int(row)
    filenm = f"{city}-{date}.txt"
    if not os.path.exists(filenm):
        mkflt(city, date)

    prices = { }  # dictionary of row numbers to prices
    rows = [] # count how many open seats in each row
    stchart = [] # seating chart

    with open(filenm) as f:
        for line in f:
            stchart.append(line)
            rows.append(line.count('O'))


    # calculate prices
    currprc = 200 # starting price
    for i in range(25):
        if rows[i] > 0:
            prices[i+1] = currprc
            currprc -= 4  # cheaper as we move toward the back

    tktprc = prices[row]

    # update file, put X for sold seat
    seats = stchart[row-1]
    st_indx = seats.index("O")
    seats = seats[:st_indx] + "X" + seats[st_indx + 1:]
    stchart[row-1] = seats
    with open(filenm, "w") as f:
        for r in stchart:
            f.write(r)

    # save ticket receipt
    tkt_id = f"{city}{date}{str(row).rjust(2,'0')}{st_indx+1}".replace('-','')
    with open(f"TKT-{tkt_id}.txt", "w") as f:
        f.write(str(tktprc))

    print(f"Ticket ID: {tkt_id}")
    print(f"Price: ${tktprc}.00")
    print(f"Destination: {city}")
    print(f"Departure Date: {date}")
    print(f"Row: {row}  Seat: {st_indx + 1}")

def refund(tkt_id):
    tfilenm = "TKT-" + tkt_id + ".txt"
    if not os.path.exists(tfilenm):
        print("Can't find that ticket.")
        return
    with open(tfilenm) as f:
        price = int(f.readline())

    # update file, put X for sold seat
    city = tkt_id[0:3]
    date = f"{tkt_id[3:5]}-{tkt_id[5:7]}"
    filenm = filenm = f"{city}-{date}.txt"
    row = int(tkt_id[7:9]) - 1
    st_indx = int(tkt_id[9]) - 1
    stchart = [] # seating chart

    with open(filenm) as f:
        for line in f:
            stchart.append(line)

    seats = stchart[row]
    seats = seats[:st_indx] + "O" + seats[st_indx + 1:]
    stchart[row-1] = seats
    with open(filenm, "w") as f:
        for r in stchart:
            f.write(r)

    os.remove(tfilenm)

    print(f"Refunded ${price}.00")



def status(tkt_id):
    filenm = "TKT-" + tkt_id + ".txt"
    if not os.path.exists(filenm):
        print("Can't find that ticket.")
        return

    with open(filenm) as f:
        price = int(f.readline())

    print(f"Ticket ID: {tkt_id}")
    print(f"Price: ${price}.00")
    print(f"Destination: {tkt_id[0:3]}")
    print(f"Departure Date: {tkt_id[3:5]}-{tkt_id[5:7]}")
    print(f"Row: {tkt_id[8:10]}  Seat: {tkt_id[9]}")
    print()

def sched(date):
    print("Date   Flight #   Destination   Time")
    print("----   --------   -----------   --------------")
    print(f"{date}  101        BOS           08:00 AM")
    print(f"{date}  102        LAX           10:00 AM")
    print(f"{date}  103        PDX           12:00 PM")
    print(f"{date}  104        JFK           02:00 PM")
    print(f"{date}  105        MIA           04:00 PM")
    print()

def remain(city, date):
    month, day = date.split('-')
    date = month.rjust(2, '0') + '-' + day.rjust(2, '0')

    filenm = f"{city}-{date}.txt"
    if not os.path.exists(filenm):
        mkflt(city, date)

    prices = { }  # dictionary of row numbers to prices
    rows = [] # count how many open seats in each row

    with open(filenm) as f:
        for line in f:
            rows.append(line.count('O'))

    # calculate prices
    currprc = 200 # starting price
    for i in range(25):
        if rows[i] > 0:
            prices[i+1] = currprc
            currprc -= 4  # decrease as we move toward the back

    for row, price in prices.items():
        print(f"Row {row}: ${price}.00")
