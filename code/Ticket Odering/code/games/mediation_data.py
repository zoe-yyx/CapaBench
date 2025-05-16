import os
import json
import random
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np
from collections import namedtuple

START = datetime(2023, 5, 31, 9)
END = datetime(2023, 6, 2, 19)
Flight = namedtuple("Flight", ["date", "start_time", "end_time", "price"])

output_dir = "./dialop/game_prompt"

def datetime_range(start, end, delta, min_hour=None, max_hour=None):
    current = start
    while current < end:
        if (not min_hour or current.hour >= min_hour) and \
            (not max_hour or current.hour <= max_hour):
            yield current
        current += delta

def random_datetime(start, end):
    delta = end - start
    mins_delta = (delta.days * 24 * 60) + delta.seconds // 60
    random_min = random.randrange(mins_delta)
    return start + timedelta(minutes=random_min)

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M")

def hr_min(delta):
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hr {minutes} min"

def hr_delta(delta):
    return delta.days * 24 + delta.seconds // (3600)

def times_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    if start1 < start2 < end1:
        return True
    if start2 < start1 < end2:
        return True
    return False

class Calendar:
    def __init__(self, p_event, max_events=10):
        self.p_event = p_event
        self.max_events = max_events
        self.private_events = []
        self.shared_events = []
        self.events = []
        self._generate()
        
    def _event_start_times(self):
        return datetime_range(
            START,
            END,
            timedelta(minutes=30),
            min_hour=9,
            max_hour=20,
        )

    def _generate(self):
        shared_events = []
        private_events = []
        last_start = START
        count = 0
        for time in self._event_start_times():
            if count >= self.max_events:
                break
            if time < last_start:
                continue
            
            if np.random.random() < self.p_event:
                length = random.choice([30, 60, 90, 120])
                importance = random.randint(1, 10)
                event = {
                    "id": len(shared_events),
                    "start": iso(time),
                    "end": iso(time + timedelta(minutes=length)),
                    "importance": importance
                }
                shared_events.append(event)
                last_start = time + timedelta(minutes=length)
                count += 1
        self.shared_events = shared_events
        self.events = shared_events[::]
        
        for time in self._event_start_times():
            if np.random.random() < self.p_event * 0.3:
                length = random.choice([30, 60, 90, 120])
                importance = random.randint(1, 10)
                private_event_start = time
                private_event_end = time + timedelta(minutes=length)
                
                overlap = False
                for event in self.events:
                    event_start = parse(event["start"])
                    event_end = parse(event["end"])
                    if times_overlap((private_event_start, private_event_end), (event_start, event_end)):
                        overlap = True
                        break
                
                if not overlap:
                    event = {
                        "id": len(private_events),
                        "start": iso(private_event_start),
                        "end": iso(private_event_end),
                        "importance": importance
                    }
                    private_events.append(event)
                    self.events.append(event)
        self.private_events = private_events

    def save(self, filepath):
        private_events_data = []
        for event in self.private_events:
            start_time = parse(event['start']).strftime("%m/%d %I:%M %p")
            end_time = parse(event['end']).strftime("%I:%M %p")
            event_data = {
                "id": event["id"],
                "importance": event["importance"],
                "start": start_time,
                "end": end_time
            }
            private_events_data.append(event_data)
        
        shared_events_data = []
        for event in self.shared_events:
            start_time = parse(event['start']).strftime("%m/%d %I:%M %p")
            end_time = parse(event['end']).strftime("%I:%M %p")
            event_data = {
                "id": event["id"],
                "importance": event["importance"],
                "start": start_time,
                "end": end_time
            }
            shared_events_data.append(event_data)
        
        data = {
            "Private calendar": private_events_data,
            "Shared calendar (visible to assistant)": shared_events_data
        }
        
        with open(filepath, 'r+') as f:
            file_data = json.load(f)
            file_data[-1].update(data)
            f.seek(0)
            json.dump(file_data, f, indent=4)

    def save_agent(self, filepath):
        shared_events_data = []
        for event in self.shared_events:
            start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M")
            end = datetime.strptime(event["end"], "%Y-%m-%dT%H:%M")
            event_data = {
                "id": event["id"],
                "start": start.strftime("%m/%d %I:%M %p"),
                "end": end.strftime("%I:%M %p")
            }
            shared_events_data.append(event_data)
        
        data = {
            "Calendar": shared_events_data
        }
        
        with open(filepath, 'r+') as file:
            file_data = json.load(file)
            file_data[-1].update(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

class FlightSet:
    def __init__(self, city_name, num_flights):
        self.name = city_name
        self.num_flights = num_flights
        self.mean_duration_m = 60 * random.randint(1, 10)
        self.mean_price = random.randrange(50, 1000)
        self._generate()

    def _generate(self):
        flights = []
        for _ in range(self.num_flights):
            start = random_datetime(START, END)
            duration = timedelta(
                minutes=self.mean_duration_m + np.random.exponential())
            flights.append({
                "id": len(flights),
                "carrier": random.choice(["JetBlue", "American", "Delta",
                                          "Southwest", "United", "Alaska"]),
                "date": str(start.date()),
                "start": iso(start),
                "end": iso(start + duration),
                "duration": hr_min(duration),
                "price": max(50, round(
                    np.random.normal(loc=self.mean_price,
                                     scale=self.mean_price)
                ))
            })
        self.flights = sorted(flights, key=lambda x: x["id"])

    def save(self, filepath):
        flights_data = []
        for flight in self.flights:
            start = datetime.strptime(flight["start"], "%Y-%m-%dT%H:%M")
            end = datetime.strptime(flight["end"], "%Y-%m-%dT%H:%M")
            flight_data = {
                "id": flight["id"],
                "carrier": flight["carrier"],
                "price": flight["price"],
                "start": start.strftime("%m/%d %I:%M %p"),
                "end": end.strftime("%I:%M %p")
            }
            flights_data.append(flight_data)
        
        with open(filepath, 'r+') as file:
            file_data = json.load(file)
            file_data[-1]["Flights"] = flights_data
            file.seek(0)
            json.dump(file_data, file, indent=4)

def clear_json_file(filepath):
    with open(filepath, 'w') as f:
        json.dump([], f)


if __name__ == "__main__":
    # print(os.listdir("./"))
    os.makedirs(output_dir, exist_ok=True)
    clear_json_file(os.path.join(output_dir, "user0.json"))
    clear_json_file(os.path.join(output_dir, "user1.json"))

    for trip in range(2, 20):
        for i in [0, 1]:
            data_filepath = os.path.join(output_dir, f"user{i}.json")
            if not os.path.exists(data_filepath):
                with open(data_filepath, 'w') as f:
                    json.dump([], f)

            trip_data = {"TRIP": trip}
            with open(data_filepath, 'r+') as f:
                file_data = json.load(f)
                file_data.append({"TRIP": trip})
                f.seek(0)
                json.dump(file_data, f, indent=4)
        
            f = FlightSet("non", 12)
            f._generate()
            f.save(data_filepath)
            c = Calendar(0.3)
            c.save(data_filepath)
            # c.save_agent(data_filepath)








# from datetime import datetime, timedelta
# from dateutil.parser import parse
# import random
# import numpy as np
# from collections import namedtuple
# import os
# import json

# START = datetime(2023, 5, 31, 9)
# END = datetime(2023, 6, 2, 19)

# Flight = namedtuple("Flight", ["date", "start_time", "end_time", "price"])

# # 创建存储数据的目录
# output_dir = "dialop-mediation/dialop/game_prompt"
# agentdata_dir = output_dir + "/agent.txt"
# # os.makedirs(output_dir, exist_ok=True)
# # os.makedirs(user0data_dir, exist_ok=True)
# # os.makedirs(user1data_dir, exist_ok=True)
# # os.makedirs(agentdata_dir, exist_ok=True)

# def datetime_range(start, end, delta, min_hour=None, max_hour=None):
#     current = start
#     while current < end:
#         if (not min_hour or current.hour >= min_hour) and \
#             (not max_hour or current.hour <= max_hour):
#             yield current
#         current += delta

# def random_datetime(start, end):
#     delta = end - start
#     mins_delta = (delta.days * 24 * 60) + delta.seconds // 60
#     random_min = random.randrange(mins_delta)
#     return start + timedelta(minutes=random_min)

# def iso(dt):
#     return dt.strftime("%Y-%m-%dT%H:%M")

# def hr_min(delta):
#     hours, remainder = divmod(delta.seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     return f"{hours} hr {minutes} min"

# def hr_delta(delta):
#     return delta.days * 24 + delta.seconds // (3600)

# def times_overlap(range1, range2):
#     start1, end1 = range1
#     start2, end2 = range2
#     if start1 < start2 < end1:
#         return True
#     if start2 < start1 < end2:
#         return True
#     return False


# class Calendar:

#     def __init__(self, p_event, max_events=10):
#         self.p_event = p_event
#         self.max_events = max_events
#         self.private_events = []
#         self.shared_events = []
#         self.events = []
#         self._generate()
        

#     def _event_start_times(self):
#         """Generate all possible start times in the date range."""
#         return datetime_range(
#             START,
#             END,
#             timedelta(minutes=30),
#             min_hour=9,
#             max_hour=20,
#         )

#     def _generate(self):
#         """生成共享和私人日历事件。"""
#         shared_events = []
#         private_events = []
#         last_start = START
#         count = 0

#         for time in self._event_start_times():
#             if count >= self.max_events:
#                 break
#             if time < last_start:
#                 continue
            
#             # 生成共享日历事件
#             if np.random.random() < self.p_event:
#                 length = random.choice([30, 60, 90, 120])
#                 importance = random.randint(1, 10)
#                 event = {
#                     "id": len(shared_events),
#                     "start": iso(time),
#                     "end": iso(time + timedelta(minutes=length)),
#                     "importance": importance
#                 }
#                 shared_events.append(event)
#                 last_start = time + timedelta(minutes=length)
#                 count += 1

#         self.shared_events = shared_events
#         self.events = shared_events[::]
        
#         # 生成私人日历事件，避免时间冲突
#         for time in self._event_start_times():
#             if np.random.random() < self.p_event * 0.3:
#                 length = random.choice([30, 60, 90, 120])
#                 importance = random.randint(1, 10)
#                 private_event_start = time
#                 private_event_end = time + timedelta(minutes=length)
                
#                 # 检查是否与公共日历事件冲突
#                 overlap = False
#                 for event in self.events:
#                     event_start = parse(event["start"])
#                     event_end = parse(event["end"])
#                     if times_overlap((private_event_start, private_event_end), (event_start, event_end)):
#                         overlap = True
#                         break
                
#                 # 如果没有冲突，添加私人事件
#                 if not overlap:
#                     event = {
#                         "id": len(private_events),
#                         "start": iso(private_event_start),
#                         "end": iso(private_event_end),
#                         "importance": importance
#                     }
#                     private_events.append(event)
#                     self.events.append(event)


#         self.private_events = private_events

#     def save(self, filepath):
#         private_events_data = []
#         for event in self.private_events:
#             start_time = parse(event['start']).strftime("%m/%d %I:%M %p")
#             end_time = parse(event['end']).strftime("%I:%M %p")
#             event_data = {
#                 "id": event["id"],
#                 "importance": event["importance"],
#                 "start": start_time,
#                 "end": end_time
#             }
#             private_events_data.append(event_data)
        
#         shared_events_data = []
#         for event in self.shared_events:
#             start_time = parse(event['start']).strftime("%m/%d %I:%M %p")
#             end_time = parse(event['end']).strftime("%I:%M %p")
#             event_data = {
#                 "id": event["id"],
#                 "importance": event["importance"],
#                 "start": start_time,
#                 "end": end_time
#             }
#             shared_events_data.append(event_data)
        
#         data = {
#             "Private calendar": private_events_data,
#             "Shared calendar (visible to assistant)": shared_events_data
#         }
        
#         with open(filepath, 'a') as f:
#             json.dump(data, f, indent=4)

#     def save_agent(self, filepath):
#         shared_events_data = []
#         for event in self.shared_events:
#             start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M")
#             end = datetime.strptime(event["end"], "%Y-%m-%dT%H:%M")
#             event_data = {
#                 "id": event["id"],
#                 "start": start.strftime("%m/%d %I:%M %p"),
#                 "end": end.strftime("%I:%M %p")
#             }
#             shared_events_data.append(event_data)
        
#         data = {
#             "Calendar": shared_events_data
#         }
        
#         with open(filepath, 'a') as file:
#             json.dump(data, file, indent=4)
#     # def save(self, filepath):
#     #     with open(filepath, "a") as f:
#     #         # f.write("TRIP 1.\n")
#     #         # f.write("Flights:\n")
#     #         # f.write("id | carrier | price | times\n")
#     #         # for flight in flight_set.flights:
#     #         #     start_time = parse(flight['start']).strftime("%m/%d %I:%M %p")
#     #         #     end_time = parse(flight['end']).strftime("%I:%M %p")
#     #         #     f.write(f"{flight['id']} | {flight['carrier']} | {flight['price']} | {start_time} - {end_time}\n")
            
#     #         f.write("Private calendar:\n")
#     #         f.write("id | importance | times\n")
#     #         for event in self.private_events:
#     #             start_time = parse(event['start']).strftime("%m/%d %I:%M %p")
#     #             end_time = parse(event['end']).strftime("%I:%M %p")
#     #             f.write(f"{event['id']} | ({event['importance']}) | {start_time} - {end_time}\n")

#     #         f.write("Shared calendar (visible to assistant):\n")
#     #         f.write("id | importance | times\n")
#     #         for event in self.shared_events:
#     #             start_time = parse(event['start']).strftime("%m/%d %I:%M %p")
#     #             end_time = parse(event['end']).strftime("%I:%M %p")
#     #             f.write(f"{event['id']} | ({event['importance']}) | {start_time} - {end_time}\n")

#     # def save_agent(self, filepath):
#     #     with open(filepath, "a") as file:
#     #         file.write("Calendar:\n")
#     #         file.write("id | times\n")
#     #         for event in self.shared_events:
#     #             start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M")
#     #             end = datetime.strptime(event["end"], "%Y-%m-%dT%H:%M")
#     #             file.write(f'{event["id"]} | {start.strftime("%m/%d %I:%M %p")} - {end.strftime("%I:%M %p")}\n')

# class FlightSet:

#     def __init__(self, city_name, num_flights):
#         self.name = city_name
#         self.num_flights = num_flights
#         # Average duration for a flight to ensure all flights
#         #  in this set take around the same time
#         self.mean_duration_m = 60 * random.randint(1, 10)
#         self.mean_price = random.randrange(50, 1000)
#         self._generate()

#     def _generate(self):
#         flights = []
#         for _ in range(self.num_flights):
#             start = random_datetime(START, END)
#             duration = timedelta(
#                 minutes=self.mean_duration_m + np.random.exponential())
#             flights.append({
#                 "id": len(flights),
#                 "carrier": random.choice(["JetBlue", "American", "Delta",
#                                           "Southwest", "United", "Alaska"]),
#                 "date": str(start.date()),
#                 "start": iso(start),
#                 "end": iso(start + duration),
#                 "duration": hr_min(duration),
#                 "price": max(50, round(
#                     np.random.normal(loc=self.mean_price,
#                                      scale=self.mean_price)
#                 ))
#             })
#         self.flights = sorted(flights, key=lambda x: x["id"])

#     def save(self, filepath):
#         flights_data = []
#         for flight in self.flights:
#             start = datetime.strptime(flight["start"], "%Y-%m-%dT%H:%M")
#             end = datetime.strptime(flight["end"], "%Y-%m-%dT%H:%M")
#             flight_data = {
#                 "id": flight["id"],
#                 "carrier": flight["carrier"],
#                 "price": flight["price"],
#                 "start": start.strftime("%m/%d %I:%M %p"),
#                 "end": end.strftime("%I:%M %p")
#             }
#             flights_data.append(flight_data)
        
#         with open(filepath, 'a') as file:
#             json.dump(flights_data, file, indent=4)
    


# if __name__ == "__main__":
#     os.makedirs(output_dir, exist_ok=True)
    
#     # source_dir0 = "dialop-mediation\dialop\game_prompt\prompt.json"
#     # source_dir1 = "dialop-mediation\dialop\prompts\mediation_user1.txt"
#     # source_dir_agent = "dialop-mediation\dialop\prompts\mediation_agent.txt"

#     # with open(source_dir0, "r") as source_file, open(os.path.join(output_dir, "user0.txt"), "w") as target_file:
#     #     for line in source_file:
#     #         target_file.write(line)
#     # with open(source_dir1, "r") as source_file, open(os.path.join(output_dir, "user1.txt"), "w") as target_file:
#     #     for line in source_file:
#     #         target_file.write(line)
#     # with open(source_dir_agent, "r") as source_file, open(os.path.join(output_dir, "agent.txt"), "w") as target_file:
#     #     for line in source_file:
#     #         target_file.write(line)

    
#     for trip in range(2, 3):
#         for i in [0, 1]:
#             # with open(os.path.join(output_dir, f"user{i}.txt"), "a") as f:
#             #     f.write(f"\nTRIP {trip}.\n")
#             # with open(os.path.join(output_dir, "agent.txt"), "a") as f:
#             #     f.write(f"\nTRIP {trip}.\n")
#             #     f.write(f"User {i} Information\n")


#             f = FlightSet("non", 12)
#             f._generate()
#             f.save(os.path.join(output_dir, f"user{i}.json"))
#             f.save(os.path.join(output_dir, "agent.json"))

#             c = Calendar(0.3)
#             c.save(os.path.join(output_dir, f"user{i}.json"))
#             c.save_agent(os.path.join(output_dir, "agent.json"))
            
            

#     # f0 = FlightSet("non", 12)
#     # f0._generate()
#     # f0.save(os.path.join(output_dir, "flights.txt"))

#     # c0 = Calendar(0.3)
#     # c0.save(os.path.join(output_dir, "user0.txt"), 0)

#     # c1 = Calendar(0.3)
#     # c1.save(os.path.join(output_dir, "user1.txt"), 1)

#     # print(f.flights)
#     # import pdb; pdb.set_trace()
# #    c = Calendar(0.1)
# #    print("\n".join([str(e) for e in c.events]))
#     # os.mkdir("dialop-mediation/dialop/test11")
