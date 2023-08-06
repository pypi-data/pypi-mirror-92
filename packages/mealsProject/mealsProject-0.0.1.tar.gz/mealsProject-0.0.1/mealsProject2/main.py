from mealsProject2.Meals import *
import random

def printMeal(meal):
    starter=meal.create_starter()
    mainCourse=meal.create_main_course()
    dessert=meal.create_dessert()

    print(f"    starter: {starter.eatStarter()}")
    print(f"    mainCourse: {mainCourse.eatMain()}")
    print(f"    dessert: {dessert.eatDessert()}")


def createOneMeal(choise):
    if choise==0:
        createOneMeal(random.randint(1,2))

    if choise==1:
        print("lets eat asian meal:")
        printMeal(Asian_meal())

    if choise==2:
        print("lets eat italian meal:")
        printMeal(Italian_meal())



c="0"
while c!="-1":
    print("Choose number for meal:")
    print("-1: Exit")
    print(" 0: Random meal")
    print(" 1: Asian meal")
    print(" 2: Italian meal")

    c=input()
    createOneMeal(int(c))
    print()