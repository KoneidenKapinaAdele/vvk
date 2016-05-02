#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import collections
import random
import numpy as np
import matplotlib.pyplot as plt

class EmployeeState:
    HOME   = 0
    WORK   = 1
    LUNCH  = 2
    QUEUE  = 3
    TOILET = 4

class EventType:
    BEGIN_DAY    = 0
    END_DAY      = 1
    BEGIN_LUNCH  = 2
    END_LUNCH    = 3
    JOIN_QUEUE   = 4
    LEAVE_TOILET = 5
    CLOSE_OFFICE = 6
    SAMPLE       = 7

class Conf:
    # prng seed
    random_seed = 12345678
    
    # number of employees
    n_employees = 150
    
    # number of toilets
    n_toilets = 2+2+5
    
    # office opening hours
    hour_first = 7.0
    hour_last = 19.0
    
    # sampling frequence for time series, in hours
    tick = 1/60
    
    # expected time between toilet breaks, in hours
    beta = 2.0
    
    # length of a toilet visit, in minutes
    visitlen_mu = 2.0
    visitlen_sigma = 3.0
    visitlen_lowerbound = 0.5
    
    # time of arrival to the working place, in hours o'clock
    arrival_mu = 9.0
    arrival_sigma = 1.0
    arrival_lowerbound = hour_first
    
    # start of lunch time, in hours
    lunch_mu = 11.0
    lunch_sigma = 1.0
    lunch_lowerbound = 10.0
    
    # duration of lunch, in hours
    lunchlen_mu = 0.5
    lunchlen_sigma = 0.5
    lunchlen_lowerbound = 0.5

    # length of the working day, in hours
    daylen_mu = 7.5
    daylen_sigma = 0.5


def error(s):
    from sys import stderr, exit
    print("ERROR:", s, file=stderr, flush=True)
    exit(1)

def rndn_lb(mu, sigma, lowerbound):
    # TODO: implement a deterministic-time algorithm instead
    while True:
        x = np.random.normal(mu, sigma)
        if x >= lowerbound:
            return x

def rndn_lb_ub(mu, sigma, lowerbound, upperbound):
    # TODO: implement a deterministic-time algorithm instead
    if lowerbound >= upperbound:
        error("rndn_lb_ub: upper bound must be greater than lower bound")
    else:
        while True:
            x = np.random.normal(mu, sigma)
            if x >= lowerbound and x <= upperbound:
                return x

def simulate(conf):
    # initialize the event queue with arrivals, departures, lunches,
    # and the first toilet breaks
    event_queue = []
    for i in range(conf.n_employees):
        t_arrival = rndn_lb(conf.arrival_mu,
                            conf.arrival_sigma,
                            conf.arrival_lowerbound)
                            
        t_departure = t_arrival + rndn_lb(conf.daylen_mu,
                                          conf.daylen_sigma,
                                          0.0)
                                          
        t_begin_lunch = rndn_lb_ub(conf.lunch_mu,
                                   conf.lunch_sigma,
                                   max(conf.lunch_lowerbound, t_arrival),
                                   t_departure)
        
        t_toilet = t_arrival + np.random.exponential(conf.beta)
                                   
        heapq.heappush(event_queue, (t_arrival, EventType.BEGIN_DAY, i))
        heapq.heappush(event_queue, (t_departure, EventType.END_DAY, i))
        heapq.heappush(event_queue, (t_begin_lunch, EventType.BEGIN_LUNCH, i))
        heapq.heappush(event_queue, (t_toilet, EventType.JOIN_QUEUE, i))

    # add the office closing time to the event queue
    heapq.heappush(event_queue, (conf.hour_last, EventType.CLOSE_OFFICE, None))

    # add the sampling events to the event queue
    t = conf.hour_first
    while t <= conf.hour_last:
        heapq.heappush(event_queue, (t, EventType.SAMPLE, None))
        t += conf.tick
        
    # initialize the time series for sampling
    ts_tick = []
    ts_occupied = [ [] for i in range(conf.n_toilets) ]

    # initialize all toilets to be unoccupied
    n_free = conf.n_toilets
    free_toilets = list(range(conf.n_toilets))
    random.shuffle(free_toilets)
    occupied_toilets = set()
    
    # initialize the toilet queue
    toilet_queue = collections.deque()
    
    # initialize employee states
    employee_state = [ EmployeeState.HOME for i in range(conf.n_employees) ]
    
    # execute the simulation
    while True:
        ev = heapq.heappop(event_queue)
        ev_time = ev[0]
        ev_type = ev[1]
        ev_employee = ev[2]
        
        if ev_type == EventType.CLOSE_OFFICE:
            break
        elif ev_type == EventType.BEGIN_DAY:
            employee_state[ev_employee] = EmployeeState.WORK
        elif ev_type == EventType.BEGIN_LUNCH:
            if employee_state[ev_employee] == EmployeeState.WORK:
                employee_state[ev_employee] = EmployeeState.LUNCH
                t_end_lunch = ev_time + rndn_lb(conf.lunchlen_mu,
                                                conf.lunchlen_sigma,
                                                conf.lunchlen_lowerbound)
                heapq.heappush(event_queue, (t_end_lunch,
                                             EventType.END_LUNCH,
                                             ev_employee))
            elif employee_state[ev_employee] in [EmployeeState.QUEUE,
                                                 EmployeeState.TOILET]:
                # try again later (TODO: make this cleaner)
                heapq.heappush(event_queue,
                               (ev_time + 1/60, ev_type, ev_employee))
            else:
                error('logic error for event ' + str(ev))
        elif ev_type == EventType.END_DAY:
            employee_state[ev_employee] = EmployeeState.HOME
        elif ev_type == EventType.END_LUNCH:
            if employee_state[ev_employee] == EmployeeState.LUNCH:
                employee_state[ev_employee] = EmployeeState.WORK
            elif employee_state[ev_employee] == EmployeeState.HOME:
                # went home already, never mind
                pass
            else:
                error('logic error: end_lunch during state %d' %
                    employee_state[ev_employee])
            
        elif ev_type == EventType.JOIN_QUEUE:
            if employee_state[ev_employee] == EmployeeState.WORK:
                if n_free == 0:
                    toilet_queue.append(ev_employee)
                    employee_state[ev_employee] = EmployeeState.QUEUE
                else:
                    n_free -= 1
                    toilet_id = free_toilets.pop()
                    occupied_toilets.add(toilet_id)
                    employee_state[ev_employee] = EmployeeState.TOILET
                    t_getout = ev_time + rndn_lb(conf.visitlen_mu,
                                                 conf.visitlen_sigma,
                                                 conf.visitlen_lowerbound) / 60
                    heapq.heappush(event_queue, (t_getout,
                                                 EventType.LEAVE_TOILET,
                                                 ev_employee,
                                                 toilet_id))
            elif employee_state[ev_employee] == EmployeeState.LUNCH:
                # try again later after lunch (TODO: make this cleaner)
                heapq.heappush(event_queue,
                               (ev_time + 1/60, ev_type, ev_employee))
            elif employee_state[ev_employee] == EmployeeState.HOME:
                # went home already, not joining the queue
                pass
            else:
                error('join_queue but state is %d' % employee_state[ev_employee])
        elif ev_type == EventType.LEAVE_TOILET:
            toilet_id = ev[3]
            if employee_state[ev_employee] == EmployeeState.TOILET:
                employee_state[ev_employee] = EmployeeState.WORK
                next_toilet_time = ev_time + np.random.exponential(conf.beta)
                heapq.heappush(event_queue, (next_toilet_time,
                                             EventType.JOIN_QUEUE,
                                             ev_employee))
            elif employee_state[ev_employee] == EmployeeState.HOME:
                # went home already, no more toilet events
                pass
            else:
                error('logic error: wanted to leave toilet but state is %d' %
                    employee_state[ev_employee])
                                         
            free_toilets.append(toilet_id)
            random.shuffle(free_toilets)
            occupied_toilets.remove(toilet_id)
            n_free += 1
            
            if len(toilet_queue) > 0:
                whonext = toilet_queue.popleft()
                if employee_state[whonext] != EmployeeState.QUEUE:
                    error('logic error: the next in toilet queue is not there')
                employee_state[whonext] = EmployeeState.TOILET
                toilet_id = free_toilets.pop()
                n_free -= 1
                occupied_toilets.add(toilet_id)
                t_getout = ev_time + rndn_lb(conf.visitlen_mu,
                                             conf.visitlen_sigma,
                                             conf.visitlen_lowerbound) / 60
                heapq.heappush(event_queue, (t_getout,
                                             EventType.LEAVE_TOILET,
                                             whonext,
                                             toilet_id))
        elif ev_type == EventType.SAMPLE:
            ts_tick.append(ev_time)
            for i in range(conf.n_toilets):
                if i in occupied_toilets:
                    ts_occupied[i].append(1)
                else:
                    ts_occupied[i].append(0)
        else:
            error("Unhandled event " + str(ev))
            
    return (ts_tick, ts_occupied)
            

def main():
    conf = Conf()
    random.seed(conf.random_seed)
    np.random.seed(conf.random_seed)
    ts_tick, ts_occupied = simulate(conf)
    n_ts = len(ts_occupied)
    for i in range(n_ts):
        plt.subplot(n_ts, 1, i + 1)
        plt.plot(ts_tick, ts_occupied[i])
        plt.ylim([-0.1, 1.1])
        plt.xlim([conf.hour_first, conf.hour_last])
        plt.xlabel('time')
        handle = plt.gca()
        for ytick in handle.axes.get_yticklabels():
            ytick.set_visible(False)
    plt.savefig('toilets.pdf', format='pdf')
    plt.show()
    ts_sum = []
    for i in range(len(ts_tick)):
        s = 0
        for j in range(n_ts):
            s += ts_occupied[j][i]
        ts_sum.append(s)
    plt.plot(ts_tick, ts_sum)
    plt.xlim([conf.hour_first, conf.hour_last])
    plt.xlabel('time')
    plt.ylabel('number of toilets occupied')
    plt.savefig('num_occupied.pdf', format='pdf')

if __name__ == "__main__":
    main()