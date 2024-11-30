# DjangoAdvanced-project
 Django Web Project @ Softuni

#### After running migrations you may start the initial_data.py(main project folder) in order to create 1st user and populate some useful objects/information.


### Project description
The **NoCardio** app is created for educational purposes as part of Python Web course in SoftUni. 
The app provides a flexible interface for creating a fitness routine, focused mainly on powerbuilding.
In order to achieve that there are some custom logic behind for creating appropriate models, relations and interactions between them and the users.


### Main  functionalities
1. Creating a Workout with main properties needed, preview of the created Workouts of all, filtered by date and/or category and view in details. Adding data or delete a workout record if neccesery. 
2. Automaticly create and update workout data(repetition maxes) related to user.
4. Creating a Meals as part of the user nutrition plan.
5. User create/auth and dynamic access and views of the website,
6. Staff/managment specific access - views and functionalities.(view, delete users).
7. Views of personal training data(see 2.)
8. Views of training data(see 2.) for public users.
Additional:
9. Custom permission for user managment view(view only).
10. Tests of some views, forms, models.


##### Detailed models description
#### Workout app models
- **WorkoutBase** - main abstract model. The base for further development. The model provides the basic relation with the User.
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
- **RepMax model** - contains user record via relation with WorkoutSet created with signals.
#### Common app
- No models. Views with static information/content.
  
#### After running migrations you may start the initial_data.py(main project folder) in order to create 1st user and populate some useful objects/information.

Kind regards,

