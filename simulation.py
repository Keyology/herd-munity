from virus import Virus
from logger import Logger
from person import Person
import random
import copy
import sys
random.seed(42)


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''

    logger = None
    population = []  # List of Person objects
    pop_size = 0  # Int
    next_person_id = 0  # Int
    virus = ''  # Virus object
    initial_infected = 0  # Int
    total_infected = 0  # Int
    current_infected = 0  # Int
    vacc_percentage = 0  # float between 0 and 1
    total_dead = 0  # Int
    file_name = ''
    newly_infected = []
    population = []
    death_total = 0
    mortality_rate = 0
    basic_repro_num = 0


    def __init__(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                 basic_repro_num, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''

        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.logger = None
        self.population = []  # List of Person objects
        self.pop_size = int(pop_size)  # Int
        self.next_person_id = 0  # Int
        self.virus_name = virus_name  # Virus object
        self.initial_infected = int(initial_infected)  # Int
        self.total_infected = 0  # Int
        self.current_infected = 0  # Int
        self.vacc_percentage = float(vacc_percentage)  # float between 0 and 1
        self.total_dead = 0  # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        # self.alive_infected = []
        self.basic_repro_num = basic_repro_num
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(
            pop_size, vacc_percentage, virus_name, 0.75, 0)
        self._create_population(initial_infected)
        self.mortality_rate = float(mortality_rate)
        self.total_vac = int(float(len(self.population)) * self.vacc_percentage)

    def _create_population(self, initial_infected):
        '''This method will create the initial population.

            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.


            Returns:
                list: A list of Person objects.

        '''

        self.population = []
        self.initial_infected = 0
        self.current_infected = 0

        while len(self.population) != self.pop_size:
            if self.current_infected != initial_infected:
                person = Person(self.next_person_id, False, Virus(self.virus_name, basic_repro_num, self.mortality_rate))
                self.population.append(person)
                self.current_infected += 1
                # self.alive_infected.append(person)
            else:
                person = Person(self.next_person_id, False)

            self.population.append(person)
            self.next_person_id = self.next_person_id + 1

        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.



            Returns:
                bool: True for simulation should continue, False if it should end.
        '''

        print('Death total:', self.total_dead)
        if self.vacc_percentage == 1:
            print('Everyone vaccinated')
            return False
        elif self.death_total == 1:
            print('Everyone dead')
            return False
        else:
            for person in self.population:
                if person.is_alive and not person.is_vaccinated:
                    # print("Someone is alive but not vaccinated")
                    return True
            print('Everyone either dead or vaccinated, population:', len(self.population), 'dead:', self.total_dead, 'vaccinated:', self.total_vac)
            return False


        # if self.current_infected > 0:

        #     for person in self.population:
                #    if person.is_alive:
                #        population_alive = True
                #        break

                # if infected_remain and population_alive:
                #    return True
                # else:
                #    return False

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0

        while self._simulation_should_continue():

            # TODO: for every iteration of this loop, call self.time_step() to compute another
            # round of this simulation.
            # print('Next Turn')
            time_step_counter += 1
            self.time_step(time_step_counter)
        print('The simulation has ended after {} turns.'.format(
            time_step_counter))

    def time_step(self, counter):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
        '''
        death_total = self.total_dead
        newly_infected_count = len(self.newly_infected)
        newly_infected = copy.deepcopy(self.newly_infected)
        # print('For loop about to start')
        for person in self.population:
            # print('For loop started, person infection:', person.infection, "person is alive:", person.is_alive)
            if person.infection and person.is_alive:
                # print('Found someone not like me')
                interaction = 0
                # print('before while loop')
                while interaction < 100:
                    # print('inside while loop')
                    ran_person = random.choice(self.population)
                    if person != ran_person and ran_person.is_alive:
                        # print('An interaction')
                        self.interaction(person, ran_person)
                        interaction += 1
                        # death_total = death_total + \
                        #     person.did_survive_infection(self.mortality_rate)
                if not person.did_survive_infection(self.mortality_rate):
                    self.total_dead += 1
                    # print('Person died')
                else:
                    # increase vacc percent
                    # print('Person vaccinated')
                    self.total_vac += 1
                    self.vacc_percentage = self.total_vac / len(self.population)
                # self.alive_infected.remove(person)
        self._infect_newly_infected()
        self.logger.log_time_step(counter, len(self.newly_infected) - newly_infected_count, self.total_dead - death_total)

        # TODO: Finish this method.
        

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person != random_person
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0 and 1.  If that number is smaller
        #     than repro_rate, random_person's ID should be appended to
        #     Simulation object's newly_infected array, so that their .infected
        #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.

        if random_person.is_vaccinated or random_person.infection:
            self.logger.log_interaction(
                person, random_person, False, random_person.is_vaccinated, random_person.infection)
        elif person.infection:
            rand = random.random()
            if rand < self.basic_repro_num:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(
                    person, random_person, True, random_person.is_vaccinated, random_person.infection)
            else:
                self.logger.log_interaction(
                    person, random_person, False, random_person.is_vaccinated, random_person.infection)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for i in self.newly_infected:
            for person in self.population:
                if person._id == i:
                    person.infection = Virus(self.virus_name, basic_repro_num, self.mortality_rate)
                    self.current_infected += 1
                    # self.alive_infected.append(person)
                    break
        self.newly_infected = []


if __name__ == "__main__":
    # params = sys.argv[1:]
    # virus_name = str(params[0])
    # repro_num = float(params[1])
    # mortality_rate = float(params[2])

    # pop_size = int(params[3])
    # vacc_percentage = float(params[4])

    # if len(params) == 6:
    #     initial_infected = int(params[5])

    # virus = Virus(name, repro_rate, mortality_rate)
    # sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    # sim.run()

    params = sys.argv[1:]

    pop_size = int(params[0]) if int(params[0]) >= 100 else 100 

    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
         initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()
