# Assignment 1 - Student's Report

## Author: Francis Ozoka - 220228986

## Class of the Agent Program

The agent is a goal based agent since it operates based on a predefined set of goals (Eat as many food as possible). Decisions on which action to take are made based on their predicted outcome of maximising the score. 

First, the food items are sorted in increasing order of their Euclidean distances from the agent, and then the agent calculates the quickest way to get to the nearest food.

Secondly, each subsequent action is selected to bring the agent closer to it's goal being the current food target. 

## AI Techniques Considered

The AI technique i considered where somewhat similar to the breadth-first search algorithm without the GraphNode class. I actually went pretty far with it but changed my mind after i came to the realisation that the GraphNode class made things a lot more simple, especially the get_Path method.

The technique was a modification of the flood fill algorithm is a model of the environment. The agent will navigate towards the food target by moving to the tile with a the smallest distance from the food target.

This techniques being similar to the BFS algorithm always tries to bring the agent closer to the food and so aligns perfectly with the objective of the agent.

## Reflections

The first problem i encountered during my problem solving was the validation function for the food sensor. It took me a while to create an appropriate lambda function to handle the validation. This also meant that i couldn't make any progress since the food array kept coming up empty. I eventually solved it by separating the different validations that needed to be made instead of try to write awesome code.

Secondly, the agent always seemed to collide with the wall every now and then, when it wasn't supposed to. I later realised that it happened because i calculated left and right relative to the direction the agent is facing instead of right being right and left just being left. After a series of action prints and going back and forth with the assignment description, i was able to fix this issue.

lastly, paths where being calculated backwards at times, especially when only the snakes head exists. This caused the snake to move straight to a wall or out of bounds if the first move happens to be in the opposite direction. It took a while to figure this out but when I did, I created a function that calculates the direction of travel of the snake and returned the coordinates of the tile immediately behind the snake if it exists. This tile is then included in the list of obstacles.

I also made it so that the initial head direction Is Node to prevent the snake from smashing into a wall at the start.