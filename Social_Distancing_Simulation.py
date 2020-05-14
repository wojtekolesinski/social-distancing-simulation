import turtle as t
import random

# -----------SIMULATION VARIABLES----------
number_of_people = 220
number_of_sick_people = 10
number_of_people_social_distancing = 10
sickness_length = 1000
simulation_length = 10000
person_size = 10


class Screen:

    def __init__(self):
        """Setting up the animation, window title
        contains variables needed for symulating collision with walls,
        correct text placement and margins"""

        t.title('Social Distancing Simulator')
        t.mode('logo')
        t.tracer(0, 0)
        t.hideturtle()
        self.HEIGHT = t.window_height()
        self.WIDTH = t.window_width()
        self.MARGX = 20
        self.MARGY = 20
        self.TXT_HEIGHT = 40
        self.BOX_COORDS = [[-self.WIDTH / 2 + self.MARGX + 10, self.WIDTH / 2 - self.MARGX - 10],
                           [-self.HEIGHT / 2 + self.MARGY + 10, self.HEIGHT / 2 - self.TXT_HEIGHT - 10]]
        self.TEXT = [[0, self.HEIGHT / 2 - 30]]

    def box(self, ball_size):
        """Drawing grey box, in which the dots will be moving"""
        self.color = 'linen'
        t.color(self.color, self.color)
        t.penup()
        t.setpos(- self.WIDTH / 2 + self.MARGX, - self.HEIGHT / 2 + self.MARGY)
        t.pendown()
        t.begin_fill()
        for i in range(2):
            t.fd(self.HEIGHT - self.MARGY - self.TXT_HEIGHT)
            t.rt(90)
            t.fd(self.WIDTH - 2 * self.MARGX)
            t.rt(90)
        t.end_fill()
        self.SIZE = ball_size / 2
        self.BOX_COORDS = [[-self.WIDTH / 2 + self.MARGX + self.SIZE, self.WIDTH / 2 - self.MARGX - self.SIZE],
                          [-self.HEIGHT / 2 + self.MARGY + self.SIZE, self.HEIGHT / 2 - self.TXT_HEIGHT - self.SIZE]]  # adjusting box borders to size of the balls

    def text(self, txt):
        """Placing a centered text in the upper part of the screen"""

        t.pencolor('black')
        t.penup()
        t.setpos(self.TEXT[0][0], self.TEXT[0][1])
        t.pendown()
        t.write(arg=txt, align='center')


class Symulation:

    def __init__(self, number_of_people, number_of_sick_people, number_of_people_social_distancing, sickness_length,
                 person_size, screen):

        """Initiating the simulation.
        Creating list of all the people, along with assigning them starting coordinates,
        speed vectors and state"""

        self.PEOPLE = number_of_people
        self.SICK = number_of_sick_people
        self.SICKNESS_LENGHT = sickness_length
        self.CURED = 0
        self.DAY = 1
        self.SIZE = person_size
        self.SOCIAL_DIST = number_of_people_social_distancing
        self.PEOPLE_LIST = [[['x', 'y'], ['dx', 'dy'], 'state', 0] for i in range(self.PEOPLE)]  # creating a list of people with nested lists for xy coordinates and speed vectors
        self.SCREEN = screen
        self.SCREEN.box(self.SIZE)
        self.X_COL, self.Y_COL = False, False

        for i in range(self.SICK):  # generating sick people
            self.person_assign(self.PEOPLE_LIST[i], 'sick')
            while self.collision(self.PEOPLE_LIST[i], self.PEOPLE_LIST[:i])[0]:  # checking for collisions between the starting positions
                self.person_assign(self.PEOPLE_LIST[i], 'sick')

        for i in range(
                self.SOCIAL_DIST):  # generating poeple, who are social distancing, with x and y speed vectors equal to 0
            self.person_assign(self.PEOPLE_LIST[i + self.SICK], 'healthy')
            while self.collision(self.PEOPLE_LIST[i + self.SICK], self.PEOPLE_LIST[:i + self.SICK])[0]:  # checking for collisions between the starting positions
                self.person_assign(self.PEOPLE_LIST[i + self.SICK], 'healthy')

            self.PEOPLE_LIST[i + self.SICK][1][0] = 0
            self.PEOPLE_LIST[i + self.SICK][1][1] = 0

        for i in range(self.SICK + self.SOCIAL_DIST, len(self.PEOPLE_LIST)):  # generating the rest of the people
            self.person_assign(self.PEOPLE_LIST[i], 'healthy')
            while self.collision(self.PEOPLE_LIST[i], self.PEOPLE_LIST[:i])[0]:  # checking for collisions between the starting positions
                self.person_assign(self.PEOPLE_LIST[i], 'healthy')

    def person_assign(self, person, state):

        """Assigning a person starting coordinates in the borders of the box,
        along with a nonzero speed vector, and a state"""

        person[0][0] = random.randrange(self.SCREEN.BOX_COORDS[0][0] + 5, self.SCREEN.BOX_COORDS[0][1] - 5)
        person[0][1] = random.randrange(self.SCREEN.BOX_COORDS[1][0] + 5, self.SCREEN.BOX_COORDS[1][1] - 5)
        person[1][0] = random.randrange(-1, 2)
        person[1][1] = random.randrange(-1, 2)
        while person[1][0] == 0 and person[1][1] == 0:  # checking, whether every person has at least one nonzero speed vector, so they won't count, as social distancing
            person[1][0] = random.randrange(-1, 2, 2)
            person[1][1] = random.randrange(-1, 2, 2)
        person[2] = state

    def draw_people(self):

        """Drawing every person in color corresponding with their current state"""

        for person in self.PEOPLE_LIST:
            t.penup()
            t.setpos(person[0][0], person[0][1])
            t.pendown()

            if person[2] == 'cured':
                t.dot(self.SIZE, 'forestgreen')
            elif person[2] == 'sick':
                t.dot(self.SIZE, 'firebrick')
            elif person[2] == 'healthy':
                t.dot(self.SIZE, 'gold')

    def collision(self, person1, people_list):

        """Checking for collision between a person, and all elements of a list of persons.
        Function return an array containing a boolean value and index of the colliding elements"""

        for i in range(len(people_list)):
            if people_list[i] == person1:
                continue
            x_distance = abs(person1[0][0] - people_list[i][0][0])
            y_distance = abs(person1[0][1] - people_list[i][0][1])
            if x_distance <= (self.SIZE - 2) and y_distance <= (self.SIZE - 2):
                return [True, i]

        return [False]

    def move_people(self):

        """Function responsible for movement between each frame.
        Each persons x and y coordinates are changing by value of the corresponding speed vector.
        Vectors are also reversed in case of a collision,
        along with changing the person's state, if needed"""

        for i in range(len(self.PEOPLE_LIST)):
            if self.PEOPLE_LIST[i][0][0] in self.SCREEN.BOX_COORDS[0]:  # checking for wall collision in the X axis
                self.PEOPLE_LIST[i][1][0] *= -1
                self.X_COL = True
            if self.PEOPLE_LIST[i][0][1] in self.SCREEN.BOX_COORDS[1]:  # checking for wall collision in the Y axis
                self.PEOPLE_LIST[i][1][1] *= -1
                self.Y_COL = True

            if self.collision(self.PEOPLE_LIST[i], self.PEOPLE_LIST)[0]:  # checking for collisions with other people
                j = self.collision(self.PEOPLE_LIST[i], self.PEOPLE_LIST)[1]
                if not self.X_COL:
                    self.PEOPLE_LIST[i][1][0] *= -1
                if not self.Y_COL:
                    self.PEOPLE_LIST[i][1][1] *= -1
                if self.PEOPLE_LIST[i][2] == 'sick':
                    if self.PEOPLE_LIST[j][2] == 'healthy':  # spreading the disease if a sick person bumps into a healthy one
                        self.PEOPLE_LIST[j][2] = 'sick'
                        self.PEOPLE_LIST[j][3] = 0
                        self.SICK += 1




            self.PEOPLE_LIST[i][0][0] += self.PEOPLE_LIST[i][1][0]
            self.PEOPLE_LIST[i][0][1] += self.PEOPLE_LIST[i][1][1]
            self.X_COL, self.Y_COL = False, False  # these variables exist to prevent people, from going out of the screen, if a wall collision occurs along with normal collision



    def check_up(self):

        """Function responsible for curing people and keeping the counters updated"""

        for person in self.PEOPLE_LIST:
            if person[2] == 'sick':
                if person[3] < self.SICKNESS_LENGHT:
                    person[3] += 1
                else:
                    person[2] = 'cured'
                    self.CURED += 1
                    self.SICK -= 1

    def symulate(self, number):

        """Function drawing all the frames, and animating the whole thing.
        It takes one parameter: the number of days, that the simulation will last"""

        for i in range(number):
            t.clear()
            self.SCREEN.box(self.SIZE)

            self.move_people()
            self.draw_people()
            self.check_up()
            self.TEXT = f'Niezakażonych = {self.PEOPLE - self.SICK - self.CURED}, zakażonych = {self.SICK}, ozdrowieńców = {self.CURED}, nieruchomych = {round(self.SOCIAL_DIST / self.PEOPLE * 100, 2)}%, dzień {self.DAY}'
            self.DAY += 1
            self.SCREEN.text(self.TEXT)

        t.done()


def main():
    screen = Screen()
    sym = Symulation(number_of_people, number_of_sick_people, number_of_people_social_distancing, sickness_length, person_size, screen)
    sym.symulate(simulation_length)


if __name__ == '__main__':
    main()
