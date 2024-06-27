def extract_events(trace_file):
    events = []

    with open(trace_file, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 3)
            if len(parts) >= 4:
                event_symbol = parts[0]
                event_time = float(parts[1])
                event_type = parts[2]
                event_details = parts[3]
                events.append((event_time, event_symbol, event_type, event_details))

    return events

def calculate_end_to_end_delay(events):
    send_times = {}
    receive_times = []

    for event in events:
        event_time, event_symbol, event_type, event_details = event

        if event_symbol == '+' and "TxQueue/Enqueue" in event_type:
            packet_id = event_details.split(" ")[2]  # Extraction de l'identifiant du paquet
            send_times[packet_id] = event_time

        elif event_symbol == 'r' and "MacRx" in event_type:
            packet_id = event_details.split(" ")[2]
            if packet_id in send_times:
                send_time = send_times.pop(packet_id)
                receive_times.append(event_time - send_time)

    if receive_times:
        average_delay = sum(receive_times) / len(receive_times)
        print(f"Average End-to-End Delay: {average_delay} seconds")
    else:
        print("No valid packets found for calculating end-to-end delay.")

def main():
    trace_file = "olsr-hna-csma.tr"
    events = extract_events(trace_file)
    print(f"Extracted {len(events)} events from trace file.")
    calculate_end_to_end_delay(events)

if __name__ == "__main__":
    main()

