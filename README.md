# DjangoAdvanced-project
 Django Web Project @ Softuni

#### After running migrations you may start the initial_data.py(main project folder) in order to create 1st user and populate some useful objects/information.


Kind regards,


### Project description
The **NoCardio** app is created for educational purposes as part of Python Web course in SoftUni. The app provides a flexible interface for creating a fitness routine, focused mainly on powerbuilding.
In order to achieve that there are some custom logic behind for creating appropriate models, relations and interactions between them and the users.


### Main  functionalities
1. Creating a Workout with main properties needed, preview of the created Workouts of all, filtered by date and/or category and view in details. Adding data or delete a workout record if neccesery. 
2. Creating a Meals as part of the user nutrition plan.
3. User and access managment of the website, including some staff special permission and views.

##### Detailed models description
#### Workout app models
- **WorkoutBase** - main abstract model. The base for future development. The model provides the basic relation with the User.
- **Workout** as a base element of the workout routine. Main logic - create an Workout object.
- **Exercise** managed by *staff* members, with categories and types.
Requires some configuration/data population. 
- **WorkoutSet** provides relation between workout-exercises and specific logic. Workout and Exercise are related with that model and it's the main funtional model of the app.

#### Nutrition app models
- **Meal** model
Main logic - provides the creation and loging the meals for the users.
Additonal simple funtionalities for preview and delete meals.
#### Users app
- **CustomUser**  login and authorization logic as AbstractUser inheritant.
Additional usage of  is_staff permissions is implemented as extended managment and rights.
- **UserProfile model** - functionalities for picture upload and future extension. Access to the respective views and funtionalities of the website.
Registered/authenticated users have different view of the website.


#### After running migrations you may start the initial_data.py(main project folder) in order to create 1st user and populate some useful objects/information.

Kind regards,

