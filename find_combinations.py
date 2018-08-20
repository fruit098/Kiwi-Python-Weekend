#!/usr/bin/env python
"""kiwi-flights.py - My solution for kiwi task."""

__author__ = "Andrej Zaujec"
__email__ = "andrej.zaujec8@gmail.com"
__license_ = "GPL"

from sys import stdin, exit, stderr
from datetime import datetime, timedelta


class Flight:

    def __init__(self, source, destination, departure, arrival, flight_number, price, bags_allowed, bag_price):
        try:
            self.source = str(source)
            self.destination = str(destination)
            self.departure = datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S")
            self.arrival = datetime.strptime(arrival, "%Y-%m-%dT%H:%M:%S")
            self.flight_number = flight_number
            self.price = int(price)
            self.bags_allowed = int(bags_allowed)
            self.bag_price = int(bag_price)
        except Exception as excp:
            print("Exception {} during parameters to object handling".format(type(excp).__name__), file=stderr)
            exit(-1)

    def __repr__(self):
        """
        Represenation for templating
        :return: string flight in csv
        """
        departure = datetime.strftime(self.departure, "%Y-%m-%dT%H:%M:%S")
        arrival = datetime.strftime(self.arrival, "%Y-%m-%dT%H:%M:%S")
        return f"{self.source},{self.destination},{departure},{arrival},{self.flight_number},{self.price},{self.bags_allowed},{self.bag_price}"

    def check_connect(self, other):
        """
        Check all necessary conditions for connection
        :param other: second Flight object to compare with
        :return: True if connection can be made and False if not
        """
        if self.flight_number == other.flight_number:
            return False

        if self.destination != other.source:
            return False

        min_time = self.arrival + timedelta(hours=1)
        max_time = self.arrival + timedelta(hours=4)
        if min_time > other.departure or other.departure > max_time:
            return False

        return True

    def check_directions(self, taken_flights):
        """
        Check if direction of flight was not already added to taken_flights and if last source is same as destination
        this has to be done due to possible recursion problems
        :param taken_flights: list of all taken flights until now in one segment
        :return: True if the direction is right and False if not
        """
        if self.source != taken_flights[-1].destination:
            return False
        for flight in taken_flights:
            if self.source == flight.source and self.destination == flight.destination:
                return False
        return True


def main():
    """
    Main function
    :return:
    """
    flight_arr = []
    stdin.readline()
    line = stdin.readline()

    while line:
        flight_arr.append(from_cvs_to_obj(line))
        line = stdin.readline()

    print("Reading Done")
    print("*"*10)
    print("Finding connections")

    for flight in flight_arr:
        find_flights(flight, flight_arr, [], 0)


def from_cvs_to_obj(csv_line):
    """
    Convert csv_line into Fligh object if some arguments are missing throw error and exit program
    :param csv_line: One line in CSV format from stdin
    :return: Flight object that has all arguments settled from csv_line
    """
    arg_arr = csv_line.split(",")
    if len(arg_arr) != 8:
        print("Error : Few data are missing", file=stderr)
        exit(-1)
    return Flight(arg_arr[0], arg_arr[1], arg_arr[2], arg_arr[3], arg_arr[4], arg_arr[5], arg_arr[6], arg_arr[7])


def find_flights(current_flight, all_flights, journey, iterations):
    """
    Function is finding all suitable flights and it is adapted for recursion
    :param current_flight: for which flight it should find connections
    :param all_flights: list of all available flights
    :param journey: list of all previous taken flights
    :param iterations: number of depth
    :return: instead of return it print ready-made template
    """
    journey.append(current_flight)
    iterations += 1

    for flight in all_flights:
        if current_flight.check_connect(flight) and flight.check_directions(journey):
            find_flights(flight, all_flights, journey.copy(), iterations)
    if len(journey) == 1:
        return None

    print(prepare_template(journey))


def prepare_template(journey):
    """
    Prepare template for printing from journey, template is made for further processing and with various prices
    :param journey: list of all flights in one segment or "all taken flights"
    :return: string template
    """
    template = ""
    road = ""
    price = 0
    bag_prices = 0
    bags_allowed = journey[0].bags_allowed

    same_baggage_through_flight = True
    baggage_not_allowed = False
    if not bags_allowed:
        baggage_not_allowed = True

    for flight in journey:
        price += flight.price
        if bags_allowed == flight.bags_allowed:
            bag_prices += flight.bag_price

        elif 0 < flight.bags_allowed:
            bag_prices += flight.bag_price
            same_baggage_through_flight = False

        else:
            same_baggage_through_flight = False
            baggage_not_allowed = True

        road += flight.source + "-" + flight.destination + ","

    source = journey[0].source
    destination = journey[-1].destination
    number_of_flights = len(journey)
    template += f"{source}->{destination},{number_of_flights},"

    if same_baggage_through_flight and bags_allowed == 2:
        template += f"3\n{road[:-1]},2bag:{price + 2*bag_prices},1bag:{ price + bag_prices},0bag:{price}"
    elif baggage_not_allowed:
        template += f"1\n{road[:-1]},0bag:{price}"
    else:
        template += f"2\n{road[:-1]},1bag:{ price + bag_prices},0bag:{price}"

    return template


if __name__ == "__main__":
    main()
