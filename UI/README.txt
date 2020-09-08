9/8/2020
CODE WRITTEN BY: Daniel Liao

PROGRAM/CODE STRUCTURE:

- The mainUI object has a 'lab' data object inside that stores the current state of the UI.
  - This 'lab' data object includes:
      - List of 'Container' data objects
      - List of 'Network' data objects
      - 'Results' Data object
      - 'Goals' Data object
  - When a user saves the lab the program writes whatever is in the 'lab' data object 
    to the lab files, namely start.config, results.config, and goals.config.
  - All Results UI/Data code are in their own package 
    and all Goals UI/Data code are in their own package
- Each Container/Network Panel Object has a Container/Network data object 
  that references the same Contaienr/Network data object in the data object 
  lists in the 'lab' data object.
     - So when you press confirm for each container/network configuration 
       dialog box, it changes the Container/Network data object in the 
       'lab' data object.

- The Results/Goals UI have their own results data object, NOT a reference pointing to
  the results/goals data object in the 'lab' data object. 
     - When initially opening the results/goals UI the results/goals data object here is 
       a copy from the main UI's 'lab' data. 
     - When the user presses confirm changes in the Goals/Results UI, it makes a deep copy
       of the current data state here and sets it to the results/goals data object in the
       'lab' data object.  

-Immediate changes to a lab's files and directories occur when the user: 
 - Deletes a container
 - Renames a container
 - Adds a container
 - Edit a container's dockerfile

- All other changes are written to the labs files when the user
  presses save lab/save lab as.


TODOS:

- RUN/BUILD Button
- Validation on User Input outside of Goals and Results UI
- Tooltips on all the fields
- LOGS Button (Pulls up terminal window that spits program output)
- Parameter Configuration Button/UI
- Menu Items
    - Help
    - Help/About
    - Help/Check For Updates
- UI Consistency in Goals UI and Results UI when a results artifact line is modified/deleted 
  and container is renamed/deleted/added, respectively


NOTES AND CONCERNS TO ADDRESS:

- The program as of now has a high potential for bugs, so
  it's imperative to do extensive testing for a series of 
  actions. 
  
  Ex. Having the Results UI opened and deleting a container 
  that an artifact line is referencing. Does the Results visual
  interface have continuity?   

- The project was 3 main functions from 3 seperate packages, 
  so the current build script may not work

- When user updates the LABTAINERS DIR path, what happens if the new set path is a 
  place where the currently opened lab does not exist. A bug can occur if the
  user opens a lab, saves/save as  a lab, renames a conainer, adds a container, 
  or deletes a container. (Essentially any part of the program that references the 
  lab path, since the lab path is relative to the LABTAINERS DIR)

- Parts of the UI that use a JPanel and JScrollPane, may make use of magic numbers when
  adding and removing subpanels from the JPanel to adjust for the exact needed height
  to fit all the subpanels visibly.  



If you have any questions about the program and code, feel free to contact me at danielliao22@gmail.com


